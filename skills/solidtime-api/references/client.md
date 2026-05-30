# Client API

## GET /v1/organizations/{org}/clients
List clients in an organization.

**Query Params:** `page`, `archived` (boolean)

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "name": "string",
    "is_archived": true,
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }]
}
```

## POST /v1/organizations/{org}/clients
Create a client.

**Body:** `{ "name": "string" (required) }`

## PUT /v1/organizations/{org}/clients/{client}
Update a client.

**Body:**
```json
{
  "name": "string (required)",
  "is_archived": "boolean"
}
```

## DELETE /v1/organizations/{org}/clients/{client}
Delete a client. Response: 204 No Content.