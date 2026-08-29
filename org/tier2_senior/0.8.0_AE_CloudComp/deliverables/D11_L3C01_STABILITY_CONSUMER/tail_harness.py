#!/usr/bin/env python3
"""Exercise check_stability_L3C01.py against Addendum 1c @28b1cab509, SPREAD_TAIL (80918 as
clarified by 80925) and Addendum 1d @ddbff010ec.

ARMS ARE TRANSCRIBED FROM THE RULING TEXT, FIELD BY FIELD, BEFORE READING THE IMPLEMENTATION
-- a harness transcribed from the implementation scores the implementation's blind spot as a
pass. Each arm names the sentence it comes from.

THE D-ARMS USE 1d's PUBLISHED NUMBERS VERBATIM, with CTO~X's own stated verdict as the
expectation (rho: no tail; J: tail at draws[0], band_of_others 0.106395). That is the only
arm in this file whose truth was not chosen by me, and it is the one that found the
tolerance defect.

The deriving artifact is committed into a THROWAWAY GIT REPO, so `git show <pin>:<path>` and
`merge-base --is-ancestor` are exercised for real. A mocked pin would test the mock.
"""
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER = os.path.join(HERE, 'check_stability_L3C01.py')
# The throwaway repo lives OUTSIDE the tree: a harness that mints git objects
# beside its own source would leave 400+ untracked files in a deliverables dir.
REPO = os.environ.get('L3C01_HARNESS_REPO') or os.path.join(
    tempfile.gettempdir(), 'l3c01_tailrepo')
SCHEME = 'half-B W1 label permutation (COX)'
SPLIT_OK = {"battery_id": "eb009c01", "seed": 20260829,
            "half_a_runs": list(range(1, 13)), "half_b_runs": list(range(13, 26)),
            "disjoint": True, "n_a": 12, "n_b": 13}


def sh(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True)


def mean(v):
    return sum(v) / float(len(v))


def sd1(v):
    m = mean(v)
    return (sum((x - m) ** 2 for x in v) / float(len(v) - 1)) ** 0.5


def battery(draws, observed, scheme=SCHEME):
    """A well-formed 1c block for whatever draws it is given. Only IN-battery values feed
    null/spread; a typed-OUT draw still counts toward n_permutations = len(draws)."""
    inb = [d for d in draws if not isinstance(d, dict)] + \
          [d['value'] for d in draws
           if isinstance(d, dict) and d.get('in_battery') is not False]
    n = len(draws)
    if len(inb) == 1:
        return {"n_permutations": n, "null": inb[0], "spread": None,
                "spread_status": "UNMEASURED", "draws": draws, "observed": observed,
                "scheme": scheme}
    return {"n_permutations": n, "null": mean(inb), "spread": sd1(inb),
            "spread_status": "MEASURED" if n >= 5 else "UNMEASURED",
            "draws": draws, "observed": observed, "scheme": scheme}


SEC63 = {
    "full_1941": {"denominator": 1941, "aucs": [0.7404, 0.5203, 0.5510],
                  "predicate_result": False},
    "both_measured_1820": {"denominator": 1820, "aucs": [0.7429, 0.5200, 0.5114],
                           "predicate_result": False},
}
RHO, J = 0.9584, 0.8033
CLEAN_RHO = [-0.14, -0.15, -0.13, -0.16, -0.12]
CLEAN_J = [0.17, 0.18, 0.19, 0.20, 0.16]

# ---- Addendum 1d @ddbff010ec, msg 80970, copied not retyped-from-memory ----
D_RHO, D_J = 0.958398, 0.803263
B1D_RHO = {"n_permutations": 6,
           "draws": [-0.144792, 0.129793, -0.059148, -0.001912, 0.090502, -0.112148],
           "null": -0.016284, "spread": 0.109991, "spread_status": "MEASURED",
           "observed": 0.958398}
B1D_J = {"n_permutations": 6,
         "draws": [0.179046, 0.042818, 0.066813, 0.002472, 0.028317, 0.013901],
         "null": 0.055561, "spread": 0.064550, "spread_status": "MEASURED",
         "observed": 0.803263,
         "tail_observation": {"draw": 0.179046, "band_of_others": 0.106395, "n_others": 5}}


