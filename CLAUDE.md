# CLAUDE.md

The rules for every agent live in `AGENTS.md`; this file adds only what is
specific to Claude Code.

@AGENTS.md

## Claude Code specifics

- **Template.** Passages marked `<!-- template-example: … -->` in the agent files
  describe the bundled example (`myproject`); after adopting the template,
  rewrite them from your own code.
- **Reuse first.** Search `docs/api/capabilities.md` (every public name in
  the package) before writing a loader, a model, a training step or a
  helper in a script or a notebook; the "Reuse before you write" table in
  `AGENTS.md` maps the usual hand-rolled code to what already exists.
- **Two environments.** `make` / `uv run` for tests, lint, types and docs;
  `pixi run` for experiments, DVC and anything CI runs.
- **GitHub.** When the `gh` CLI is unavailable, use the GitHub MCP tools for
  the same operations (PRs, issues, review threads, check runs).
