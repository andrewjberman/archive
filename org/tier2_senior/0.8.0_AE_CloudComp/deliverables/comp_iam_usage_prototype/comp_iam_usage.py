#!/usr/bin/env python3
"""comp-iam-usage PROTOTYPE -- the access-plane coldness signal comp-iam lacks (NFRA decommission research).

Validates COMP_IAM_USAGE_DESIGN_20260717.md against LIVE AWS. comp-iam answers deploy-time correctness
(DESIRED + a live simulate); this answers the LIFECYCLE question -- is this role/grant still USED, and who
still reaches a resource. Read-only, advisory, NEVER deletes. Prototype in the research lane; production
lands at the ANY_EXEC engine home (org/modules/graph/), separately staffed.

THE ARCHITECTURE: `role-cold` is comp_debris.classify() on the IDENTITY plane. RoleLastUsed.LastUsedDate ->
last_activity_day; role CreateDate -> creation; the SAME bands + three refinements. A role created but never
assumed is STILLBORN-OR-GUARD (a break-glass role is a guard, not debris) -- never ranked cold. This imports
comp_debris and reuses classify/_HELD_RX VERBATIM -- the same coldness engine as comp-debris, one plane over.

RULE-22a (fix-or-carry comp-iam's 3 limits, never inherit silently): `who-can-reach` reads LIVE resource
policies (APPLIED, the limit-2 fix); an unreadable policy is UNKNOWN, never "no reach" (limit 3).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO = _HERE.parents[5]
_ENGINE_DIR = _REPO / "org" / "modules" / "graph"
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))
import comp_debris as cd  # noqa: E402  (classify, BANDS, _HELD_RX reused verbatim)


def _iam():
    import boto3
    return boto3.client("iam")


# ---- role-cold: comp_debris.classify() on the identity plane --------------------------------
def list_roles(iam) -> list:
    out, marker = [], None
    while True:
        kw = {"Marker": marker} if marker else {}
        r = iam.list_roles(**kw)
        for role in r.get("Roles", []):
            out.append({"name": role["RoleName"], "created": role.get("CreateDate")})
        marker = r.get("Marker")
        if not r.get("IsTruncated"):
            break
    return out


def role_last_used(iam, name: str):
    """(read_ok, last_used_iso_or_None). ListRoles does NOT populate RoleLastUsed -> GetRole does.
    A read failure is UNKNOWN, never assumed-unused (refinement 2 / Rule-22a limit 3)."""
    try:
        lu = iam.get_role(RoleName=name)["Role"].get("RoleLastUsed") or {}
        d = lu.get("LastUsedDate")
        return True, (d.astimezone(dt.timezone.utc).date().isoformat() if d else None)
    except Exception:  # noqa: BLE001
        return False, None


def role_records(iam, limit: int) -> list:
    roles = list_roles(iam)
    if limit:
        roles = roles[:limit]
    recs = []
    for r in roles:
        read_ok, last = role_last_used(iam, r["name"])
        created = r["created"].astimezone(dt.timezone.utc).isoformat() if r.get("created") else ""
        recs.append({"rtype": "IAM_ROLE", "name": r["name"], "created": created,
                     "hist": ({"read": True, "last_invoked_day": last} if read_ok
                              else {"read": False, "error": "get_role failed"}),
                     "signal_basis": "iam-role-last-used"})
    return recs


def iam_ledger(records: list, now_date, days: int, hot_days: int) -> dict:
    held, classified = [], []
    for rec in records:
        if cd._HELD_RX.search(rec["name"]):
            held.append(rec["name"])
            continue
        band = cd.classify({"name": rec["name"], "last_modified": rec["created"]},
                           rec["hist"], now_date, days, hot_days)
        band["rtype"] = rec["rtype"]
        band["signal_basis"] = rec["signal_basis"]
        classified.append(band)
    by_band = {b: [c for c in classified if c["band"] == b] for b in cd.BANDS}
    reap = sorted(by_band["COLD-DORMANT"], key=lambda c: -c.get("dormant_days", 0))
    return {"window_days": days, "hot_days": hot_days, "n_total": len(records),
            "n_held_excluded": len(held), "held_excluded": sorted(held),
            "counts": {b: len(by_band[b]) for b in cd.BANDS},
            "reap_rank_cold_dormant": reap,
            "purpose_review_stillborn_or_guard": by_band["STILLBORN-OR-GUARD"],
            "too_young": by_band["TOO-YOUNG"], "unknown": by_band["UNKNOWN"], "hot": by_band["HOT"]}


def _render_roles(led: dict) -> str:
    L = ["comp-iam-usage (PROTOTYPE) role-cold -- last-assume coldness (ADVISORY; NEVER deletes; hold-aware)",
         "  window %dd (hot %dd) | %d roles sampled | %d held EXCLUDED"
         % (led["window_days"], led["hot_days"], led["n_total"], led["n_held_excluded"]),
         "  bands: " + " ".join("%s=%d" % (b, led["counts"][b]) for b in cd.BANDS),
         "",
         "  REAP RANK -- COLD-DORMANT roles (used, then went dormant; coldest first):"]
    if not led["reap_rank_cold_dormant"]:
        L.append("    (none dormant-after-use in window)")
    for c in led["reap_rank_cold_dormant"][:25]:
        L.append("    %4dd  %-48s last-used=%s  [%s]"
                 % (c.get("dormant_days", 0), c["name"], c.get("last_invoked"), c["signal_basis"]))
    sob = led["purpose_review_stillborn_or_guard"]
    if sob:
        L += ["", "  PURPOSE REVIEW -- STILLBORN-OR-GUARD (%d): older than window, NEVER assumed" % len(sob),
              "  (a break-glass/emergency role is a guard, NOT debris -- a human decides):"]
        for c in sob[:20]:
            L.append("    created=%s  %s" % (c["created"], c["name"]))
    if led["counts"]["UNKNOWN"]:
        L += ["", "  UNKNOWN (%d): RoleLastUsed unreadable/absent -- BLIND, not unused." % led["counts"]["UNKNOWN"]]
    return "\n".join(L)


# ---- who-can-reach <arn>: the APPLIED resource-side (Rule-22a limit-2 fix) ------------------
def who_can_reach(arn: str) -> dict:
    """Resource-policy principals for an ARN (S3 demo). An UNREADABLE policy is UNKNOWN, never
    'no reach' (Rule-22a limit 3). Production unions this with every identity policy referencing the ARN."""
    import boto3
    if ":s3:::" not in arn:
        return {"arn": arn, "note": "prototype demos S3 only; prod covers KMS/SQS/SNS/Lambda resource policies"}
    bucket = arn.split(":::", 1)[1].split("/", 1)[0]
    s3 = boto3.client("s3")
    try:
        pol = json.loads(s3.get_bucket_policy(Bucket=bucket)["Policy"])
    except Exception as e:  # noqa: BLE001
        # NoSuchBucketPolicy = genuinely no resource policy; any OTHER error = UNKNOWN (not "no reach").
        msg = str(e)
        if "NoSuchBucketPolicy" in msg:
            return {"arn": arn, "resource_policy": "none", "principals": [], "read": True}
        return {"arn": arn, "resource_policy": "UNREADABLE", "principals": [], "read": False, "error": msg[:120]}
    princ = []
    for st in pol.get("Statement", []):
        p = st.get("Principal", {})
        vals = []
        if isinstance(p, str):
            vals = [p]
        elif isinstance(p, dict):
            for v in p.values():
                vals += v if isinstance(v, list) else [v]
        princ.append({"sid": st.get("Sid"), "effect": st.get("Effect"),
                      "action": st.get("Action"), "principals": vals})
    return {"arn": arn, "resource_policy": "present", "read": True, "statements": princ}


# ---- offline self-test ---------------------------------------------------------------------
def _self_test() -> int:
    print("=== comp-iam-usage --self-test (offline band mutants; reuses cd.classify) ===")
    now = dt.date(2026, 7, 17)
    days, hot = 90, 7
    def iso(d):
        return "%sT00:00:00+00:00" % d
    recs = [
        {"rtype": "IAM_ROLE", "name": "role-dormant", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": "2026-05-01"}, "signal_basis": "iam-role-last-used"},
        {"rtype": "IAM_ROLE", "name": "breakglass-emergency", "created": iso("2025-06-01"),
         "hist": {"read": True, "last_invoked_day": None}, "signal_basis": "iam-role-last-used"},  # never assumed, OLD
        {"rtype": "IAM_ROLE", "name": "role-new", "created": iso("2026-07-10"),
         "hist": {"read": True, "last_invoked_day": None}, "signal_basis": "iam-role-last-used"},  # new, never used
        {"rtype": "IAM_ROLE", "name": "role-blind", "created": iso("2026-01-01"),
         "hist": {"read": False, "error": "AccessDenied"}, "signal_basis": "iam-role-last-used"},
        {"rtype": "IAM_ROLE", "name": "inf-gold-dispatch-role", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": None}, "signal_basis": "iam-role-last-used"},  # HELD
        {"rtype": "IAM_ROLE", "name": "role-hot", "created": iso("2026-01-01"),
         "hist": {"read": True, "last_invoked_day": "2026-07-16"}, "signal_basis": "iam-role-last-used"},
    ]
    led = iam_ledger(recs, now, days, hot)
    ok = []
    def ck(n, c, d=""):
        ok.append(c)
        print(f"  [{'PASS' if c else 'FAIL'}] {n}" + (f"  ({d})" if d else ""))
    reap = {c["name"] for c in led["reap_rank_cold_dormant"]}
    ck("dormant_role_is_reap", reap == {"role-dormant"}, f"reap={reap}")
    ck("breakglass_never_used_is_stillborn_NOT_reap",
       any(c["name"] == "breakglass-emergency" for c in led["purpose_review_stillborn_or_guard"]) and "breakglass-emergency" not in reap)
    ck("new_never_used_is_too_young", any(c["name"] == "role-new" for c in led["too_young"]) and "role-new" not in reap)
    ck("blind_is_unknown_NOT_unused", any(c["name"] == "role-blind" for c in led["unknown"]) and "role-blind" not in reap)
    ck("held_excluded", "inf-gold-dispatch-role" in led["held_excluded"])
    ck("hot_is_hot", any(c["name"] == "role-hot" for c in led["hot"]) and "role-hot" not in reap)
    good = all(ok)
    print("\n" + ("OK: never-used!=cold, break-glass-guard-not-debris, UNKNOWN-band, hold-aware -- all held"
                  if good else "ERROR: comp-iam-usage self-test FAILED"))
    return 0 if good else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="comp-iam-usage",
                                 description="comp-iam-usage PROTOTYPE -- access-plane coldness. Advisory; NEVER deletes.")
    sub = ap.add_subparsers(dest="cmd")
    pr = sub.add_parser("role-cold", help="rank roles by last-assume coldness (reuses comp_debris bands)")
    pr.add_argument("--days", type=int, default=90)
    pr.add_argument("--hot-days", type=int, default=7)
    pr.add_argument("--limit", type=int, default=50, help="sample size (get-role is per-role; 0=all 209)")
    pr.add_argument("--json", action="store_true")
    pw = sub.add_parser("who-can-reach", help="resource-policy principals for an ARN (S3 demo)")
    pw.add_argument("arn")
    sub.add_parser("self-test", help="offline band mutants (no AWS)")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(errors="replace")
        except Exception:  # noqa: BLE001
            pass

    if args.cmd == "self-test":
        return _self_test()
    if args.cmd == "role-cold":
        recs = role_records(_iam(), args.limit)
        led = iam_ledger(recs, dt.datetime.now(dt.timezone.utc).date(), args.days, args.hot_days)
        print(json.dumps(led, indent=1, default=str) if args.json else _render_roles(led))
        return 0
    if args.cmd == "who-can-reach":
        print(json.dumps(who_can_reach(args.arn), indent=1, default=str))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
