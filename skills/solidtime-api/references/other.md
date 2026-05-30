# Currency, Export & Import API

## Currency

### GET /v1/currencies
Get all supported currencies. No authentication required.

---

## Export

### POST /v1/organizations/{org}/export
Export all organization data. Returns a ZIP file containing:
- One CSV file per entity (time entries, projects, tasks, clients, tags, members, etc.)
- `meta.json` with export metadata

---

## Import

### GET /v1/organizations/{org}/importers
Get information about available importers and their required data formats.

### POST /v1/organizations/{org}/import
Import data into the organization.

**Body:**
```json
{
  "type": "string (required) — importer type",
  "data": "string (required) — import data payload"
}
```

**Supported import types:** Toggl, Clockify, Timeentry CSV.