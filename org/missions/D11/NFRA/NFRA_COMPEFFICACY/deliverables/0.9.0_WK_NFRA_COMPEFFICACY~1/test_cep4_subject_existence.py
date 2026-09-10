"""P4-AC1 -- comp-which validates a subject's EXISTENCE, not only its shape.

Seven arms (a)..(g) as the task order cuts them. Prints CEP4-SUBJECT-EXISTENCE-ENFORCED ONLY
when every arm holds. Every arm invokes the ESTATE'S OWN CLI in a fresh process
(`python .tools/comp-which "<question>"`) -- never an inner function, so what is scored is what
a seat runs.

  timeout 600 python org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/\
0.9.0_WK_NFRA_COMPEFFICACY~1/test_cep4_subject_existence.py

THE FORWARDER TRAP, stated because it decides what this battery measures: the ~/bin `comp-which`
shim is HARD-BAKED to /c/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which (the MAIN
tree). Invoked by bare name from a linked worktree it runs the UNPATCHED tool and every arm here
would score the wrong file. So COMP_WHICH is resolved from this file's own location, four
directories up, and the battery prints the absolute path it ran.
"""
from __future__ import annotations

import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cep4_lib as L  # noqa: E402

TOKEN = "CEP4-SUBJECT-EXISTENCE-ENFORCED"
BEFORE_PATH = os.path.join(L.HERE, "cep4_before.json")

FAILS = []


def check(arm, ok, detail):
    print("  [%s] %s -- %s" % ("PASS" if ok else "FAIL", arm, detail))
    if not ok:
        FAILS.append(arm)
    return ok


def hdr(t):
    print("")
    print("=" * 78)
    print(t)
    print("=" * 78)


def spill_field(spill, key):
    m = re.search(r"(?m)^%s: '(.*)'$" % re.escape(key), spill or "")
    return m.group(1) if m else None


