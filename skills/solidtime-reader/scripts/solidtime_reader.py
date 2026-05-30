#!/usr/bin/env python3
"""SolidTime Reader — Read-only API client for SolidTime time tracking."""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

BASE_URL = os.environ.get("SOLIDTIME_BASE_URL", "https://app.solidtime.io/api")
TOKEN = os.environ.get("SOLIDTIME_API_TOKEN", "")

# ── output format ────────────────────────────────────────────────────────────

FORMAT = "pretty"  # pretty | json | csv | table

def _set_format(fmt):
    global FORMAT
    if fmt not in ("pretty", "json", "csv", "table"):
        print(f"Unknown format: {fmt} (use: pretty, json, csv, table)", file=sys.stderr)
        sys.exit(3)
    FORMAT = fmt

def _extract_format(args):
    """Remove --format/-f from args list, return remaining args."""
    remaining = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--format", "-f") and i + 1 < len(args):
            _set_format(args[i + 1])
            i += 2
        elif a.startswith("--format="):
            _set_format(a.split("=", 1)[1])
            i += 1
        else:
            remaining.append(a)
            i += 1
    return remaining

# ── formatters ───────────────────────────────────────────────────────────────

def _fmt_duration(seconds):
    if seconds is None:
        return "—"
    h, m = divmod(int(seconds), 3600)
    m2, s = divmod(m, 60)
    if h:
        return f"{h}h {m2}m"
    if m2:
        return f"{m2}m {s}s"
    return f"{s}s"

def _fmt_duration_csv(seconds):
    """Duration as decimal hours for CSV/JSON structured output."""
    if seconds is None:
        return ""
    return round(seconds / 3600, 2)

def _fmt_rate(cents):
    if cents is None:
        return "—"
    return f"${cents/100:.2f}/hr"

def _fmt_rate_csv(cents):
    if cents is None:
        return ""
    return cents / 100

def _fmt_ts(ts):
    if not ts:
        return "—"
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return ts

def _fmt_ts_csv(ts):
    if not ts:
        return ""
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ts or ""

def _out(items, headers, formatters_pretty, formatters_struct):
    """Unified output dispatcher.

    items:        list of dicts (one per row)
    headers:      list of column names (for csv/table)
    formatters_pretty:   dict {header: func(value)} for pretty print
    formatters_struct:   dict {header: func(value)} for csv/json structured data
    """
    if FORMAT == "json":
        rows = []
        for item in items:
            row = {}
            for h in headers:
                val = item.get(h)
                row[h] = formatters_struct.get(h, lambda v: v)(val)
            rows.append(row)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    if FORMAT == "csv":
        import csv, io
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(headers)
        for item in items:
            row = []
            for h in headers:
                val = item.get(h)
                row.append(formatters_struct.get(h, lambda v: v if v is not None else "")(val))
            writer.writerow(row)
        print(buf.getvalue(), end="")
        return

    if FORMAT == "table":
        # Build markdown table
        col_widths = [len(h) for h in headers]
        rows = []
        for item in items:
            row = []
            for i, h in enumerate(headers):
                val = item.get(h)
                cell = str(formatters_pretty.get(h, lambda v: v if v is not None else "—")(val))
                row.append(cell)
                col_widths[i] = max(col_widths[i], len(cell))
            rows.append(row)
        fmt = "|" + "|".join(f" {{:<{w}}} " for w in col_widths) + "|"
        sep = "|" + "|".join(f" {'—' * w} " for w in col_widths) + "|"
        print(fmt.format(*headers))
        print(sep)
        for row in rows:
            print(fmt.format(*row))
        return

    # FORMAT == "pretty" (default): use custom per-command formatting
    # Fall back: caller handles pretty output themselves
    # If we reach here, the command didn't handle pretty itself, use table as fallback
    _out(items, headers, formatters_pretty, formatters_struct)

# ── API helper ────────────────────────────────────────────────────────────────

def _api(path, params=None):
    """Make an authenticated GET request. Returns parsed JSON or None for 204/404."""
    url = f"{BASE_URL}{path}"
    if params:
        qs = urlencode(params, doseq=True)
        if qs:
            url += f"?{qs}"
    req = Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    })
    try:
        with urlopen(req, timeout=30) as resp:
            if resp.status == 204:
                return None
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body[:200]}", file=sys.stderr)
        sys.exit(1)

def _org_path(org_id, suffix):
    return f"/v1/organizations/{org_id}{suffix}"

def _week_range():
    now = datetime.now(timezone.utc)
    monday = now - timedelta(days=now.weekday())
    start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ")

