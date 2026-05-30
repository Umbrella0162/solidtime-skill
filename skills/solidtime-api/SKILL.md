---
name: solidtime-api
description: |
  Interact with the SolidTime API for time tracking, project management, and reporting. Use this skill whenever the user mentions SolidTime, solidtime, time tracking API, time entry CRUD, project/task management via API, tracking billable hours, generating time reports, or managing organizations/members/tags/clients programmatically. Also activate when the user wants to automate time tracking workflows, integrate SolidTime with other tools, or asks about SolidTime REST API endpoints. Trigger on keywords like "solidtime timer", "start/stop timer solidtime", "solidtime projects", "solidtime report", "log hours solidtime", "track time solidtime".
---

# SolidTime API Skill

SolidTime is a modern open-source time-tracking application with a comprehensive REST API. This skill enables you to interact with the SolidTime API to manage time entries, projects, tasks, clients, tags, members, reports, and more.

## Quick Start

### Authentication

All API requests require a Bearer token in the Authorization header:

```
Authorization: Bearer <api-token>
```

Create a token via UI: Profile Settings → Create API Token. Or via API:
```bash
curl -X POST https://app.solidtime.io/api/v1/users/me/api-tokens \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <existing-token>" \
  -d '{"name": "My API Token"}'
```
⚠️ The `access_token` is shown only once in the response — save it immediately.

### Base URL

- **Production**: `https://app.solidtime.io/api`
- **Staging**: `https://app.staging.solidtime.io/api`
- **Self-hosted**: `https://<your-domain>/api`

### Key Conventions

- **Organization Context**: Most endpoints require `{organization}` path param (org ID). Get your orgs via `GET /v1/users/me/memberships`.
- **Timestamps**: ISO 8601 UTC format, e.g. `"2024-02-26T17:17:17Z"`.
- **Billable Rates**: Stored in **cents per hour** (integer). $50/hr = 5000.
- **Durations**: In **seconds** (integer). 1.5 hours = 5400 seconds.
- **Pagination**: List endpoints support `page` query parameter.

## Safety & Data Integrity

This skill interacts with a live API that stores real work data. Follow these rules:

- **Read operations** (GET) are safe to execute freely — they only retrieve information.
- **Write operations** (POST, PUT, PATCH, DELETE) modify, create, or delete real data. Before executing any write operation, clearly explain what will happen and wait for explicit user confirmation. For example: "This will create a new project called 'X' in organization Y. Proceed?"
- **Destructive operations** (DELETE, revoke, remove) are irreversible. Always show exactly what will be deleted and require confirmation. When multiple items are affected (bulk delete, merge member), list them explicitly.
- **Never execute bulk modifications** (PATCH multiple time entries, DELETE multiple entries, merge member) without first showing the affected item count and getting approval.
- **Credential safety**: Never log, echo, or persistently store API tokens. Use them only in request headers. If a token is accidentally exposed in conversation, advise the user to revoke it immediately.

## Core Workflows

These are the most common workflows you'll help users with. For full endpoint details, load the relevant `references/<module>.md` file.

### Start a Timer
```bash
# 1. Get org ID and member ID
curl -H "Authorization: Bearer $TOKEN" \
  https://app.solidtime.io/api/v1/users/me/memberships

# 2. Start timer (omit "end" to make it active/running)
curl -X POST https://app.solidtime.io/api/v1/organizations/$ORG_ID/time-entries \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"member_id":"MEMBER_ID","start":"2026-05-29T09:00:00Z","billable":true,"project_id":"PROJECT_ID","description":"Working on feature X"}'
```

### Stop a Timer
```bash
# 1. Get active time entry
curl -H "Authorization: Bearer $TOKEN" \
  https://app.solidtime.io/api/v1/users/me/time-entries/active

# 2. Set end time to stop
curl -X PUT https://app.solidtime.io/api/v1/organizations/$ORG_ID/time-entries/$ENTRY_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"end":"2026-05-29T17:00:00Z"}'
```

### Create Project + Task + Start Tracking
```bash
# Create project
curl -X POST https://app.solidtime.io/api/v1/organizations/$ORG_ID/projects \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Website Redesign","color":"#FF5733","is_billable":true,"billable_rate":7500}'

# Create task
curl -X POST https://app.solidtime.io/api/v1/organizations/$ORG_ID/tasks \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Design homepage","project_id":"PROJECT_ID","estimated_time":14400}'

# Start tracking on the task
curl -X POST https://app.solidtime.io/api/v1/organizations/$ORG_ID/time-entries \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"member_id":"MEMBER_ID","start":"2026-05-29T09:00:00Z","billable":true,"project_id":"PROJECT_ID","task_id":"TASK_ID"}'
```

