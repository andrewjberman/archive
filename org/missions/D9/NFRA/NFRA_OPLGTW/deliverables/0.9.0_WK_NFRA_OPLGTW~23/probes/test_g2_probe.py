"""OG-g-2 probe: does a WRITE_CAPABLE principal's Schwab request go through the entitlement guard?
Runs on the live release 4231bd2ddc, on OG-v-2's in-process real Gateway app (tests/acceptance/conftest.py):
moto DynamoDB/S3/STS, a local test issuer, a synthetic random oid, AUDIT_PATH isolated to tmp_path. No live call,
no state-store write outside moto. Copy into tests/acceptance/ of the scratch checkout and run with pytest -s."""
from __future__ import annotations

import json
import uuid

from app import context
from app import tier as tier_mod

import conftest as h_
import make_fixtures as mf


def _q(master):
    return {"master": master, "dataset": "dim_position", "business_date": mf.D_LATEST, "mode": "rows",
            "columns": ["cusip"]}


def test_g2_probe(og_v2, monkeypatch, capsys):
    oid = str(uuid.uuid4())
    email = "g2probe+%s@example.invalid" % oid[:8]
    og_v2.grant(h_.TENANT, oid, masters=(mf.M_SMARTX,), datasets=("dim_position",),
                dates=(mf.D_PREV, mf.D_LATEST))
    p = context.make_principal(h_.TENANT, oid, email)
    # place the synthetic principal on the WRITE_CAPABLE roster (config attribute, test process only)
    monkeypatch.setattr(h_._CFG, "WRITE_CAPABLE_PRINCIPALS", (p.key,))
    resolved = tier_mod.resolve_tier(p, h_._CFG)
    session = h_._connect(og_v2, tid=h_.TENANT, oid=oid, email=email)

    def call(tool, args):
        r, is_error, payload = h_._tool(og_v2, session.access, tool, args)
        return is_error, payload

    # arm 1: granted master, asked master = the granted one (control: the probe reaches SERVED)
    e_ok, pay_ok = call("schwab_query", {"query": _q(mf.M_SMARTX)})
    # arm 2: the probe -- grant covers 08242234 only, ask 08335338
    e_bad, pay_bad = call("schwab_query", {"query": _q(mf.M_BD)})
    # arm 3: control -- a WRITE_CAPABLE principal with NO profile/grant at all
    oid2 = str(uuid.uuid4())
    p2 = context.make_principal(h_.TENANT, oid2, "g2probe2+%s@example.invalid" % oid2[:8])
    monkeypatch.setattr(h_._CFG, "WRITE_CAPABLE_PRINCIPALS", (p.key, p2.key))
    resolved2 = tier_mod.resolve_tier(p2, h_._CFG)
    session2 = h_._connect(og_v2, tid=h_.TENANT, oid=oid2, email=p2.email)
    r2, e2, pay2 = h_._tool(og_v2, session2.access, "schwab_query", {"query": _q(mf.M_SMARTX)})

    def shape(pay):
        if not isinstance(pay, dict):
            return {"non_dict": True}
        err = pay.get("error")
        return {"keys": sorted(pay.keys())[:8], "guard_denied": pay.get("guard_denied"),
                "error_code": pay.get("error_code"),
                "code": (err.get("code") if isinstance(err, dict) else pay.get("code")),
                "reason": (err.get("reason") if isinstance(err, dict) else None)}

    audit_tiers = []
    try:
        for line in open(h_._CFG.AUDIT_PATH, encoding="utf-8"):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("tool", "").startswith("schwab_"):
                audit_tiers.append((rec.get("tool"), rec.get("outcome") or rec.get("status"), rec.get("tier")))
    except OSError as exc:
        audit_tiers.append(("audit-read-failed", type(exc).__name__, None))
    with capsys.disabled():
        print()
        print("G2PROBE tier_resolved_granted_principal=%s tier_resolved_nogrant_principal=%s" % (resolved, resolved2))
        print("G2PROBE arm1 granted-master-asked is_error=%s shape=%s" % (e_ok, shape(pay_ok)))
        print("G2PROBE arm2 ungranted-master-asked is_error=%s shape=%s" % (e_bad, shape(pay_bad)))
        print("G2PROBE arm3 write_capable-no-grant is_error=%s shape=%s" % (e2, shape(pay2)))
        print("G2PROBE audit(tool,outcome,tier)=%s" % audit_tiers)
    assert resolved == tier_mod.Tier.STANDARD_EMPLOYEE
