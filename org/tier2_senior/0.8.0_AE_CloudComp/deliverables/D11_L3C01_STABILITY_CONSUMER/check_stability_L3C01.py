#!/usr/bin/env python3
"""THE CONSUMING HALF of L3-C01's stability binding -- PREPARED, not yet delivered.

Built during the `after-fusion-output` gate from the DECLARATION (@9c1a45ad28), which is
what fixes this contract -- not from COX's artifact, which does not exist yet. NO STABILITY
VALUE IS WRITTEN by preparing this; it is the refusal mechanism the binding rows will name.

L3-C01 requires, of a fused artifact offered as evidence:
  * split-half over DISJOINT halves of the accepted N=25 battery (runs 1-12 / 13-25)
  * BOTH statistics -- Spearman rho AND top-decile pair-set Jaccard -- never one
  * the pair DENOMINATOR beside them
  * a PERMUTED-LABELS control that MUST drop below both floors

  exit 0  admissible: both statistics present with their denominator, both at/above floor,
          and the permuted control dropped below both
  exit 2  measured but NOT admissible: a statistic is below floor, or the permuted control
          did NOT drop -> the statistics are not measuring agreement and NO artifact is
          admitted on them
  exit 3  REFUSED: a required field is ABSENT. An absent statistic is never a pass, and a
          single statistic is refused outright -- the zero-mass agreement is why.
  exit 4  a SEPARATE axis (sec 6.3 frame shape). Never turns an L3-C01 verdict either way.

TYPED RESULTS on the L3-C01 axis, each its own value and none a synonym for another:
  FORM_DEFECT           shape or provenance is wrong (incl. 1c's four battery refusals)
  PROVENANCE_UNVERIFIED a provenance claim could not be MEASURED here -- not admitted as
                        verified, and not refused as false either
  SPREAD_TAIL           an IN-BATTERY draw at the deriving pin lies outside the band of the
                        other draws -> REFUSE TO DERIVE the floor for that statistic
  SPREAD_SANITY_FAIL    the DERIVING run's own observed does not clear the floor it produced
  STABILITY_FAIL        THIS run's observed is below a floor that binds
"""
import io
import hashlib
import json
import os
import re
import subprocess
import sys

FLOOR_RHO = 0.90
FLOOR_J = 0.80
# ADDENDUM 1d item 1 @ddbff010ec: `permuted_control` is REMOVED as a leaf -- its value now
# lives at draws[0] of each statistic's battery. A POINTER {in_battery: true, draw_index: 0}
# is permitted; a BARE NUMBER is FORM_DEFECT. So the control is no longer a required top-level
# field: it is resolved out of the battery, which is what makes it one carrier instead of two.
REQ = ['floor_status', 'metric_domain_predicate',
       'spearman_rho', 'topdecile_jaccard', 'pair_denominator']
# MEASURED against the real artifact @f8c1ad1b09 before trusting my own field list: this
# consumer had invented two SLOT NAMES the producer never agreed to. L3-C01 sec 1 fixes the
# SUBSTANCE (a split-half over disjoint halves; the union pair domain beside the metric one)
# and names no JSON key. So both are looked for wherever a producer may reasonably put them,
# and only a genuine ABSENCE of the substance refuses. A slot name is not a requirement.
OD_PATHS = [('stability_L3C01', 'output_domain_pairs'), ('output_domain', 'pairs'),
            ('output_domain', 'output_domain_pairs')]
SPLIT_KEYS = ['split_half', 'split_half_declaration', 'split_halves', 'split_half_basis']
# ADDENDUM 1e (A) @77c8d4e74c: FROM RUN 2, stability_L3C01.split_half carries this block.
# Overlapping run sets -> FORM_DEFECT; absent -> PROVENANCE_UNVERIFIED (never a silent pass).
# b6 is a run-1 artifact and its missing declaration stands as an OBSERVATION, not a refusal:
# wave 2's admission rests on the fired control and 1e does not reopen it.
SPLIT_REQ = ['battery_id', 'seed', 'half_a_runs', 'half_b_runs', 'disjoint', 'n_a', 'n_b']


# ---------------------------------------------------------------------------------------
# SEPARATE AXIS, on 3.0.0_SA_CVO~X's request 042659Z. The corrected artifact must carry TWO
# sec-6.3 frames. This is deliberately NOT folded into the L3-C01 verdict: my binding rows
# bind L3-C01, and a missing 6.3 frame is not an L3-C01 defect. One axis, one intent
# (Rule 24 iii) -- so it reports under its own exit code and never turns an L3-C01 pass into
# a fail or the reverse. Wave 2 SUPPLIES 6.3; it does not discharge it, and nothing here claims it.
SEC63_FRAMES = {'full_1941': 1941, 'both_measured_1820': 1820}


# THE THIRD invented slot name, found the same way as the other two -- by running against the
# real artifact instead of against my own idea of it. The producer's carrier is top-level
# `prd_6_3` with frame_A_full_locked_cohort / frame_B_both_measured_sub_cohort, each holding
# view1/view2/fused AUCs and a typed `predicate_fused_ge_view1`. Same substance, different
# keys. Normalised here rather than demanded there.
SEC63_ALIASES = [('full_1941', 'frame_A_full_locked_cohort'),
                 ('both_measured_1820', 'frame_B_both_measured_sub_cohort')]


def _sec63_frames(a):
    if isinstance(a.get('sec_6_3_frames'), dict):
        return a['sec_6_3_frames'], 'sec_6_3_frames'
    p = a.get('prd_6_3')
    if not isinstance(p, dict):
        return None, None
    out = {}
    for name, key in SEC63_ALIASES:
        fr = p.get(key)
        if isinstance(fr, dict):
            out[name] = {
                'denominator': fr.get('cohort'),
                'aucs': [fr[k] for k in ('view1_AUC', 'view2_AUC', 'fused_AUC') if k in fr],
                'predicate_result': fr.get('predicate_fused_ge_view1'),
            }
    return out, 'prd_6_3'