### Get This Week's Time Entries
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://app.solidtime.io/api/v1/organizations/$ORG_ID/time-entries?start=2026-05-25T00:00:00Z&end=2026-05-31T23:59:59Z"
```

## API Endpoint Summary

Below is a quick-reference table. For full request/response schemas and all query parameters, load the relevant `references/<module>.md` file.

| Resource | Method | Endpoint | Summary |
|----------|--------|----------|---------|
| **User** | GET | `/v1/users/me` | Get current user |
| | GET | `/v1/users/me/memberships` | Get user memberships (with org info) |
| | GET | `/v1/users/me/time-entries/active` | Get active/running time entry |
| **ApiToken** | GET | `/v1/users/me/api-tokens` | List API tokens |
| | POST | `/v1/users/me/api-tokens` | Create API token |
| | POST | `/v1/users/me/api-tokens/{id}/revoke` | Revoke token |
| | DELETE | `/v1/users/me/api-tokens/{id}` | Delete token |
| **Organization** | GET | `/v1/organizations/{org}` | Get organization |
| | PUT | `/v1/organizations/{org}` | Update organization |
| **TimeEntry** | GET | `/v1/organizations/{org}/time-entries` | List time entries (many filters) |
| | POST | `/v1/organizations/{org}/time-entries` | Create time entry |
| | PUT | `/v1/organizations/{org}/time-entries/{id}` | Update time entry |
| | PATCH | `/v1/organizations/{org}/time-entries` | Update multiple entries |
| | DELETE | `/v1/organizations/{org}/time-entries/{id}` | Delete entry |
| | DELETE | `/v1/organizations/{org}/time-entries` | Delete multiple entries |
| | GET | `/v1/organizations/{org}/time-entries/export` | Export (csv/xlsx) |
| | GET | `/v1/organizations/{org}/time-entries/aggregate` | Aggregated data |
| | GET | `/v1/organizations/{org}/time-entries/aggregate/export` | Export aggregated |
| **Project** | GET | `/v1/organizations/{org}/projects` | List projects |
| | POST | `/v1/organizations/{org}/projects` | Create project |
| | GET | `/v1/organizations/{org}/projects/{id}` | Get project |
| | PUT | `/v1/organizations/{org}/projects/{id}` | Update project |
| | DELETE | `/v1/organizations/{org}/projects/{id}` | Delete project |
| **Task** | GET | `/v1/organizations/{org}/tasks` | List tasks |
| | POST | `/v1/organizations/{org}/tasks` | Create task |
| | PUT | `/v1/organizations/{org}/tasks/{id}` | Update task |
| | DELETE | `/v1/organizations/{org}/tasks/{id}` | Delete task |
| **Client** | GET | `/v1/organizations/{org}/clients` | List clients |
| | POST | `/v1/organizations/{org}/clients` | Create client |
| | PUT | `/v1/organizations/{org}/clients/{id}` | Update client |
| | DELETE | `/v1/organizations/{org}/clients/{id}` | Delete client |
| **Tag** | GET | `/v1/organizations/{org}/tags` | List tags |
| | POST | `/v1/organizations/{org}/tags` | Create tag |
| | PUT | `/v1/organizations/{org}/tags/{id}` | Update tag |
| | DELETE | `/v1/organizations/{org}/tags/{id}` | Delete tag |
| **Member** | GET | `/v1/organizations/{org}/members` | List members |
| | PUT | `/v1/organizations/{org}/members/{id}` | Update member |
| | DELETE | `/v1/organizations/{org}/members/{id}` | Remove member |
| | POST | `/v1/organizations/{org}/members/{id}/invite-placeholder` | Invite placeholder |
| | POST | `/v1/organizations/{org}/members/{id}/make-placeholder` | Make placeholder |
| | POST | `/v1/organizations/{org}/member/{id}/merge-into` | Merge member |
| **ProjectMember** | GET | `/v1/organizations/{org}/projects/{pid}/project-members` | List project members |
| | POST | `/v1/organizations/{org}/projects/{pid}/project-members` | Add project member |
| | PUT | `/v1/organizations/{org}/project-members/{id}` | Update project member |
| | DELETE | `/v1/organizations/{org}/project-members/{id}` | Remove project member |
| **Invitation** | GET | `/v1/organizations/{org}/invitations` | List invitations |
| | POST | `/v1/organizations/{org}/invitations` | Invite user |
| | POST | `/v1/organizations/{org}/invitations/{id}/resend` | Resend invitation |
| | DELETE | `/v1/organizations/{org}/invitations/{id}` | Remove invitation |
| **Report** | GET | `/v1/organizations/{org}/reports` | List reports |
| | POST | `/v1/organizations/{org}/reports` | Create report |
| | GET | `/v1/organizations/{org}/reports/{id}` | Get report |
| | PUT | `/v1/organizations/{org}/reports/{id}` | Update report |
| | DELETE | `/v1/organizations/{org}/reports/{id}` | Delete report |
| | GET | `/v1/public/reports` | Get public report |
| **Chart** | GET | `/v1/organizations/{org}/charts/*` | 8 chart endpoints (see reference) |
| **Other** | GET | `/v1/currencies` | Get all currencies |
| | POST | `/v1/organizations/{org}/export` | Export org data (ZIP) |
| | GET | `/v1/organizations/{org}/importers` | Get available importers |
| | POST | `/v1/organizations/{org}/import` | Import data |

## Request Body Schemas

### Create Time Entry (POST /time-entries)
```json
{
  "member_id": "string (required)",
  "start": "ISO8601 (required)",
  "billable": true,
  "end": "ISO8601|null (omit to start timer)",
  "project_id": "string|null",
  "task_id": "string|null",
  "description": "string|null",
  "tags": ["tag_id"]|null
}
```

### Create Project (POST /projects)
```json
{
  "name": "string (required, unique per client+org)",
  "color": "string (required, e.g. #FF5733)",
  "is_billable": true,
  "client_id": "string|null",
  "billable_rate": "integer|null (cents/hr)",
  "estimated_time": "integer|null (seconds)",
  "is_public": true|false
}
```

### Create Task (POST /tasks)
```json
{
  "name": "string (required)",
  "project_id": "string (required)",
  "estimated_time": "integer|null (seconds)"
}
```

### Create Client (POST /clients)
```json
{
  "name": "string (required)"
}
```

### Create Tag (POST /tags)
```json
{
  "name": "string (required)"
}
```

### Invite User (POST /invitations)
```json
{
  "email": "string (required)",
  "role": "string (required)"
}
```

## Time Entry Query Parameters

The GET time-entries endpoint supports rich filtering:

| Parameter | Type | Description |
|-----------|------|-------------|
| `member_id` | string | Filter by member |
| `start` | ISO8601 | Entries starting after this time |
| `end` | ISO8601 | Entries starting before this time |
| `active` | boolean | Only active (running) entries |
| `billable` | boolean | Only billable entries |
| `limit` | integer | Max entries to return |
| `offset` | integer | Pagination offset |
| `only_full_dates` | boolean | Only entries with start and end |
| `user_id` | string | Filter by user |
| `member_ids[]` | string[] | Filter by multiple members |
| `project_ids[]` | string[] | Filter by multiple projects |
| `client_ids[]` | string[] | Filter by multiple clients |
| `tag_ids[]` | string[] | Filter by multiple tags |
| `task_ids[]` | string[] | Filter by multiple tasks |
| `rounding_type` | string | Rounding mode |
| `rounding_minutes` | integer | Rounding interval in minutes |

## Error Responses

| Status | Meaning |
|--------|---------|
| 401 | Unauthenticated — check Bearer token |
| 403 | Authorization error — insufficient permissions |
| 404 | Not found — check resource ID |
| 422 | Validation error — check request body |
| 400 | API exception — check error message |

## Self-Hosted Instances

Replace the base URL: `https://<your-domain>/api` instead of `https://app.solidtime.io/api`. All endpoint paths remain the same.

Docker deployment guide: https://docs.solidtime.io/self-hosting/guides/docker

## Reference Files (Progressive Loading)

Only load the reference file you need for the current task. Do not load all at once.

| File | When to Load |
|------|-------------|
| `references/user.md` | User info, memberships, API token management, active timer query |
| `references/timeentry.md` | Time entry CRUD, start/stop timer, bulk update/delete, export, aggregation |
| `references/project.md` | Project CRUD, archive, billable rate, estimated time |
| `references/task.md` | Task CRUD, mark done, assign to project |
| `references/client.md` | Client CRUD, archive |
| `references/tag.md` | Tag CRUD |
| `references/member.md` | Member management, project members, merge, placeholder |
| `references/organization.md` | Organization settings, invitations |
| `references/report.md` | Report CRUD, public sharing, aggregated data |
| `references/chart.md` | Dashboard chart data (8 endpoints) |
| `references/other.md` | Currencies, organization export/import |
