# Report API

## GET /v1/organizations/{org}/reports
List reports.

**Query Params:** `page`

**Response 200:**
```json
{
  "data": [{
    "id": "string",
    "name": "string",
    "description": "string|null",
    "is_public": true,
    "public_until": "string|null",
    "shareable_link": "string|null",
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  }]
}
```

## POST /v1/organizations/{org}/reports
Create a report.

**Body:**
```json
{
  "name": "string (required)",
  "is_public": "boolean (required)",
  "properties": "object (required)",
  "description": "string|null",
  "public_until": "ISO8601|null (after this date the report auto-sets to private)"
}
```

## GET /v1/organizations/{org}/reports/{report}
Get a single report with full data.

**Response 200:** Includes all basic fields plus: `currency`, `number_format`, `currency_format`, `date_format`, `interval_format`, `time_format`, `currency_symbol`, `data` (aggregated data object), `history_data` (historic aggregated data object).

## PUT /v1/organizations/{org}/reports/{report}
Update a report.

**Body (all optional):**
```json
{
  "name": "string",
  "description": "string|null",
  "is_public": "boolean",
  "public_until": "ISO8601|null"
}
```

## DELETE /v1/organizations/{org}/reports/{report}
Delete a report. Response: 204 No Content.

## GET /v1/public/reports
Get a report by share secret. No authentication required. Returns same shape as GET single report.