def artifact(floor_status, brho, bj, deriv=None, run_id="run-2", pc=None, rho=RHO, j=J):
    s = {
        "run_id": run_id,
        "floor_status": floor_status,
        "metric_domain_predicate": "both-measured pairs",
        "pair_denominator": 8596731,
        "spearman_rho": rho,
        "topdecile_jaccard": j,
        "permutation_battery": {"rho": brho, "J": bj},
        "split_half": json.loads(json.dumps(SPLIT_OK)),
    }
    if pc is not None:
        s['permuted_control'] = pc
    if deriv is not None:
        s['floor_derivation'] = deriv
    return {"stability_L3C01": s, "sec_6_3_frames": SEC63,
            "output_domain": {"entities": 19482, "pairs": 189764421}}


def deriv_block(pin, path, brho, bj, run="run-1", obs_rho=0.95, obs_j=0.79, tweak=None,
                scheme=SCHEME):
    """floor_derivation whose null/spread/n_permutations/observed are COPIED from the battery
    it cites -- 1c: 'the two carriers are one contract'."""
    def one(b, obs):
        return {"derived_from_run_id": run, "derived_at_commit": pin,
                "derived_from_path": path, "metric_domain": "both-measured pairs",
                "n_permutations": b['n_permutations'],
                "null": b['null'], "spread": b['spread'], "multiplier": 3, "scheme": scheme,
                "floor": b['null'] + 3 * b['spread'], "deriving_run_observed": obs}
    d = {"spearman_rho": one(brho, obs_rho), "topdecile_jaccard": one(bj, obs_j)}
    if tweak:
        tweak(d)
    return d