def _month_range():
    now = datetime.now(timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end = now.replace(year=now.year+1, month=1, day=1) - timedelta(seconds=1)
    else:
        end = now.replace(month=now.month+1, day=1) - timedelta(seconds=1)
    return start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ")

def _today_range():
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=23, minute=59, second=59)
    return start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ")

def _print_json(data):
    if data is None:
        print("(empty)")
        return
    print(json.dumps(data, indent=2, ensure_ascii=False))

# ── user ─────────────────────────────────────────────────────────────────────

def cmd_me(args):
    r = _api("/v1/users/me")
    d = r.get("data", r)
    if FORMAT != "pretty":
        _out([d], ["id", "name", "email", "timezone", "week_start"],
             {}, {k: lambda v: v or "" for k in ["id","name","email","timezone","week_start"]})
        return
    print(f"User: {d.get('name')} <{d.get('email')}>")
    print(f"Timezone: {d.get('timezone')}")
    print(f"Week starts: {d.get('week_start')}")

def cmd_memberships(args):
    r = _api("/v1/users/me/memberships")
    items = []
    for m in r.get("data", []):
        org = m.get("organization", {})
        items.append({"org_id": org.get("id",""), "org_name": org.get("name",""), "role": m.get("role","")})
    _out(items, ["org_id", "org_name", "role"],
         {}, {k: lambda v: v or "" for k in ["org_id","org_name","role"]})
    if FORMAT == "pretty":
        # Override with aligned output
        for i in items:
            print(f"  {i['org_id']}  {i['org_name']}  role={i['role']}")

def cmd_active_timer(args):
    r = _api("/v1/users/me/time-entries/active")
    empty = r is None or (isinstance(r, dict) and not r.get("data"))
    if empty:
        if FORMAT == "json":
            print("[]")
        elif FORMAT in ("csv", "table"):
            print("No active timer" if FORMAT == "table" else "")
        else:
            print("No active timer")
        return
    d = r.get("data", r) if isinstance(r, dict) else r
    if isinstance(d, list):
        d = d[0] if d else {}
    if FORMAT != "pretty":
        _out([d], ["id", "start", "end", "duration", "description", "project_id", "task_id", "billable"],
             {"duration": _fmt_duration, "start": _fmt_ts, "end": _fmt_ts},
             {"duration": _fmt_duration_csv, "start": _fmt_ts_csv, "end": _fmt_ts_csv})
        return
    print(f"Active: {_fmt_ts(d.get('start'))}  duration={_fmt_duration(d.get('duration'))}")
    desc = d.get("description") or ""
    if desc:
        print(f"  {desc}")
    pid = d.get("project_id")
    tid = d.get("task_id")
    if pid:
        print(f"  project={pid}  task={tid or '—'}")

def cmd_tokens(args):
    r = _api("/v1/users/me/api-tokens")
    items = []
    for t in r.get("data", []):
        items.append({"id": t.get("id",""), "name": t.get("name",""), "revoked": t.get("revoked", False), "expires_at": t.get("expires_at") or "never"})
    _out(items, ["id", "name", "revoked", "expires_at"],
         {"revoked": lambda v: "REVOKED" if v else "active"},
         {"revoked": lambda v: str(v), "expires_at": lambda v: v or "never"})
    if FORMAT == "pretty":
        for i in items:
            rev = "REVOKED" if i["revoked"] else "active"
            print(f"  {i['id'][:8]}…  {i['name']}  {rev}  expires={i['expires_at']}")

# ── org ───────────────────────────────────────────────────────────────────────

def cmd_org(args):
    org_id = args[0]
    r = _api(f"/v1/organizations/{org_id}")
    d = r.get("data", r)
    if FORMAT != "pretty":
        _out([d], ["id", "name", "currency", "billable_rate", "is_personal", "prevent_overlapping_time_entries"],
             {"billable_rate": _fmt_rate},
             {"billable_rate": _fmt_rate_csv})
        return
    print(f"Organization: {d.get('name')}")
    print(f"  Currency: {d.get('currency_symbol','')} {d.get('currency','')}")
    print(f"  Billable rate: {_fmt_rate(d.get('billable_rate'))}")
    print(f"  Personal: {d.get('is_personal')}")
    print(f"  Overlap prevention: {d.get('prevent_overlapping_time_entries')}")

# ── time entries ──────────────────────────────────────────────────────────────

