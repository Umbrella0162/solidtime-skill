# Tag API

## GET /v1/organizations/{org}/tags
List tags in an organization.

**Query Params:** `page`

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "name": "string",
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }]
}
```

## POST /v1/organizations/{org}/tags
Create a tag.

**Body:** `{ "name": "string" (required) }`

## PUT /v1/organizations/{org}/tags/{tag}
Update a tag.

**Body:** `{ "name": "string" (required) }`

## DELETE /v1/organizations/{org}/tags/{tag}
Delete a tag. Response: 204 No Content.