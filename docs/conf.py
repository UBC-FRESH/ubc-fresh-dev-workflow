"""Sphinx configuration for the UBC-FRESH dev workflow documentation."""

project = "UBC-FRESH Dev Workflow"
author = "UBC FRESH Lab"
copyright = "2026, UBC FRESH Lab"

extensions = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_title = "UBC-FRESH Dev Workflow"
html_extra_path = ["llms.txt"]
