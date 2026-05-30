# SolidTime API Skill

A skill for interacting with the [SolidTime](https://www.solidtime.io/) REST API — the modern open-source time-tracking application.

## What It Does

- **Time Tracking**: Start/stop timers, create/update/delete time entries, bulk operations
- **Project Management**: CRUD projects, tasks, clients, tags
- **Team Management**: Members, project members, invitations
- **Reporting**: Reports, aggregated time data, chart data
- **Data**: Export (CSV/XLSX/ZIP), import (Toggl/Clockify/CSV)

## Safety

All write operations (POST, PUT, PATCH, DELETE) require explicit user confirmation before execution. Read operations (GET) are safe and can be used freely.

## Structure

```
solidtime/
├── SKILL.md                 # Core skill instructions (progressive disclosure L2)
├── agents/
│   └── openai.yaml          # UI metadata
├── references/
│   ├── user.md              # User, memberships, API tokens
│   ├── timeentry.md         # Time entry CRUD, timer, aggregation, export
│   ├── project.md           # Project CRUD
│   ├── task.md              # Task CRUD
│   ├── client.md            # Client CRUD
│   ├── tag.md               # Tag CRUD
│   ├── member.md            # Member & project member management
│   ├── organization.md     # Organization settings & invitations
│   ├── report.md            # Report CRUD & public sharing
│   ├── chart.md             # Dashboard chart endpoints
│   └── other.md             # Currencies, export/import
└── .gitignore
```

Reference files are loaded progressively — only the module needed for the current task is loaded into context.

## Installation

```bash
# Via LobeHub Skill Market
# Search for "solidtime" and install

# Via GitHub URL
# Import from this repository URL
```

## Configuration

Set these environment variables (or provide via your agent platform):

| Variable | Description |
|----------|-------------|
| `SOLIDTIME_API_TOKEN` | Your SolidTime Bearer token |
| `SOLIDTIME_BASE_URL` | Override base URL for self-hosted instances (default: `https://app.solidtime.io/api`) |

## License

MIT