def check_sec63(a):
    f, carrier = _sec63_frames(a)
    if isinstance(f, dict):
        print("  sec-6.3: frames read from `%s`" % carrier)
    if not isinstance(f, dict):
        print("  sec-6.3: FRAMES ABSENT -> exit 4. Two frames are required (full 1,941 with "
              "pass-through/ABSENT treatment; both-measured 1,820 fusion-only).")
        return 4
    bad = []
    for name, den in SEC63_FRAMES.items():
        fr = f.get(name)
        if not isinstance(fr, dict):
            bad.append("%s: frame absent" % name)
            continue
        if fr.get('denominator') != den:
            bad.append("%s: denominator %r != %d" % (name, fr.get('denominator'), den))
        aucs = fr.get('aucs')
        if not isinstance(aucs, list) or len(aucs) != 3:
            bad.append("%s: needs THREE AUCs, got %r" % (name, aucs))
        # CVO 042934Z: each frame now carries an EVALUATED TRUE/FALSE predicate result
        # (CTO 80836 / CRO reconciliation). This checker validates that the value is a TYPED
        # TRUTH VALUE and does NOT decide whether the numbers imply it -- deciding would be
        # this seat evaluating a claim it does not own.
        pr = fr.get('predicate_result')
        if isinstance(pr, bool):
            pass
        elif isinstance(pr, str) and pr.strip().upper() in ('TRUE', 'FALSE'):
            pass
        else:
            bad.append("%s: predicate_result must be a TYPED truth value (true/false), got %r"
                       % (name, pr))
    if bad:
        print("  sec-6.3: INCOMPLETE -> exit 4: %s" % bad)
        return 4
    hist = 0.5114
    full = f['full_1941']
    if hist in (full.get('aucs') or []):
        print("  sec-6.3: REFUSED -> exit 4: the historical %.4f appears in the FULL 1,941 frame. "
              "It belongs only to the both-measured 1,820 frame if reproduced -- carrying it on "
              "the pass-through frame would compare a fusion-only baseline against a frame whose "
              "pairs are largely view-1 pass-through." % hist)
        return 4
    # WORDING HISTORY, kept so the churn is legible rather than invisible: CVO 042934Z called
    # "SUPPLIED, not discharged" stale and supplied replacement text; CVO 043012Z WITHDREW that
    # correction on CTO 80850, which accepts the phrase as durable scope discipline. The phrase
    # is retained. What was NOT withdrawn is the typed-truth-value requirement above -- the
    # artifact must carry each frame's EVALUATED TRUE/FALSE result -- so both survive: this
    # checker validates that the results are typed and present, and does NOT discharge sec 6.3.
    print("  sec-6.3: both frames present, 3 AUCs each, denominators 1,941 / 1,820, predicate "
          "results typed (full_1941=%s, both_measured_1820=%s). SUPPLIED, not discharged -- this "
          "check validated presence, denominators, AUC count and TYPED truth values, and did NOT "
          "decide whether the numbers imply those results."
          % (f['full_1941'].get('predicate_result'), f['both_measured_1820'].get('predicate_result')))
    return 0


# ---------------------------------------------------------------------------------------
# ADDENDUM 1c @28b1cab509 -- THE STRUCTURED N=1 CARRIER. Before 1c the N=1 permutation case
# lived in PROSE beside the block, and 3.0.0_SA_CVO~X 050309Z held this consumer on exactly
# that: "N=1 and spread UNMEASURED are prose-only. Do not treat prose as the carrier." 1c
# makes it a field a consumer can REJECT ON, and says so in its own words: a checker reads
# n_permutations and spread_status and never parses prose. Nothing in this file reads prose.
BATTERY_KEYS = [('spearman_rho', 'rho'), ('topdecile_jaccard', 'J')]
BATT_REQ = ['n_permutations', 'null', 'spread', 'spread_status', 'draws', 'observed']
TAIL_MULT = 3.0
TAIL_RETRY_N = 20
# 1a's canonical floor_derivation field list names NO artifact path, but 1c binds the two
# carriers as ONE contract ("reads null / spread / n_permutations / observed FROM this block
# at the deriving pin"). A pin without a path does not address a block, so this accepts any
# of these carriers and REFUSES rather than skipping when none is present -- an unrunnable
# provenance check is not a passed one. The gap itself is surfaced to the design lane.
PATH_FIELDS = ['derived_from_path', 'derived_from_artifact', 'derived_from_artifact_path']


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


# ---------------------------------------------------------------------------------------
# TOLERANCE IS DERIVED FROM THE ARTIFACT'S OWN STATED PRECISION, NEVER A CONSTANT.
# Found by transcribing 1d's PUBLISHED numbers into the harness before trusting this file:
# 1c's refusal "null != mean(draws)" is UNIMPLEMENTABLE as exact equality. 1d's rho battery
# declares null -0.016284 while the mean of its own six 6-decimal draws is -0.0162841666...,
# and J declares 0.055561 against 0.0555611666... A 1e-9 test REFUSES BOTH -- it would have
# rejected the very artifact the ruling commissions. A fixed 1e-6 is no better: it is too
# tight for a 4-decimal artifact and too loose for a 12-decimal one.
def _decimals(x):
    r = repr(float(x))
    if 'e' in r or 'E' in r:
        return 12
    return len(r.split('.')[1]) if '.' in r else 0


def _block_p(b, inb):
    """ADDENDUM 1e (1) @77c8d4e74c: the battery carries `precision_decimals: p`. ABSENT, p is
    the largest printed decimal count in the block AND THE CONSUMER PRINTS THE INFERENCE --
    an inferred tolerance that does not announce itself is a silent widening of every arm."""
    v = b.get('precision_decimals')
    if isinstance(v, int) and not isinstance(v, bool) and v >= 0:
        return v, False
    vals = [x for x in (b.get('null'), b.get('spread'), b.get('observed')) if _num(x)] + list(inb)
    return (max([_decimals(x) for x in vals]) if vals else 9), True


def _close(a, b, refs, slack=1.0):
    """An ARITHMETIC IDENTITY holds to the precision of the COARSEST input, times the slack the
    operation's own rounding needs (null + m*spread accumulates three roundings, not one)."""
    p = max([_decimals(v) for v in refs] or [9])
    return abs(float(a) - float(b)) <= max(slack * (10.0 ** -p), 1e-12)


def _agree(a, b):
    """TWO CARRIERS OF ONE NUMBER agree to the precision of the LESS precise one. A top-level
    statistic rendered at 4 decimals and a battery `observed` at 6 do not disagree; demanding
    they match at 1e-9 manufactures a defect out of a rendering choice."""
    p = min(_decimals(a), _decimals(b))
    return abs(float(a) - float(b)) <= max(0.5 * (10.0 ** -p), 1e-12)


def _mean(v):
    return sum(v) / float(len(v))


def _sd(v):
    """SAMPLE sd (ddof=1), used ONLY for the leave-one-out tail band -- never to recompute the
    artifact's own `spread`, which this checker READS and does not second-guess. 1c fixes
    neither the estimator nor ddof; the choice is DECLARED in the output because at the N=5
    floor ddof moves the band by about 12 percent."""
    if len(v) < 2:
        return 0.0
    m = _mean(v)
    return (sum((x - m) ** 2 for x in v) / float(len(v) - 1)) ** 0.5


