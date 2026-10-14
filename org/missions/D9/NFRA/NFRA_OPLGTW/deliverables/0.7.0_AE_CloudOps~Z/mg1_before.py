#!/usr/bin/env python
"""OG-mg-1 Phase A step 1: the before-record of the POLICY# partitions, written WITHOUT identifiers.

Two outputs, deliberately split:

  W/MG1_BEFORE.json  -- committed. Carries pk_hash (first 10 hex of sha256 of the pk) and record
                        state only. No tid, oid or email, per the order.
  X/mg1_identities.json -- NEVER committed. X is %LOCALAPPDATA%/opal/og-salt/mg1/, outside the
                        worktree (asserted at run time). Holds the tid/oid the write will need.

Roles resolve the way the order specifies: a principal WITH a profile by its profile's email
prefix; a principal with NO profile by its roster oid. Andrew is the roster's master_admin; the
Bloomberg principal is the roster entry whose oid carries the Part D prefix the order names.

The scan is strongly consistent and FULLY paginated, and the denominator is printed. A single
Scan page would read as a complete census and silently omit whatever sat past the 1 MB boundary;
DynamoDB's own ItemCount is no help either -- it is refreshed about every six hours, and it read
1493 against a live 1504 while this was written.

Usage: python mg1_before.py   (from the repo root)
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys

TABLE = "gateway-access-state-table"
SECRET = "gateway/principals/rosters"
BBG_OID_PREFIX = "517aa5ee"          # Part D 2026-09-30, named in the order
SHIM = os.path.join(".tools", "aws.cmd" if sys.platform == "win32" else "aws")
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~Z")


def aws(*args: str) -> str:
    r = subprocess.run([SHIM, *args], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("FAILED aws %s: %s" % (" ".join(args[:3]), r.stderr.decode("utf-8", "replace")[:300]))
    return r.stdout.decode("utf-8", "replace").strip()


def h(pk: str) -> str:
    return hashlib.sha256(pk.encode("utf-8")).hexdigest()[:10]


def sval(item: dict, key: str) -> str:
    v = item.get(key) or {}
    return v.get("S") or v.get("N") or ""


def x_dir() -> str:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    d = os.path.join(base, "opal", "og-salt", "mg1")
    os.makedirs(d, exist_ok=True)
    # The whole point of X is that it is NOT the repo. Assert it rather than trust the path string.
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree (%s)" % d)
    return d


def scan_all() -> list[dict]:
    items, token, pages = [], None, 0
    while True:
        args = ["dynamodb", "scan", "--table-name", TABLE, "--consistent-read", "--output", "json"]
        if token:
            args += ["--starting-token", token]
        page = json.loads(aws(*args))
        items.extend(page.get("Items", []))
        pages += 1
        token = page.get("NextToken")
        if not token:
            break
    print("  scan: %d item(s) over %d page(s), consistent, fully paginated" % (len(items), pages))
    return items


def main() -> int:
    X = x_dir()
    roster = json.loads(aws("secretsmanager", "get-secret-value", "--secret-id", SECRET,
                            "--query", "SecretString", "--output", "text"))
    # Every roster value that carries tid/oid pairs, comma-separated.
    pairs: dict[str, list[str]] = {}
    for k, v in roster.items():
        if isinstance(v, str) and "/" in v:
            pairs[k] = [p.strip() for p in v.split(",") if "/" in p]
    print("  roster: %s" % {k: len(v) for k, v in pairs.items()})

    andrew = pairs.get("master_admin", [None])[0]
    bbg = next((p for v in pairs.values() for p in v if p.split("/")[-1].startswith(BBG_OID_PREFIX)), None)
    print("  andrew resolved from master_admin: %s" % bool(andrew))
    print("  bbg resolved by oid prefix %s: %s" % (BBG_OID_PREFIX, bool(bbg)))

    items = scan_all()
    pol = [it for it in items if sval(it, "pk").startswith("POLICY#")]
    profiles = [it for it in pol if sval(it, "record_type") == "principal_profile"]
    grants = [it for it in pol if sval(it, "record_type") == "data_entitlement"]
    print("  POLICY# %d of %d; principal_profile %d; data_entitlement %d" % (len(pol), len(items), len(profiles), len(grants)))

    def pk_of(pair: str | None) -> str | None:
        if not pair or "/" not in pair:
            return None
        tid, oid = pair.split("/", 1)
        return "POLICY#%s#%s" % (tid, oid)

    known = {"andrew": pk_of(andrew), "bbg": pk_of(bbg)}
    out_principals = []

    # alyssa: the ACTIVE profile, identified by its own email prefix, not by a hardcoded id.
    for it in profiles:
        if sval(it, "status") != "active":
            continue
        email = sval(it, "email")
        role = email.split("@")[0].split(".")[0].lower() if email else "unknown"
        if role not in ("andrew", "bbg"):
            known.setdefault(role, sval(it, "pk"))

    for role, pk in known.items():
        if not pk:
            out_principals.append({"role": role, "pk_hash": None, "profile": None,
                                   "profile_revision": None, "grant_scope_keys": [],
                                   "note": "could not resolve this principal from the roster"})
            continue
        prof = next((it for it in profiles if sval(it, "pk") == pk), None)
        gr = [it for it in grants if sval(it, "pk") == pk]
        gr_active = next((it for it in gr if sval(it, "status") == "active"), None)
        scope_keys = []
        if gr_active:
            raw = gr_active.get("scope") or {}
            inner = raw.get("M") if "M" in raw else None
            scope_keys = sorted(inner) if isinstance(inner, dict) else sorted(
                k for k in gr_active if k not in ("pk", "sk", "record_type"))
        out_principals.append({
            "role": role, "pk_hash": h(pk),
            "profile": None if prof is None else {
                "status": sval(prof, "status"), "revision": sval(prof, "revision"),
                "grant_revision": sval(prof, "grant_revision"), "kind": sval(prof, "profile_kind")},
            "profile_revision": None if prof is None else sval(prof, "revision"),
            "grant_scope_keys": scope_keys,
            "grant_revisions_present": sorted(sval(g, "revision") for g in gr),
        })

    rec = {
     "read_at": aws("sts", "get-caller-identity", "--query", "Account", "--output", "text") and
                __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
     "read_as": "the calling principal's own read access (A1: the role holds neither Scan nor Query)",
     "denominator": {"policy_items_scanned": len(pol), "items_scanned_total": len(items),
                     "principal_profiles": len(profiles), "data_entitlements": len(grants)},
     "method": "strongly consistent Scan, fully paginated (NextToken followed to exhaustion); DynamoDB ItemCount is NOT used -- it refreshes about every six hours and read 1493 against a live 1504",
     "identifiers": "NONE in this file by construction: pk_hash is the first 10 hex of sha256 of the pk. The tid/oid live only in %LOCALAPPDATA%/opal/og-salt/mg1/, asserted at run time to be outside the worktree.",
     "principals": out_principals,
    }
    with io.open(os.path.join(W, "MG1_BEFORE.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    with io.open(os.path.join(X, "mg1_identities.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"andrew": andrew, "bbg": bbg, "pk": known}, fh, indent=1)
        fh.write("\n")
    for p in out_principals:
        print("    %-8s pk_hash %-11s profile %-34s scope_keys %d"
              % (p["role"], p["pk_hash"], json.dumps(p["profile"]) if p["profile"] else "NONE",
                 len(p["grant_scope_keys"])))
    print("  wrote %s/MG1_BEFORE.json (no identifiers) and X/mg1_identities.json (off-repo)" % W)
    return 0


if __name__ == "__main__":
    sys.exit(main())
