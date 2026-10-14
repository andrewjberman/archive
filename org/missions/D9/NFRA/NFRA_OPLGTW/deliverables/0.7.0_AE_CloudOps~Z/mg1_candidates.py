#!/usr/bin/env python
"""OG-mg-1 Phase A step 3: build the three candidates, call prepare(), and diff against the template.

NOTHING IS WRITTEN TO THE STORE. prepare() validates, strongly reads the current profile/grant,
prints its own diff and returns a Plan; activate() is never called here.

TWO DIFFERENT DIFFS, and conflating them would hide the check the order actually asks for:

  prepare()'s diff   -- candidate scope vs THIS PRINCIPAL'S CURRENT grant. Andrew and bbg hold no
                        grant, so it is "everything added". True, and uninformative.
  the TEMPLATE diff  -- candidate scope vs ALYSSA'S REVISION-4 scope, the store's only v2.2-width
                        grant. This is the one the order gates on: R1 may differ ONLY by the window
                        (calendar_months 13) and identity, plus `operations` on branch b. Any other
                        changed key is a STOP.

Identifiers never reach the repo. The candidates (which carry tid, oid and email) are written under
X = %LOCALAPPDATA%/opal/og-salt/mg1/, asserted at run time to resolve outside the worktree. The
repo-side record carries the source, sha256(lower(email))[:10] and the domain only, per A2.

Usage: python mg1_candidates.py   (from the repo root)
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import subprocess
import sys

GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~Z")
SHIM = os.path.join(".tools", "aws.cmd" if sys.platform == "win32" else "aws")
BBG_EMAIL = "opalbloomberg@opalinvest.com"      # A2: pinned in code, named by OPAL_USERS_ONLY
INSTANCE = "i-07dccb1615503ac99"


def x_dir() -> str:
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    d = os.path.join(base, "opal", "og-salt", "mg1")
    os.makedirs(d, exist_ok=True)
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree (%s)" % d)
    return d


def ehash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()[:10]


def master_admin_email() -> str:
    """A2: the ONE alias in the live host .env. Exactly one, or STOP."""
    params = {"commands": ["cd /opt/opal-gateway && grep -E '^MASTER_ADMIN_EMAILS=' .env | head -1 | cut -d= -f2-"]}
    X = x_dir()
    pf = os.path.join(X, "_ssm_env.json")
    with io.open(pf, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(params, fh)
    cid = subprocess.run([SHIM, "ssm", "send-command", "--instance-ids", INSTANCE,
                          "--document-name", "AWS-RunShellScript", "--parameters", "file://" + pf,
                          "--query", "Command.CommandId", "--output", "text"],
                         capture_output=True).stdout.decode().strip()
    out = ""
    for _ in range(10):
        r = subprocess.run([SHIM, "ssm", "get-command-invocation", "--command-id", cid,
                            "--instance-id", INSTANCE, "--query", "[Status,StandardOutputContent]",
                            "--output", "text"], capture_output=True).stdout.decode("utf-8", "replace")
        if r.startswith("Success"):
            out = r.split("\t", 1)[1] if "\t" in r else ""
            break
        if r.startswith("Failed"):
            raise SystemExit("STOP: the MASTER_ADMIN_EMAILS read failed on the host")
        import time
        time.sleep(4)
    aliases = [a for a in out.replace(",", " ").split() if "@" in a]
    if len(aliases) != 1:
        raise SystemExit("STOP (BLOCKING row): MASTER_ADMIN_EMAILS resolved to %d alias(es), not exactly 1" % len(aliases))
    return aliases[0]


def changed_keys(a: dict, b: dict, path: str = "") -> list[str]:
    """Key paths whose VALUE differs. Keys only ever leave this function -- never a value."""
    out = []
    for k in sorted(set(a) | set(b)):
        p = "%s.%s" % (path, k) if path else k
        va, vb = a.get(k), b.get(k)
        if isinstance(va, dict) and isinstance(vb, dict):
            out.extend(changed_keys(va, vb, p))
        elif va != vb:
            out.append(p)
    return out


def main() -> int:
    X = x_dir()
    sys.path.insert(0, os.path.abspath(GW))
    import app.access_state as acs                      # noqa: E402
    sys.path.insert(0, os.path.abspath(os.path.join(GW, "ops")))
    import schwab_entitlement_admin as sea              # noqa: E402

    ident = json.load(io.open(os.path.join(X, "mg1_identities.json"), encoding="utf-8"))
    store = acs.AccessState()

    # The template: Alyssa's revision-4 scope, read through the module's own round-trip rather than
    # hand-converted from DynamoDB's typed shape.
    alyssa_pk = ident["pk"].get("alyssa")
    if not alyssa_pk:
        # resolve her from the active profile, as the before-record did
        raise SystemExit("STOP: no alyssa pk in X; re-run mg1_before.py")
    a_tid, a_oid = alyssa_pk.split("#")[1], alyssa_pk.split("#")[2]
    _, a_grant = sea.current_state(store, a_tid, a_oid)
    if a_grant is None:
        raise SystemExit("STOP: the template grant is not readable")
    template_raw = sea._scope_to_raw(a_grant.scope)
    print("  template: alyssa revision %s, scope keys %s" % (a_grant.revision, sorted(template_raw)))

    andrew_email = master_admin_email()
    print("  R1 email: source=live host .env MASTER_ADMIN_EMAILS, aliases=1, sha10=%s domain=%s"
          % (ehash(andrew_email), andrew_email.split("@")[-1]))
    print("  R2 email: source=code-pinned OPAL_USERS_ONLY, sha10=%s domain=%s"
          % (ehash(BBG_EMAIL), BBG_EMAIL.split("@")[-1]))

    def candidate(pair: str, email: str, ops_extra: str | None = None) -> dict:
        tid, oid = pair.split("/", 1)
        scope = copy.deepcopy(template_raw)
        # calendar_months is NOT a top-level scope key: parse_scope refuses anything outside
        # (masters, datasets, accounts, dates, columns, operations[, portal_channels]). The rolling
        # window lives INSIDE `dates`, beside `mode` (:306-319). Measured, after the parser refused
        # all three candidates built the other way.
        dates = dict(scope.get("dates") or {})
        dates["calendar_months"] = 13
        scope["dates"] = dates
        if ops_extra:
            cur = list(scope.get("operations") or [])
            if ops_extra not in cur:
                cur.append(ops_extra)
            scope["operations"] = sorted(cur)
        return {"tid": tid, "oid": oid, "email": email, "scope": scope}

    cands = {
        "r1": candidate(ident["andrew"], andrew_email),
        "r2": candidate(ident["bbg"], BBG_EMAIL),
        "r1b": candidate(ident["andrew"], andrew_email, "download_filtered"),
    }

    record = {"built_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
              "template": {"role": "alyssa", "grant_revision": a_grant.revision,
                           "scope_keys": sorted(template_raw)},
              "emails": {
                "r1": {"source": "live host .env MASTER_ADMIN_EMAILS (exactly 1 alias, or STOP)",
                       "sha256_lower_10": ehash(andrew_email), "domain": andrew_email.split("@")[-1]},
                "r2": {"source": "code-pinned identity, app/identity_scope.py OPAL_USERS_ONLY",
                       "sha256_lower_10": ehash(BBG_EMAIL), "domain": BBG_EMAIL.split("@")[-1]}},
              "candidates": []}

    for name, raw in cands.items():
        buf = io.StringIO()
        try:
            plan = sea.prepare(store, raw, sea.load_contract(None), out=buf)
            ok, err = True, None
        except Exception as exc:                        # CandidateRejected and anything else
            plan, ok, err = None, False, "%s: %s" % (type(exc).__name__, exc)
        prepare_diff = buf.getvalue()
        tmpl_changed = changed_keys(template_raw, raw["scope"])
        entry = {
            "name": name,
            "prepare_accepted": ok, "prepare_error": err,
            "prepare_diff_lines": len([ln for ln in prepare_diff.split("\n") if ln.strip()]),
            "template_changed_keys": tmpl_changed,
            "base_profile_revision": None if plan is None else plan.base_profile_revision,
            "base_grant_revision": None if plan is None else plan.base_grant_revision,
            "deny_email_count": None if plan is None else len(plan.deny_emails),
        }
        record["candidates"].append(entry)
        print("    %-4s prepare=%-5s template_changed_keys=%-34s base_prof=%s base_grant=%s deny=%s"
              % (name, ok, tmpl_changed, entry["base_profile_revision"],
                 entry["base_grant_revision"], entry["deny_email_count"]))
        if err:
            print("         REJECTED: %s" % err)
        with io.open(os.path.join(X, "%s_candidate.json" % name), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(raw, fh, indent=1)
            fh.write("\n")
        with io.open(os.path.join(X, "%s_prepare_diff.txt" % name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(prepare_diff)

    # R2's scope must equal R1's, identity aside.
    r2_vs_r1 = changed_keys(cands["r1"]["scope"], cands["r2"]["scope"])
    record["r2_scope_equals_r1"] = (r2_vs_r1 == [])
    record["r2_vs_r1_changed_keys"] = r2_vs_r1
    print("  R2 scope equals R1's (identity aside): %s  changed_keys=%s" % (r2_vs_r1 == [], r2_vs_r1))

    with io.open(os.path.join(W, "MG1_CANDIDATES.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(record, fh, indent=1)
        fh.write("\n")
    print("  wrote %s/MG1_CANDIDATES.json (keys, hashes and domains only); candidates under X" % W)
    return 0


if __name__ == "__main__":
    sys.exit(main())