def _parse_entry_filters(args):
    filters = {}
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--start" and i+1 < len(args):
            filters["start"] = args[i+1] + "T00:00:00Z"; i += 2
        elif a == "--end" and i+1 < len(args):
            filters["end"] = args[i+1] + "T23:59:59Z"; i += 2
        elif a == "--member" and i+1 < len(args):
            filters["member_id"] = args[i+1]; i += 2
        elif a == "--project" and i+1 < len(args):
            filters["project_ids[]"] = args[i+1]; i += 2
        elif a == "--client" and i+1 < len(args):
            filters["client_ids[]"] = args[i+1]; i += 2
        elif a == "--tag" and i+1 < len(args):
            filters.setdefault("tag_ids[]", [])
            if isinstance(filters["tag_ids[]"], list):
                filters["tag_ids[]"].append(args[i+1])
            i += 2
        elif a == "--task" and i+1 < len(args):
            filters["task_ids[]"] = args[i+1]; i += 2
        elif a == "--active":
            filters["active"] = "true"; i += 1
        elif a == "--billable":
            filters["billable"] = "true"; i += 1
        elif a == "--limit" and i+1 < len(args):
            filters["limit"] = args[i+1]; i += 2
        else:
            i += 1
    return filters

def _entries_out(r):
    entries = r.get("data", [])
    if not entries:
        if FORMAT == "json":
            print("[]")
        else:
            print("No time entries found")
        return
    if FORMAT == "pretty":
        total = 0
        for e in entries:
            dur = e.get("duration") or 0
            total += dur
            billable = "💰" if e.get("billable") else "  "
            end = e.get("end") or "running"
            desc = (e.get("description") or "")[:40]
            print(f"  {billable} {_fmt_ts(e.get('start'))} → {end if end=='running' else _fmt_ts(end)}  {_fmt_duration(dur)}  {desc}")
        print(f"  Total: {_fmt_duration(total)} ({len(entries)} entries)")
        return
    _out(entries,
         ["id", "start", "end", "duration", "description", "project_id", "task_id", "billable"],
         {"duration": _fmt_duration, "start": _fmt_ts, "end": _fmt_ts,
          "billable": lambda v: "yes" if v else "no"},
         {"duration": _fmt_duration_csv, "start": _fmt_ts_csv, "end": _fmt_ts_csv,
          "billable": lambda v: str(v), "description": lambda v: v or "",
          "project_id": lambda v: v or "", "task_id": lambda v: v or ""})

def cmd_entries(args):
    org_id = args[0]
    filters = _parse_entry_filters(args[1:])
    r = _api(_org_path(org_id, "/time-entries"), filters)
    _entries_out(r)

def cmd_entries_today(args):
    org_id = args[0]
    s, e = _today_range()
    r = _api(_org_path(org_id, "/time-entries"), {"start": s, "end": e})
    _entries_out(r)

def cmd_entries_week(args):
    org_id = args[0]
    s, e = _week_range()
    r = _api(_org_path(org_id, "/time-entries"), {"start": s, "end": e})
    _entries_out(r)

def cmd_entries_month(args):
    org_id = args[0]
    s, e = _month_range()
    r = _api(_org_path(org_id, "/time-entries"), {"start": s, "end": e})
    _entries_out(r)

def cmd_entry(args):
    org_id, entry_id = args[0], args[1]
    r = _api(_org_path(org_id, f"/time-entries/{entry_id}"))
    d = r.get("data", r) if isinstance(r, dict) else r
    if FORMAT != "pretty":
        _out([d] if isinstance(d, dict) else d, ["id","start","end","duration","description","project_id","task_id","billable","tags"],
             {"duration": _fmt_duration, "start": _fmt_ts, "end": _fmt_ts},
             {"duration": _fmt_duration_csv, "start": _fmt_ts_csv, "end": _fmt_ts_csv})
        return
    _print_json(r)

def cmd_aggregate(args):
    org_id = args[0]
    filters = _parse_entry_filters(args[1:])
    r = _api(_org_path(org_id, "/time-entries/aggregate"), filters)
    _print_json(r)

# ── projects / tasks / clients / tags ────────────────────────────────────────

def cmd_projects(args):
    org_id = args[0]
    params = {}
    extra = args[1:]
    if "--archived" in extra:
        params["archived"] = "true"
    r = _api(_org_path(org_id, "/projects"), params)
    items = r.get("data", [])
    if FORMAT == "pretty":
        for p in items:
            arch = " [ARCHIVED]" if p.get("is_archived") else ""
            bill = "💰" if p.get("is_billable") else "  "
            spent = _fmt_duration(p.get("spent_time", 0))
            est = _fmt_duration(p.get("estimated_time")) if p.get("estimated_time") else "—"
            print(f"  {bill} {p.get('id','?')[:8]}…  {p.get('name','?')}{arch}  spent={spent} est={est}")
        return
    _out(items, ["id", "name", "is_billable", "is_archived", "billable_rate", "spent_time", "estimated_time", "is_public"],
         {"billable_rate": _fmt_rate, "spent_time": _fmt_duration, "estimated_time": _fmt_duration,
          "is_billable": lambda v: "yes" if v else "no", "is_archived": lambda v: "yes" if v else "no",
          "is_public": lambda v: "yes" if v else "no"},
         {"billable_rate": _fmt_rate_csv, "spent_time": _fmt_duration_csv,
          "estimated_time": _fmt_duration_csv, "is_billable": lambda v: str(v),
          "is_archived": lambda v: str(v), "is_public": lambda v: str(v)})

