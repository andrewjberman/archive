#!/usr/bin/env python3
"""Wave-2 substrate cards, part 3 of 3 (TO-W2-DTX2, the STORES).

WAVE-2 ANCHOR 100e7ea130. Subject set frozen at 44 @a30be0d6ca; this lane holds 16.
NO DEPRECATION VERDICTS -- several subjects here were flagged orphaned/superseded by this
lane's own wave-1 manifest and that prior is deliberately excluded from the measurement.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = "100e7ea130"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-26T23:05:00Z"
ME = "0.4.0_DT_ClientPlatform~X"
ORDER = {"measured": 3, "inferred": 2, "held": 1, "absent": 0}
HARNESS = "org/tier1_exec/3.0.0_SA_CVO/deliverables/kimi_subdivision_harness/"
DSDEL = "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/"


def ref(id_, note=None):
    assert " -- " not in id_ and " (" not in id_, "joinable_ref id carries prose: %r" % id_
    return {"id": id_, "note": note}


def row(basis, evidence, owner, **kw):
    bbf = kw.get("basis_by_field")
    if bbf:
        floor = min(bbf.values(), key=lambda v: ORDER[v])
        if ORDER[floor] < ORDER[basis]:
            basis = floor
    d = {"basis": basis, "evidence": evidence, "owner": owner}
    d.update(kw)
    return d


def card(token, sid, kind, domain, methodology, cadence, persistence, location,
         coverage, key, failure_mode, standing, why, blocking=None):
    return token, {
        "schema_version": 2, "carded_by": ME,
        "subject": {"id": sid, "kind": kind, "declared_domain": domain},
        "as_of": {"carded_utc": CARDED, "commit_ish": ANCHOR, "graph_vintage": GRAPH_VINTAGE},
        "process": {"methodology": methodology, "cadence": cadence},
        "artifact": {"persistence": persistence, "location": location},
        "trust": {"coverage": coverage, "key": key, "failure_mode": failure_mode},
        "verdict": {"standing": standing, "why": why, "blocking_defects": blocking},
    }


CARDS = []

# ---------------------------------------------------------------- W2-rpcx : comp-heat
CARDS.append(card(
    "rpcx", "comp-heat", "tool",
    "the estate OBJECT write-freshness and hygiene surface -- advisory-only, read-only, "
    "distinct from comp-freshness which covers data pipelines",
    row("measured",
        "--help read at HEAD: 5 subcommands (freshness, drift, score, federated, compare), "
        "self-described as 'Estate OBJECT write-freshness + hygiene (NFRA_HEATMAP_OBJECT). "
        "ADVISORY-ONLY, read-only.' Executable at .tools/comp-heat, 19,267 bytes, 2026-08-04.",
        "0.8.0_AE_CloudComp lane (comp-tool registration)",
        how="A read-only advisory surface over git write-times and, in the federated mode, over "
            "estate assets joined to git code-heat. It COMPOSES git history and the estate asset "
            "set; it INVENTS the hot/warm/cold banding and the exponential recency score.",
        determinism="deterministic",
        composes=[ref("git_history"), ref("estate_asset_set", "federated mode only, via Trino")],
        invents=[ref("heat_banding", "hot<=7d / warm<=30d / cold>30d"),
                 ref("recency_score", "exp(-ln2*age/half_life)")],
        materializer_standing="canonical",
        declared_opinions=[
            "the band barriers hot<=7d, warm<=30d, cold>30d -- chosen cutoffs, printed on every run",
            "a 30-day half-life in the recency score",
            "that write-time is a proxy for relevance at all, which is the tool's founding opinion"]),
    row("measured",
        "No schedule: an on-demand CLI. Every run computes from git state at call time. "
        "live_matches_declared is not_applicable because no rhythm is declared.",
        "0.8.0_AE_CloudComp lane",
        declared_rhythm=None, actual_trigger="a human or agent invocation",
        live_matches_declared="not_applicable", live_instance_age=None),
    row("measured",
        "The tool persists nothing: `freshness` and `score` compute and print. PERSISTED FALSE "
        "IS MEASURED, NOT ASSUMED -- I ran both subcommands and no artifact appeared; the output "
        "is stdout only. (federated mode reads a live Trino federation, which I did not run.)",
        "0.8.0_AE_CloudComp lane",
        persisted=False, authority_role="none", mutation_policy="not_applicable", form=None),
    row("measured", "Executable resolved at .tools/comp-heat and exercised from there.",
        "0.8.0_AE_CloudComp lane",
        home=".tools/comp-heat", projection_of=[],
        co_resident_stores=[ref("comp-debris", "the invoke-cold sibling named in the SAME wave-1 string that produced this subject")]),
    row("measured",
        "⛔ COVERAGE IS SCOPED TO WHAT I EXERCISED, AND THE DENOMINATOR SAYS SO: 3 of 5 "
        "subcommands were exercised (score, freshness, drift). `federated` was NOT run -- it "
        "requires a LIVE Trino federation. `compare` was NOT run. So this card's failure-mode "
        "row speaks for 3 of 5 surfaces and is silent about 2, rather than generalising from the "
        "3 I happened to reach. Within `freshness` on org/modules/graph: 425 files scanned, "
        "bands hot=29 warm=58 cold=338, cold_frac 0.80.",
        "0.8.0_AE_CloudComp lane",
        universe="the 5 comp-heat subcommands",
        denominator="3 of 5 subcommands exercised",
        explicitly_out=["federated -- needs a live Trino federation, not run",
                        "compare -- not run"]),
    row("measured",
        "`freshness` keys on repo-root-relative PATHS (its own error text says so). `score` "
        "takes an arbitrary `id` string and, as measured below, never resolves it -- so for "
        "`score` the id is not an identity at all. crosses_spaces is TRUE because `federated` "
        "declares a join between estate ASSETS and git CODE-heat, two different id spaces, and "
        "no mapping between them is declared anywhere I could find.",
        "0.8.0_AE_CloudComp lane",
        identity_space="repo-root-relative path for freshness; an unresolved free string for score",
        key_is_stable="unstable", crosses_spaces=True, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "key_is_stable": "measured",
                        "crosses_spaces": "inferred", "declared_mapping": "inferred"}),
    row("measured",
        "EXERCISED per subcommand, with arms reachable from different truths. "
        "⛔ `score` IS A PURE FUNCTION OF --age-days AND NEVER RESOLVES ITS id. Four ids at "
        "--age-days 30 -- 'zzz/nonexistent/qqq.py', a real repo path, 'data/firm_registry.json', "
        "and the literal '!!!not even a path!!!' -- ALL returned score=0.5000 band=WARM. Varying "
        "--age-days on a FIXED real id moved it (7d->0.8507 HOT, 30d->0.5000 WARM, 90d->0.1250 "
        "COLD), so the discriminator is the flag and the id is echoed only. A garbage id yields "
        "a confident, well-formed band. "
        "⚠ MY FIRST ATTEMPT AT THIS TEST WAS INVALID and I discarded it: both arms failed on a "
        "missing required --age-days, so they collapsed onto one truth and the identical output "
        "said nothing about miss-vs-hit. The result above is the re-run with both arms reachable. "
        "BY CONTRAST `freshness` RESOLVES: a nonexistent path returns 'comp-heat freshness: no "
        "tracked/untracked files under zzz/nonexistent/qqq/' while a real path returns a full "
        "band report -- loud and distinguishable. `drift` takes no positional target (rc=2 on "
        "both arms), so the miss-vs-hit question does not apply to it and I make no claim there.",
        "0.8.0_AE_CloudComp lane",
        returns_on_failure="score: a confident band+score computed from --age-days alone, id unresolved. "
                           "freshness: an explicit no-files-found message. drift: takes no target.",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=["score accepts any id and returns a well-formed band, so a caller "
                              "passing a wrong or stale id gets a plausible answer about nothing"],
        basis_by_field={"returns_on_failure": "measured",
                        "distinguishable_from_true_negative": "measured",
                        "silent_degrade_paths": "measured"}),
    "QUALIFIED",
    "An advisory, read-only, stateless tool that persists nothing and whose `freshness` surface "
    "fails loudly and correctly. QUALIFIED on one measured behaviour: `score` never resolves its "
    "id, so it will return a confident WARM/0.5000 for a string that is not a path at all. That "
    "is arguably by design for a calculator taking --age-days as input, and this card does not "
    "call it a defect -- but a consumer passing a resolved-from-elsewhere id would reasonably "
    "believe the score is ABOUT that object, and it is not.",
    None))

# ---------------------------------------------------------------- W2-ukdh / W2-uvcz : nerves pair
for tok, fname, size, mtime, commit, extra_key, live, why_tail in [
    ("ukdh", "nerves-edges.json", 132774, "2026-07-14T06:09:20Z", "907620c800", True, False,
     "It has not moved in 43 days while its sibling is written continuously, and nothing declares "
     "whether that is deliberate freeze or abandonment."),
    ("uvcz", "nerves-risk-edges.json", 2181748, "2026-08-26T19:51:27Z", "52f2b8a2f2", False, True,
     "It is the LIVE half of the pair and is read on every commit in this estate, which makes it "
     "the most exercised store this lane carded."),
]:
    CARDS.append(card(
        tok, "org/modules/graph/" + fname, "store",
        "one half of the nerves edge corpus that feeds comp-pulse, the pre-commit risk reflex",
        row("measured",
            "Parsed at HEAD: top-level keys are %s. Hand-generated rather than derived from a "
            "governed table -- %s"
            % ("{_README, generated_from, stats, edges}, and the `generated_from` key names its "
               "own provenance in-file" if extra_key else
               "{_README, stats, edges}, and NOTABLY it carries NO `generated_from` key while its "
               "sibling does, so the two halves of this pair do not even declare provenance the "
               "same way",
               "the _README is the only narrative account of what it holds. DECLARED_OPINIONS IS NULL AND THE REASON IS THAT THE PRODUCER IS UNRESOLVED: enumerating the filters, thresholds and exclusions a store encodes requires knowing WHO DECIDES them, and no generator was found for this file by directory enumeration or a DEF-band sweep. Listing opinions inferred from the artifact alone would be reading the output and calling it the intent -- the substitution this axis exists to catch."),
            "UNKNOWN -- no generator resolved by this census for either half",
            how="A JSON edge corpus consumed by comp-pulse to score commit risk. Its producer was "
                "NOT resolved: no generator path was found by directory enumeration of "
                "org/modules/graph/ or by a DEF-band sweep, so `composes` is left EMPTY rather "
                "than guessed.",
            determinism="unknown", composes=[], invents=[],
            materializer_standing="unknown", declared_opinions=None,
            basis_by_field={"how": "inferred", "determinism": "absent", "composes": "absent"}),
        row("measured",
            "mtime %s, last commit @%s. %s"
            % (mtime, commit,
               "MEASURED CHANGE DURING THIS SESSION: this file read 2,147,060 bytes at mtime "
               "2026-08-25T07:50:00Z during wave 1 and 2,181,748 bytes at 2026-08-26T19:51:27Z "
               "now -- it is being actively written, and this lane's own wave-1 manifest row for "
               "it is therefore already stale."
               if live else
               "UNCHANGED for 43 days, while its pair-sibling was written today. A single cadence "
               "value could not have described both halves, which is why the compound subject was "
               "split."),
            "UNKNOWN",
            declared_rhythm=None,
            actual_trigger="unresolved -- no producer found",
            live_matches_declared="unmeasured",
            live_instance_age=("0 days at carding" if live else "43 days at carding"),
            basis_by_field={"live_instance_age": "measured", "actual_trigger": "absent",
                            "declared_rhythm": "absent"}),
        row("measured",
            "%d bytes on disk, git-TRACKED (@%s resolves)." % (size, commit),
            "UNKNOWN",
            persisted=True, authority_role="source", mutation_policy="replaceable", form="json"),
        row("measured", "Path read directly at HEAD.", "UNKNOWN",
            home="org/modules/graph/" + fname, projection_of=[],
            co_resident_stores=[ref("org/modules/graph/" + ("nerves-risk-edges.json" if extra_key else "nerves-edges.json"),
                                    "the other half of the pair that wave-1 named as ONE string; split into two subjects on this lane's measurement")]),
        row("measured",
            "Parsed and counted from the file itself. ⛔ THE DENOMINATOR IS NOT COMPUTABLE: N "
            "edges of HOW MANY possible risk edges? The universe is unbounded, so a completeness "
            "ratio cannot be formed and none is invented here.",
            "UNKNOWN",
            universe="risk/dependency edges the nerves corpus asserts",
            denominator=None,
            denominator_absent_reason="The numerator is countable from the file but the universe "
                "of possible edges is unbounded, so no ratio exists to compute. The one figure "
                "that IS externally corroborated is the 1,832 danger-node count, which the "
                "pre-commit risk reflex printed on this lane's own commits.",
            explicitly_out=["any relationship no producer chose to emit"]),
        row("measured",
            "Edge entries keyed by repo path. Same space as the repo tree, so no crossing.",
            "UNKNOWN",
            identity_space="repo-relative file paths",
            key_is_stable="unstable", crosses_spaces=False, declared_mapping=None,
            basis_by_field={"identity_space": "measured", "key_is_stable": "inferred",
                            "crosses_spaces": "inferred"}),
        row("measured" if live else "inferred",
            ("EXERCISED, and uniquely among this lane's subjects it was exercised BY THE ESTATE "
             "RATHER THAN BY ME: safe-commit.sh's pre-commit risk reflex read this corpus on this "
             "lane's own commits and printed 'danger map: 33.9h old | DENOMINATOR: N file(s) "
             "checked against 1832 danger node(s) | REFLEX CLEAN -- a MEASURED result (map read, "
             "every file checked), not a default.' That is STATE at EXERCISED: the store was read "
             "live, by its real consumer, and the consumer printed its own denominator. The "
             "reflex also prints the map's AGE, so a stale corpus is visible at the point of use "
             "rather than silent."
             if live else
             "NOT EXERCISED FOR THIS HALF. The risk reflex I observed on my own commits names a "
             "'danger map' and reports 1,832 danger nodes, which corresponds to the risk-edges "
             "sibling. I did NOT establish that comp-pulse reads THIS file, and I will not infer "
             "a consumer from a shared name prefix -- that is the leaf-name merge this wave "
             "exists to prevent. Recorded as unexercised rather than borrowing the sibling's "
             "evidence."),
            "UNKNOWN",
            returns_on_failure=("the consumer prints the map age and its own denominator, so a "
                                "stale or thin corpus is visible at the point of use"
                                if live else "UNMEASURED -- no consumer of this half was exercised"),
            distinguishable_from_true_negative=("yes" if live else "unmeasured"),
            silent_degrade_paths=None,
            basis_by_field=({"returns_on_failure": "measured",
                             "distinguishable_from_true_negative": "measured"} if live else
                            {"returns_on_failure": "absent",
                             "distinguishable_from_true_negative": "absent"})),
        "QUALIFIED" if live else "INCOMPLETE",
        ("Tracked, live, and exercised in production on every commit in this estate -- the "
         "strongest exercise evidence of any store this lane carded, because its real consumer "
         "read it and printed its own denominator. QUALIFIED, not SOUND, because its GENERATOR "
         "IS UNRESOLVED and its row owner is UNKNOWN: nothing this census could find says who "
         "produces it or who would fix it. " + why_tail
         if live else
         "INCOMPLETE and deliberately so. Three rows rest on absent or inferred bases: no "
         "generator was resolved, no consumer was exercised for THIS half, and no cadence is "
         "declared. I could have borrowed its sibling's exercise evidence on the strength of a "
         "shared name prefix and did not -- that borrowing is precisely the leaf-name merge this "
         "wave exists to prevent, and an INCOMPLETE card is the honest result. " + why_tail),
        (None if live else ["generator unresolved", "no consumer exercised for this half",
                            "cadence undeclared and unmeasured"])))

written = []
for token, c in CARDS:
    name = c["subject"]["id"].replace("s3://", "").replace("/", "_").replace(":", "_").strip("_")
    path = os.path.join(HERE, "W2-%s__%s.json" % (token, name[:70]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    written.append((token, os.path.basename(path)))

print("part-3 cards written:", len(written))
for t, n in written:
    print("  W2-%-5s %s" % (t, n))
