# Claude Code Context

@AGENTS.md

## Claude-Specific Instructions

### Slash Commands

- `/project:wrap-up` -- End-of-session routine (update RESUME.md, STATUS.md, commit, push)
- `/project:status-report` -- Generate client-ready status summary

### Tool Permissions

See `.claude/settings.local.json` for allowed bash commands.

### Important

- Always update STATUS.md when tasks complete or status changes
- Always update RESUME.md at end of session
- Use `project.yml` for machine-readable metadata, not hardcoded values
- Detailed conventions are in `.claude/rules/precept-conventions.md` (auto-loaded)