def _draw_values(draws):
    """Split `draws` into IN-battery and typed-OUT values.

    1c types `draws` as an array of NUMBERS. 80918 as clarified by 80925 adds a draw that may
    be typed OUT of the battery (`in_battery: false` with a NAMED scheme), which does not
    trigger SPREAD_TAIL. Both shapes are accepted, and A BARE NUMBER IS IN BATTERY -- only an
    explicit typed exclusion excludes, so an untyped array behaves exactly as 1c specifies.
    """
    inb, out, bad, seq = [], [], [], []
    for i, dr in enumerate(draws):
        if _num(dr):
            inb.append(float(dr))
            seq.append((float(dr), True))
        elif isinstance(dr, dict):
            v = dr.get('value')
            if not _num(v):
                bad.append("draw %d is typed but carries no numeric `value`" % i)
                seq.append((None, None))
            elif dr.get('in_battery') is False:
                if not str(dr.get('scheme', '') or '').strip():
                    bad.append("draw %d is typed OUT of the battery with no NAMED scheme -- an "
                               "untypeable exclusion is how a draw gets quietly dropped" % i)
                    seq.append((None, None))
                else:
                    out.append((float(v), dr.get('scheme')))
                    seq.append((float(v), False))
            else:
                inb.append(float(v))
                seq.append((float(v), True))
        else:
            bad.append("draw %d is neither a number nor a typed draw (%r)" % (i, dr))
            seq.append((None, None))
    return inb, out, bad, seq


def check_battery(s, label):
    """1c's battery block. Returns (rc, {stat: battery}); rc 0 clean | 2 FORM_DEFECT | 3 ABSENT.

    1c enumerates FOUR typed refusals, all FORM_DEFECT, and they are implemented verbatim
    below. ABSENCE is exit 3, not FORM_DEFECT: 1c's list is about MALFORMED blocks, and this
    file's standing discipline is that an absent field is refused, never read as a value.
    """
    pb = s.get('permutation_battery')
    if not isinstance(pb, dict):
        print("REFUSED (exit 3): `permutation_battery` ABSENT on %s. Addendum 1c places it on "
              "EVERY run-N fusion artifact, one block per statistic S in {rho, J}. The N=1 "
              "permutation case carried in PROSE is not a carrier -- there is nothing here for "
              "a checker to read, which is the whole defect 1c cures." % label)
        return 3, None
    absent, form, got = [], [], {}
    for stat, key in BATTERY_KEYS:
        b = pb.get(key)
        if not isinstance(b, dict):
            absent.append("permutation_battery.%s (the block for %s)" % (key, stat))
            continue
        miss = [k for k in BATT_REQ if k not in b]
        if miss:
            absent.append("permutation_battery.%s missing %s" % (key, miss))
            continue
        n, st, sp, dr = b['n_permutations'], b['spread_status'], b['spread'], b['draws']
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            form.append("%s: n_permutations %r -- 1c requires an integer >= 1" % (key, n))
            continue
        if st not in ('MEASURED', 'UNMEASURED'):
            form.append("%s: spread_status %r is not one of MEASURED / UNMEASURED" % (key, st))
            continue
        if not _num(b['null']) or not _num(b['observed']):
            form.append("%s: null and observed must both be numbers (got %r / %r)"
                        % (key, b['null'], b['observed']))
            continue
        if sp is not None and not _num(sp):
            form.append("%s: spread must be a number or null (got %r)" % (key, sp))
            continue
        # --- 1c's four typed refusals, in its own order ---
        if st == 'MEASURED' and n < 5:
            form.append("%s: spread_status=MEASURED with n_permutations=%d -- 1c requires N>=5 "
                        "before a spread may be called MEASURED" % (key, n))
        if st == 'UNMEASURED' and sp is not None:
            form.append("%s: spread is non-null (%r) while spread_status=UNMEASURED -- a value "
                        "beside a status that denies it is the prose-as-carrier defect in a "
                        "field" % (key, sp))
        if not isinstance(dr, list) or len(dr) != n:
            form.append("%s: len(draws)=%s != n_permutations=%d"
                        % (key, len(dr) if isinstance(dr, list) else 'not-a-list', n))
            continue
        inb, out, dbad, seq = _draw_values(dr)
        if dbad:
            form.append("%s: %s" % (key, dbad))
            continue
        if not inb:
            form.append("%s: every draw is typed OUT of the battery -- there is no null" % key)
            continue
        # 1c: null != mean(draws), or != draws[0] at N=1. WHERE 1c IS SILENT: when a draw is
        # typed OUT (80918/80925), the mean is taken over the IN-BATTERY draws only, because a
        # draw declared not part of the battery cannot be part of the battery's null. With no
        # typed exclusion the two readings are IDENTICAL, so this is 1c-faithful wherever 1c
        # actually speaks. Named here rather than chosen silently.
        # CTO~X 81027 / CVO~X 055751Z: `spread` is the SAMPLE standard deviation, ddof=1. 1c's
        # form said only "sd of draws" and left the divisor open; it is pinned now, and a
        # POPULATION-sd artifact must fail as FORM_DEFECT (for b6 that is 0.100407 / 0.058926
        # against the contract's 0.109991 / 0.064550 -- a 9 percent gap, not a rounding one).
        pdec, inferred = _block_p(b, inb)
        tol = 10.0 ** -pdec
        if inferred:
            print("  battery %-4s precision_decimals ABSENT -> INFERRED p=%d from the largest "
                  "printed decimal count in the block; arms run at 10^-%d" % (key, pdec, pdec))
        if sp is not None and abs(float(sp) - _sd(inb)) > tol:
            form.append("%s: |spread - stdev(draws, ddof=1)| > 10^-%d. Declared %r, sample sd "
                        "%.9f, population sd %.9f -- population sd is NOT the contract."
                        % (key, pdec, sp, _sd(inb),
                           _sd(inb) * ((len(inb) - 1) / float(len(inb))) ** 0.5 if len(inb) > 1
                           else 0.0))
            continue
        want = inb[0] if len(inb) == 1 else _mean(inb)
        if abs(float(b['null']) - want) > tol:
            form.append("%s: |null - %s| > 10^-%d. Declared %r, computed %.10g"
                        % (key, 'draws[0] at N=1' if len(inb) == 1 else 'mean(draws)',
                           pdec, b['null'], want))
            continue
        got[stat] = dict(b, _in=inb, _out=out, _seq=seq, _key=key)
    if absent:
        print("REFUSED (exit 3): battery field(s) ABSENT on %s: %s. An absent battery is never "
              "a pass." % (label, absent))
        return 3, None
    if form:
        print("REFUSED (exit 2) result=FORM_DEFECT: battery on %s: %s" % (label, form))
        return 2, None
    return 0, got


