---
name: solidtime-reader
description: |
  Read-only SolidTime API skill for querying time tracking data safely. Use this skill whenever the user wants to view, check, or query SolidTime data — reading time entries, listing projects/tasks/members, checking active timer, generating reports or charts — without making any modifications. Trigger on keywords like "check solidtime", "view my time entries", "solidtime status", "how many hours this week", "list solidtime projects", "solidtime report", "read solidtime data". Prefer this over solidtime-api when the user only needs to read data.
---

# SolidTime Reader Skill

A **read-only** skill for SolidTime. Uses a bundled Python script (`scripts/solidtime_reader.py`) to query the API — no curl, no manual URL construction, no risk of accidental data modification.

## Safety

This skill **only performs GET requests**. It cannot create, update, or delete any data. Safe to use freely without confirmation.

## Quick Start

### Prerequisites

Set environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `SOLIDTIME_API_TOKEN` | Yes | Your SolidTime Bearer token |
| `SOLIDTIME_BASE_URL` | No | Override for self-hosted (default: `https://app.solidtime.io/api`) |

### First Run

```bash
# Discover your organizations
python3 scripts/solidtime_reader.py me
python3 scripts/solidtime_reader.py memberships
```

## Output Format

All commands support the `--format` / `-f` flag to control output format:

| Format | Flag | Description |
|--------|------|-------------|
| **pretty** | `-f pretty` | Human-readable, aligned (default) |
| **json** | `-f json` | JSON array of objects, machine-parsable |

```bash
# Default: pretty
python3 scripts/solidtime_reader.py entries-week ORG_ID

# For scripts / piping
python3 scripts/solidtime_reader.py entries-week ORG_ID -f json
```

### Structured data notes

- **Durations**: pretty = `3h 24m`, json = `3.4` (decimal hours)
- **Billable rates**: pretty = `$50.00/hr`, json = `50.0` (decimal)
- **Timestamps**: pretty = `2026-05-29 09:00 UTC`, json = `2026-05-29T09:00:00Z`
- **Null/empty**: pretty = `—`, json = `null`

## Commands Reference

Run with `python3 scripts/solidtime_reader.py <command> [args]`

### User & Auth

| Command | Args | Description |
|---------|------|-------------|
| `me` | — | Get current user info |
| `memberships` | — | List all organizations you belong to |
| `active-timer` | — | Get currently running time entry (or "No active timer") |
| `tokens` | — | List your API tokens |

### Organization

| Command | Args | Description |
|---------|------|-------------|
| `org` | `<org_id>` | Get organization details |

### Time Entries

| Command | Args | Description |
|---------|------|-------------|
| `entries` | `<org_id>` | List time entries (supports filters) |
| `entries-today` | `<org_id>` | Today's time entries |
| `entries-week` | `<org_id>` | This week's time entries |
| `entries-month` | `<org_id>` | This month's time entries |
| `aggregate` | `<org_id> [--group <field>]` | Aggregated time data |
| `entry` | `<org_id> <entry_id>` | Get single time entry |

### Projects, Tasks, Clients, Tags

| Command | Args | Description |
|---------|------|-------------|
| `projects` | `<org_id> [--archived]` | List projects |
| `project` | `<org_id> <project_id>` | Get project detail |
| `tasks` | `<org_id> [--project <id>] [--done]` | List tasks |
| `task` | `<org_id> <task_id>` | Get task detail |
| `clients` | `<org_id> [--archived]` | List clients |
| `tags` | `<org_id>` | List tags |

### Team

| Command | Args | Description |
|---------|------|-------------|
| `members` | `<org_id>` | List organization members |
| `project-members` | `<org_id> <project_id>` | List project members |
| `invitations` | `<org_id>` | List pending invitations |

### Reports & Charts

| Command | Args | Description |
|---------|------|-------------|
| `reports` | `<org_id>` | List reports |
| `report` | `<org_id> <report_id>` | Get report with data |
| `charts` | `<org_id> <chart_name>` | Get chart data |

Available chart names: `weekly-project-overview`, `latest-tasks`, `last-seven-days`, `latest-team-activity`, `daily-tracked-hours`, `total-weekly-time`, `total-weekly-billable-time`, `total-weekly-billable-amount`, `weekly-history`

### Other

| Command | Args | Description |
|---------|------|-------------|
| `currencies` | — | List supported currencies |
| `importers` | `<org_id>` | List available importers |

## Filter Options for `entries`

| Flag | Example | Description |
|------|---------|-------------|
| `--start` | `--start 2026-05-01` | Entries starting after date |
| `--end` | `--end 2026-05-31` | Entries starting before date |
| `--member` | `--member abc123` | Filter by member ID |
| `--project` | `--project abc123` | Filter by project ID |
| `--client` | `--client abc123` | Filter by client ID |
| `--tag` | `--tag abc123` | Filter by tag ID (repeatable) |
| `--task` | `--task abc123` | Filter by task ID |
| `--active` | `--active` | Only running entries |
| `--billable` | `--billable` | Only billable entries |
| `--limit` | `--limit 50` | Max entries to return |

## Examples

```bash
# What am I working on right now?
python3 scripts/solidtime_reader.py active-timer

# This week's hours, JSON format for processing
python3 scripts/solidtime_reader.py entries-week ORG_ID -f json

# Month's entries as JSON
python3 scripts/solidtime_reader.py entries ORG_ID --start 2026-05-01 --end 2026-05-31 -f json

# Aggregate by project
python3 scripts/solidtime_reader.py aggregate ORG_ID --group project

# Team activity chart
python3 scripts/solidtime_reader.py charts ORG_ID latest-team-activity

# All tasks for a project
python3 scripts/solidtime_reader.py tasks ORG_ID --project PROJECT_ID
```

## Key Conventions

- **Billable Rates**: Stored in **cents per hour**. Script displays them as currency (e.g. 5000 → $50.00/hr in pretty, `50.0` in json).
- **Durations**: Returned in **seconds**. Pretty = `Xh Ym`, json = decimal hours.
- **Timestamps**: ISO 8601 UTC. Pretty = `YYYY-MM-DD HH:MM UTC`, json = ISO 8601.
- **Pagination**: The script fetches the first page. Use `--limit` for more results.

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | API error (check message) |
| 2 | Missing SOLIDTIME_API_TOKEN |
| 3 | Invalid arguments or unknown command |

## Self-Hosted

Set `SOLIDTIME_BASE_URL=https://your-domain/api` before running.
