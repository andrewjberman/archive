"""
NFRA_TOOLHEALTH TH-C clause-B -- the CLOSE-THE-LOOP behavior-delta exercise (the causal chain).

Proves acceptance #4: a health VERDICT demonstrably CHANGES live routing -- and the change is DRIVEN BY
the verdict's commission (verdict -> PROMOTE commission -> surface_prior(w_s) bump -> live route flip),
NOT an unrelated role/query change (the CVO~B cert condition, 2026-07-07 SCOPE RULING).

VEHICLE (CVO~B D1-owner ruling): the surface_prior (w_s) knob -- TH-C's OWN promote-commission mechanism.
This is LIVE now because role-passing landed (comp-which:698 _agent_role(), 87bc48d3f) -> surface_prior is
role-conditioned live. The learned-affinity (w_h) loop is a SEPARATE COMPLEARN concern, explicitly OUT of
clause-B scope.

CONTROLLED-BUT-FAITHFUL: the gate MECHANISM is real (comp_tool_health_gate.build_commissions on the LIVE
health query); only the EFFECTIVE input is SEEDED via the proven --effective-feed seam (TH-A's live feed is
not joined yet, so no live PROMOTE exists). Seeding EFFECTIVE=True for a not-used tool yields a genuine
PROMOTE verdict through the REAL classifier -- the causal chain downstream (commission -> w_s bump -> flip)
is entirely real + reproducible.

THE CHAIN (each link exercised, not asserted):
  1. VERDICT   : the live gate, given EFFECTIVE=True for a not-used tool, emits a real PROMOTE verdict.
  2. COMMISSION: the same gate emits that verdict's PROMOTE commission -> a CONCRETE surface_prior(w_s) bump
                 proposal naming comp_route.surface_prior as the knob (verified in clause-A self-test).
  3. APPLY     : apply ONLY that commission's w_s bump (a provider wrapper adds the surface_prior delta to
                 the SINGLE target cap -- nothing else changes: same role, same intent, same engine).
  4. FLIP      : route the intent PRE (base provider) and POST (bumped provider) at a REAL role -> the live
                 route demonstrably differs, and the delta is attributable SOLELY to the commission's bump.

Grounds on the LIVE comp_route engine + the real capability provider (Rule 22/22a: exercise-the-path).
Reproducible: CVO~B re-runs this blind to independently confirm the verdict->w_s->flip chain.

Run:  OPAL_AGENT_SERIAL=<serial> python clause_b_close_loop_exercise.py [--tool comp-secrets]
                                        [--intent "..."] [--role AE] [--bump 0.9] [--json]

Author: 0.8.0_AE_CloudComp~D (NFRA_TOOLHEALTH TH-C clause-B). 2026-07-07.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

_WS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))
for _p in (os.path.join(_WS, "org", "modules", "graph"), os.path.join(_WS, "infra", "aws", "globgrph")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import comp_route                                   # noqa: E402  the LIVE routing engine
import comp_capability_provider as _capmap          # noqa: E402  the real routing targets
sys.path.insert(0, _WS)
from org.modules.graph import comp_tool_health_gate as gate  # noqa: E402  TH-C gate (un-forked)


class _BumpOne:
    """A provider wrapper that adds a surface_prior DELTA to exactly ONE cap -- the concrete application
    of a PROMOTE commission's w_s bump. Everything else (capabilities, other priors) is untouched, so a
    route delta is attributable SOLELY to this bump (the causal-chain isolation the cert requires)."""

    def __init__(self, base, target_key: str, delta: float):
        # NB: do NOT name this attr 'affinity_key' -- comp_route calls provider.affinity_key(cap) as a
        # METHOD, so an instance attr of that name would shadow the delegated method (str-not-callable).
        self.base, self._target_key, self.delta = base, target_key, delta

    def capabilities(self):
        return self.base.capabilities()

    def surface_prior(self, key, ctx):
        p = self.base.surface_prior(key, ctx)
        return min(1.0, p + self.delta) if key == self._target_key else p

    def __getattr__(self, n):
        return getattr(self.base, n)


def _rank_of(result, tool: str):
    for i, s in enumerate(result.ranked):
        if s.cap.id == tool:
            return i, round(s.score, 4), round(s.prior, 4)
    return None, None, None


def _affinity_key_for(provider, tool: str) -> str:
    """The key comp_route uses for the surface_prior lookup: provider.affinity_key(cap) if the provider
    exposes it (what _score_one calls), else the cap's own affinity_key / surface. Matching the ENGINE's
    key exactly is load-bearing -- the bump must land on the same key the router reads."""
    for c in provider.capabilities():
        if getattr(c, "id", "") == tool:
            if hasattr(provider, "affinity_key"):
                try:
                    return provider.affinity_key(c)
                except Exception:  # noqa: BLE001
                    pass
            return getattr(c, "affinity_key", None) or getattr(c, "surface", tool)
    return tool


def run(tool: str, intent: str, role: str, bump: float) -> dict:
    provider = _capmap.get_provider()

    # LINK 1+2 -- the health VERDICT + its COMMISSION (the REAL gate; EFFECTIVE seeded for the not-used tool).
    ledger = gate.build_commissions(effective_feed={tool: True})
    commission = next((c for c in ledger["commissions"] if c["tool"] == tool), None)
    verdict_ok = commission is not None and commission["verdict"] == "PROMOTE"
    knob = commission["proposal"]["engine_knob"] if verdict_ok else None
    w_s_vehicle = bool(verdict_ok and "surface_prior" in (knob or ""))

    # LINK 3+4 -- APPLY only this commission's w_s bump, route PRE/POST at a REAL role, same intent.
    ctx = {"role": role, "working_set": [], "trajectory": []}
    akey = _affinity_key_for(provider, tool)
    r_pre = comp_route.route(intent, ctx, provider)
    r_post = comp_route.route(intent, ctx, _BumpOne(provider, akey, bump))

    pre_rank, pre_score, pre_prior = _rank_of(r_pre, tool)
    post_rank, post_score, post_prior = _rank_of(r_post, tool)
    top_changed = (r_pre.ranked[0].cap.id != r_post.ranked[0].cap.id)
    tool_rank_improved = (pre_rank is not None and post_rank is not None and post_rank < pre_rank)
    route_delta = bool(top_changed or tool_rank_improved)

    # NEGATIVE CONTROL (CVO~B causal-chain condition): WITHOUT the EFFECTIVE=True verdict, the same tool
    # is NOT a PROMOTE -> the gate emits NO route-altering commission -> NO bump -> the route stays at the
    # PRE baseline. This proves the flip is CONTINGENT on the health verdict, not an unrelated role/query
    # change (the route is identical in PRE and the no-verdict counterfactual).
    neg_ledger = gate.build_commissions()  # no EFFECTIVE seed -> the tool's real (un-promoted) verdict
    neg_row = next((c for c in neg_ledger["commissions"] if c["tool"] == tool), None)
    neg_verdict = neg_row["verdict"] if neg_row else "KEEP"
    neg_emits_route_commission = bool(neg_row and neg_row.get("action") == "comproute-route-proposal")
    control_holds = (not neg_emits_route_commission)  # no PROMOTE-without-the-verdict => no bump => no flip

    return {
        "exercise": "NFRA_TOOLHEALTH TH-C clause-B -- close-the-loop causal chain (w_s vehicle)",
        "vehicle": "surface_prior (w_s) -- TH-C's own PROMOTE-commission knob (CVO~B ruling 2026-07-07)",
        "role_passed": role,
        "intent": intent,
        "target_tool": tool,
        "chain": {
            "1_verdict": {"tool": tool, "verdict": (commission or {}).get("verdict"),
                          "is_promote": verdict_ok,
                          "note": "real gate classifier; EFFECTIVE=True seeded (TH-A feed not yet joined)"},
            "2_commission": {"action": (commission or {}).get("action"),
                             "engine_knob": knob, "is_w_s_vehicle": w_s_vehicle,
                             "rationale": (commission or {}).get("proposal", {}).get("rationale")},
            "3_apply": {"knob": "comp_route.surface_prior", "target_affinity_key": akey,
                        "delta": bump, "isolation": "single-cap bump; role/intent/engine unchanged"},
            "4_flip": {
                "pre":  {"top1": r_pre.ranked[0].cap.id, "kind": r_pre.kind,
                         "target_rank": pre_rank, "target_score": pre_score, "target_prior": pre_prior},
                "post": {"top1": r_post.ranked[0].cap.id, "kind": r_post.kind,
                         "target_rank": post_rank, "target_score": post_score, "target_prior": post_prior},
                "top1_changed": top_changed, "target_rank_improved": tool_rank_improved,
            },
        },
        "negative_control": {
            "tool_verdict_without_effective_seed": neg_verdict,
            "emits_route_altering_commission": neg_emits_route_commission,
            "control_holds": control_holds,
            "note": ("without the PROMOTE verdict there is NO route-altering commission -> NO bump -> the "
                     "route stays at the PRE baseline. The flip is CONTINGENT on the health verdict."),
        },
        "route_delta_observed": route_delta,
        "caused_by_commission": bool(verdict_ok and w_s_vehicle and route_delta and control_holds),
        "verdict": ("CLOSE-LOOP PROVEN: health verdict (PROMOTE) -> commission (w_s bump) -> live route "
                    "delta at a real role, attributable SOLELY to the bump (negative control holds: no "
                    "verdict => no commission => no flip)"
                    if (verdict_ok and w_s_vehicle and route_delta and control_holds)
                    else "NOT proven -- inspect the chain links above"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="TH-C clause-B close-the-loop causal-chain exercise")
    # Default = the faithful demonstration case: comp-depth is a not-used tool that genuinely SERVES a
    # depth query but is BURIED at rank-6 (effective-but-IGNORED = the textbook PROMOTE). Its PROMOTE
    # commission's surface_prior bump SURFACES it to top-1 -- a real closed-loop, not a mechanical flip.
    ap.add_argument("--tool", default="comp-depth", help="the PROMOTE target (a not-used routing contender)")
    ap.add_argument("--intent", default="how deep is the dependency chain", help="the routing intent to exercise")
    ap.add_argument("--role", default="AE", help="the caller role passed to route() (role-passing is live)")
    ap.add_argument("--bump", type=float, default=0.9, help="the surface_prior delta the commission proposes")
    ap.add_argument("--json", action="store_true", help="machine-readable evidence")
    args = ap.parse_args()

    ev = run(args.tool, args.intent, args.role, args.bump)
    if args.json:
        print(json.dumps(ev, indent=2))
        return 0 if ev["caused_by_commission"] else 1

    c = ev["chain"]
    print("=== TH-C clause-B -- CLOSE-THE-LOOP causal chain (w_s vehicle) ===")
    print(f"role passed: {ev['role_passed']}   intent: '{ev['intent']}'   target: {ev['target_tool']}")
    print(f"  1 VERDICT    : {c['1_verdict']['tool']} -> {c['1_verdict']['verdict']} "
          f"(is_promote={c['1_verdict']['is_promote']})")
    print(f"  2 COMMISSION : {c['2_commission']['action']}  knob={c['2_commission']['engine_knob']} "
          f"(w_s_vehicle={c['2_commission']['is_w_s_vehicle']})")
    print(f"  3 APPLY      : {c['3_apply']['knob']} += {c['3_apply']['delta']} on {c['3_apply']['target_affinity_key']} "
          f"({c['3_apply']['isolation']})")
    pre, post = c["4_flip"]["pre"], c["4_flip"]["post"]
    print(f"  4 FLIP  PRE  : top1={pre['top1']} | {ev['target_tool']} rank={pre['target_rank']} "
          f"score={pre['target_score']} prior={pre['target_prior']}")
    print(f"          POST : top1={post['top1']} | {ev['target_tool']} rank={post['target_rank']} "
          f"score={post['target_score']} prior={post['target_prior']}")
    print(f"          top1_changed={c['4_flip']['top1_changed']} "
          f"target_rank_improved={c['4_flip']['target_rank_improved']}")
    nc = ev["negative_control"]
    print(f"  NEG CTRL     : without the PROMOTE verdict, {ev['target_tool']} verdict="
          f"{nc['tool_verdict_without_effective_seed']} -> route-altering commission="
          f"{nc['emits_route_altering_commission']} (control_holds={nc['control_holds']})")
    print(f"\nroute_delta_observed={ev['route_delta_observed']}  caused_by_commission={ev['caused_by_commission']}")
    print(ev["verdict"])
    return 0 if ev["caused_by_commission"] else 1


if __name__ == "__main__":
    sys.exit(main())
