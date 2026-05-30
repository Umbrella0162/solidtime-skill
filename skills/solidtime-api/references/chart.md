# Chart API

All chart endpoints are GET requests under `/v1/organizations/{org}/charts/`. They return data for dashboard visualizations.

## GET /v1/organizations/{org}/charts/weekly-project-overview
**Response 200:**
```json
[{ "value": "integer", "name": "string", "color": "string" }]
```

## GET /v1/organizations/{org}/charts/latest-tasks
**Response 200:**
```json
[{ "task_id": "string", "name": "string", "description": "string|null", "status": "boolean", "time_entry_id": "string|null" }]
```

## GET /v1/organizations/{org}/charts/last-seven-days
**Response 200:**
```json
[{ "date": "string", "duration": "integer", "history": ["integer"] }]
```

## GET /v1/organizations/{org}/charts/latest-team-activity
**Response 200:**
```json
[{ "member_id": "string", "name": "string", "description": "string|null", "time_entry_id": "string", "task_id": "string|null", "status": "boolean" }]
```

## GET /v1/organizations/{org}/charts/daily-tracked-hours
**Response 200:**
```json
[{ "date": "string", "duration": "integer" }]
```

## GET /v1/organizations/{org}/charts/total-weekly-time
**Response 200:** `integer` (total seconds)

## GET /v1/organizations/{org}/charts/total-weekly-billable-time
**Response 200:** `integer` (total billable seconds)

## GET /v1/organizations/{org}/charts/total-weekly-billable-amount
**Response 200:** `integer` (total billable amount)

## GET /v1/organizations/{org}/charts/weekly-history
**Response 200:** Weekly history data array.