def resolve_control(s, batt):
    """ADDENDUM 1d item 1: the permuted control's value IS draws[0] of each statistic.

    Returns (rc, {stat: value}). Accepted carriers, and nothing else:
      * `permuted_control` ABSENT           -> draws[0], the removed-leaf shape 1d mandates
      * {in_battery: true, draw_index: N}   -> draws[N], which MUST be an in-battery draw
      * a BARE NUMBER                       -> FORM_DEFECT (1d item 1, verbatim)

    A bare number is refused because it is a SECOND carrier of a number the battery already
    holds; the leaf was removed precisely so the two could not drift apart.
    """
    pc = s.get('permuted_control')
    form, vals = [], {}
    for stat, key in BATTERY_KEYS:
        seq = batt[stat]['_seq']
        node = pc.get(key, pc.get(stat)) if isinstance(pc, dict) else pc
        idx = 0
        if node is not None:
            if _num(node):
                form.append("%s: permuted_control is a BARE NUMBER (%r). 1d item 1 removed the "
                            "leaf: the value lives at draws[0]. A pointer "
                            "{in_battery: true, draw_index: 0} is the only permitted carrier."
                            % (key, node))
                continue
            if not isinstance(node, dict):
                form.append("%s: permuted_control %r is neither absent nor a pointer" % (key, node))
                continue
            if node.get('in_battery') is not True:
                form.append("%s: the permuted_control pointer must carry in_battery: true -- a "
                            "control drawn from outside the battery is not draws[i]" % key)
                continue
            idx = node.get('draw_index', 0)
            if not isinstance(idx, int) or isinstance(idx, bool) or not (0 <= idx < len(seq)):
                form.append("%s: draw_index %r is not a valid index into %d draw(s)"
                            % (key, idx, len(seq)))
                continue
        v, inb = seq[idx]
        if not inb:
            form.append("%s: draws[%d] is typed OUT of the battery, so it cannot be the "
                        "permuted control" % (key, idx))
            continue
        vals[stat] = v
    if form:
        print("REFUSED (exit 2) result=FORM_DEFECT: permuted control: %s" % form)
        return 2, None
    return 0, vals


def _loo_tail(vals, mult=TAIL_MULT):
    """LEAVE-ONE-OUT band test -- 80918 as clarified by 80925: a draw lies outside the band
    (null + mult*spread) OF THE OTHER DRAWS. Leave-one-out is load-bearing: a draw included in
    its own spread inflates the band and hides itself.

    Returns (upper, two_sided, runnable). THE BINDING ARM IS `upper` -- the ruling's band as
    WRITTEN is one-sided (null + 3*spread). `two_sided` is REPORTED and never acted on, and it
    is reported because a LOW outlier deflates the spread, which LOWERS the derived floor and
    makes the NEXT run's acceptance easier: a one-sided band is blind to exactly the error
    direction that produces a false ACCEPT. Naming that is this checker's job; moving the band
    is the design lane's.
    """
    upper, both = [], []
    if len(vals) < 3:
        return upper, both, False
    for i, v in enumerate(vals):
        others = vals[:i] + vals[i + 1:]
        m, sd = _mean(others), _sd(others)
        if v > m + mult * sd + 1e-12:
            upper.append((i, v, m, sd))
        if abs(v - m) > mult * sd + 1e-12:
            both.append((i, v, m, sd))
    return upper, both, True


def _blob_sha256(path, commit):
    try:
        env = dict(os.environ, MSYS_NO_PATHCONV='1')
        r = subprocess.run(['git', 'show', '%s:%s' % (commit, path)],
                           capture_output=True, env=env)
        return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 else None
    except Exception:
        return None


def _load_at_pin(path, commit):
    """Read one JSON artifact at a pin. MSYS_NO_PATHCONV is set because the argument is a
    slashed `<commit>:<path>` -- the documented argv-mangling shape on this platform."""
    try:
        env = dict(os.environ, MSYS_NO_PATHCONV='1')
        r = subprocess.run(['git', 'show', '%s:%s' % (commit, path)],
                           capture_output=True, text=True, env=env)
        if r.returncode != 0:
            return None, (r.stderr or 'git show failed with no stderr').strip()[:200]
        return json.loads(r.stdout), None
    except Exception as e:
        return None, repr(e)


