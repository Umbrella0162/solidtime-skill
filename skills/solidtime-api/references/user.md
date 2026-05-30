# User API

## GET /v1/users/me
Get current authenticated user.

**Response 200:**
```json
{
  "data": {
    "id": "string",
    "name": "string",
    "email": "string",
    "profile_photo_url": "string",
    "timezone": "string (e.g. Europe/Berlin)",
    "week_start": "string (Monday|Sunday|Saturday)"
  }
}
```

## GET /v1/users/me/memberships
Get user memberships with embedded organization info.

**Response 200:**
```json
{
  "data": [{
    "id": "string (membership ID)",
    "organization": {
      "id": "string",
      "name": "string",
      "is_personal": true,
      "billable_rate": "integer|null (cents/hr)",
      "currency": "string (ISO 4217)",
      "currency_symbol": "string",
      "employees_can_see_billable_rates": true,
      "employees_can_manage_tasks": true,
      "prevent_overlapping_time_entries": true
    },
    "role": "string"
  }]
}
```

## GET /v1/users/me/time-entries/active
Get the currently running time entry. Returns TimeEntryResource on 200, 404 if none is active.

## GET /v1/users/me/api-tokens
List all API tokens of the current user. Independent of organization.

**Response 200:**
```json
{
  "data": [{
    "id": "string (NOT a UUID)",
    "name": "string",
    "revoked": true,
    "scopes": ["string"],
    "created_at": "ISO8601",
    "expires_at": "ISO8601|null"
  }]
}
```

## POST /v1/users/me/api-tokens
Create a new API token. The `access_token` is only shown in this response and cannot be retrieved later.

**Body:** `{ "name": "string" (1-255 chars) }`

**Response 200:**
```json
{
  "data": {
    "id": "string",
    "name": "string",
    "revoked": true,
    "scopes": ["string"],
    "created_at": "ISO8601",
    "expires_at": "ISO8601|null",
    "access_token": "string"
  }
}
```

## POST /v1/users/me/api-tokens/{apiToken}/revoke
Revoke an API token. Response: 204 No Content.

## DELETE /v1/users/me/api-tokens/{apiToken}
Delete an API token. Response: 204 No Content.