def commit_deriv(brho, bj, tag, rho=RHO, j=J):
    doc = artifact("HELD-UNEXERCISED", brho, bj, run_id="run-1", rho=rho, j=j)
    io.open(os.path.join(REPO, 'deriv.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(doc, indent=1) + "\n")
    sh('git', 'add', 'deriv.json')
    sh('git', '-c', 'user.name=h', '-c', 'user.email=h@h', 'commit', '-q', '-m', tag)
    return sh('git', 'rev-parse', 'HEAD').stdout.strip()


def run(doc):
    io.open(os.path.join(REPO, 'apply.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(doc, indent=1) + "\n")
    r = subprocess.run([sys.executable, CHECKER, 'apply.json', 'HEAD'],
                       cwd=REPO, capture_output=True, text=True)
    out = r.stdout + r.stderr
    kind = ''
    for tok in ('FORM_DEFECT', 'PROVENANCE_UNVERIFIED', 'SPREAD_TAIL', 'SPREAD_SANITY_FAIL',
                'STABILITY_FAIL'):
        if 'result=' + tok in out:
            kind = tok
            break
    return r.returncode, kind, out


def _force_rm(func, path, _exc):
    """git's object files are read-only on Windows, so ignore_errors leaves the tree behind
    and the next makedirs fails. Clear the bit and retry rather than swallowing it."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    if os.path.isdir(REPO):
        shutil.rmtree(REPO, onerror=_force_rm)
    os.makedirs(REPO)
    subprocess.run(['git', 'init', '-q'], cwd=REPO, capture_output=True, text=True)
    io.open(os.path.join(REPO, '.gitignore'), 'w').write("apply.json\n")
    sh('git', 'add', '.gitignore')
    sh('git', '-c', 'user.name=h', '-c', 'user.email=h@h', 'commit', '-q', '-m', 'base')

    bR, bJ = battery(CLEAN_RHO, 0.95), battery(CLEAN_J, 0.79)
    pin_clean = commit_deriv(bR, bJ, 'clean battery')

    out_draws = [-0.14, -0.15, -0.13, -0.16, 0.50]
    bR_tail = battery(out_draws, 0.95)
    pin_tail = commit_deriv(bR_tail, bJ, 'tail battery')

    typed = [-0.14, -0.15, -0.13, -0.16,
             {"value": 0.50, "in_battery": False, "scheme": "adversarial-label-swap control"}]
    bR_typed = battery(typed, 0.95)
    pin_typed = commit_deriv(bR_typed, bJ, 'tail draw typed OUT')

    noscheme = [-0.14, -0.15, -0.13, -0.16, {"value": 0.50, "in_battery": False}]
    pin_ns = commit_deriv(battery(noscheme, 0.95), bJ, 'typed OUT with no scheme')
    bR_ns = battery(noscheme, 0.95)

    hi = [0.95, 0.96, 0.94, 0.97, 0.93]
    bR_hi = battery(hi, 0.998)
    pin_hi = commit_deriv(bR_hi, bJ, 'high null -> binding floor')

    # b6 names its scheme only in draws_0_provenance PROSE, so a derivation FROM it cannot
    # measure scheme agreement. These copies carry the field the forward binding requires.
    S1D_RHO = dict(B1D_RHO, scheme=SCHEME)
    S1D_J = dict(B1D_J, scheme=SCHEME)
    pin_1ds = commit_deriv(S1D_RHO, S1D_J, '1d battery, scheme named', rho=D_RHO, j=D_J)

    j20 = [round(0.050 + 0.001 * i, 6) for i in range(20)]
    bJ20 = battery(j20, 0.79)
    pin_j20 = commit_deriv(bR, bJ20, 'J battery at N=20, clean')

    N1R, N1J = battery([-0.1448], RHO), battery([0.1790], J)

    arms = []

    def arm(name, sentence, doc, want_rc, want_kind):
        rc, kind, out = run(doc)
        arms.append((rc == want_rc and kind == want_kind, name, sentence,
                     want_rc, want_kind, rc, kind, out))

    # ---- Addendum 1c: "TYPED REFUSALS (all FORM_DEFECT)", in its order ----
    b = dict(N1R)
    b.update(n_permutations=1, spread_status='MEASURED')
    arm('B1', '1c: spread_status=MEASURED with n_permutations<5',
        artifact('HELD-UNEXERCISED', b, N1J), 2, 'FORM_DEFECT')

    b = dict(N1R)
    b['spread'] = 0.01
    arm('B2', '1c: spread non-null with spread_status=UNMEASURED',
        artifact('HELD-UNEXERCISED', b, N1J), 2, 'FORM_DEFECT')

    b = dict(bR)
    b['n_permutations'] = 4
    arm('B3', '1c: len(draws) != n_permutations',
        artifact('HELD-UNEXERCISED', b, bJ), 2, 'FORM_DEFECT')

    b = dict(bR)
    b['null'] = b['null'] + 0.05
    arm('B4', '1c: null != mean(draws) at N>=5',
        artifact('HELD-UNEXERCISED', b, bJ), 2, 'FORM_DEFECT')

    b = dict(N1R)
    b['null'] = 0.4242
    arm('B5', '1c: null != draws[0] at N=1',
        artifact('HELD-UNEXERCISED', b, N1J), 2, 'FORM_DEFECT')

    d = artifact('HELD-UNEXERCISED', N1R, N1J)
    del d['stability_L3C01']['permutation_battery']
    arm('B6', '1c PLACEMENT: on EVERY run-N artifact (this is 1f5d4f6136 as it stands)',
        d, 3, '')

    arm('B7', '1c: a VALID N=1 block -- THE OTHER TRUTH',
        artifact('HELD-UNEXERCISED', N1R, N1J), 0, '')

    b = dict(N1R)
    b['observed'] = 0.111
    arm('B8', 'consumer-added arm: battery.observed vs the top-level statistic',
        artifact('HELD-UNEXERCISED', b, N1J), 2, 'FORM_DEFECT')

    # ---- Addendum 1d item 1: the permuted_control leaf ----
    arm('C1', '1d item 1: a BARE NUMBER is FORM_DEFECT',
        artifact('HELD-UNEXERCISED', N1R, N1J,
                 pc={"rho": -0.1448, "J": 0.1790}), 2, 'FORM_DEFECT')

    arm('C2', '1d item 1: a POINTER {in_battery: true, draw_index: 0} is permitted',
        artifact('HELD-UNEXERCISED', N1R, N1J,
                 pc={"rho": {"in_battery": True, "draw_index": 0},
                     "J": {"in_battery": True, "draw_index": 0}}), 0, '')

    arm('C3', '1d item 1: a pointer that is not in_battery is not draws[i]',
        artifact('HELD-UNEXERCISED', N1R, N1J,
                 pc={"rho": {"in_battery": False, "draw_index": 0},
                     "J": {"in_battery": True, "draw_index": 0}}), 2, 'FORM_DEFECT')

    arm('C4', '1d item 1: ABSENT resolves to draws[0] -- the removed-leaf shape',
        artifact('HELD-UNEXERCISED', battery(CLEAN_RHO, RHO), battery(CLEAN_J, J)),
        0, '')

    # ---- Addendum 1d: the PUBLISHED battery, CTO~X's own verdict as the expectation ----
    arm('D1', '1d: the commissioned run-1 artifact is ADMITTED (tail binds forward, not now)',
        artifact('HELD-UNEXERCISED', B1D_RHO, B1D_J, run_id='run-1', rho=D_RHO, j=D_J),
        0, '')

    arm('D2', '1d item 2: the J floor may NOT be derived from N=6 (rho has no tail, J does)',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_1ds, 'deriv.json', S1D_RHO, S1D_J,
                             obs_rho=D_RHO, obs_j=D_J)), 2, 'SPREAD_TAIL')

    dd = deriv_block(pin_clean, 'deriv.json', bR, bJ)
    dd['topdecile_jaccard']['tail_observed_at_n'] = 6
    arm('D3', '1d item 2: a CLEAN battery still waits -- a prior tail at N=6 binds until N>=20',
        artifact('RE-DERIVED', N1R, N1J, dd), 2, 'SPREAD_TAIL')

    dd = deriv_block(pin_j20, 'deriv.json', bR, bJ20)
    dd['topdecile_jaccard']['tail_observed_at_n'] = 6
    arm('D4', '1d item 2 THE OTHER TRUTH: at N=20 the recorded tail clears and J derives',
        artifact('RE-DERIVED', N1R, N1J, dd), 0, '')

    # ---- 80918 / 80925: SPREAD_TAIL ----
    arm('T1', '80925: an IN-BATTERY draw outside the band of the OTHER draws -> SPREAD_TAIL',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_tail, 'deriv.json', bR_tail, bJ)), 2, 'SPREAD_TAIL')

    arm('T2', '80925: a draw typed OUT (in_battery:false, scheme named) does NOT trigger it',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_typed, 'deriv.json', bR_typed, bJ)), 0, '')

    arm('T3', 'the consuming half of the exclusion: typed OUT with NO scheme named',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_ns, 'deriv.json', bR_ns, bJ)), 2, 'FORM_DEFECT')

    arm('T4', 'a clean battery derives normally -- SPREAD_TAIL is not always-on',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_clean, 'deriv.json', bR, bJ)), 0, '')

    # ---- 1c: "the two carriers are ONE contract" ----
    arm('X1', '1c 6b: null/spread/n_permutations/observed are READ FROM the battery at the pin',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_clean, 'deriv.json', bR, bJ,
                             tweak=lambda d: d['spearman_rho'].update(null=-0.9))),
        2, 'FORM_DEFECT')

    dd = deriv_block(pin_clean, 'deriv.json', bR, bJ)
    for k in ('spearman_rho', 'topdecile_jaccard'):
        del dd[k]['derived_from_path']
    arm('X2', 'a pin without a path does not address a block -> UNRUN, not passed',
        artifact('RE-DERIVED', N1R, N1J, dd), 3, 'PROVENANCE_UNVERIFIED')

    # ---- a84d5e9c76 sec 10 / 060402Z: floor_derivation must NAME ITS SCHEME ----
    dd = deriv_block(pin_clean, 'deriv.json', bR, bJ)
    for k in ('spearman_rho', 'topdecile_jaccard'):
        del dd[k]['scheme']
    arm('S1', 'sec 10: a floor without its scheme cannot be compared to anything',
        artifact('RE-DERIVED', N1R, N1J, dd), 2, 'FORM_DEFECT')

    arm('S2', 'sec 10: nulls compare only WITHIN one scheme',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_clean, 'deriv.json', bR, bJ,
                             scheme='view-2 label permutation (CTO~Y)')), 2, 'FORM_DEFECT')

    bR_ns2, bJ_ns2 = battery(CLEAN_RHO, 0.95, scheme=None), battery(CLEAN_J, 0.79, scheme=None)
    pin_noscheme = commit_deriv(bR_ns2, bJ_ns2, 'deriving battery names no scheme')
    arm('S3', 'a deriving battery with no scheme -> UNRUN, never assumed to match',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_noscheme, 'deriv.json', bR_ns2, bJ_ns2)),
        3, 'PROVENANCE_UNVERIFIED')

    arm('S4', '81027/CVO: spread is SAMPLE sd -- population sd must fail FORM_DEFECT',
        artifact('HELD-UNEXERCISED', dict(B1D_RHO, spread=0.100407), B1D_J,
                 run_id='run-1', rho=D_RHO, j=D_J), 2, 'FORM_DEFECT')

    # ---- L3-C01's OWN falsifier, both arms (face AC2: reachable from different truths) ----
    arm('K1', 'L3-C01: the permuted control does NOT drop -> NO artifact is admitted on it',
        artifact('HELD-UNEXERCISED', battery(hi, RHO), battery(CLEAN_J, J), run_id='run-1'),
        2, '')

    arm('K2', 'L3-C01 THE OTHER TRUTH: the control DROPS below both floors -> admitted',
        artifact('HELD-UNEXERCISED', battery(CLEAN_RHO, RHO), battery(CLEAN_J, J),
                 run_id='run-1'), 0, '')

    # ---- Addendum 1e @77c8d4e74c, each item as its own arm ----
    b = dict(B1D_RHO, precision_decimals=6, null=-0.016284 + 2e-6)
    arm('E1', '1e(1): |null - mean(draws)| > 10^-p at the DECLARED p',
        artifact('HELD-UNEXERCISED', b, B1D_J, run_id='run-1', rho=D_RHO, j=D_J),
        2, 'FORM_DEFECT')

    b = dict(B1D_RHO, precision_decimals=3, null=-0.016284 + 2e-6)
    arm('E2', '1e(1) THE OTHER TRUTH: the same delta PASSES at a coarser declared p',
        artifact('HELD-UNEXERCISED', b, B1D_J, run_id='run-1', rho=D_RHO, j=D_J), 0, '')

    d = artifact('RE-DERIVED', N1R, N1J, deriv_block(pin_clean, 'deriv.json', bR, bJ))
    d['stability_L3C01']['split_half']['half_b_runs'] = list(range(12, 26))
    arm('E3', '1e(A): OVERLAPPING halves -- disjointness is MEASURED, not read',
        d, 2, 'FORM_DEFECT')

    d = artifact('RE-DERIVED', N1R, N1J, deriv_block(pin_clean, 'deriv.json', bR, bJ))
    del d['stability_L3C01']['split_half']
    arm('E4', '1e(A): absent on a RUN-2 artifact -> PROVENANCE_UNVERIFIED',
        d, 3, 'PROVENANCE_UNVERIFIED')

    d = artifact('HELD-UNEXERCISED', N1R, N1J, run_id='run-1')
    del d['stability_L3C01']['split_half']
    arm('E5', '1e(A) THE OTHER TRUTH: absent on a RUN-1 artifact is an OBSERVATION (b6)',
        d, 0, '')

    dd = deriv_block(pin_clean, 'deriv.json', bR, bJ)
    dd['spearman_rho']['derived_artifact_sha256'] = 'de' * 32
    arm('E6', '1e(3): a digest that does not match the bytes at the pin',
        artifact('RE-DERIVED', N1R, N1J, dd), 2, 'FORM_DEFECT')

    dd = deriv_block(pin_clean, 'deriv.json', bR, bJ)
    for k in ('spearman_rho', 'topdecile_jaccard'):
        del dd[k]['n_permutations']
    dd['n_permutations'] = 5
    arm('E7', "1e(2): 1a's LEVEL-WIDE n_permutations is superseded, not a fallback",
        artifact('RE-DERIVED', N1R, N1J, dd), 2, 'FORM_DEFECT')

    # ---- regression: arms bound before 1c must still hold ----
    arm('J0', '1b: same-run emission is impossible, not merely paused',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_clean, 'deriv.json', bR, bJ, run='run-2')), 2, 'FORM_DEFECT')

    arm('J3', '1b: an unresolvable derived_at_commit is UNVERIFIED, never assumed',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block('0' * 40, 'deriv.json', bR, bJ)), 3, 'PROVENANCE_UNVERIFIED')

    arm('J5', 'a floor that BINDS: this run below the re-derived floor',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_hi, 'deriv.json', bR_hi, bJ, obs_rho=0.998)),
        2, 'STABILITY_FAIL')

    bR_flat = battery(hi, 0.96)   # 0.96 < its own floor 0.95 + 3*0.0158 = 0.9974
    pin_flat = commit_deriv(bR_flat, bJ, 'deriving observed below its own floor')
    arm('J6', 'the DERIVING run does not clear the floor it produced',
        artifact('RE-DERIVED', N1R, N1J,
                 deriv_block(pin_flat, 'deriv.json', bR_flat, bJ, obs_rho=0.96)),
        2, 'SPREAD_SANITY_FAIL')

    print("ARM  VERDICT EXPECTED                  GOT                       SENTENCE")
    npass = 0
    for ok, name, sent, wrc, wk, rc, k, _o in arms:
        npass += 1 if ok else 0
        print("%-4s %-7s exit=%d %-19s exit=%d %-19s %s"
              % (name, 'PASS' if ok else 'FAIL', wrc, wk or '-', rc, k or '-', sent[:60]))
    print("\n%d of %d arms as expected (denominator %d)" % (npass, len(arms), len(arms)))
    for ok, name, _s, _wrc, _wk, _rc, _k, out in arms:
        if not ok:
            print("\n===== %s OUTPUT =====\n%s" % (name, out))
    return 0 if npass == len(arms) else 1


if __name__ == '__main__':
    sys.exit(main())
