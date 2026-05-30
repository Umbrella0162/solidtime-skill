# TimeEntry API

## GET /v1/organizations/{org}/time-entries
Get time entries in an organization with rich filtering.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `member_id` | string | Filter by member |
| `user_id` | string | Filter by user |
| `start` | ISO8601 | Entries starting after this time |
| `end` | ISO8601 | Entries starting before this time |
| `active` | boolean | Only active/running entries |
| `billable` | boolean | Only billable entries |
| `limit` | integer | Max entries to return |
| `offset` | integer | Pagination offset |
| `only_full_dates` | boolean | Only entries with both start and end |
| `rounding_type` | string | Rounding mode |
| `rounding_minutes` | integer | Rounding interval in minutes |
| `member_ids[]` | string[] | Filter by multiple members |
| `client_ids[]` | string[] | Filter by multiple clients |
| `project_ids[]` | string[] | Filter by multiple projects |
| `tag_ids[]` | string[] | Filter by multiple tags |
| `task_ids[]` | string[] | Filter by multiple tasks |

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "start": "ISO8601",
    "end": "ISO8601|null (null = running timer)",
    "duration": "integer|null (seconds)",
    "description": "string|null",
    "task_id": "string|null",
    "project_id": "string|null",
    "organization_id": "string",
    "user_id": "string",
    "tags": ["string (tag IDs)"],
    "billable": true
  }]
}
```

## POST /v1/organizations/{org}/time-entries
Create a time entry. Omit `end` to start a running timer.

**Body:**
```json
{
  "member_id": "string (required)",
  "start": "ISO8601 (required, e.g. 2000-02-22T14:58:59Z)",
  "billable": "boolean (required)",
  "end": "ISO8601|null (omit to start timer)",
  "project_id": "string|null",
  "task_id": "string|null",
  "description": "string|null",
  "tags": ["string (tag IDs)"]|null
}
```

## PUT /v1/organizations/{org}/time-entries/{timeEntry}
Update a time entry. Set `end` to stop a running timer.

**Body (all optional):**
```json
{
  "member_id": "string",
  "start": "ISO8601",
  "end": "ISO8601|null",
  "billable": "boolean",
  "project_id": "string|null",
  "task_id": "string|null",
  "description": "string|null",
  "tags": ["string"]|null
}
```

## PATCH /v1/organizations/{org}/time-entries
Update multiple time entries at once.

**Body:**
```json
{
  "ids": ["string (time entry IDs)"],
  "changes": {
    "project_id": "string|null",
    "billable": true,
    "tags": ["string"]|null
  }
}
```

## DELETE /v1/organizations/{org}/time-entries
Delete multiple time entries. **Query Params:** `ids` (repeated) — Time entry IDs to delete.

## DELETE /v1/organizations/{org}/time-entries/{timeEntry}
Delete a single time entry. Response: 204 No Content.

## GET /v1/organizations/{org}/time-entries/export
Export time entries as CSV or XLSX.

**Query Params:** `format` (csv|xlsx), `debug` (boolean), plus same filters as GET time-entries.

## GET /v1/organizations/{org}/time-entries/aggregate
Get aggregated time entry data.

**Additional Query Params:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `group` | string | Group results by (e.g. project, date) |
| `sub_group` | string | Sub-group within groups |
| `fill_gaps_in_time_groups` | boolean | Fill date gaps with zero values |

Also supports all same filters as GET time-entries.

## GET /v1/organizations/{org}/time-entries/aggregate/export
Export aggregated data as CSV or XLSX.

**Query Params:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | string (csv|xlsx) | Export format |
| `group` | string | Group results by |
| `sub_group` | string | Sub-group within groups |
| `history_group` | string|null | Group for history data |
| `fill_gaps_in_time_groups` | boolean | Fill date gaps with zero values |
| `debug` | boolean | Debug mode |
| `member_id` | string | Filter by member |
| `user_id` | string | Filter by user |
| `start` | ISO8601|null | Entries starting after |
| `end` | ISO8601|null | Entries starting before |
| `active` | boolean | Only active entries |
| `billable` | boolean | Only billable entries |
| `rounding_type` | string|null | Rounding mode |
| `rounding_minutes` | integer|null | Rounding interval |
| `member_ids` | string[] | Multiple members |
| `project_ids` | string[] | Multiple projects |
| `client_ids` | string[] | Multiple clients |
| `tag_ids` | string[] | Multiple tags |
| `task_ids` | string[] | Multiple tasks |