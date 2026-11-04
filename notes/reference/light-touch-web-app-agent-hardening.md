# Light-touch web app and agent hardening

Status: reference pattern, 2026-11-04
Origin: FRESH x IRSS demo (`UBC-FRESH/fresh-irss-demo`, PR #16)
Audience: maintainers of FRESH demo prototypes, dashboards, and small web apps
Scope: trusted, identity-gated prototypes running in a dev container

## Why this note exists

The first FRESH x IRSS demo needed a grounded assistant inside a small public
communication site. The useful pattern was not a full public-app security
program. It was a set of small moves that:

- keep the public artifact static and honest;
- keep an assistant opt-in and same-origin;
- give the assistant enough context to find things across a large multi-repo
  workspace;
- prevent the assistant from accidentally modifying or deleting the workspace;
- make citations and claims testable; and
- leave the heavier controls for a real public deployment.

This note records that pattern so the next FRESH prototype can reuse it without
re-deriving the trade-offs.

## Trust model first

The demo is reached through:

```text
browser -> Cloudflare Access -> Globus OAuth -> UBC CWL -> tunnel -> dev container
```

The application itself adds no login. That is intentional. The identity boundary
is outside the app, and the users are trusted research collaborators. The app’s
job is to prevent accidents and keep information accurate, not to defend against
a determined insider who already passed the institutional gate.

Do not copy the no-auth choice into a different deployment. If the app later
loses the identity gate, becomes writable by untrusted users, or handles secrets,
move to the escalation list at the end of this note.

## Pattern at a glance

| Layer | Move | Prevents | User impact |
| --- | --- | --- | --- |
| Static site | Keep the public artifact dependency-free and read-only | A backend becoming an accidental public service | None |
| Assistant | Enable only when a same-origin endpoint is injected | Provider keys in the browser; accidental remote calls | None on the static page |
| Agent | Dedicated read-only agent with full workspace read | Accidental edits and destructive commands | More useful answers |
| Shell | Read-only command allowlist | Accidental `rm`, moves, writes, and tool side effects | Agent can still search |
| Provider call | No `--auto`; use `--standalone --agent` | Auto-approved tool calls; stale cached agent permissions | Slightly slower requests |
| Retrieval | Index the real registry, notes, docs, and lane data | Shallow answers from demo docs alone | Better grounding |
| Citations | Map to local docs or canonical repos; never to retired Pages | Dead or misleading evidence links | Verifiable answers |
| Markdown | Small safe renderer plus URL allowlist | Raw HTML injection and bad link schemes | Readable chat replies |
| Server | Path containment, clear 404s, MIME types, local docs route | Serving outside the intended roots | Current docs work locally |
| Tests | Config, command, retrieval, URL, and XSS checks | Silent drift in the safety contract | Repeatable |

## 1. Static-first, opt-in assistant

Keep three states separate:

1. **Static demo** — HTML, CSS, and JavaScript only. It must remain useful with
   no backend.
2. **Local assistant** — an opt-in same-origin service served by a local
   process. The service injects `window.FRESH_IRSS_DEMO.assistantEndpoint`.
3. **Public deployment** — the static GitHub Pages artifact. It has
   `assistantEndpoint: null` and never loads a provider key.

The default configuration is:

```js
window.FRESH_IRSS_DEMO = {
  assistantEndpoint: null,
};
```

The local server injects the same-origin path:

```js
window.FRESH_IRSS_DEMO = {
  assistantEndpoint: "/api/assistant",
};
```

The client should resolve the endpoint against `location.origin` and require an
exact origin match. Reject protocol-relative and absolute URLs. This is an
accident-prevention check, not a substitute for the identity gate.

Reference implementation:

- `web/config.js`
- `web/app.js` — endpoint resolution and disabled state
- `server/assistant.py` — injected `/config.js`
- `docs/assistant.rst` — request and response contract

## 2. A dedicated read-only agent

Do not let the app reuse the default build agent. Give it a named profile with a
small, reviewable permission set. In the IRSS demo, the profile is
`irss-guide` in the tracked `opencode.json`.

The profile has:

- **Read:** every repository under the workspace.
- **Discovery:** `read`, `glob`, `grep`, and external-directory access.
- **Shell:** a read-only allowlist, not a broad permit.
- **Denied:** `edit`, `execute` (Code Mode), `webfetch`, `websearch`, and
  `subagent`.
- **Steps:** a bounded number, so a search loop cannot run forever.
- **No `--auto`:** the provider invocation must not auto-approve tools.

### Why shell is allowed

An agent that can only read files still has to find the right file in a large
workspace of clones, worktrees, archives, and reports. `rg`, `git status`,
`git log`, `ls`, and read-only `find` are the difference between useful research
and guessing.

The shell policy is fail-closed:

```json
{
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "deny" },
    { "action": "shell", "resource": "rg *", "effect": "allow" },
    { "action": "shell", "resource": "grep *", "effect": "allow" },
    { "action": "shell", "resource": "ls *", "effect": "allow" },
    { "action": "shell", "resource": "git status *", "effect": "allow" },
    { "action": "shell", "resource": "git log *", "effect": "allow" },
    { "action": "shell", "resource": "git show *", "effect": "allow" },
    { "action": "shell", "resource": "find *", "effect": "allow" },
    { "action": "shell", "resource": "find * -delete*", "effect": "deny" },
    { "action": "shell", "resource": "find * -exec*", "effect": "deny" },
    { "action": "shell", "resource": "find * -ok*", "effect": "deny" }
  ]
}
```

Order matters: OpenCode uses the last matching rule. Start with a broad deny,
then add narrow read-only allows, then add negative exceptions for commands that
can mutate through an otherwise read-only tool.

A practical allowlist for a FRESH workspace is:

```text
pwd, ls, tree, rg, grep, find (no -delete/-exec/-ok), fd,
git status/log/show/diff/blame/rev-parse/branch/tag/remote -v/ls-files/grep,
cat, head, tail, wc, file, stat, du, sort, uniq, cut, jq, sed -n, awk
```

This is **not a sandbox**. An allowed `cat` can still read a credential file, and
an allowed `awk` can write through redirection or `system()`. The point is to
stop accidents by a trusted collaborator's assistant, not to contain an
adversary. If the trust boundary changes, move the agent into a real sandbox or
drop shell access.

### Provider invocation

Use a private, fresh agent runtime rather than a shared OpenCode service that may
have cached an older permission set:

```text
opencode run --standalone \
  --agent irss-guide \
  --model <provider/model> \
  --format json \
  "<prompt with retrieved evidence>"
```

Do **not** use `--auto`. That flag auto-approves permissions that are not
explicitly denied and turns a useful research assistant into an unrestricted
tool runner.

Test two things:

1. A fake provider call receives `--standalone`, `--agent irss-guide`, and no
   `--auto`.
2. A real shell probe can run an allowed search (for example `rg`), and a probe
   that asks for `touch` or `rm` is denied and leaves no file.

Reference implementation:

- `opencode.json` — agent profile, system prompt, and permissions
- `server/assistant.py` — provider command and timeout
- `tests/test_assistant_server.py` — command and permission contracts

## 3. Give the assistant real workspace context

A shallow assistant reads the demo’s own README and calls it evidence. A useful
assistant reads the registry and the notes that the demo summarizes.

The IRSS implementation indexes:

- the sibling `irss-expansion/registry/candidates.yaml`;
- `notes/**/*.md` from the expansion checkout, including subdirectories;
- the demo’s own notes and docs;
- `web/lanes.js` and `web/lab.js`, so lane claims and lab values are findable.

Default the expansion root to a sibling checkout, with an environment override:

```text
FRESH_ASSISTANT_EXPANSION=/path/to/irss-expansion
FRESH_ASSISTANT_REGISTRY=/path/to/candidates.yaml
```

If the expansion checkout is absent, the service still works from the demo
docs. Say so in the docs; do not tell the assistant that a registry is present
when it is not.

### Ranking

Do not rank documents by “number of matching words divided by document length.”
That rewards short READMEs over the specific note that contains the answer. Use a
small BM25-style score with:

- stopword removal;
- token frequency saturation;
- inverse document frequency;
- a path/title boost for exact IDs such as `CARB-03`; and
- a minimum-score/no-answer path.

Keep a fixture test with a short README and a specific note. Assert that the
specific note wins for `CARB-03`.

## 4. Citation rules

Citations should point at a source a collaborator can open now.

| Source | Citation target |
| --- | --- |
| Demo docs (`docs/*.rst`) | local `/docs/<page>.html` from the current Sphinx build |
| Demo notes | `github.com/<org>/<demo>/blob/main/notes/...` |
| Expansion notes | `github.com/<org>/irss-expansion/blob/main/notes/...` |
| Registry | `github.com/<org>/irss-expansion/blob/main/registry/candidates.yaml` |
| Retired Pages site | not cited |

Do not cite a public Pages page for branch-only content. It is stale until the PR
merges and deploys, and an assistant can use that stale page to “support” a claim
it does not actually contain. Serving the current local docs under `/docs/` is a
small way to keep citations honest during development.

Each cited URL should have a content or mapping test. A 200 response is not proof
that the page contains the claim.

## 5. Safe Markdown in the chat drawer

Assistant output is untrusted text even when the provider is trusted. Render a
small Markdown subset rather than assigning raw HTML:

- paragraphs, headings, emphasis, inline code, fenced code;
- lists, blockquotes, rules, simple pipe tables;
- links with an allowlist (`http`, `https`, `mailto`, same-origin path,
  fragment); and
- escaped HTML for everything else.

Keep citations in a separate list below the answer. Do not let a model-authored
link inherit the citation UI’s trust.

Test raw HTML, `javascript:` URLs, `data:` URLs, protocol-relative URLs,
backslash paths, quoted attributes, fenced code, tables, and line breaks.
Reference: `web/markdown.js` and `tests/markdown_check.js`.

## 6. Service surface

For a dev-container prototype, a small static server plus one API route is
enough:

- serve `web/`;
- serve the current `_build/html` at `/docs/`;
- inject `/config.js`;
- expose `/api/assistant`;
- contain every resolved path under its intended root;
- set correct MIME types and `Cache-Control: no-store`;
- return clear 404/413/504 responses; and
- keep runtime logs and PID files untracked.

The service does not need app-level authentication when the network and identity
gate is the actual boundary. It does need to be described accurately: if it is
bound to `0.0.0.0` for a tunnel, say that; do not call it “loopback-only.”

Reference: `server/assistant.py`, `.gitignore`.

## 7. Quality gates that keep the pattern from drifting

Add tests for the behavior that matters:

- the static page remains disabled by default;
- the client rejects an external endpoint;
- the provider command has `--standalone`, `--agent`, and no `--auto`;
- the agent config allows read/search and denies edit, destructive shell, Code
  Mode, web, and subagent;
- a real or recorded shell probe can search and cannot create a file;
- the retrieval fixture prefers the specific registry note;
- every citation URL maps to the expected surface;
- Markdown escapes raw HTML and rejects unsafe URL schemes; and
- the public page still renders with the backend absent.

For a prototype, a committed Node script plus a Python wrapper is cheap. Keep the
existing Python dashboard green; do not add a build step just for the assistant.

## 8. Copy checklist for the next prototype

1. Start from the static template. Default `assistantEndpoint` to `null`.
2. Add the small same-origin server; keep the static artifact independently
   deployable.
3. Add a tracked `opencode.json` agent profile. Copy the deny-first shell
   allowlist and adapt the command names.
4. Point the evidence index at the real workspace registry, notes, and demo data.
   Add environment overrides for other checkouts.
5. Use local docs for `docs/` citations; use canonical repositories for notes and
   registry files.
6. Add the safe Markdown renderer and its contract tests.
7. Wire the client endpoint through exact-origin resolution.
8. Add the config, command, retrieval, citation, and XSS tests.
9. Document the trust model and the “not a sandbox” caveat in the prototype’s
   README.
10. Keep logs, PID files, and generated docs out of git.
11. Restart the local service and run the real assistant once before sharing.
12. Keep the public static deployment free of the assistant unless a hosting
    decision explicitly says otherwise.

## 9. When to escalate beyond this pattern

Add application-level controls only when the deployment changes:

- the app leaves the Cloudflare Access / Globus / CWL boundary;
- untrusted users can reach the backend;
- the app accepts writes, uploads, or account actions;
- the assistant can access secrets it should not read;
- the provider is billed per request by an unknown audience; or
- the app becomes a public service rather than a collaborator demo.

At that point, add authentication, Origin/CSRF checks, rate limits, request
schema validation, response caps, a human review path, and a secret boundary.
Do not bolt those onto a trusted prototype just to make the security checklist
look complete.

## Evidence from the IRSS demo

- Implementation branch: `UBC-FRESH/fresh-irss-demo`, `feature/p2-assistant`
- Agent profile: `opencode.json`
- Assistant service: `server/assistant.py`
- Chat renderer: `web/markdown.js`
- Retrieval and citation tests: `tests/test_assistant_server.py`
- Markdown contract: `tests/markdown_check.js`
- Agent commit: `178fb9c` (read-only shell allowlist), with the broader accuracy
  pass in `d40480b`

Verified during the build:

- a real `rg` search through the agent found `CARB-03` in the expansion registry;
- a `touch` request was denied and created no file;
- the assistant returned cited, non-dead answers from the local docs and the
  expansion notes; and
- the dashboard and PR CI were green.
