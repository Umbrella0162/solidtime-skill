# Project API

## GET /v1/organizations/{org}/projects
List projects visible to the current user.

**Query Params:** `page` (string), `archived` (boolean)

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "name": "string",
    "color": "string",
    "client_id": "string|null",
    "is_archived": true,
    "billable_rate": "integer|null (cents/hr)",
    "is_billable": true,
    "estimated_time": "integer|null (seconds)",
    "spent_time": "integer (seconds, excl. running entries)",
    "is_public": true
  }]
}
```

## POST /v1/organizations/{org}/projects
Create a project.

**Body:**
```json
{
  "name": "string (required, unique per client+org)",
  "color": "string (required, e.g. #FF5733)",
  "is_billable": "boolean (required)",
  "client_id": "string|null",
  "billable_rate": "integer|null (cents/hr)",
  "estimated_time": "integer|null (seconds)",
  "is_public": "boolean"
}
```

## GET /v1/organizations/{org}/projects/{project}
Get a single project. Response: same shape as one item from the list.

## PUT /v1/organizations/{org}/projects/{project}
Update a project.

**Body:**
```json
{
  "name": "string (required)",
  "color": "string (required)",
  "is_billable": "boolean (required)",
  "is_archived": "boolean",
  "is_public": "boolean",
  "client_id": "string|null",
  "billable_rate": "integer|null (cents/hr)",
  "estimated_time": "integer|null (seconds)"
}
```

## DELETE /v1/organizations/{org}/projects/{project}
Delete a project. Response: 204 No Content.