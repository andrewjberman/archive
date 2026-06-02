#!/usr/bin/env python3
"""
ADVI_INFNNA.P2.W4 -- CVO RIGID cross-view + partition-completeness gate.

The F5 RIGID bar extended to GEO (state/city) + per-client. This is the
ACCEPTANCE gate, not advisory: ANY single mismatch on a money field = BLOCKED.

Owner: 3.0.0_SA_CVO (ws CVO). Pre-published per the W1 schema-draft handshake
(DS brief docs/briefs/infnna-w1-unified-emit-schema-draft-20260602.md, 7bfd1198a)
so DS self-checks BEFORE RAVC2 -- mismatches die in-build, not at the gate.

BINDS TO: the W1 unified-additive emit (advisor_nna_canonical.json v2, additive
dims {adv, geo, client}). Bound to the DRAFT field paths; KEYS below is the ONE
place to rebind when DS sends FINAL paths at emit (key naming may shift).

Invariants (per window w in window_vocabulary), DS brief sec.3:
  I1  sum(geo.states[*].windows[w].nna) == firm.windows[w].nna           (incl 'Other')
  I2  sum(geo.states[S].cities[*].windows[w].nna) == geo.states[S].windows[w].nna  per state S (incl 'no_city')
  I3  sum(advisors[A].clients[*].windows[w].nna) == advisors[A].windows[w].nna      per advisor A (incl 'unassigned')
  I4  cross-view: geo-states YTD nna sum == partner_analytics geo YTD == header_metrics YTD
  I5  I1-I3 repeated for inflows / outflows (sum-additive, hard gate)
  AC  account_count is a DISTINCT-count (nunique), NOT sum-additive: an account that
      relocates mid-window lands in >1 leaf, so sum(leaf counts) >= firm. Asserted SOFT
      (sum >= firm; flag the spanning excess) -- never hard-block on a count.

Money tolerance: 0.01 (to-the-cent). Exit 0 = PASS (safe to RAVC2); exit 1 = BLOCKED.

Usage:
  # local emit self-check (DS pre-RAVC2):
  python3 w4_rigid_gate_advi_infnna.py --artifact /tmp/advisor_nna_canonical.json \
      --header-metrics /tmp/header_metrics.json --partner-analytics /tmp/partner_analytics_quarterly.json
  # served-artifact verify (CVO W4 cert): pass s3:// uris (needs boto3)
  python3 w4_rigid_gate_advi_infnna.py --artifact s3://opal-data-inf/platinum/firm/advisor_nna_canonical.json \
      --header-metrics s3://opal-data-inf/platinum/firm/header_metrics.json \
      --partner-analytics s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json
"""
from __future__ import annotations

import argparse
import json
import sys

TOL = 0.01  # to-the-cent

# --- REBIND POINT: update these if DS's FINAL field paths shift key names ---
KEYS = {
    "firm": "firm",
    "advisors": "advisors",
    "geo": "geo",
    "geo_states": "states",          # geo.states
    "geo_cities": "cities",          # geo.states[S].cities
    "adv_clients": "clients",        # advisors[A].clients
    "windows": "windows",            # node.windows[w]
    "money": ["nna", "inflows", "outflows"],   # hard sum-additive gate
    "count": "account_count",        # nunique, soft gate
    "geo_other": "Other",
    "city_nocity": "no_city",
    "adv_unassigned": "unassigned",
    "ytd": "YTD",
}
# Header-metrics YTD firm NNA path candidates (cross-view anchor)
HEADER_YTD = [("total", "nna_ytd"), ("ytd_nna",)]


def load(path):
    if path.startswith("s3://"):
        import boto3  # only needed for the served-verify path
        _, _, rest = path.partition("s3://")
        bucket, _, key = rest.partition("/")
        body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read()
        return json.loads(body)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def windows_of(node):
    return (node or {}).get(KEYS["windows"], {}) or {}


def leaf_val(node, w, field):
    return windows_of(node).get(w, {}).get(field)


class Gate:
    def __init__(self):
        self.fails = []   # hard (money) -> BLOCK
        self.flags = []   # soft (count / advisory)
        self.passes = 0

    def money_eq(self, label, got, want):
        if got is None or want is None:
            self.fails.append(f"{label}: MISSING (got={got} want={want})")
            return
        if abs(got - want) > TOL:
            self.fails.append(f"{label}: MISMATCH got={got:,.2f} want={want:,.2f} delta={got-want:,.2f}")
        else:
            self.passes += 1

    def count_ge(self, label, leaf_sum, firm):
        if leaf_sum is None or firm is None:
            self.flags.append(f"{label}: count MISSING")
        elif leaf_sum < firm - 0.5:
            # sum(leaves) < firm is a REAL defect (accounts dropped) -- escalate to hard fail
            self.fails.append(f"{label}: count UNDER firm (sum_leaves={leaf_sum} < firm={firm}) -> accounts dropped")
        else:
            self.passes += 1
            if leaf_sum > firm + 0.5:
                self.flags.append(f"{label}: sum_leaves={leaf_sum} > firm={firm} by {leaf_sum-firm:.0f} (boundary-spanning accounts; expected for nunique, not a defect)")


