# CLAUDE.md

The rules for every agent live in `AGENTS.md`; this file adds only what is specific to Claude Code.

@AGENTS.md

## Claude Code specifics

- **Template.** Passages marked `<!-- template-example: … -->` in the agent files describe the bundled example (`myproject`); after adopting the template, rewrite them from your own code (the `adopt-template` skill).
- **Reuse first.** Search `docs/api/capabilities.md` (every public name in the package) before writing a loader, a model, a training step or a helper in a script or a notebook; the "Reuse before you write" table in `AGENTS.md` maps the usual hand-rolled code to what already exists.
- **One environment manager.** Everything runs through `pixi run <task>` (the `[tool.pixi.*]` tables in `pyproject.toml`; `pixi task list` shows them), the same commands CI runs.
- **Skills** in `.claude/skills/` load on their own when a task matches their description (or run them as `/<name>`):
  - adopting the template: `adopt-template`;
  - research workflow: `add-experiment`, `add-dataset`, `add-model`, `add-notebook`, `reproduce-results`, `write-up-results`;
  - shipping: `pre-pr-check`, `myproject-review`, `squash-commit`;
  - GitHub housekeeping: `create-gh-issue`, `link-gh-issues`.
- **Personal skills** from [jejagents](https://github.com/jejjohnson/jejagents), when installed in `~/.claude/skills/`, set the house style: `python-style` for any Python, `eman-style-math` for any maths, `code-sketch` for pseudocode, `eman-prose-tech` for write-ups (with `write-up-results`), `derivation` / `derivation-myst` for derivations in the docs, `report` before `create-gh-issue`. The "House style" and "Personal skills" sections of `AGENTS.md` say which covers what; where a skill and `AGENTS.md` disagree, `AGENTS.md` wins.
- **Subagents** (`.claude/agents/`), both read-only, both used by `myproject-review`; run them on any diff that adds code, configs or pipeline stages, before committing:
  - `reuse-reviewer`: does the diff re-implement something in the package (`docs/api/capabilities.md`), a script, a config or a tool, or put reusable code in a script or notebook?
  - `reproducibility-reviewer`: seeds, hard-coded settings, incomplete DVC stages, leakage between splits, metrics written where nothing reads them, working-directory paths, results that cannot be regenerated.
- **GitHub.** GraphQL is blocked in Claude sessions, so issues, sub-issue and blocked-by links go through REST (`gh api repos/...`, as `create-gh-issue`, `link-gh-issues` and `.github/scripts/link-issues.sh` do). When the `gh` CLI is unavailable, use the GitHub MCP tools for the same operations (PRs, issues, review threads, check runs).
- **Commits.** No `Co-Authored-By: Claude` trailer and no "Generated with Claude Code" line, unless the maintainer asks.