def cmd_project(args):
    org_id, pid = args[0], args[1]
    r = _api(_org_path(org_id, f"/projects/{pid}"))
    _print_json(r)

def cmd_tasks(args):
    org_id = args[0]
    params = {}
    extra = args[1:]
    i = 0
    while i < len(extra):
        if extra[i] == "--project" and i+1 < len(extra):
            params["project_id"] = extra[i+1]; i += 2
        elif extra[i] == "--done":
            params["done"] = "true"; i += 1
        else:
            i += 1
    r = _api(_org_path(org_id, "/tasks"), params)
    items = r.get("data", [])
    if FORMAT == "pretty":
        for t in items:
            done = "✓" if t.get("is_done") else " "
            spent = _fmt_duration(t.get("spent_time", 0))
            est = _fmt_duration(t.get("estimated_time")) if t.get("estimated_time") else "—"
            print(f"  [{done}] {t.get('id','?')[:8]}…  {t.get('name','?')}  spent={spent} est={est}")
        return
    _out(items, ["id", "name", "is_done", "project_id", "estimated_time", "spent_time"],
         {"is_done": lambda v: "done" if v else "open", "estimated_time": _fmt_duration, "spent_time": _fmt_duration},
         {"is_done": lambda v: str(v), "estimated_time": _fmt_duration_csv, "spent_time": _fmt_duration_csv})

def cmd_task(args):
    org_id, tid = args[0], args[1]
    r = _api(_org_path(org_id, f"/tasks/{tid}"))
    _print_json(r)

def cmd_clients(args):
    org_id = args[0]
    params = {}
    if "--archived" in args[1:]:
        params["archived"] = "true"
    r = _api(_org_path(org_id, "/clients"), params)
    items = r.get("data", [])
    if FORMAT == "pretty":
        for c in items:
            arch = " [ARCHIVED]" if c.get("is_archived") else ""
            print(f"  {c.get('id','?')[:8]}…  {c.get('name','?')}{arch}")
        return
    _out(items, ["id", "name", "is_archived"],
         {"is_archived": lambda v: "yes" if v else "no"},
         {"is_archived": lambda v: str(v)})

def cmd_tags(args):
    org_id = args[0]
    r = _api(_org_path(org_id, "/tags"))
    items = r.get("data", [])
    if FORMAT == "pretty":
        for t in items:
            print(f"  {t.get('id','?')[:8]}…  {t.get('name','?')}")
        return
    _out(items, ["id", "name"], {}, {})

# ── team ──────────────────────────────────────────────────────────────────────

def cmd_members(args):
    org_id = args[0]
    r = _api(_org_path(org_id, "/members"))
    items = r.get("data", [])
    if FORMAT == "pretty":
        for m in items:
            ph = " [placeholder]" if m.get("is_placeholder") else ""
            rate = _fmt_rate(m.get("billable_rate"))
            print(f"  {m.get('id','?')[:8]}…  {m.get('name','?')}  role={m.get('role','?')}  rate={rate}{ph}")
        return
    _out(items, ["id", "user_id", "name", "email", "role", "is_placeholder", "billable_rate"],
         {"billable_rate": _fmt_rate, "is_placeholder": lambda v: "yes" if v else "no"},
         {"billable_rate": _fmt_rate_csv, "is_placeholder": lambda v: str(v)})

def cmd_project_members(args):
    org_id, pid = args[0], args[1]
    r = _api(_org_path(org_id, f"/projects/{pid}/project-members"))
    items = r.get("data", [])
    if FORMAT == "pretty":
        for m in items:
            rate = _fmt_rate(m.get("billable_rate"))
            print(f"  {m.get('id','?')[:8]}…  member={m.get('member_id','?')[:8]}…  rate={rate}")
        return
    _out(items, ["id", "member_id", "project_id", "billable_rate"],
         {"billable_rate": _fmt_rate}, {"billable_rate": _fmt_rate_csv})

