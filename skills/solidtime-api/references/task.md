# Task API

## GET /v1/organizations/{org}/tasks
List tasks in an organization.

**Query Params:** `page`, `project_id` (string), `done` (boolean)

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "name": "string",
    "is_done": true,
    "project_id": "string",
    "estimated_time": "integer|null (seconds)",
    "spent_time": "integer (seconds, excl. running entries)",
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }]
}
```

## POST /v1/organizations/{org}/tasks
Create a task.

**Body:**
```json
{
  "name": "string (required)",
  "project_id": "string (required)",
  "estimated_time": "integer|null (seconds)"
}
```

## PUT /v1/organizations/{org}/tasks/{task}
Update a task.

**Body:**
```json
{
  "name": "string (required)",
  "is_done": "boolean",
  "estimated_time": "integer|null (seconds)"
}
```

## DELETE /v1/organizations/{org}/tasks/{task}
Delete a task. Response: 204 No Content.