# Organization & Invitation API

## Organization

### GET /v1/organizations/{org}
Get organization details.

**Response 200:**
```json
{
  "data": {
    "id": "string",
    "name": "string",
    "is_personal": true,
    "billable_rate": "integer|null (cents/hr)",
    "employees_can_see_billable_rates": true,
    "employees_can_manage_tasks": true,
    "prevent_overlapping_time_entries": true,
    "currency": "string (ISO 4217)",
    "currency_symbol": "string",
    "number_format": "string",
    "currency_format": "string",
    "date_format": "string",
    "interval_format": "string",
    "time_format": "string"
  }
}
```

### PUT /v1/organizations/{org}
Update organization settings.

**Body (all optional):**
```json
{
  "name": "string",
  "billable_rate": "integer|null (cents/hr)",
  "employees_can_see_billable_rates": "boolean",
  "employees_can_manage_tasks": "boolean",
  "prevent_overlapping_time_entries": "boolean",
  "number_format": "string",
  "currency_format": "string",
  "date_format": "string",
  "interval_format": "string",
  "time_format": "string"
}
```

---

## Invitation

### GET /v1/organizations/{org}/invitations
List invitations of an organization.

**Query Params:** `page`

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "email": "string",
    "role": "string"
  }]
}
```

### POST /v1/organizations/{org}/invitations
Invite a user to the organization.

**Body:**
```json
{
  "email": "string (required)",
  "role": "string (required)"
}
```

Response: 204 No Content.

### POST /v1/organizations/{org}/invitations/{invitation}/resend
Resend email for a pending invitation. Response: 204 No Content.

### DELETE /v1/organizations/{org}/invitations/{invitation}
Remove a pending invitation. Response: 204 No Content.