def cmd_invitations(args):
    org_id = args[0]
    r = _api(_org_path(org_id, "/invitations"))
    items = r.get("data", [])
    if FORMAT == "pretty":
        for inv in items:
            print(f"  {inv.get('id','?')[:8]}…  {inv.get('email','?')}  role={inv.get('role','?')}")
        return
    _out(items, ["id", "email", "role"], {}, {})

# ── reports / charts ──────────────────────────────────────────────────────────

def cmd_reports(args):
    org_id = args[0]
    r = _api(_org_path(org_id, "/reports"))
    items = r.get("data", [])
    if FORMAT == "pretty":
        for rp in items:
            pub = "public" if rp.get("is_public") else "private"
            link = rp.get("shareable_link") or ""
            print(f"  {rp.get('id','?')[:8]}…  {rp.get('name','?')}  [{pub}]  {link}")
        return
    _out(items, ["id", "name", "is_public", "shareable_link", "created_at", "updated_at"],
         {"is_public": lambda v: "public" if v else "private"}, {"is_public": lambda v: str(v)})

def cmd_report(args):
    org_id, rid = args[0], args[1]
    r = _api(_org_path(org_id, f"/reports/{rid}"))
    _print_json(r)

CHARTS = [
    "weekly-project-overview", "latest-tasks", "last-seven-days",
    "latest-team-activity", "daily-tracked-hours", "total-weekly-time",
    "total-weekly-billable-time", "total-weekly-billable-amount", "weekly-history",
]

def cmd_charts(args):
    org_id, name = args[0], args[1]
    if name not in CHARTS:
        print(f"Unknown chart: {name}", file=sys.stderr)
        print(f"Available: {', '.join(CHARTS)}", file=sys.stderr)
        sys.exit(3)
    r = _api(_org_path(org_id, f"/charts/{name}"))
    _print_json(r)

# ── other ─────────────────────────────────────────────────────────────────────

def cmd_currencies(args):
    r = _api("/v1/currencies")
    items = r if isinstance(r, list) else r.get("data", [])
    if FORMAT == "pretty":
        for c in items:
            if isinstance(c, dict):
                print(f"  {c.get('code','?')}  {c.get('name','?')}")
        return
    _out([i for i in items if isinstance(i, dict)], ["code", "name"], {}, {})

def cmd_importers(args):
    org_id = args[0]
    r = _api(_org_path(org_id, "/importers"))
    _print_json(r)

# ── CLI dispatch ──────────────────────────────────────────────────────────────

COMMANDS = {
    "me": (cmd_me, 0),
    "memberships": (cmd_memberships, 0),
    "active-timer": (cmd_active_timer, 0),
    "tokens": (cmd_tokens, 0),
    "org": (cmd_org, 1),
    "entries": (cmd_entries, 1),
    "entries-today": (cmd_entries_today, 1),
    "entries-week": (cmd_entries_week, 1),
    "entries-month": (cmd_entries_month, 1),
    "entry": (cmd_entry, 2),
    "aggregate": (cmd_aggregate, 1),
    "projects": (cmd_projects, 1),
    "project": (cmd_project, 2),
    "tasks": (cmd_tasks, 1),
    "task": (cmd_task, 2),
    "clients": (cmd_clients, 1),
    "tags": (cmd_tags, 1),
    "members": (cmd_members, 1),
    "project-members": (cmd_project_members, 2),
    "invitations": (cmd_invitations, 1),
    "reports": (cmd_reports, 1),
    "report": (cmd_report, 2),
    "charts": (cmd_charts, 2),
    "currencies": (cmd_currencies, 0),
    "importers": (cmd_importers, 1),
}

def main():
    if not TOKEN:
        print("Error: SOLIDTIME_API_TOKEN not set", file=sys.stderr)
        sys.exit(2)

    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(f"Usage: {sys.argv[0]} <command> [args...] [-f json|csv|table|pretty]")
        print(f"\nCommands: {', '.join(sorted(COMMANDS))}")
        print(f"\nFormats:  pretty (default), json, csv, table")
        sys.exit(0)

    cmd_name = sys.argv[1]
    if cmd_name not in COMMANDS:
        print(f"Unknown command: {cmd_name}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(COMMANDS))}", file=sys.stderr)
        sys.exit(3)

    handler, min_args = COMMANDS[cmd_name]
    raw = _extract_format(sys.argv[2:])  # strip -f/--format before counting positional args
    positional = [a for a in raw if not a.startswith("--")]
    if len(positional) < min_args:
        print(f"Usage: {sys.argv[0]} {cmd_name} {'<arg> ' * min_args}[options]", file=sys.stderr)
        sys.exit(3)

    handler(raw)

if __name__ == "__main__":
    main()
