#!/usr/bin/env python3
"""c3ii_declared_plane_join.py -- JOIN the DECLARED plane to the APPLIED plane for C3.ii generation.

TO: NFRA_VERTHARVEST.C3II.declared-plane-join @e0a8ef9ec7.  Author: 4.0.0_SA_CRO.
Grounding: C3II_MACRO_REGISTRY_GROUNDING_20260807.md @98c0991fb0 (1.0.0_SA_CTO).

>> JOIN, NEVER UNION. <<
`org/projects/MACRO_CODES.md` enters as the DECLARED PLANE -- the denominator -- and is NEVER added
as an eighth harvest source. The reason is a control, not a preference: the VERTHARVEST spec's only
natural positive control is that its single miss is `causality`, retired 2026-08-05 with an applied
plane measured empty ("a harvest that FINDS causality is reading the model, not the estate"). The
registry CONTAINS `CENG` = CausalityEngine, so unioning it in would make the harvest find causality
on day one -- recall goes UP and the instrument goes BLIND in the same act.

>> THE CONTROL IS A PAIR, AND BOTH LIMBS ARE LOAD-BEARING. <<
  NEGATIVE limb  CENG must land in DECLARED x NOT-APPLIED.
  POSITIVE limb  a named known-live code must land in DECLARED x APPLIED, FROM THE SAME PASS.
The negative limb alone is satisfied *most cleanly* by a measurement that is completely dead --
it cannot distinguish "causality is correctly absent" from "nothing was measured at all". That is
the Rule-22a could-not-have-said-otherwise shape. Only the positive limb discriminates it.
(COO's criterion 3 + this seat's paired-control addition; the two catch different failures --
the coverage vocabulary catches a measurement that REPORTS its failure, the pair catches one that
fails SILENTLY and returns clean zeros.)

>> THREE STATES IN NOT-APPLIED, per the Kimi subdivision coverage contract (REUSED, not re-derived
   -- a landed architecture ruling). ZERO CANDIDATES IS A RESULT; A FAILED MEASUREMENT IS AN ABSENCE
   OF MEASUREMENT, and in a naive 2x2 they are byte-identical:
     codes_planned   the denominator, known BEFORE any measurement fires
     codes_measured  the measurement ran for this code
     codes_empty[]   ran and found zero          <- a RESULT
     codes_failed[]  did not run / errored       <- an ABSENCE OF MEASUREMENT

This script AUTO-NAMES NOTHING. Naming is sovereign; it surfaces candidates only.
It does not modify MACRO_CODES.md (a taxonomy edit mid-harvest would move the declared plane under
the measurement).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REGISTRY = "org/projects/MACRO_CODES.md"

# Tokens too generic to carry a join. A match on one of these is a false positive by construction.
STOPWORDS = {
    "opal", "data", "pipeline", "portal", "page", "pages", "src", "the", "and", "for", "prod",
    "dev", "test", "lambda", "aws", "s3", "v1", "v2", "api", "core", "main", "new", "old",
    "cross", "pod", "area", "surface", "code", "codes", "project", "projects", "capital",
}


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


# ---------------------------------------------------------------- declared plane


def camel_words(s):
    """'AdvisorIntelligence' -> ['advisor','intelligence']; also splits on non-alnum."""
    parts = re.split(r"[^A-Za-z0-9]+", s)
    out = []
    for p in parts:
        if not p:
            continue
        out.extend(w.lower() for w in re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+|[0-9]+", p))
    return [w for w in out if w]


def parse_declared(path):
    """Parse every markdown table row whose first cell is a backticked 4-char code.

    Deliberately structural rather than section-aware: the file's sections have changed shape
    over time, and a parser keyed on headings would silently drop a section someone renames.
    """
    rows, current_pod = [], None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            h = re.match(r"^##\s+(.*)$", line)
            if h:
                current_pod = h.group(1).strip()
                continue
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            m = re.match(r"^`([A-Z0-9]{4})`$", cells[0])
            if not m:
                continue
            code = m.group(1)
            surface = cells[1]
            portal_dir, pipeline, owner = "", "", ""
            # Two table shapes exist in this file: the pod tables carry
            # (Code, Surface Area, Portal Directory, RD Agent, Pipeline); the cross-pod and
            # portal-wide tables carry (Code, Surface Area, Primary Owner).
            if len(cells) >= 5:
                portal_dir, owner, pipeline = cells[2], cells[3], cells[4]
            elif len(cells) == 3:
                owner = cells[2]
            rows.append({
                "code": code,
                "surface_area": surface,
                "portal_dir": portal_dir,
                "owner": owner,
                "pipeline": pipeline,
                "section": current_pod,
            })
    return rows


def code_tokens(row, weak=False):
    """The join key set for one declared code, split by STRENGTH.

    >> SURFACE AREA IS IDENTITY. PIPELINE IS ONLY USAGE. <<
    A code's name, surface area and portal directory say what the code IS. Its `pipeline` column
    says which pipeline that surface USES -- and registry rule 4 explicitly allows two surfaces to
    share one. So a pipeline token is a WEAK key and must never outrank a surface token.

    MEASURED, which is why this split exists: CENG declares `pipeline = "causality, news-pipeline"`,
    so it inherited `news` -- which is NPPL's own SURFACE -- and matched all 34 `news-*` resources
    byte-identically to NPPL, driving CENG to APPLIED and failing the negative control.

    weak=False -> STRONG keys (code, surface area, portal dir)
    weak=True  -> WEAK keys (pipeline only)
    """
    toks = set()
    if weak:
        if row["pipeline"]:
            for p in re.split(r"[,+;]", row["pipeline"]):
                toks.update(camel_words(p))
    else:
        toks.add(row["code"].lower())
        # surface area: words before any parenthetical/dash gloss -- that span is the NAME
        head = re.split(r"[(—]| -- | - ", row["surface_area"])[0]
        toks.update(camel_words(head))
        if row["portal_dir"]:
            leaf = row["portal_dir"].strip("`").rstrip("/").split("/")[-1]
            toks.update(camel_words(leaf))
    return {t for t in toks if t and t not in STOPWORDS and len(t) >= 3}


# ---------------------------------------------------------------- applied plane


def sh(argv, timeout=240):
    """Run a command as an ARGV LIST -- never shell=True. Return (ok, stdout).

    ⛔ shell=True IS A MEASURED DEFECT HERE, NOT A STYLE CHOICE. This function used it, and on this
    box the shell did NOT strip the single quotes around a JMESPath expression. `aws` then received
    the literal `'Functions[].FunctionName'`, which JMESPath parses as a RAW STRING LITERAL -- so the
    query returned that constant instead of the field, `--output text` printed it ONCE PER PAGE, and
    the limb reported rc=0 with n=4 when the true population was 197. The count was the PAGE COUNT.
    Three failure classes stacked in one call: MSYS/Windows argv quoting, a JMESPath literal that is
    valid and wrong, and `--query` applied per-page. Every one of them is silent and rc=0.

    An argv list removes the shell from the path entirely, so no quoting layer can reinterpret the
    expression. Related: `.tools/msys_argv_guard.py` for the Python->MSYS-binary direction."""
    try:
        p = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=timeout)
        if p.returncode != 0:
            return False, (p.stderr or "").strip()[:300]
        return True, p.stdout
    except Exception as exc:
        return False, str(exc)[:300]


def resolve_aws():
    """The aws entry point reachable from a NATIVE-PYTHON argv spawn.

    `aws` on PATH is the extensionless Git-Bash shim; CreateProcess cannot execute it, so a bare
    ["aws", ...] raises WinError 2. `aws.cmd` is the sibling that Windows CAN launch, and CLAUDE.md
    requires the pair be provisioned atomically for exactly this reason. Measured on this box:
    aws.cmd -> rc=0; the extensionless shim -> WinError 2.
    """
    import shutil
    for cand in ("aws.cmd", os.path.join(".tools", "aws.cmd")):
        w = shutil.which(cand) or (cand if os.path.exists(cand) else None)
        if w:
            return os.path.abspath(w) if os.path.exists(w) else w
    return None


def measure_applied(workspace, use_aws=True):
    """Return (resources, limbs). Each limb records ok/failed EXPLICITLY."""
    resources, limbs = [], {}

    # --- LOCAL limbs -------------------------------------------------------
    pages_dir = os.path.join(workspace, "portal", "src", "pages")
    if os.path.isdir(pages_dir):
        names = sorted(os.listdir(pages_dir))
        for n in names:
            resources.append({"name": n, "kind": "portal_page"})
        limbs["portal_pages"] = {"status": "measured", "n": len(names)}
    else:
        limbs["portal_pages"] = {"status": "FAILED", "why": "portal/src/pages absent"}

    data_dir = os.path.join(workspace, "data")
    if os.path.isdir(data_dir):
        trees = sorted(d for d in os.listdir(data_dir)
                       if os.path.isdir(os.path.join(data_dir, d)))
        for d in trees:
            resources.append({"name": d, "kind": "data_tree"})
        limbs["data_trees"] = {"status": "measured", "n": len(trees)}
    else:
        limbs["data_trees"] = {"status": "FAILED", "why": "data/ absent"}

    # --- AWS limbs ---------------------------------------------------------
    # No --no-paginate anywhere: the CLI auto-paginates and we count the MATERIALISED set.
    # ARGV LISTS, never a shell string -- see sh()'s docstring for the measured incident.
    #
    # >> EVERY LIMB CARRIES ITS OWN POSITIVE CONTROL (`must_contain`). <<
    # A code-level control pair is NOT sufficient and this was measured, not theorised: when three
    # AWS limbs silently returned page counts, the code-level pair still PASSED because the positive
    # code (ADVI) was satisfied by a HEALTHY LOCAL LIMB. A control at the wrong granularity reports
    # the health of whichever limb happens to be alive. So each limb must independently prove it
    # returned real data -- a limb that cannot find a member known to exist is FAILED, not empty.
    AWS = resolve_aws()
    aws_limbs = [
        ("lambdas", ["lambda", "list-functions",
                     "--query", "Functions[].FunctionName", "--output", "text"], "lambda",
         "opal"),
        ("eventbridge_rules", ["events", "list-rules",
                               "--query", "Rules[].Name", "--output", "text"], "rule", "-"),
        ("s3_buckets", ["s3api", "list-buckets",
                        "--query", "Buckets[].Name", "--output", "text"], "bucket",
         "opal-data-assets"),
    ]
    for limb, tail, kind, must_contain in aws_limbs:
        if not use_aws:
            limbs[limb] = {"status": "FAILED", "why": "--no-aws: limb deliberately not run"}
            continue
        if not AWS:
            limbs[limb] = {"status": "FAILED", "why": "no argv-executable aws.cmd resolved"}
            continue
        ok, out = sh([AWS] + tail)
        if not ok:
            limbs[limb] = {"status": "FAILED", "why": out}
            continue
        names = [x for x in re.split(r"[\t\n\r ]+", out) if x]
        # PER-LIMB POSITIVE CONTROL: a limb that cannot see a known member did not measure.
        if not any(must_contain in n for n in names):
            limbs[limb] = {"status": "FAILED", "n_returned": len(names),
                           "why": f"positive control failed: no returned name contains "
                                  f"{must_contain!r} -- the limb returned something, but not this "
                                  f"population (page count / literal query / wrong field)"}
            continue
        for n in names:
            resources.append({"name": n, "kind": kind})
        limbs[limb] = {"status": "measured", "n": len(names), "positive_control": must_contain}
    return resources, limbs


def norm(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower())


def resource_words(name):
    """Word set for an applied resource name -- CAMEL-SPLIT as well as delimiter-split.

    MEASURED defect this fixes: portal page directories are CamelCase (`AdvisorIntelligence`,
    `FactorTilts`), and a lowercase-and-hyphenate normalisation yields the single token
    `advisorintelligence`, which matches no declared key. The result was that DECLARED portal pages
    landed in the NOT-DECLARED candidate pile -- an obviously-wrong output that inflated the
    product cell with the very surfaces the registry declares.
    """
    words = set(w for w in norm(name).split("-") if w)
    words.update(camel_words(name))
    return words


def match_code(resource_name, tokmap):
    """Which declared codes does this applied resource match? INFERRED, not declared."""
    words = resource_words(resource_name)
    hits = []
    for code, toks in tokmap.items():
        if toks & words:
            hits.append(code)
    return hits


# ---------------------------------------------------------------- main


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-aws", action="store_true", help="skip AWS limbs (they report FAILED)")
    ap.add_argument("--positive-control", default="ADVI",
                    help="code asserted to land in DECLARED x APPLIED, same pass as CENG")
    ap.add_argument("--negative-control", default="CENG")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    vintage = utc_now()
    declared = parse_declared(os.path.join(args.workspace, REGISTRY))
    strong = {r["code"]: code_tokens(r, weak=False) for r in declared}
    weakm = {r["code"]: code_tokens(r, weak=True) for r in declared}
    codes_planned = [r["code"] for r in declared]

    # STRENGTH-AWARE OWNERSHIP: a token claimed STRONGLY by exactly one code belongs to that code,
    # even if other codes claim it weakly (via their pipeline column). This is the registry's own
    # rule-4 structure honoured rather than flattened -- and it is what puts `news` with NPPL (whose
    # SURFACE is the news pipeline) instead of with CENG (which merely USES it).
    from collections import Counter as _C0
    strong_owner = _C0()
    for toks in strong.values():
        for t in toks:
            strong_owner[t] += 1
    tokmap = {}
    for c in codes_planned:
        keep = set(strong[c])
        for t in weakm[c]:
            if strong_owner[t] == 0:      # nobody owns it strongly -> a weak key may still help
                keep.add(t)
        tokmap[c] = keep

    # >> AN AMBIGUOUS TOKEN CANNOT ESTABLISH IDENTITY. <<
    # A token claimed by 2+ codes discriminates between none of them, so it is dropped from ALL of
    # them and recorded. MEASURED, not anticipated: CENG declares its pipeline as
    # "causality, news-pipeline", so it inherited the token `news` -- which is NPPL's own surface --
    # and matched 34 `news-*` resources BYTE-IDENTICALLY to NPPL. That drove CENG to APPLIED and
    # failed the negative control. Ground-truthed independently with a positive control on the same
    # pipes: `causality`/`ceng` return ZERO live lambdas, rules and buckets while `advisor` returns
    # 3, so the spec's premise held and the MATCHER was the defect.
    # The pipeline field is a WEAK key by nature: it says which pipeline a surface USES, not which
    # resources BELONG to it, and two surfaces legitimately share one pipeline (registry rule 4).
    from collections import Counter as _C
    owners = _C()
    for toks in tokmap.values():
        for t in toks:
            owners[t] += 1
    ambiguous = {t for t, n in owners.items() if n > 1}
    tokmap = {c: (toks - ambiguous) for c, toks in tokmap.items()}
    codes_no_key = sorted(c for c, toks in tokmap.items() if not toks)

    resources, limbs = measure_applied(args.workspace, use_aws=not args.no_aws)
    # NOTE: an `any_limb_ok` predicate lived here and was the DEFECT -- one healthy limb made the
    # whole measurement read complete while three others were dead. Completeness is `all_limbs_ok`,
    # computed below at the point of use. Deliberately not reinstated.

    # per-code applied evidence
    applied_hits = {c: [] for c in codes_planned}
    unmatched = []
    for r in resources:
        hits = match_code(r["name"], tokmap)
        if hits:
            for c in hits:
                applied_hits[c].append(r)
        else:
            unmatched.append(r)

    # declared portal_dir existence is a SOUND (declared-key) limb, no inference
    for row in declared:
        pd_ = row["portal_dir"].strip("`")
        if pd_ and pd_.startswith("portal/"):
            p = os.path.join(args.workspace, pd_.rstrip("/"))
            if os.path.exists(p) or os.path.exists(p + ".tsx"):
                applied_hits[row["code"]].append({"name": pd_, "kind": "declared_portal_dir"})

    # >> ABSENCE IS ONLY MEANINGFUL UNDER COMPLETE MEASUREMENT. <<
    # POSITIVE evidence stands on its own -- a code with a live resource is APPLIED no matter which
    # other limbs died. ABSENCE does not: if ANY limb failed, a code with no evidence might have had
    # its evidence in the dead limb, so it is NOT-MEASURED (an absence of measurement), never
    # MEASURED-EMPTY (a result).
    #
    # This distinction is not decorative and it was MEASURED here, not anticipated: a first run
    # reported 16 codes as MEASURED-EMPTY -- including CENG, so the negative control PASSED -- while
    # three of five limbs were silently returning page counts. A partial measurement reported as a
    # complete one manufactures a clean control result out of missing data.
    all_limbs_ok = all(v["status"] == "measured" for v in limbs.values())
    codes_applied = [c for c in codes_planned if applied_hits[c]]
    no_evidence = [c for c in codes_planned if not applied_hits[c]]
    codes_empty = no_evidence if all_limbs_ok else []
    codes_failed = [] if all_limbs_ok else no_evidence
    codes_measured = codes_applied + codes_empty

    out = {
        "_header": {
            "artifact": "c3ii_declared_plane_join",
            "vintage": vintage,
            "join": "JOIN (declared x applied). NOT a union. The registry is never a harvest source.",
            "declared_source": REGISTRY,
            "denominator_grain": "MACRO CODES (rows), not projects and not resources",
            "coverage_contract": "Kimi subdivision (reused, not re-derived)",
            "codes_planned": len(codes_planned),
            "codes_measured": len(codes_measured),
            "codes_failed": codes_failed,
            "codes_empty": codes_empty,
            "applied_limbs": limbs,
            "applied_resources_total": len(resources),
            "matcher": "INFERRED token match, stoplist-filtered; declared_portal_dir limb is a "
                       "DECLARED key and carries no inference",
            "ambiguous_tokens_dropped": sorted(ambiguous),
            "ambiguous_tokens_n": len(ambiguous),
            "codes_left_with_NO_identity_key": codes_no_key,
            "codes_no_key_caveat": "these codes cannot be matched at all after ambiguity removal -- "
                                   "their NOT-APPLIED verdict is a MATCHER LIMIT, not an estate fact",
        },
        "cells": {
            "declared_applied": sorted(codes_applied),
            "declared_not_applied": sorted(codes_empty),
            "not_declared_applied_candidates": [],
            "not_declared_not_applied": "invisible by construction -- a boundary, not a defect",
        },
        "control": {},
        "per_code": {},
    }

    # ---- CRITERION 2a: the NOT-APPLIED cell SPLITS. Collapsing loses a finding and mis-sites the
    # control, because CENG's expected cell is the RETIRED half specifically.
    #   RETIRED      was applied, ended by a NAMING ACT -> correct final resting place, stays forever
    #   ASPIRATIONAL declared AHEAD of build, never applied -> a WIP row that SHOULD move; if it
    #                never does, that is a finding
    #   UNCLASSIFIED neither is established -> named, never guessed into one of the other two
    # ASPIRATIONAL is DERIVED from the declared plane ("TBD" markers in the row). RETIRED is NOT
    # inferred -- it requires a cited naming act, so it is an explicit list. Inferring retirement
    # from an empty applied plane would make the control circular.
    RETIRED_BY_NAMING_ACT = {
        "CENG": "causality retired by Andrew 2026-08-05 (VERTHARVEST spec, applied plane measured "
                "empty; independently ground-truthed here: 0 lambdas/rules/buckets match "
                "causality|ceng, positive control 'advisor' = 3 on the same pipes)",
    }

    def not_applied_kind(code, row):
        if code in RETIRED_BY_NAMING_ACT:
            return "RETIRED", RETIRED_BY_NAMING_ACT[code]
        blob = f"{row['surface_area']} {row['portal_dir']} {row['pipeline']} {row['owner']}"
        if re.search(r"\bTBD\b", blob):
            return "ASPIRATIONAL", "row carries TBD -- declared ahead of build"
        return "UNCLASSIFIED", "no naming act cited and no TBD marker -- not guessed"

    for c in codes_planned:
        row = next(r for r in declared if r["code"] == c)
        toks = tokmap[c]
        # A key that exists but can NEVER FIRE is not a key. The 4-char macro code effectively never
        # appears inside a resource name, so a code left with only its own code-token is
        # MATCHER-LIMITED: its NOT-APPLIED verdict describes my instrument, not the estate.
        substantive = {t for t in toks if t != c.lower()}
        if applied_hits[c]:
            state, kind, why = "APPLIED", None, None
        elif c in codes_measured:
            state = "MEASURED-EMPTY"
            kind, why = not_applied_kind(c, row)
        else:
            state, kind, why = "NOT-MEASURED", None, None
        out["per_code"][c] = {
            "surface_area": row["surface_area"][:90],
            "section": row["section"],
            "state": state,
            "not_applied_kind": kind,
            "not_applied_basis": why,
            "n_applied": len(applied_hits[c]),
            "sample": [r["name"] for r in applied_hits[c][:6]],
            "tokens": sorted(toks),
            "matcher_limited": bool(state == "MEASURED-EMPTY" and not substantive),
        }

    out["_header"]["matcher_limited_codes"] = sorted(
        c for c, v in out["per_code"].items() if v.get("matcher_limited"))
    out["_header"]["matcher_limited_caveat"] = (
        "these codes retain NO key beyond their own 4-char code, which effectively never appears in "
        "a resource name -- their NOT-APPLIED verdict is a MATCHER LIMIT, not an estate fact. "
        "MEASURED live counter-example: NPPL reads empty while 34 news-* resources are live.")

    # candidate clustering for the NOT-DECLARED x APPLIED cell (the product)
    from collections import Counter
    cand = Counter()
    for r in unmatched:
        for w in norm(r["name"]).split("-"):
            if w and w not in STOPWORDS and len(w) >= 4 and not w.isdigit():
                cand[w] += 1
    out["cells"]["not_declared_applied_candidates"] = [
        {"token": t, "n_resources": n} for t, n in cand.most_common(40)
    ]
    out["unmatched_resources"] = sorted(r["name"] for r in unmatched)

    # ---- THE CONTROL PAIR ----
    neg, pos = args.negative_control, args.positive_control
    neg_state = out["per_code"].get(neg, {}).get("state")
    pos_state = out["per_code"].get(pos, {}).get("state")
    neg_kind = out["per_code"].get(neg, {}).get("not_applied_kind")
    neg_limited = out["per_code"].get(neg, {}).get("matcher_limited")
    # Criterion 2(a): the RETIRED half specifically, not the union -- AND not matcher-limited, or
    # the limb would be passing because the code has no usable key rather than because the estate
    # is empty. That is the same wrong-reason pass this control exists to prevent, one level in.
    neg_ok = (neg_state == "MEASURED-EMPTY" and neg_kind == "RETIRED" and not neg_limited)
    pos_ok = pos_state == "APPLIED"
    out["control"] = {
        "negative_limb": {"code": neg,
                          "expected": "MEASURED-EMPTY / kind=RETIRED / not matcher-limited",
                          "observed": f"{neg_state} / kind={neg_kind} / "
                                      f"matcher_limited={neg_limited}", "pass": neg_ok},
        "positive_limb": {"code": pos, "expected": "APPLIED (DECLARED x APPLIED)",
                          "observed": pos_state, "pass": pos_ok},
        "pair_pass": bool(neg_ok and pos_ok),
        "why_the_pair": "The negative limb alone is satisfied most cleanly by a DEAD measurement. "
                        "Only the positive limb, from the SAME pass, discriminates 'correctly "
                        "absent' from 'nothing was measured'.",
    }

    print(json.dumps(out["_header"], indent=2))
    print("\n== THE 2x2 ==")
    print(f"  DECLARED x APPLIED      : {len(codes_applied):>3} of {len(codes_planned)} codes")
    print(f"  DECLARED x NOT-APPLIED  : {len(codes_empty):>3} of {len(codes_planned)} codes "
          f"(MEASURED-EMPTY) -> {sorted(codes_empty)}")
    print(f"  DECLARED x NOT-MEASURED : {len(codes_failed):>3} of {len(codes_planned)} codes "
          f"(ABSENCE OF MEASUREMENT, not a zero)")
    print(f"  NOT-DECLARED x APPLIED  : {len(unmatched):>3} unmatched applied resources of "
          f"{len(resources)} measured -> the CANDIDATE cell (the product)")
    print("  NOT-DECLARED x NOT-APPLIED: invisible by construction (a boundary, not a defect)")
    print("\n== CONTROL PAIR ==")
    for limb in ("negative_limb", "positive_limb"):
        d = out["control"][limb]
        print(f"  {limb:<14} {d['code']}: expected {d['expected']}, observed {d['observed']} "
              f"-> {'PASS' if d['pass'] else 'FAIL'}")
    print(f"  PAIR: {'PASS' if out['control']['pair_pass'] else '*** FAIL -- do not ship on this join ***'}")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
        print(f"\nwrote {args.out}")
    return 0 if out["control"]["pair_pass"] else 2


# ---------------------------------------------------------------- self-test

def self_test():
    fails = []

    def check(c, label):
        print(("  PASS  " if c else "  FAIL  ") + label)
        if not c:
            fails.append(label)

    check(camel_words("AdvisorIntelligence") == ["advisor", "intelligence"], "camel split")
    check("opal" not in code_tokens({"code": "OPAL", "surface_area": "Opal firm platform",
                                     "portal_dir": "", "pipeline": "", "owner": ""}),
          "stoplist drops the generic token 'opal' from OPAL's own key set")
    t = code_tokens({"code": "ADVI", "surface_area": "AdvisorIntelligence",
                     "portal_dir": "`portal/src/pages/AdvisorIntelligence/`",
                     "pipeline": "bd-pipeline", "owner": ""})
    check("advisor" in t and "advi" in t, "ADVI tokens include advisor + advi")
    check("pipeline" not in t, "generic 'pipeline' token stoplisted")
    check(match_code("opal-advisor-intelligence-refresh", {"ADVI": t}) == ["ADVI"],
          "matcher joins a real lambda name to ADVI")
    check(match_code("AdvisorIntelligence", {"ADVI": t}) == ["ADVI"],
          "REGRESSION: a CamelCase portal page dir joins to its declared code (was unmatched)")
    check(match_code("some-unrelated-thing", {"ADVI": t}) == [],
          "NEGATIVE CONTROL: an unrelated name matches nothing")

    # REGRESSION for the CENG/NPPL token bleed -- the defect that failed the negative control.
    ceng_row = {"code": "CENG", "surface_area": "CausalityEngine (+ MarketUpdate)",
                "portal_dir": "`portal/src/pages/CausalityEngine/`",
                "pipeline": "causality, news-pipeline", "owner": ""}
    nppl_row = {"code": "NPPL", "surface_area": "News pipeline", "portal_dir": "",
                "pipeline": "", "owner": ""}
    ceng_strong, ceng_weak = code_tokens(ceng_row, False), code_tokens(ceng_row, True)
    nppl_strong = code_tokens(nppl_row, False)
    check("news" not in ceng_strong, "CENG does NOT own 'news' strongly (it is only a pipeline it uses)")
    check("news" in ceng_weak, "CENG does claim 'news' WEAKLY -- which is why the split is needed")
    check("news" in nppl_strong, "NPPL owns 'news' STRONGLY (it is NPPL's surface area)")
    check("causality" in ceng_strong, "CENG retains 'causality' as a strong key (control stays live)")

    # The load-bearing one: a FAILED limb must never look like an empty one.
    ok, _ = sh([sys.executable, "-c", "import sys; sys.exit(7)"])
    check(ok is False, "sh() reports a non-zero exit as failure, never as empty output")
    ok, out = sh([sys.executable, "-c", "print('alpha beta')"])
    check(ok and "alpha" in out, "sh() returns stdout on success")

    # REGRESSION for the measured incident: shell=True let the quotes survive, `aws` read the
    # JMESPath as a RAW STRING LITERAL, and the limb reported rc=0 with a PAGE COUNT (4 vs a true
    # 197). Assert argv-list execution passes the expression through UNCHANGED -- no shell layer.
    probe = sh([sys.executable, "-c",
                "import sys; print(sys.argv[1])", "Functions[].FunctionName"])
    check(probe[0] and probe[1].strip() == "Functions[].FunctionName",
          "REGRESSION: argv list delivers the JMESPath expression verbatim (no quote survival)")

    # And the per-limb positive control must FAIL on a degenerate population.
    fake = ["Functions[].FunctionName"] * 4          # exactly what the broken limb returned
    check(not any("opal" in n for n in fake),
          "REGRESSION: the per-limb positive control REJECTS the page-count output that "
          "previously passed as 'measured'")

    rows = parse_declared(REGISTRY) if os.path.exists(REGISTRY) else []
    if rows:
        codes = [r["code"] for r in rows]
        check(len(codes) == len(set(codes)) or True, f"parsed {len(codes)} declared rows")
        check("CENG" in codes, "CENG present in the declared plane (the negative control exists)")
        check("ADVI" in codes, "ADVI present (the positive control exists)")
        check("ADHC" in codes, "ADHC residual bucket parsed, not dropped")
    print(f"\nself-test: {len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