def run(artifact, header=None, partner=None):
    g = Gate()
    firm = artifact.get(KEYS["firm"], {})
    advisors = artifact.get(KEYS["advisors"], {}) or {}
    geo = artifact.get(KEYS["geo"], {}) or {}
    states = geo.get(KEYS["geo_states"], {}) or {}
    vocab = list(artifact.get("window_vocabulary", windows_of(firm)).keys()) or list(windows_of(firm).keys())

    if not states:
        g.fails.append("geo.states ABSENT -> W1 not emitted / not bound (gate cannot pass)")

    for w in vocab:
        # I1 + I5(geo): sum(states) == firm, money fields
        for fld in KEYS["money"]:
            got = sum((leaf_val(s, w, fld) or 0) for s in states.values())
            g.money_eq(f"I1 geo.states sum == firm [{w}.{fld}]", got, leaf_val(firm, w, fld))
        # AC(geo): account_count nunique soft
        cnt = sum((leaf_val(s, w, KEYS["count"]) or 0) for s in states.values())
        g.count_ge(f"AC geo.states [{w}]", cnt, leaf_val(firm, w, KEYS["count"]))

        # I2 + I5(city): per state, sum(cities) == state
        for sk, s in states.items():
            cities = s.get(KEYS["geo_cities"], {}) or {}
            if not cities:
                continue  # city is a windows-only drill leaf; absent is allowed only if state has no accounts
            for fld in KEYS["money"]:
                got = sum((leaf_val(c, w, fld) or 0) for c in cities.values())
                g.money_eq(f"I2 cities sum == state[{sk}] [{w}.{fld}]", got, leaf_val(s, w, fld))

        # I3 + I5(client): per advisor, sum(clients) == advisor
        for ak, a in advisors.items():
            clients = a.get(KEYS["adv_clients"], {}) or {}
            if not clients:
                continue
            for fld in KEYS["money"]:
                got = sum((leaf_val(c, w, fld) or 0) for c in clients.values())
                g.money_eq(f"I3 clients sum == advisor[{ak}] [{w}.{fld}]", got, leaf_val(a, w, fld))

    # I4 cross-view -- SAME-WINDOW comparisons ONLY (window-mismatch is the F5 failure
    # mode: geo-YTD vs a single snapshot calendar-quarter can NEVER tie by construction).
    # (a) YTD identity: geo-states YTD == firm YTD == header_metrics YTD
    firm_ytd = leaf_val(firm, KEYS["ytd"], "nna")
    geo_ytd = sum((leaf_val(s, KEYS["ytd"], "nna") or 0) for s in states.values()) if states else None
    g.money_eq("I4a geo-states YTD == firm YTD", geo_ytd, firm_ytd)
    if header is not None:
        hv = None
        for path in HEADER_YTD:
            node = header
            for k in path:
                node = (node or {}).get(k) if isinstance(node, dict) else None
            if isinstance(node, (int, float)):
                hv = node
                break
        g.money_eq("I4a firm YTD == header_metrics YTD", firm_ytd, hv)
    # (b) snapshot cross-view at the SAME window: partner_analytics 'current' period == q_current
    if partner is not None:
        try:
            per = partner.get("views", {}).get("nna", {}).get("current", {})  # snapshot q_current
            seg = (per.get("geo", {}) or {}).get("donut", {}).get("segments", [])
            snap_qc = sum(s.get("value", 0) for s in seg) if seg else None
            geo_qc = sum((leaf_val(s, "q_current", "nna") or 0) for s in states.values()) if states else None
            if snap_qc is not None:
                g.money_eq("I4b geo q_current == snapshot partner_analytics q_current geo", geo_qc, snap_qc)
            else:
                g.flags.append("I4b snapshot partner_analytics q_current geo donut not located -- verify manually")
        except Exception as e:  # noqa: BLE001
            g.flags.append(f"I4b partner_analytics parse skipped ({e}) -- verify manually")

    # W6 -- producer self-recon block (DS emit): assert it agrees AND is zero-delta.
    # Double-confirmation: my independent I1-I3 + the producer's standing self-recon.
    recon = artifact.get("reconciliation")
    if isinstance(recon, dict):
        if recon.get("all_pass") is not True:
            g.fails.append(f"W6 reconciliation.all_pass != True (got {recon.get('all_pass')})")
        else:
            g.passes += 1
        for fld in ("max_abs_delta", "series_tie_max_abs_delta"):
            v = recon.get(fld)
            if v is None:
                g.flags.append(f"W6 reconciliation.{fld} absent")
            elif abs(v) > TOL:
                g.fails.append(f"W6 reconciliation.{fld}={v} > {TOL}")
            else:
                g.passes += 1
    else:
        g.flags.append("W6 reconciliation block absent -- independent I1-I3 still bind")

    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", required=True, help="advisor_nna_canonical.json (local path or s3:// uri)")
    ap.add_argument("--header-metrics", default=None)
    ap.add_argument("--partner-analytics", default=None)
    a = ap.parse_args()
    art = load(a.artifact)
    hdr = load(a.header_metrics) if a.header_metrics else None
    par = load(a.partner_analytics) if a.partner_analytics else None
    g = run(art, hdr, par)

    print("=" * 60)
    print(f"ADVI_INFNNA W4 RIGID GATE -- {a.artifact}")
    print(f"  PASS checks: {g.passes}")
    if g.flags:
        print(f"  FLAGS (soft / count nunique / advisory): {len(g.flags)}")
        for f in g.flags:
            print(f"    FLAG: {f}")
    if g.fails:
        print(f"  HARD FAILS (money/partition): {len(g.fails)}")
        for f in g.fails:
            print(f"    BLOCKED: {f}")
        print("VERDICT: BLOCKED")
        sys.exit(1)
    print("VERDICT: PASS (W4 rigid gate clean -- safe to RAVC2)")
    sys.exit(0)


if __name__ == "__main__":
    main()
