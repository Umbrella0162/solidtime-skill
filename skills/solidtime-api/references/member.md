# Member & ProjectMember API

## Member

### GET /v1/organizations/{org}/members
List members of an organization.

**Query Params:** `page`

**Response 200:**
```json
{
  "data": [{
    "id": "string (membership ID)",
    "user_id": "string",
    "name": "string",
    "email": "string",
    "role": "string",
    "is_placeholder": true,
    "billable_rate": "integer|null (cents/hr)"
  }]
}
```

### PUT /v1/organizations/{org}/members/{member}
Update a member.

**Body:**
```json
{
  "role": "string",
  "billable_rate": "integer|null (cents/hr)"
}
```

### DELETE /v1/organizations/{org}/members/{member}
Remove a member.

**Query Params:** `delete_related`

Response: 204 No Content.

### POST /v1/organizations/{org}/members/{member}/invite-placeholder
Invite a placeholder member to become a real member. Response: 204 No Content.

### POST /v1/organizations/{org}/members/{member}/make-placeholder
Make a member a placeholder. Response: 204 No Content.

### POST /v1/organizations/{org}/member/{member}/merge-into
Merge one member into another.

**Body:** `{ "member_id": "string (destination member ID)" }`

Response: 204 No Content.

---

## ProjectMember

### GET /v1/organizations/{org}/projects/{project}/project-members
List project members for a project.

**Query Params:** `page`

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "billable_rate": "integer|null (cents/hr)",
    "member_id": "string",
    "project_id": "string"
  }]
}
```

### POST /v1/organizations/{org}/projects/{project}/project-members
Add a project member.

**Body:**
```json
{
  "member_id": "string (required)",
  "billable_rate": "integer|null (cents/hr)"
}
```

### PUT /v1/organizations/{org}/project-members/{projectMember}
Update a project member.

**Body:** `{ "billable_rate": "integer|null (cents/hr)" }`

### DELETE /v1/organizations/{org}/project-members/{projectMember}
Remove a project member. Response: 204 No Content.