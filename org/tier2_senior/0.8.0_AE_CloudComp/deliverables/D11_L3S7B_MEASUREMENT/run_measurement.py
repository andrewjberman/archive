"""THE PRODUCER for FACE 1's three cells -- the program that makes the numbers.

⛔ WHY THIS FILE EXISTS, AND IT IS A DEFECT REPORT AGAINST MY OWN FIRST DELIVERY.
The first commit of this deliverable (6e574dec5b / 07d9e1bc6a) carried the RESULT JSONs and the
two packaging builders but NOT the programs that produced the numbers -- those lived only in a
session scratchpad. The proof's AC1/AC3 rows then cited `python ac1.py` and `python ac3.py`,
which resolve to nothing in this repository (tracked count: 0). A certifier could read the
values and could not re-derive one of them. Raised as a certification hold on FACE 1; correct,
and fixed here by committing the producer rather than by softening the claim.

⛔ THE ENGINE IS READ FROM ITS PIN, NOT FROM A COPY. `git show e2ab79fba4:<engine>` into a
temporary file, sha256 asserted equal to the declared digest before a single number is
computed. A scratchpad copy of an engine is not the engine -- it is a copy whose provenance
dies with the session that made it.

⛔ ORDER IS ENFORCED BY CONSTRUCTION, NOT BY COMMENT. AC1 (the UNFUSED baseline) must be
produced before any fused arm exists on this rectangle; AC3's control needs C1 = SNF(W1, W1),
which IS a fused arm. This module therefore computes and WRITES AC1 first, records the wall
clock, and only then makes its first snf() call -- whose timestamp becomes AC1's
produced_before. A run that reordered these would produce a FORM_DEFECT and the module refuses
rather than allowing it (see the _first_fusion guard).

RE-RUNNING THIS: the numbers are deterministic -- the null battery draws from
SeedSequence(20260830).spawn(20), so every AUC reproduces bit-for-bit. TIMESTAMPS DO NOT, by
nature: produced_at and produced_before are wall-clock readings of the run that took them. A
certifier re-running should diff the VALUES and expect the two ISO fields to differ. Write
somewhere else with --out to avoid overwriting the certified artifacts.

  python run_measurement.py --out <dir>

Author: 0.8.0_AE_CloudComp~Y.  TO: NFRA_C3MATERIALIZE.TO-L3S7B-CCY.measurement.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[5]   # the REPO ROOT; parents[4] is <repo>/org
HERE = Path(__file__).resolve().parent

ENGINE_REL = ("org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_L3W3_KSWEEP/snf_ksweep.py")
ENGINE_PIN = "e2ab79fba4"
ENGINE_SHA = "86ae5ca5f72ed8748cc035535ac6ea8db02fb5c47d0fe7391562400b25f58374"

DELIV = "org/tier2_senior/0.7.0_AE_CloudOps/deliverables/"
MASK_REL = DELIV + "D11_L3W2_FUSION/mask_carrier_union.json"
COHORT_REL = DELIV + "D11_L3W2_FUSION/firm_cohort_shared.json"

# Device-local, UNTRACKED inputs. Declared as a named gap on every carrier this face emits
# (same class as the portal graph, 87247/87275): retrievable here by digest, not re-derivable
# from git at any pin. Overridable so a certifier on another device can point at its own copy.
DEFAULT_SCRATCH = ("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
                   "C--Users-AndrewBerman-Desktop-ajb-workspace/"
                   "b3cf19c0-4b0d-4065-b24b-caf9685c8a2a/scratchpad/")
VIEW1_SHA = "e91d69910fc9d4eabb58eedb8a73165476225ab838977e8d6c16604af3f5e19a"
L2_SHA = "9ca36c50e588b7f911826eb7b73e069ed172509dfea3ea5842778e265a83800c"

ROOT_SEED = 20260830
N_DRAWS = 20
K = 20
T = 20
PRECISION = 6
REFUSAL_THRESHOLD = 0.90   # declaration 3 @e04cad153a: distance 0.1, refusal_threshold 0.9

_first_fusion: list = []


def iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_engine_at_pin():
    """Materialise the engine FROM ITS PIN and refuse if the bytes are not the declared ones."""
    raw = subprocess.run(["git", "show", f"{ENGINE_PIN}:{ENGINE_REL}"], cwd=str(ROOT),
                         capture_output=True, check=True).stdout
    got = hashlib.sha256(raw).hexdigest()
    if got != ENGINE_SHA:
        raise SystemExit(f"FAIL: engine at {ENGINE_PIN} hashes {got}, declared {ENGINE_SHA}")
    tmp = Path(tempfile.gettempdir()) / f"snf_ksweep_{ENGINE_PIN}.py"
    tmp.write_bytes(raw)
    spec = importlib.util.spec_from_file_location("snf_ksweep_pinned", tmp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for fn in ("view1_affinity", "firm_separation_auc", "permute_view", "snf",
               "exact_zero_count", "load_view1_partitions"):
        if not hasattr(mod, fn):
            raise SystemExit(f"FAIL: engine at {ENGINE_PIN} has no {fn} -- wrong pin")
    return mod, got


def fused(M, views, k, t):
    """Every snf() call in this module goes through here, so the FIRST one is recorded once."""
    if not _first_fusion:
        _first_fusion.append(iso())
    return M.snf(views, k=k, t=t)


def build_frames(M, scratch: str):
    parts = M.load_view1_partitions(scratch + "W_STRUCTURE_FACTORIZED.json")
    mask = np.array(json.load(open(ROOT / MASK_REL, encoding="utf-8"))["vector"], dtype=np.uint8)
    cohort = json.load(open(ROOT / COHORT_REL, encoding="utf-8"))["cohort"]
    L2 = json.load(open(scratch + "L2_VIEW_ARTIFACTS.json", encoding="utf-8"))
    pop = [e["entity_id"] for e in
           [v for v in L2["views"] if v.get("view_id") == "STRUCTURE"][0]["entity_set"]["entities"]]
    bm_idx = np.flatnonzero(mask == 1)
    firm_of = {c["entity_id"]: c["firm"] for c in cohort}
    ids = [c["entity_id"] for c in cohort]
    pos_of = {e: i for i, e in enumerate(pop)}
    idxA = np.array([pos_of[e] for e in ids])
    sel = np.isin(idxA, bm_idx)
    idxB = idxA[sel]
    firmsA = [firm_of[e] for e in ids]
    firmsB = [firmsA[i] for i in np.flatnonzero(sel)]
    return parts, pop, bm_idx, idxA, idxB, firmsA, firmsB


def c2(n: int) -> int:
    return n * (n - 1) // 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE),
                    help="output directory (default: this deliverable)")
    ap.add_argument("--scratch", default=DEFAULT_SCRATCH,
                    help="directory holding the two untracked inputs")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    M, engine_sha = load_engine_at_pin()
    v1_sha = sha256_file(args.scratch + "W_STRUCTURE_FACTORIZED.json")
    l2_sha = sha256_file(args.scratch + "L2_VIEW_ARTIFACTS.json")
    for name, got, want in (("W_STRUCTURE_FACTORIZED.json", v1_sha, VIEW1_SHA),
                            ("L2_VIEW_ARTIFACTS.json", l2_sha, L2_SHA)):
        if got != want:
            raise SystemExit(f"FAIL: {name} hashes {got}, declared {want} -- different bytes, "
                             f"NOT-COMPARABLE rather than a wrong number")
    print(f"engine @{ENGINE_PIN} sha {engine_sha[:16]}...  inputs verified by digest")

    parts, pop, bm_idx, idxA, idxB, firmsA, firmsB = build_frames(M, args.scratch)
    print(f"population {len(pop):,}  both-measured {bm_idx.size:,}  "
          f"frame A {len(idxA):,}  frame B {len(idxB):,}")

    # ---------- AC1 : UNFUSED. Must precede every fused arm. ----------
    ac1 = {"produced_at": iso(), "engine_pin": ENGINE_PIN, "engine_sha256": engine_sha,
           "fusion": "NONE -- W1 passed directly to firm_separation_auc, no snf() call"}
    if _first_fusion:
        raise SystemExit("FAIL: a fused arm ran before the unfused baseline -- FORM_DEFECT")
    for nm, idx, firms in (("B", idxB, firmsB), ("A", idxA, firmsA)):
        t0 = time.time()
        W1 = M.view1_affinity(parts, idx)
        auc, nw, nc, ties = M.firm_separation_auc(W1, firms)
        ac1[f"frame_{nm}"] = {
            "members": int(len(idx)), "auc_w1_unfused": round(float(auc), PRECISION),
            "n_within": int(nw), "n_cross": int(nc), "pairs_judged": int(nw + nc),
            "frame_pair_domain": c2(len(idx)),
            "declared_pair_domain": c2(len(idx)),
            "pairs_judged_equals_domain": bool(nw + nc == c2(len(idx))),
            "ties_at_decision": int(ties), "seconds": round(time.time() - t0, 1)}
        r = ac1[f"frame_{nm}"]
        print(f"  AC1 frame {nm}: AUC(W1) unfused {r['auc_w1_unfused']:.6f}  "
              f"judged {r['pairs_judged']:,} == C(n,2) {r['frame_pair_domain']:,}")
        if nm == "B":
            W1_B = W1
    ac1["headroom_declaration_3"] = {
        "threshold": REFUSAL_THRESHOLD,
        "tested": "AUC(W1) on frame B (no V exists yet)",
        "auc_B": ac1["frame_B"]["auc_w1_unfused"],
        "frame_B_refused": bool(ac1["frame_B"]["auc_w1_unfused"] > REFUSAL_THRESHOLD),
        "margin_to_threshold": round(REFUSAL_THRESHOLD - ac1["frame_B"]["auc_w1_unfused"],
                                     PRECISION)}
    (out / "_ac1_result.json").write_text(json.dumps(ac1, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")

    # ---------- AC3 : the rebuilt instrument, exercised on perm(W1) ----------
    C1m = fused(M, [W1_B, W1_B], K, T)                     # <- the FIRST fused arm
    c1_auc, c1_nw, c1_nc, c1_ties = M.firm_separation_auc(C1m, firmsB)
    print(f"  AC3 C1 = SNF(W1,W1) K={K} T={T}: AUC {c1_auc:.6f}")

    children = np.random.SeedSequence(ROOT_SEED).spawn(N_DRAWS)
    draws = []
    for i, ch in enumerate(children):
        seed_i = int(ch.generate_state(1, dtype=np.uint32)[0])
        t0 = time.time()
        Sf = fused(M, [W1_B, M.permute_view(W1_B, seed_i)], K, T)
        a, _, _, _ = M.firm_separation_auc(Sf, firmsB)
        draws.append({"draw": i + 1, "child_seed": seed_i, "auc": round(float(a), PRECISION),
                      "exact_zero_pairs": M.exact_zero_count(Sf),
                      "seconds": round(time.time() - t0, 1)})
        print(f"    draw {i+1:2d}/{N_DRAWS} seed={seed_i:<11} AUC={a:.6f}")

    vals = np.array([d["auc"] for d in draws])
    null_mean, spread = float(vals.mean()), float(vals.std(ddof=1))
    gate = c1_auc - 3.0 * spread
    lo, hi = null_mean - 3 * spread, null_mean + 3 * spread
    ac3 = {
        "produced_at": iso(), "criterion": "L3S7B-CCY-AC3", "frame": "B",
        "members": int(len(idxB)), "K": K, "T": T,
        "engine_pin": ENGINE_PIN, "engine_sha256": engine_sha,
        "instrument": {
            "rebuilt": True, "reused_wave2_arm": False,
            "wave2_arm_status": "UNSOUND AS A GATE @4e7016f471 -- not used",
            "scheme": "permute-V-entity-labels-within-frame; V=W1 for this control arm "
                      "(Addendum 1m(iv))",
            "rng": {"form": "numpy SeedSequence(root).spawn(n), one independent child per draw",
                    "root_seed": ROOT_SEED, "n": N_DRAWS,
                    "child_seed_derivation":
                        "child.generate_state(1,uint32)[0] -> permute_view(W,seed)"},
            "spread_ddof": 1, "precision_decimals": PRECISION, "one_null_per_artifact": True,
            "failure_signal": "mean(F(W1,perm(W1))) >= C1 - 3*spread => the instrument cannot "
                              "see a permutation and NO clause-1 verdict is admissible on it"},
        "C1": {"definition": "SNF(W1,W1) same frame, same (K,T)",
               "auc": round(float(c1_auc), PRECISION),
               "exact_zero_pairs": int(M.exact_zero_count(C1m)),
               "n_within": int(c1_nw), "n_cross": int(c1_nc)},
        "null": {"n_permutations": N_DRAWS, "draws": draws,
                 "null_mean": round(null_mean, PRECISION), "spread": round(spread, PRECISION),
                 "band_lo": round(lo, PRECISION), "band_hi": round(hi, PRECISION),
                 "tail_observations": [d for d in draws if not (lo <= d["auc"] <= hi)]},
        "control_verdict": {"gate": "null_mean < C1 - 3*spread",
                            "gate_value": round(gate, PRECISION),
                            "null_mean": round(null_mean, PRECISION),
                            "margin": round(gate - null_mean, PRECISION),
                            "PASS": bool(null_mean < gate)}}
    (out / "_ac3_result.json").write_text(json.dumps(ac3, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")

    # AC1's produced_before is the FIRST fused arm's clock, taken by the guard above.
    ac1["produced_before"] = _first_fusion[0]
    ac1["produced_before_evidence"] = (
        "the ISO clock of the first snf() call in this run, recorded by the fused() guard that "
        "every fusion in this module passes through -- not a mtime read after the fact")
    (out / "_ac1_result.json").write_text(json.dumps(ac1, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")

    # ---------- the determinism control: re-run draw 1 from its own seed ----------
    d1 = draws[0]
    a_re, _, _, _ = M.firm_separation_auc(
        fused(M, [W1_B, M.permute_view(W1_B, d1["child_seed"])], K, T), firmsB)
    stable = round(float(a_re), PRECISION) == d1["auc"]
    ctl = {"determinism_stable": stable, "rerun_auc": round(float(a_re), PRECISION),
           "first_auc": d1["auc"], "seed": d1["child_seed"],
           "mutant_note": "the MUTANT control is on the frame-block census and lives in "
                          "build_measurement_carriers.py's output; see _controls_result.json "
                          "as committed, and check_frame_mutant() below re-runs it"}
    ctl.update(check_frame_mutant(out))
    (out / "_controls_result.json").write_text(json.dumps(ctl, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")

    print(f"\n  AC1 frame B {ac1['frame_B']['auc_w1_unfused']:.6f}  "
          f"frame A {ac1['frame_A']['auc_w1_unfused']:.6f}")
    print(f"  AC1 produced_at {ac1['produced_at']}  produced_before {ac1['produced_before']}")
    print(f"  AC3 C1 {c1_auc:.6f}  null {null_mean:.6f} +/- {spread:.6f}  gate {gate:.6f}  "
          f"{'PASS' if null_mean < gate else 'FAIL'} margin {gate-null_mean:+.6f}")
    print(f"  determinism: {'STABLE' if stable else 'UNSTABLE'}   "
          f"mutant: {'FIRED' if ctl['mutant_fired'] else 'DID NOT FIRE'}")
    print(f"  WROTE _ac1_result.json _ac3_result.json _controls_result.json -> {out}")


def check_frame_mutant(out: Path) -> dict:
    """Re-run the frame-block mutant: the census must REFUSE a perturbed frame."""
    import copy
    names = ["L3S7B-1c16-3.frame_declaration.json",
             "L3S7B-1c16-1.auc_w1_unfused.json",
             "L3S7B-0b5f-1.null_battery_instrument.json"]
    src = [HERE / n for n in names]
    if not all(p.exists() for p in src):
        return {"mutant_fired": None,
                "mutant_note_2": "carriers absent -- run build_measurement_carriers.py first"}
    def canon(o):
        return json.dumps(o, ensure_ascii=True, sort_keys=True, separators=(",", ":"))

    def sha(s):
        return hashlib.sha256(s.encode()).hexdigest()

    frames = [json.loads(p.read_text(encoding="utf-8"))["frame"] for p in src]
    base = len({sha(canon(f)) for f in frames})
    mut = copy.deepcopy(frames)
    mut[2]["B"]["pair_domain"] = 8596731        # the exact error correction-1 fixed
    got = len({sha(canon(f)) for f in mut})
    return {"mutant_baseline_distinct": base, "mutant_distinct": got,
            "mutant_fired": bool(got != 1 and base == 1)}


if __name__ == "__main__":
    main()