def _is_ancestor(commit, carrier):
    """True / False / None(unresolvable). Ancestry is MEASURED, never assumed."""
    try:
        r = subprocess.run(['git', 'cat-file', '-e', commit + '^{commit}'],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return None
        r = subprocess.run(['git', 'merge-base', '--is-ancestor', commit, carrier],
                           capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return None


def main(argv):
    if len(argv) < 2:
        print("usage: check_stability_L3C01.py <fused_artifact.json> [carrier_ref]")
        return 64
    carrier = argv[2] if len(argv) > 2 and not argv[2].startswith('--') else 'HEAD'
    try:
        a = json.load(io.open(argv[1], encoding='utf-8'))
    except Exception as e:
        print("REFUSED (exit 3): unreadable -- %r" % (e,))
        return 3
    s = a.get('stability_L3C01')
    if not isinstance(s, dict):
        print("REFUSED (exit 3): no `stability_L3C01` block. L3-C01 is not honoured in prose; "
              "an artifact offered as fused evidence carries the block or is not admitted.")
        return 3
    miss = [k for k in REQ if k not in s]
    if miss:
        print("REFUSED (exit 3): missing required field(s) %s. An absent statistic is NEVER a pass." % miss)
        return 3
    if not isinstance(s['pair_denominator'], int) or s['pair_denominator'] <= 0:
        print("REFUSED (exit 3): pair_denominator absent or not a positive count -- a statistic "
              "without the domain it was computed over is a frame error.")
        return 3
    # RULED 1.0.0_SA_CTO~X 80806: TWO domains, both printed, NEVER conflated. The OUTPUT domain
    # is the UNION (all ratified entities, all pairs, each carrying its per-view mask); the
    # METRIC domain for rho/J/control is the BOTH-MEASURED pairs, because over one-view pairs the
    # "fused" value is view 1 passed through and a stability statistic there measures view 1's
    # self-agreement -- high for the wrong reason. A bare positive integer cannot tell those
    # apart, and the conflation is exactly what refused the first fused artifact.
    if 'metric_domain_predicate' not in s or not str(s.get('metric_domain_predicate', '')).strip():
        print("REFUSED (exit 3): `metric_domain_predicate` absent. AC3 requires the count beside "
              "WHAT IT IS A COUNT OF; a bare pair_denominator cannot distinguish the union "
              "output domain from the both-measured metric domain.")
        return 3
    od, od_at = None, None
    for root, key in OD_PATHS:
        node = s if root == 'stability_L3C01' else a.get(root)
        if isinstance(node, dict) and isinstance(node.get(key), int) and node[key] > 0:
            od, od_at = node[key], '%s.%s' % (root, key)
            break
    if od is None:
        print("REFUSED (exit 3): the UNION pair domain is absent. The artifact must print BOTH "
              "denominators -- the union it is DEFINED on and the predicate the statistics were "
              "COMPUTED on -- or a reader cannot tell which one a number belongs to. Searched: "
              "%s. This is a SUBSTANCE requirement (L3-C01 sec 1), not one slot name."
              % ['.'.join(x) for x in OD_PATHS])
        return 3
    if s['pair_denominator'] >= od:
        print("REFUSED (exit 2): pair_denominator (%d) is not SMALLER than the output domain "
              "(%d). The metric domain is the both-measured subset; a metric denominator equal "
              "to the union means the statistics were computed over one-view pass-through pairs, "
              "where they measure view 1's self-agreement rather than fusion stability."
              % (s['pair_denominator'], od))
        return 2
    print("  metric domain    %d of %d output pairs (%.2f%%) -- %s"
          % (s['pair_denominator'], od, 100.0 * s['pair_denominator'] / od,
             s['metric_domain_predicate']))

    # ADDENDUM 1c: the battery is required on EVERY run-N artifact, including this one.
    rcb, batt = check_battery(s, 'this artifact')
    if rcb:
        return rcb
    obs_bad = []
    for stat, key in BATTERY_KEYS:
        if not _agree(batt[stat]['observed'], s[stat]):
            obs_bad.append("%s: permutation_battery.%s.observed=%r != stability_L3C01.%s=%r"
                           % (key, key, batt[stat]['observed'], stat, s[stat]))
    if obs_bad:
        # NOT one of 1c's four enumerated refusals -- declared as a checker-added arm rather
        # than smuggled in. It can only fire when two carriers of the SAME number disagree,
        # which is a defect under any reading of the contract.
        print("REFUSED (exit 2) result=FORM_DEFECT [arm added by this consumer, not in 1c's "
              "enumerated four]: %s. The battery's `observed` and the top-level statistic are "
              "two carriers of one number; when they disagree, neither can be quoted." % obs_bad)
        return 2
    rcc, ctl = resolve_control(s, batt)
    if rcc:
        return rcc
    for stat, key in BATTERY_KEYS:
        b = batt[stat]
        print("  battery %-4s N=%-3d null=%.6f spread=%s (%s) observed=%.6f%s"
              % (key, b['n_permutations'], float(b['null']),
                 ('%.6f' % b['spread']) if b['spread'] is not None else 'null',
                 b['spread_status'], float(b['observed']),
                 '' if not b['_out'] else '  [%d draw(s) typed OUT: %s]'
                 % (len(b['_out']), [sc for _v, sc in b['_out']])))

    # L3-C01 sec 1 item 1, at source @9c1a45ad28: the halves must be DISJOINT halves of the
    # named N-run battery ("runs 1-12 and 13-25 of the accepted N=25 battery"). An artifact
    # that does not say WHICH runs form its halves makes that disjointness unfalsifiable, so
    # the requirement is real; the KEY it lives under is not fixed by the declaration.
    sh = next((s[k] for k in SPLIT_KEYS if s.get(k)), None)
    # RUN 1 vs RUN 2 is DERIVED, not read from a label: a producing run carries
    # floor_status HELD-UNEXERCISED and no floor_derivation (1b forbids same-run derivation);
    # a consuming run carries the block. 1e (A) binds split_half "from run 2".
    is_run2 = s.get('floor_status') == 'RE-DERIVED' or isinstance(s.get('floor_derivation'), dict)
    if sh is None:
        rep = (a.get('rows') or {}).get('reproducibility') if isinstance(a.get('rows'), dict) else None
        if not is_run2:
            print("  split_half: ABSENT, and this is a RUN-1 artifact (floor_status "
                  "HELD-UNEXERCISED, no floor_derivation). Recorded as an OBSERVATION per 1e "
                  "(A), NOT a refusal -- admission rests on the fired control. rows."
                  "reproducibility is %s and records that halves were run without naming them."
                  % ('present' if rep else 'absent'))
        else:
            print("REFUSED (exit 3) result=PROVENANCE_UNVERIFIED: split_half ABSENT on a RUN-2 "
                  "artifact. 1e (A) requires {battery_id, seed, half_a_runs, half_b_runs, "
                  "disjoint, n_a, n_b} from run 2; without the run sets, DISJOINTNESS -- the "
                  "whole point of a split half -- cannot be measured.")
            return 3
    elif isinstance(sh, dict):
        miss = [k for k in SPLIT_REQ if k not in sh]
        if miss:
            print("REFUSED (exit 3) result=PROVENANCE_UNVERIFIED: split_half missing %s (1e A)."
                  % miss)
            return 3
        ha, hb = sh['half_a_runs'], sh['half_b_runs']
        if not isinstance(ha, list) or not isinstance(hb, list):
            print("REFUSED (exit 2) result=FORM_DEFECT: half_a_runs / half_b_runs must be run "
                  "LISTS; counts alone cannot show disjointness.")
            return 2
        # DISJOINTNESS IS MEASURED, never read off the `disjoint` field -- a claim about the
        # halves is not the halves. The declared flag is then checked AGAINST the measurement.
        overlap = sorted(set(ha) & set(hb))
        if overlap:
            print("REFUSED (exit 2) result=FORM_DEFECT: the halves OVERLAP on %s. Two halves "
                  "sharing a run are not disjoint, and a split-half statistic over them "
                  "measures the shared runs agreeing with themselves." % overlap)
            return 2
        if sh['disjoint'] is not True:
            print("REFUSED (exit 2) result=FORM_DEFECT: measured overlap is EMPTY but the "
                  "artifact declares disjoint=%r -- the declaration contradicts its own runs."
                  % (sh['disjoint'],))
            return 2
        if sh['n_a'] != len(ha) or sh['n_b'] != len(hb):
            print("REFUSED (exit 2) result=FORM_DEFECT: n_a/n_b (%r/%r) do not count their own "
                  "run lists (%d/%d)." % (sh['n_a'], sh['n_b'], len(ha), len(hb)))
            return 2
        print("  split_half: battery %r seed %r -- %d + %d runs, overlap MEASURED empty"
              % (sh['battery_id'], sh['seed'], len(ha), len(hb)))
    print("stability check | pair domain %d | union domain from %s"
          % (s['pair_denominator'], od_at))
    print("  spearman_rho        %.4f  (floor %.2f)" % (s['spearman_rho'], FLOOR_RHO))
    print("  topdecile_jaccard   %.4f  (floor %.2f)" % (s['topdecile_jaccard'], FLOOR_J))
    print("  permuted rho / J    %.6f / %.6f  (MUST be below both floors; resolved from "
          "draws[0] per 1d item 1, not from a removed leaf)"
          % (ctl['spearman_rho'], ctl['topdecile_jaccard']))

    ctl_dropped = ctl['spearman_rho'] < FLOOR_RHO and ctl['topdecile_jaccard'] < FLOOR_J
    if not ctl_dropped:
        print("REFUSED (exit 2): the PERMUTED control did NOT drop below both floors. The "
              "statistics are not measuring agreement between views, the threshold means "
              "nothing, and NO fused artifact is admitted on them. This is a defect in the "
              "instrument, reported as such.")
        return 2
    # RULED 1.0.0_SA_CTO~X 80787, BEFORE the first pin: the HELD floors DO NOT BIND THE FIRST
    # RUN IN EITHER DIRECTION. A first-run J of 0.8033 is not a pass by 0.0033, and 0.7967 would
    # not have been a fail -- both read a typed constant as though it had seen its own
    # distribution. What ADMITS the first run is the CONTROL FIRING plus the observed-vs-permuted
    # gap. The floor is re-derived from this run's own permuted null and binds the NEXT run.
    floor_status = s.get('floor_status')
    if floor_status not in ('HELD-UNEXERCISED', 'RE-DERIVED'):
        print("REFUSED (exit 3): `floor_status` absent or not one of HELD-UNEXERCISED / "
              "RE-DERIVED. An artifact that does not say whether its floor has ever seen a "
              "distribution invites a held constant to be read as a measured bar.")
        return 3
    below = [n for n, v, f in (('spearman_rho', s['spearman_rho'], FLOOR_RHO),
                               ('topdecile_jaccard', s['topdecile_jaccard'], FLOOR_J)) if v < f]
    if floor_status == 'HELD-UNEXERCISED':
        print("  floor_status HELD-UNEXERCISED -- the floors are REPORTED, not applied (ruling 80787)")
        print("  observed vs permuted gap: rho %.4f vs %.4f | J %.4f vs %.4f"
              % (s['spearman_rho'], ctl['spearman_rho'], s['topdecile_jaccard'], ctl['topdecile_jaccard']))
        if below:
            print("  NOTE: %s sits below its HELD floor. That is REPORTED, not a refusal: the held "
                  "floor does not bind this run in either direction." % below)
        print("OK (exit 0): ADMITTED ON THE CONTROL, not on the floor. The permuted control "
              "dropped below both floors, which is L3-C01's validity arm. No acceptance is "
              "claimed against the held floor; the floor is re-derived from this run's own "
              "permuted null and binds the NEXT run.")
        rc63 = check_sec63(a)
        print("L3-C01: ADMITTED-ON-CONTROL (floors HELD-UNEXERCISED); sec-6.3 frames: %s"
              % ('present' if rc63 == 0 else 'absent/malformed'))
        return rc63 or 0
    # RE-DERIVED regime. CANONICAL CARRIER: L3-C01 Addendum 1a @61891652ef (CTO~X 80863),
    # with CVO 045438Z's exception on derived_at_commit. Per statistic, floor_derivation.<S>:
    #   derived_from_run_id / derived_at_commit / metric_domain / null / spread /
    #   n_permutations (>=5, else NO block) / multiplier (3, held) / floor / deriving_run_observed
    # THE CHECKER RECOMPUTES floor = null + multiplier * spread; a mismatch is FORM_DEFECT.
    # a84d5e9c76 sec 10 (relayed 060402Z; CVO 060443Z carries the same, sender-unverified):
    # floor_derivation carries `scheme` as a NAMED STRING, and a derivation citing draws
    # from a different scheme than the artifact it binds is FORM_DEFECT/provenance. Two
    # batteries with different schemes measure different nulls: COX permutes half-B's W1
    # labels, CTO~Y permutes view 2's. Nulls compare only WITHIN one scheme.
    CANON = ['derived_from_run_id', 'metric_domain', 'null', 'spread', 'multiplier', 'floor',
             'deriving_run_observed', 'scheme']
    d = s.get('floor_derivation')
    if not isinstance(d, dict):
        print("REFUSED (exit 3): floor_status RE-DERIVED with no `floor_derivation` block. A "
              "re-derived floor must carry its derivation or it is a new constant wearing a "
              "derived label.")
        return 3
    # 1a puts n_permutations at the floor_derivation LEVEL, one value for both statistics. 1d
    # item 2 makes the two statistics DIVERGE -- rho may derive at N>=5 while J waits for
    # N>=20 -- so a single level-wide value can no longer represent the derivation. A
    # PER-STATISTIC n_permutations is therefore read where present and the level-wide value is
    # the fallback; absent both is a refusal. Surfaced to the design lane: the field needs to
    # move, and until it does an artifact obeying 1d cannot satisfy 1a's shape.
    n = d.get('n_permutations')
    if n is not None and (not isinstance(n, int) or isinstance(n, bool) or n < 5):
        # 1a types this FORM_DEFECT (exit 2) when a block is PRESENT: N=1 must emit no block at
        # all and stay HELD-UNEXERCISED, so a block with N<5 is a malformed derivation, not a
        # missing field.
        print("REFUSED (exit 2) result=FORM_DEFECT: n_permutations = %r; the form requires N >= 5. "
              "A single permutation gives one null POINT and no spread -- that case must emit NO "
              "floor_derivation block and carry floor_status HELD-UNEXERCISED." % (n,))
        return 2
    evaluated_run = s.get('run_id')
    bad, sanity, unresolved, tails = [], [], [], []
    deriv_cache = {}
    for nm, obs in (('spearman_rho', s['spearman_rho']), ('topdecile_jaccard', s['topdecile_jaccard'])):
        e = d.get(nm)
        if not isinstance(e, dict):
            bad.append("%s: floor_derivation.%s absent" % (nm, nm))
            continue
        miss = [k for k in CANON if k not in e]
        if miss:
            bad.append("%s: missing canonical field(s) %s" % (nm, miss))
            continue
        ns = e.get('n_permutations')
        if not isinstance(ns, int) or isinstance(ns, bool) or ns < 5:
            bad.append("%s: floor_derivation.<S>.n_permutations is %r. 1e (2) makes it PER "
                       "STATISTIC and SUPERSEDES 1a's level-wide field, because 1d lets rho "
                       "(N>=5) and J (N>=20) diverge; >= 5 required." % (nm, ns))
            continue
        # ADDENDUM 1b @4c1886a50f -- THE NON-CIRCULAR SHAPE. There is NO same-run emission:
        # run N's artifact carries the battery as EVIDENCE with floor_status HELD-UNEXERCISED and
        # NO floor_derivation block; the block lives only in the CONSUMING run, citing run N's
        # commit. So a self-derivation is not "paused", it is IMPOSSIBLE -- my previous branch
        # admitted it with enforcement deferred, and 1b makes that a refusal.
        if evaluated_run is not None and e['derived_from_run_id'] == evaluated_run:
            bad.append("%s: RE-DERIVED with derived_from_run_id == this artifact's run_id (%r). "
                       "Addendum 1b forbids same-run emission: run N emits the battery as "
                       "EVIDENCE at HELD-UNEXERCISED with NO block; the block belongs to the "
                       "CONSUMING run." % (nm, evaluated_run))
            continue
        c = e.get('derived_at_commit')
        if not isinstance(c, str) or not re.fullmatch(r'[0-9a-f]{7,40}', c or ''):
            bad.append("%s: derived_at_commit absent or not a commit-ish (%r). Under 1b it is "
                       "always a PRIOR run's commit and is always required." % (nm, c))
            continue
        # 1b's provenance falsifier: the cited commit must be a STRICT ANCESTOR of the carrier.
        anc = _is_ancestor(c, carrier)
        if anc is False:
            bad.append("%s: derived_at_commit %s is NOT an ancestor of the carrier %s -- 1b's "
                       "provenance falsifier. A floor cannot be derived from a run that does not "
                       "precede the artifact applying it." % (nm, c, carrier))
            continue
        if anc is None:
            unresolved.append("%s: derived_at_commit %s could not be resolved in this repo -- "
                              "ancestry UNVERIFIED, reported rather than assumed" % (nm, c))
        # ---- ADDENDUM 1c, "the two carriers are ONE contract": null / spread /
        # n_permutations / observed are READ FROM THE BATTERY AT THE DERIVING PIN, not typed
        # into floor_derivation. So this reads that block and compares. A derivation whose
        # numbers do not match the battery they claim to come from is a new constant wearing a
        # derived label -- which is the exact defect the RE-DERIVED status exists to prevent.
        dpath = next((e[k] for k in PATH_FIELDS if isinstance(e.get(k), str) and e[k].strip()),
                     None)
        if not dpath:
            unresolved.append(
                "%s: floor_derivation cites commit %s but NO artifact path, so the deriving "
                "battery cannot be addressed and 1c's two-carriers-are-one-contract check is "
                "UNRUN. An unrunnable provenance check is not a passed one. (1a's canonical "
                "field list names no path carrier -- surfaced to the design lane, not invented "
                "here; any of %s satisfies it.)" % (nm, c, PATH_FIELDS))
            continue
        ck = (dpath, c)
        if ck not in deriv_cache:
            doc, err = _load_at_pin(dpath, c)
            if doc is None:
                deriv_cache[ck] = ('ERR', err)
            elif not isinstance(doc.get('stability_L3C01'), dict):
                deriv_cache[ck] = ('ERR', 'no stability_L3C01 block at that pin')
            else:
                rcd, bt = check_battery(doc['stability_L3C01'], '%s @%s' % (dpath, c))
                deriv_cache[ck] = ('ERR', 'battery refused at the deriving pin '
                                   '(exit %d, printed above)' % rcd) if rcd else ('OK', bt)
        kind, payload = deriv_cache[ck]
        if kind == 'ERR':
            if payload.startswith('battery refused'):
                bad.append("%s: %s @%s -- %s" % (nm, dpath, c, payload))
            else:
                unresolved.append("%s: could not read %s @%s -- %s" % (nm, dpath, c, payload))
            continue
        if not str(e.get('scheme', '') or '').strip():
            bad.append("%s: floor_derivation carries no named `scheme`. Two batteries tonight "
                       "measure different nulls under different schemes; a floor without its "
                       "scheme cannot be compared to anything." % nm)
            continue
        db = payload.get(nm)
        if db is None:
            bad.append("%s: the deriving battery at %s @%s carries no block for this statistic"
                       % (nm, dpath, c))
            continue
        mism = []
        for fld, ev in (('null', e['null']), ('spread', e['spread']),
                        ('observed', e['deriving_run_observed'])):
            dv = db['observed' if fld == 'observed' else fld]
            if dv is None or ev is None:
                if dv is not ev:
                    mism.append("%s: derivation %r vs battery %r" % (fld, ev, dv))
            elif not _agree(ev, dv):
                mism.append("%s: derivation %r vs battery %r" % (fld, ev, dv))
        want_sha = e.get('derived_artifact_sha256')
        if isinstance(want_sha, str) and want_sha.strip():
            got_sha = _blob_sha256(dpath, c)
            if got_sha is None:
                unresolved.append("%s: derived_artifact_sha256 carried but the blob at %s @%s "
                                  "could not be re-read to check it" % (nm, dpath, c))
                continue
            if got_sha.lower() != want_sha.strip().lower():
                bad.append("%s: derived_artifact_sha256 %s does not match the bytes at %s @%s "
                           "(%s). The pin and the digest name different content."
                           % (nm, want_sha[:16], dpath, c, got_sha[:16]))
                continue
        bsch = db.get('scheme')
        if not str(bsch or '').strip():
            unresolved.append(
                "%s: the deriving battery at %s @%s names no `scheme`, so 'same scheme as the "
                "artifact it binds' CANNOT BE MEASURED here. Reported UNRUN rather than "
                "assumed -- the b6 battery @f8c1ad1b09 carries its scheme only in "
                "draws_0_provenance PROSE, and prose is not the carrier."
                % (nm, dpath, c))
            continue
        if str(bsch).strip() != str(e['scheme']).strip():
            bad.append("%s: floor_derivation scheme %r != the cited battery's scheme %r. Nulls "
                       "compare only within one scheme (a84d5e9c76 sec 10)."
                       % (nm, e['scheme'], bsch))
            continue
        own = (batt.get(nm) or {}).get('scheme')
        if str(own or '').strip() and str(own).strip() != str(e['scheme']).strip():
            bad.append("%s: the derivation binds THIS artifact, whose own battery scheme is %r, "
                       "with a floor derived under scheme %r." % (nm, own, e['scheme']))
            continue
        if db['n_permutations'] != ns:
            mism.append("n_permutations: derivation %r vs battery %r"
                        % (ns, db['n_permutations']))
        if mism:
            bad.append("%s: floor_derivation disagrees with the battery it cites at %s @%s -- %s"
                       % (nm, dpath, c, mism))
            continue
        # ---- SPREAD_TAIL (80918, clarified by 80925). The draws under test are the DERIVING
        # run's, because those are the draws the floor is built from.
        up, both, runnable = _loo_tail(db['_in'])
        if not runnable:
            unresolved.append("%s: the leave-one-out tail band needs at least 3 in-battery "
                              "draws and this battery carries %d -- the test is UNRUN, which is "
                              "reported and never scored as 'no tail'" % (nm, len(db['_in'])))
            continue
        # 1d places tail_observation INSIDE permutation_battery.<S> (the producing run's own
        # disclosure) and tail_observed_at_n on floor_derivation.<S> (the record a LATER
        # derivation carries forward). BOTH ARE READ, NEITHER IS COMPUTED HERE.
        declared = db.get('tail_observation')
        prior_n = e.get('tail_observed_at_n')
        # 1e (1) STRIKES the band comparison I had here: "Bands are DERIVED by the consumer
        # from typed fields, never compared." The consumer computes its own band from the
        # draws and does not adjudicate a declared one against it.
        if up or declared:
            tails.append(
                "%s: %s. No floor is derived for this statistic; floor_status stays "
                "HELD-UNEXERCISED for it and derivation waits for N >= %d (this deriving "
                "battery N=%d, %s). tail_observation=%r, tail_observed_at_n=%r -- both READ "
                "from the artifact, neither computed here. A two-sided band would flag %d "
                "draw(s) [REPORTED, never binding]."
                % (nm,
                   ("%d in-battery draw(s) lie outside the band null+%g*spread of the OTHER "
                    "draws: %s" % (len(up), TAIL_MULT,
                                   [(i, round(v, 6), round(m2 + TAIL_MULT * sd2, 6))
                                    for i, v, m2, sd2 in up])) if up
                   else "the battery DECLARES a tail and this consumer does not overrule a "
                        "producer's own disclosure downward",
                   TAIL_RETRY_N, ns,
                   'eligible on N' if ns >= TAIL_RETRY_N else 'NOT eligible on N',
                   declared, prior_n, len(both)))
            continue
        if prior_n is not None:
            # 1d item 2, the carried-forward case: a tail was observed for this statistic at an
            # EARLIER N (J at N=6). This battery is clean, but the block may not be derived
            # until N >= 20. Without this branch a clean N=6 retry would derive the very floor
            # 1d forbids -- the tail's whole forward effect would be silently discarded.
            if ns < TAIL_RETRY_N:
                tails.append("%s: the battery is clean, but floor_derivation records "
                             "tail_observed_at_n=%r -- a tail was observed for this statistic "
                             "at an earlier N. 1d item 2: derivation waits for N >= %d and this "
                             "deriving battery is N=%d." % (nm, prior_n, TAIL_RETRY_N, ns))
                continue
            print("  %s: prior tail at N=%r is RECORDED and cleared -- deriving battery N=%d "
                  ">= %d (1d item 2)" % (nm, prior_n, ns, TAIL_RETRY_N))
        m = e['multiplier']
        want = e['null'] + m * e['spread']
        if not _close(e['floor'], want, [e['null'], e['spread'], e['floor']],
                      slack=(2.0 + abs(float(m))) * 0.5):
            bad.append("%s: floor %.6f != null + %s*spread = %.6f (recomputed, not trusted)"
                       % (nm, e['floor'], m, want))
            continue
        if not (e['deriving_run_observed'] > e['floor']):
            sanity.append("%s: deriving_run_observed %.6f is not strictly above the re-derived "
                          "floor %.6f (derived_from_run_id=%r)"
                          % (nm, e['deriving_run_observed'], e['floor'], e['derived_from_run_id']))
    if bad:
        print("REFUSED (exit 2) result=FORM_DEFECT: %s" % bad)
        return 2
    if unresolved:
        print("REFUSED (exit 3) result=PROVENANCE_UNVERIFIED: %s. Ancestry could not be measured "
              "in this repo; an unverifiable provenance claim is not admitted as a verified one."
              % unresolved)
        return 3
    if tails:
        print("REFUSED (exit 2) result=SPREAD_TAIL: %s" % tails)
        print("      ITS OWN VALUE, per CTO~X 80925. NOT SPREAD_SANITY_FAIL (which is about the "
              "DERIVING run's observed against the floor it produced) and NOT FORM_DEFECT "
              "(shape/provenance). The battery is well formed and the provenance holds; what "
              "fails is that a null distribution with a tail cannot support a floor. "
              "CONSEQUENCE: no floor is derived for that statistic, floor_status stays "
              "HELD-UNEXERCISED for it, and derivation is retried only at N >= %d." % TAIL_RETRY_N)
        print("      BAND DECLARED: leave-one-out, null + %g * spread of the OTHER draws, spread "
              "as SAMPLE sd (ddof=1). Leave-one-out because a draw inside its own spread "
              "inflates the band and hides itself. The ruling fixes neither ddof nor a side; "
              "both choices are named here and neither is silent." % TAIL_MULT)
        return 2
    if sanity:
        print("REFUSED (exit 2) result=SPREAD_SANITY_FAIL: %s" % sanity)
        print("      NOT a stability failure. The deriving run did NOT fail a binding floor -- the "
              "re-derived floor is too high to discriminate, a finding about the SPREAD. "
              "CONSEQUENCE: record EXCESSIVE SPREAD, floor_status remains HELD-UNEXERCISED, the "
              "battery is re-run on the next run, and the multiplier is NOT raised. Addendum 1 "
              "raises the multiplier ONLY when the sec-6 falsifier fires (a second, INDEPENDENT "
              "battery under which the observed no longer clears), and never lowers it.")
        return 2
    below = [nm for nm, obs in (('spearman_rho', s['spearman_rho']),
                                ('topdecile_jaccard', s['topdecile_jaccard']))
             if obs <= d[nm]['floor']]
    if below:
        print("REFUSED (exit 2) result=STABILITY_FAIL: %s below the RE-DERIVED floor "
              "(null + 3*spread), which does "
              "bind. BOTH statistics are required -- a rank correlation over a heavily "
              "zero-weighted pair domain can read high on the agreeing zeros while disagreeing "
              "about every pair that carries signal." % below)
        return 2
    print("  floors RE-DERIVED per Addendum 1a: rho >= %.6f, J >= %.6f (null + m*spread, m=%s, "
          "N per-stat %s, recomputed not trusted); sanity holds against deriving_run_observed"
          % (d['spearman_rho']['floor'], d['topdecile_jaccard']['floor'],
             d['spearman_rho']['multiplier'],
             [d[k].get('n_permutations', n) for k in ('spearman_rho', 'topdecile_jaccard')]))
    print("OK (exit 0): both statistics at/above the RE-DERIVED floor and the permuted control "
          "dropped below both.")
    rc63 = check_sec63(a)
    print("L3-C01: ADMITTED (re-derived floor); sec-6.3 frames: %s"
          % ('present' if rc63 == 0 else 'absent/malformed'))
    return rc63 or 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
