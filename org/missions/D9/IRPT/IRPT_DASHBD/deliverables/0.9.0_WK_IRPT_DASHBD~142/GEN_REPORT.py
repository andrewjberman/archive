"""Emit the tab's contract copy and the synthetic filled report from the contract bytes.

Writes (ASCII only):
  portal/src/pages/InvestorReporting/dashboard/report/contractMembers.ts
  portal/src/pages/InvestorReporting/dashboard/report/fixtures/syntheticReport.ts
Prints the contract sha256 and the member count.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
CONTRACT = ROOT / "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
REPORT = ROOT / "portal/src/pages/InvestorReporting/dashboard/report"
FIXTURE = REPORT / "fixtures/syntheticReport.ts"

raw = CONTRACT.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
c = json.loads(raw.decode("utf-8"))
members = c["members"]
sections = c["sections"]


def ts(v):
    return json.dumps(v, ensure_ascii=True)


# ---------- contractMembers.ts ----------
lines = []
lines.append("/* GENERATED from %s (sha256 %s) by the TO-DB-b-176 worker's emitter; do not hand-edit. */" % ("org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json", sha))
lines.append("")
lines.append("export const CONTRACT_PATH = %s" % ts("org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"))
lines.append("export const CONTRACT_SHA256 = %s" % ts(sha))
lines.append("")
lines.append("export type SectionId = %s" % " | ".join(ts(s["id"]) for s in sections))
lines.append("export type MemberUnit = 'dollars' | 'percent' | 'text' | 'series'")
lines.append("")
lines.append("export interface ContractSection {\n  readonly id: SectionId\n  readonly title: string\n}")
lines.append("")
lines.append("/** The eight sections, in the contract's order. */")
lines.append("export const CONTRACT_SECTIONS: readonly ContractSection[] = [")
for s in sections:
    lines.append("  { id: %s, title: %s }," % (ts(s["id"]), ts(s["title"])))
lines.append("]")
lines.append("")
lines.append("export interface MemberSpec {\n  readonly id: string\n  readonly section: SectionId\n  readonly label: string\n  readonly unit: MemberUnit\n  /** True when the contract marks the member ABSENT (its source is not carried by any sibling). */\n  readonly sourceAbsent: boolean\n}")
lines.append("")
lines.append("/** The contract's members, in the contract's order (%d). */" % len(members))
lines.append("export const MEMBER_SPECS: readonly MemberSpec[] = [")
for m in members:
    lines.append("  { id: %s, section: %s, label: %s, unit: %s, sourceAbsent: %s }," % (
        ts(m["id"]), ts(m["section"]), ts(m["label"]), ts(m["unit"]), "true" if m["source"] == "ABSENT" else "false"))
lines.append("]")
lines.append("")
(REPORT / "contractMembers.ts").write_text("\n".join(lines) + "\n", encoding="ascii")

# ---------- fixture ----------
ACCOUNTS = [
    {"account_id": "SYN-0001", "last4": "1001", "first_data_date": "2019-03-04",
     "window_status": {"qtd": "MEASURED", "ytd": "MEASURED", "last_12_months": "MEASURED", "since_inception": "MEASURED"}},
    {"account_id": "SYN-0002", "last4": "1002", "first_data_date": "2026-02-02",
     "window_status": {"qtd": "MEASURED", "ytd": "NOT_SPANNED", "last_12_months": "NOT_SPANNED", "since_inception": "MEASURED"}},
]
CLASSES = ["cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"]
ROW_KEYS = [a["account_id"] for a in ACCOUNTS]
VS_COLS = ("qtd", "ytd", "last_12_months", "since_inception")


def is_by_row(mid):
    if mid.startswith(("avs.", "glr.", "trgl.")):
        return True
    if mid.startswith("act.") and mid.endswith(".account"):
        return True
    return mid == "hold.allocation"


def money(seed):
    return ((seed * 7919) % 400001) + 20000


def pct(seed):
    return round((((seed * 37) % 301) - 80) / 1000.0, 4)


TEXT_VALUES = {
    "cover.as_of_date": "2026-09-30",
    "convention.fee_basis_label": None,  # filled from the contract label below
    "holdings.rows.class_hierarchy": ", ".join(CLASSES),
    "convention.inception_per_household_and_account": "Since-inception columns are headed with the inception date of that household or account.",
    "convention.not_held_for_entire_period": "Not held for the entire period",
}
dates = ["2025-10-31", "2025-11-28", "2025-12-31", "2026-01-30", "2026-02-27", "2026-03-31",
         "2026-04-30", "2026-05-29", "2026-06-30", "2026-07-31", "2026-08-31", "2026-09-30"]


def series_value(mid):
    if mid == "overview.chart.allocation_by_asset_class":
        out = []
        for k, cls in enumerate(CLASSES[:5]):
            pts = [{"date": d, "value": round(0.1 + 0.02 * k + 0.001 * j, 4)} for j, d in enumerate(dates)]
            out.append({"name": cls, "points": pts})
        return out
    if mid == "accounts.chart.allocation_by_account":
        return [{"name": a["account_id"], "points": [{"date": d, "value": round(0.45 + 0.05 * k + 0.002 * j, 4)} for j, d in enumerate(dates)]}
                for k, a in enumerate(ACCOUNTS)]
    if mid == "accounts.chart.ending_value_and_net_additions_last_12_months":
        return [{"name": a["account_id"], "points": [{"date": d, "value": 500000 + 1000 * (k + 1) * (j + 1)} for j, d in enumerate(dates)]}
                for k, a in enumerate(ACCOUNTS)]
    raise SystemExit("no series rule for %s" % mid)


def build_values(label_by_id, absent_by_id):
    vals = {}
    for i, m in enumerate(members):
        mid = m["id"]
        if m["source"] == "ABSENT":
            vals[mid] = {"absent": m["reason"]}
            continue
        unit = m["unit"]
        if unit == "series":
            vals[mid] = series_value(mid)
            continue
        if unit == "text":
            if mid == "convention.fee_basis_label":
                vals[mid] = label_by_id[mid]
            else:
                vals[mid] = TEXT_VALUES.get(mid, "Synthetic text for %s" % mid)
            continue
        make = money if unit == "dollars" else pct
        if is_by_row(mid):
            keys = CLASSES if mid == "hold.allocation" else ROW_KEYS
            if unit == "percent" and mid == "hold.allocation":
                vals[mid] = {"by_row": {k: round(0.05 + 0.01 * j, 4) for j, k in enumerate(keys)}}
            else:
                vals[mid] = {"by_row": {k: make(i * 3 + j * 11 + 5) for j, k in enumerate(keys)}}
        else:
            vals[mid] = make(i * 3 + 1)
    return vals


label_by_id = {m["id"]: m["label"] for m in members}
absent_by_id = {m["id"]: m.get("reason") for m in members}
values = build_values(label_by_id, absent_by_id)

out = []
out.append("/**")
out.append(" * SYNTHETIC filled report for the Performance tab (TO-DB-b-176). Made-up figures and ids only: no real client,")
out.append(" * account, name or figure. GENERATED from the contract bytes (sha256 %s) by the worker's emitter." % sha)
out.append(" * Layout: the contract's document layout (household, accounts, values by member id; by_row for account and class grain).")
out.append(" * Two firm variants differ ONLY in the firm word and the household reference: the layout never branches on the firm.")
out.append(" */")
out.append("")
out.append("import type { AccountEntry, FilledReport, MemberValue } from '../reportModel'")
out.append("")
out.append("const BASE_VALUES: Readonly<Record<string, MemberValue>> = {")
for m in members:
    v = values[m["id"]]
    out.append("  %s: %s," % (ts(m["id"]), json.dumps(v, ensure_ascii=True, separators=(", ", ": "))))
out.append("}")
out.append("")
out.append("const ACCOUNTS: readonly AccountEntry[] = %s" % json.dumps(ACCOUNTS, ensure_ascii=True, indent=2))
out.append("")
out.append("export const SYNTHETIC_REPORT_ALPHA: FilledReport = {")
out.append("  household: { household_ref: 'SYN-HH-ALPHA', as_of: '2026-09-30', first_data_date: '2019-03-04', accounts: ACCOUNTS },")
out.append("  values: BASE_VALUES,")
out.append("}")
out.append("")
out.append("export const SYNTHETIC_REPORT_BRAVO: FilledReport = {")
out.append("  household: { household_ref: 'SYN-HH-BRAVO', as_of: '2026-09-30', first_data_date: '2019-03-04', accounts: ACCOUNTS },")
out.append("  values: BASE_VALUES,")
out.append("}")
out.append("")
out.append("/** Two firms, one layout: the firm word is the only difference a reader may see in the cover header. */")
out.append("export const SYNTHETIC_FIRM_VARIANTS: readonly { readonly firmWord: string; readonly report: FilledReport }[] = [")
out.append("  { firmWord: 'Alpha Advisors', report: SYNTHETIC_REPORT_ALPHA },")
out.append("  { firmWord: 'Bravo Partners', report: SYNTHETIC_REPORT_BRAVO },")
out.append("]")
out.append("")
FIXTURE.parent.mkdir(parents=True, exist_ok=True)
FIXTURE.write_text("\n".join(out) + "\n", encoding="ascii")
print("contract_sha256 %s" % sha)
print("members %d sections %d" % (len(members), len(sections)))