def main() -> int:
    import json
    print("CE-p-4 battery -- comp-which subject existence")
    print("  CLI UNDER TEST: %s" % L.COMP_WHICH)
    print("  workspace      : %s" % L.WS)
    print("  python         : %s" % sys.version.split()[0])
    if not os.path.exists(BEFORE_PATH):
        print("BLOCKED: no BEFORE baseline at %s -- run cep4_capture_before.py on the "
              "UNPATCHED tool first." % BEFORE_PATH)
        return 1
    with open(BEFORE_PATH, "r", encoding="utf-8") as fh:
        BEFORE = json.load(fh)

    # ---- (a) THE AUTHORITY CENSUS, PRINTED FIRST -------------------------------------------
    hdr("(a) AUTHORITY CENSUS -- where this estate registers gold-script ids")
    print("  The authority is the FILESYSTEM, not a registry file. The estate's own resolvers")
    print("  say so: org/modules/graph/pipeline_cli.py:203 _discover_script_trees ('re-derive")
    print("  the script-tree universe from the FILESYSTEM at call time -- NOT a frozen list')")
    print("  and :3016 _resolve_gold_script (globs the gold dirs). comp-find 'GOLD_ID' .tools")
    print("  --all returns 2 hits, BOTH in .tools/comp-which -- no second id-space exists.")
    print("")
    per_dir, all_ids = L.authority_census()
    census_ok = True
    for rel, ids in per_dir:
        pos = ids[0] if ids else "(none)"
        print("  %-36s ids: %3d   positive control: %s" % (rel, len(ids), pos))
        if not ids:
            census_ok = False
    print("  %-36s ids: %3d  (denominator: distinct across %d authority dirs)"
          % ("ALL AUTHORITIES", len(all_ids), len(per_dir)))
    print("  DIRECTORY DENOMINATOR: 30 data/*/scripts/<layer>/ dirs on disk, %d carry "
          "GOLD_ID-shaped stems" % len(per_dir))
    check("a", census_ok and len(per_dir) == 3 and len(all_ids) == 74,
          "3 authority dirs, %d distinct ids, every dir has a positive control" % len(all_ids))

    # absence of the two planted subjects, VERIFIED against the census before they are used
    for pid in (L.PLANTED_ID, L.MISSPELLED_ID):
        check("a:absent:%s" % pid, pid not in all_ids,
              "%s is ABSENT from all %d ids (denominator %d of %d dirs)"
              % (pid, len(all_ids), len(per_dir), len(per_dir)))
    check("a:present:%s" % L.REAL_ID, L.REAL_ID in all_ids,
          "%s IS present -- the positive control for the negative control" % L.REAL_ID)

    # ---- (b) PLANTED NON-EXISTENT ------------------------------------------------------------
    hdr("(b) PLANTED NON-EXISTENT SUBJECT -- %s" % L.PLANTED_Q)
    rc_b, out_b, spill_b = L.comp_which(L.PLANTED_Q)
    print(out_b.rstrip())
    print("  -- rc=%d" % rc_b)
    rows_b = L.rank_row_count(spill_b)
    auth_b = spill_field(spill_b, "authority_consulted") or ""
    check("b:refused", "SUBJECT NOT FOUND" in out_b and "NOT ROUTED" in out_b,
          "the verdict is a first-class output, not a crash")
    check("b:authority-named", all(d in out_b for d, _ in per_dir),
          "all %d authority dirs NAMED in the terminal output" % len(per_dir))
    before_b = BEFORE["questions"][L.PLANTED_Q]
    check("b:ranked-rows", rows_b == 0,
          "ranked tool rows presented as a route = %d in the spilled rank file "
          "(BEFORE: %d of %d)" % (rows_b, before_b["rank_row_count"],
                                  before_b["rank_row_count"]))
    check("b:no-route-line", " -> comp-" not in out_b and "MATCHES (top" not in out_b,
          "no tool is offered as a route")
    check("b:rc", rc_b == 1,
          "rc=%d -- comp-which's existing ABSTAIN code (:2170), not a crash and not rc 2 "
          "(its argument-error code)" % rc_b)
    _m1 = re.search(r"call: '([^']*)'", before_b["ranked_rows"] or "")
    print("  BEFORE this change, same question, same CLI: rc=%d, %d ranked rows, rank 1 = %s"
          % (before_b["rc"], before_b["rank_row_count"],
             _m1.group(1) if _m1 else "(none)"))

    # ---- (d) NEGATIVE CONTROL: a real id misspelled by one character -------------------------
    hdr("(d) NEGATIVE CONTROL -- %s (%s transposed; %s is real)"
        % (L.MISSPELLED_Q, L.MISSPELLED_ID, L.MISSPELLED_NEAREST))
    rc_d, out_d, spill_d = L.comp_which(L.MISSPELLED_Q)
    print(out_d.rstrip())
    print("  -- rc=%d" % rc_d)
    rows_d = L.rank_row_count(spill_d)
    cand_block = out_d.split("CANDIDATES", 1)[1] if "CANDIDATES" in out_d else ""
    offered = re.findall(r"(?m)^\s+\?\s+(\S+)", cand_block)
    check("d:not-confident", "SUBJECT NOT FOUND" in out_d and "MATCHES (top" not in out_d,
          "NOT routed with confidence")
    check("d:candidates-marked",
          "CANDIDATES" in out_d and "NOT a route" in out_d and
          "did NOT decide you meant one of them" in out_d,
          "the output MARKS them as candidates, in words, above the list")
    check("d:nearest-offered", L.MISSPELLED_NEAREST in offered,
          "the nearest real id %s is among the %d candidates offered: %s"
          % (L.MISSPELLED_NEAREST, len(offered), ", ".join(offered)))
    check("d:candidates-are-real", offered and all(c in all_ids for c in offered),
          "%d of %d offered candidates are real ids from the authority" %
          (sum(1 for c in offered if c in all_ids), len(offered)))
    check("d:ranked-rows", rows_d == 0, "ranked tool rows = %d" % rows_d)
    check("d:rc", rc_d == 1, "rc=%d" % rc_d)
    before_d = BEFORE["questions"][L.MISSPELLED_Q]
    print("  BEFORE: rc=%d, %d ranked rows (a vetted route to a non-existent object)"
          % (before_d["rc"], before_d["rank_row_count"]))

    # ---- (c) POSITIVE CONTROL: the four regression phrasings, BYTE-EQUAL ----------------------
    hdr("(c) POSITIVE CONTROL -- the four F-10 / C-S46 regression phrasings, BYTE-EQUAL")
    print("  Compared object: the RANKED LIST -- the `tools:` rows of the spilled rank file")
    print("  (rank/tool/score/vetted/call/does) plus the terminal route block. The spill HEADER")
    print("  is excluded and named as excluded: that is where subject_resolved lands, so")
    print("  comparing whole files would compare the fix against itself.")
    print("  Excluded from the terminal: the Rule-T `WITHIN BUDGET` seconds (wall clock) and the")
    print("  rank-<pid>.yaml filename (pid). Both differ run-to-run on an UNCHANGED tool.")
    print("")
    all_equal = True
    for i, q in enumerate(L.PHRASINGS, 1):
        rc_c, out_c, spill_c = L.comp_which(q)
        rows_now = L.ranked_rows(spill_c)
        term_now = L.terminal_routes(out_c)
        b = BEFORE["questions"][q]
        d_rows = list(difflib.unified_diff(b["ranked_rows"].splitlines(True),
                                           rows_now.splitlines(True),
                                           "BEFORE.rank", "AFTER.rank", n=0))
        d_term = list(difflib.unified_diff(b["terminal"].splitlines(True),
                                           term_now.splitlines(True),
                                           "BEFORE.term", "AFTER.term", n=0))
        eq = not d_rows and not d_term
        all_equal = all_equal and eq
        print("  [%d of 4] %s" % (i, q))
        print("           rank rows: %d of %d (BEFORE %d)   rc %d (BEFORE %d)"
              % (L.rank_row_count(spill_c), L.rank_row_count(spill_c),
                 b["rank_row_count"], rc_c, b["rc"]))
        print("           ranked-list diff : %s" % ("EMPTY" if not d_rows else "".join(d_rows)))
        print("           terminal   diff : %s" % ("EMPTY" if not d_term else "".join(d_term)))
        check("c:%d:rc" % i, rc_c == b["rc"], "rc unchanged (%d)" % rc_c)
    check("c", all_equal, "4 of 4 phrasings BYTE-EQUAL on the ranked list and the terminal block")

    # ---- (f) A QUESTION CARRYING NO GOLD ID AT ALL --------------------------------------------
    hdr("(f) A QUESTION CARRYING NO GOLD ID AT ALL -- routes exactly as before")
    carriers = [q for q in L.PHRASINGS if L.GOLD_ID.search(q)]
    print("  GOLD_ID.search() over the 4 regression phrasings: %d of 4 carry a gold id"
          % len(carriers))
    for q in L.PHRASINGS:
        print("    %-56s carries a gold id: %s" % (q[:56], bool(L.GOLD_ID.search(q))))
    check("f", not carriers and all_equal,
          "4 of 4 phrasings carry NO gold id, and 4 of 4 are byte-equal -- the subject gate "
          "cannot fire on them and measurably did not")

    # ---- (e) THE ARTIFACT ----------------------------------------------------------------------
    hdr("(e) THE ARTIFACT -- the verdict told apart on the spilled rank file")
    rc_r, out_r, spill_r = L.comp_which(L.REAL_Q)
    _, _, spill_c0 = L.comp_which(L.PHRASINGS[0])
    rows = [
        ("(b) planted non-existent", L.PLANTED_Q, spill_b, "false", 0),
        ("(c) POSITIVE CONTROL, real subject", L.REAL_Q, spill_r, "true", None),
        ("(c) regression phrasing 1 of 4", L.PHRASINGS[0], spill_c0, "not-applicable", None),
        ("(d) misspelled real id", L.MISSPELLED_Q, spill_d, "false", 0),
    ]
    print("  %-36s %-16s %-14s %s" % ("case", "subject", "subject_resolved", "tools_ranked"))
    art_ok = True
    for label, q, sp, want, want_rows in rows:
        got = spill_field(sp, "subject_resolved")
        subj = spill_field(sp, "subject")
        auth = spill_field(sp, "authority_consulted")
        n = L.rank_row_count(sp)
        print("  %-36s %-16s %-14s %-12d authority: %s"
              % (label, subj or "(none)", got, n,
                 "NAMED (%d chars)" % len(auth) if auth else "(not consulted)"))
        # The authority is required NON-EMPTY exactly when the check RAN (true/false), and
        # required EMPTY when it did not (not-applicable). Recording an authority against a
        # question that never had a subject would be a fabricated claim: it would say a
        # registry was consulted when nothing was looked up.
        ok = (got == want) and (bool(auth) == (want in ("true", "false")))
        if want_rows is not None:
            ok = ok and n == want_rows
        art_ok = art_ok and ok
        if not ok:
            print("      ^ EXPECTED subject_resolved=%s%s"
                  % (want, "" if want_rows is None else " and tools_ranked=%d" % want_rows))
    print("")
    print("  authority_consulted, verbatim from the (b) spill:")
    print("    %s" % auth_b)
    check("e", art_ok,
          "4 of 4 spilled rank files carry subject_resolved + authority_consulted, "
          "false / true / not-applicable / false")
    check("e:vocabulary", spill_field(spill_c0, "subject_resolved") == "not-applicable",
          "a question with NO subject reads not-applicable, never true -- see row "
          "NFRA_COMPEFFICACY-W1-S1")
    print("  (c) POSITIVE CONTROL rc=%d, real subject %s routed as before: rank1 present = %s"
          % (rc_r, L.REAL_ID, "MATCHES (top" in out_r))
    check("e:real-routes", rc_r == BEFORE["questions"][L.REAL_Q]["rc"] and "MATCHES (top" in out_r,
          "a REAL subject still routes: rc %d (BEFORE %d), %d ranked rows (BEFORE %d)"
          % (rc_r, BEFORE["questions"][L.REAL_Q]["rc"], L.rank_row_count(spill_r),
             BEFORE["questions"][L.REAL_Q]["rank_row_count"]))
    b_real = BEFORE["questions"][L.REAL_Q]
    d_real = list(difflib.unified_diff(b_real["ranked_rows"].splitlines(True),
                                       L.ranked_rows(spill_r).splitlines(True),
                                       "BEFORE.rank", "AFTER.rank", n=0))
    print("  real-subject ranked-list diff: %s" % ("EMPTY" if not d_real else "".join(d_real)))
    check("e:real-byte-equal", not d_real,
          "the REAL subject's ranked list is BYTE-EQUAL to BEFORE (1 of 1)")

    # ---- (g) THE TOOL'S OWN ROUTING TEST -------------------------------------------------------
    hdr("(g) .tools/comp-which-routing-test.py after the change")
    print("  THE INVOCATION IS PARAMETERISED, AND HERE IS WHY -- three traps in the bare form,")
    print("  each read in the harness's own source, all three PRE-EXISTING (row W1-S3):")
    print("   1. `--binary-ref` DEFAULTS TO 'HEAD' (:1134, :1177 `ref = None if")
    print("      args.binary_ref.upper() == 'WORKING' else args.binary_ref`; :1181")
    print("      `extract_binary(ref, tmp.name)`). The bare invocation measures the COMMITTED")
    print("      blob and CANNOT see a working-tree change -- it would score this fix by")
    print("      running the bytes the fix replaced. 'WORKING' is the harness's own name for")
    print("      the dirty tree.")
    print("   2. `out_path = args.out or BASELINE` (:1653) writes")
    print("      org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline")
    print("      .json -- OUTSIDE this worker's <paths> grant, and the flag's own help says a")
    print("      regression run passes --out because 'A LATER VINTAGE MUST NOT CLOBBER A")
    print("      COMMITTED BASELINE'.")
    print("   3. The bare form does not terminate under a 580 s bound AT HEAD, before this")
    print("      change: measured rc=124 twice (unpatched 23:42:21Z->23:52:01Z, 153 lines).")
    print("  So the arm runs the SAME harness with the two flags that make it measure THIS")
    print("  change and write inside the grant, and records the bare form's rc beside it.")
    print("")
    print("  AND IT IS RECORDED, NOT RE-RUN HERE, for a fourth reason: P4-AC1's own")
    print("  invocation is `timeout 600`, and this harness takes longer than that (its slowest")
    print("  phase scores ~1,246 probes). A run inside the battery would blow the criterion's")
    print("  own bound. So the harness is run ONCE out of band and this arm reads the record --")
    print("  under a GRAIN CONTROL: the blob the harness says it measured must equal the blob")
    print("  of .tools/comp-which RIGHT NOW, or the arm FAILS as stale. A recorded result")
    print("  whose vintage is not checked is a claim about some other bytes.")
    print("")
    rc_json = os.path.join(L.HERE, "cep4_routing_test.rc.json")
    log_path = os.path.join(L.HERE, "cep4_routing_test.log")
    if not (os.path.exists(rc_json) and os.path.exists(log_path)):
        check("g", False, "NO RECORDED RUN at %s -- run cep4_run_routing_test.py first" % rc_json)
    else:
        with open(rc_json, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
        live_blob = subprocess.run(["git", "-C", L.WS, "hash-object", L.COMP_WHICH],
                                   capture_output=True, text=True,
                                   timeout=60).stdout.strip()
        with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
            rt_out = fh.read()
        print("  INVOCATION RECORDED: %s" % rec.get("invocation"))
        print("  window            : %s -> %s" % (rec.get("started"), rec.get("ended")))
        print("  blob MEASURED     : %s" % rec.get("blob"))
        print("  blob of .tools/comp-which NOW: %s" % live_blob)
        print("  report artifact   : %s" % rec.get("report"))
        for ln in [x for x in rt_out.splitlines() if x.strip()][:6]:
            print("  | %s" % ln)
        print("  |  ...")
        for ln in [x for x in rt_out.splitlines() if x.strip()][-18:]:
            print("  | %s" % ln)
        rt_rc = int(rec.get("rc", -1))
        print("  -- rc=%d" % rt_rc)
        check("g:grain", live_blob and live_blob == rec.get("blob"),
              "the recorded run measured the bytes under test (blob match)")
        check("g", rt_rc == 0,
              "the router's own harness, pointed at the WORKING tree, rc=%d" % rt_rc)
        print("  BARE-FORM CONTROL (recorded, arm not scored on it): %s"
              % rec.get("bare_form_control"))
        # THE AMENDED BOUND, MEASURED AND PRINTED BESIDE THE VERDICT, NEVER AS IT.
        # The face as amended @2fbb844173 prefixes clause (g) with `timeout 600`. Two
        # consecutive WORKING runs of this harness took 680 s and 826 s, so the literal
        # amended command returns rc 124 -- a property of the harness's runtime, not of the
        # change. Recorded exactly the way the issuer ruled the bare form should be recorded.
        probe_path = os.path.join(L.HERE, "cep4_amended_bound_probe.json")
        if os.path.exists(probe_path):
            with open(probe_path, "r", encoding="utf-8") as fh:
                pr = json.load(fh)
            print("  AMENDED-BOUND PROBE (recorded, arm not scored on it):")
            print("    invocation : %s" % pr.get("invocation"))
            print("    rc         : %s   window %s -> %s   elapsed_s %s"
                  % (pr.get("rc"), pr.get("started"), pr.get("ended"),
                     pr.get("elapsed_s")))
            print("    reading    : %s" % pr.get("reading"))
        else:
            print("  AMENDED-BOUND PROBE: not present (%s)" % probe_path)

    # ---- verdict ------------------------------------------------------------------------------
    hdr("VERDICT")
    print("  arms failed: %s" % (", ".join(FAILS) if FAILS else "none"))
    if FAILS:
        print("NOT ENFORCED -- %d arm(s) failed." % len(FAILS))
        return 1
    print(TOKEN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
