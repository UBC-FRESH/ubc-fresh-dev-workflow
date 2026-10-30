Basecamp pings for blocking decisions
=====================================

A coding agent may need a human decision while a long task is running: an MFA
approval, an expired credential, a scope choice, or a failure that the logs
cannot explain. Polling a chat window or repeatedly retrying the same command is
not an acceptable substitute for asking. A Basecamp ping gives the agent one
asynchronous, attributable channel to the maintainer.

The ping is a **blocking-notification channel**, not a progress feed.

Agent identity
--------------

Use an identity that belongs to the agent, with its own Basecamp account and CLI
profile. Never sign in as the maintainer, and never reuse the maintainer's
profile. The ping shows who sent it; that attribution is the point.

Keep the profile name and account ID in local configuration, not in a tracked
file. A typical setup is:

.. code-block:: bash

   basecamp profile create <agent-profile>
   basecamp auth status --profile <agent-profile> --json
   basecamp pings post "<maintainer>" "<message>" --profile <agent-profile> --agent

Basecamp's **agent connection** flow is not available for every account. If
``basecamp auth agent connect`` reports that agents cannot be connected, use the
normal ``basecamp profile create`` or ``basecamp auth login`` OAuth flow instead.
The ping permission is the same; do not route around the account restriction.

Authentication and verification
-------------------------------

The CLI may require a browser, device code, or email verification on first use.
The agent may complete an email verification only in its own mailbox. Never put a
password, OAuth token, device code, or verification code in a ping, issue, commit,
or session transcript.

If a step needs a human MFA action, or the agent cannot access its own mailbox,
stop and ask the maintainer through the agreed fallback. Do not generate repeated
push notifications or retry the same login in a loop.

When to ping
------------

Ping only when the agent cannot continue without a human decision or approval:

- an MFA, Duo, or device approval is required;
- a credential or external account has expired or is unavailable;
- a scope decision is needed;
- a long-running job failed in a way that logs do not explain;
- the agent is about to do something outside the approved scope.

Do not ping for routine progress, a green test run, a completed analysis, or a
question that the repository documentation already answers.

Message contract
----------------

A useful ping contains:

1. the project and task;
2. the exact blocker;
3. the action needed from the maintainer;
4. the current state and the evidence already verified;
5. the deadline or expiry, if any.

Keep it short and specific. Do not include secrets. Do not attach raw transcripts
or private data.

After the ping
--------------

Stop and wait. Do not poll the maintainer's phone, send duplicate pings, or
repeat the failed operation while waiting. When the maintainer responds, resume
from the verified state and record the decision in the appropriate issue, ADR,
or changelog entry.

If the ping channel itself is unavailable
-----------------------------------------

If the Basecamp CLI is unauthenticated or the ping cannot be posted, report that
fact in the current session with the exact command and error. Do not claim the
ping was sent. The maintainer can repair the channel before the next blocking
step.
