"""IB-pr-390 packet writer: renders NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md from IB97-3_release_census.json and
IB97-3_release_replay.json (re-run after the census and replay are re-run at a new pin). ASCII only.
    python replay/make_packet.py <deliverables_dir>
"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
cen = json.loads((D / "IB97-3_release_census.json").read_text(encoding="utf-8"))
rep = json.loads((D / "IB97-3_release_replay.json").read_text(encoding="utf-8"))
ROLLBACK = {  # S3 version holding each live zip, read 2026-10-09 (content-sha256 metadata == live CodeSha256, IsLatest)
    "irpt-49f-reporting-read-lambda": "fvLqMaaeFSi6ZarBY7IjcfEWWmVllVX8",
    "irpt-directory-search": "7L6kC0.B6Z2viqOJPKYrX86pVYngSWTn",
    "irpt-export-render": "QK8IR0k6Ek7HmbMvA.GqjpfTGNKmDKdi",
    "irpt-holdings": "GbQOO4bhv7LjZ0kiUVyc5V4TSDK85GNZ",
    "irpt-narrative": "ELQQZdHYUJHbDZSOxC2AAKQ_nXFqApoJ",
    "irpt-performance-adapter": "5nyq8P6vP8ZC7tceMqvLoKTl4F.1MvRP",
    "irpt-status": "Ji6C92YJzsOWQtvO0fJkTV2yYhqfE2bx",
    "irpt-ycharts-generate": "VWdbar2YhmyNzR1BT0VkLo1c.nc2E3Gf",
}
S3KEY = {"irpt-49f-reporting-read-lambda": "irpt-reporting-read-lambda"}
TF = {"irpt-49f-reporting-read-lambda": "reporting-read/lambda.tf", "irpt-directory-search": "directory/lambda.tf",
      "irpt-export-render": "export/lambda.tf", "irpt-holdings": "holdings/lambda.tf", "irpt-narrative": "narrative/lambda.tf",
      "irpt-performance-adapter": "performance/lambda.tf", "irpt-status": "ops/lambda.tf", "irpt-ycharts-generate": "ycharts/generate.tf"}
pin = cen["pin"]
arts = cen["artifacts"]
HELD = cen["held_out"]
L = []
w = L.append


def short_owner(m):
    return ", ".join(o["commit"] for o in m["owner_commits"][:6]) + (" +%d" % (len(m["owner_commits"]) - 6) if len(m["owner_commits"]) > 6 else "")


w("# Never-widen sign-off packet -- IB-pr-390: release of IB-pr-385 + IB-pr-387 (`_authz/served.py` hosts) -- svc-custody-statement admitted on three routes, internal callers narrowed by their profile row")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~201 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. "
  "Files beside this packet: `IB97-3_release_census.json`, `IB97-3_release_replay.json`, `replay/` (the scripts). `lambda-source-map.candidate.json` and `amendment1_ALL_never_admits.patch` are SUPERSEDED history of the pre-amendment packet (the patch is now committed; the real map is restaged; no candidate map is used). Model: `0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`.")
w("")
w("**READ THIS FIRST -- this packet is AMENDMENT 1 (issuer 2.0.0_SA_COO~P2, CTO msg 2569) and releases 6 of the 8 `served.py` hosts.**")
w("")
w("1. **ALL never admits an internal caller, and it is in this pin.** A profile `allowedFirmIds` equal to the string `ALL`, or a list holding `ALL`, is refused FIRM_BINDING at the internal narrowing step (code commit `%s`, `_authz` suite 304 passed). Measured live 2026-10-09 (the pre-amendment packet): of 83 `opal-users-v2` profile rows, 2 carry `allowedFirmIds` -- one internal `Dev` row with a LIST of six ids that covers all four firms, and one service row `cottonwood`; **0 internal rows hold `ALL`**, so the change refuses no live caller today." % cen["code_pin"][:10])
w("2. **The real source map carries the change.** `served.py`'s staged row of each released host pins `%s` (restage commit `c2bb612234`); the artifacts below are built at the REAL `lambda-source-map.json`, no candidate map, no override." % cen["code_pin"][:10])
w("3. **HELD OUT, not in this pair: `irpt-holdings` (row S5) and `irpt-narrative` (row S6); their source-map rows are NOT restaged.** Every route they serve is **NOT YET NARROWED** -- see the section below, which names the follow-up cell.")
w("")
w("## The pin and the builds")
w("")
w("- **Release pin P (census pin): `%s`** (branch `wk-IRPT_BCKEND-201`). **Code pin `%s`** (the commit that adds ALL-never-admits to `served.py`; it sits on IB-pr-385 `7e0bfc3222` and IB-pr-387 `b4b544fb15`). P is two commits on: the restage `c2bb612234` and the routes.json denominator `71e9aacf27`. `served.py` at the code pin is blob `87d9ecc49747`." % (pin, cen["code_pin"][:10]))
w("- **Census: the 6 RELEASED hosts of the 8 that package `_authz/served.py`** (a token census of `served.py` in `files[]` and `staged_from` over all 229 functions found 8; the layer map carries no copy): %s. Held out, with their rows: %s. The layer map carries no copy (0 hits)." % (", ".join("`%s`" % f for f in cen["functions_packaging_served_py"]), "; ".join("`%s` -- %s" % (k, v) for k, v in HELD.items())))
w("- BUILD_ONLY from a clean tree (porcelain 0 lines before and after every build), each function built twice, byte-identical: **%s** (%d of %d built). Command: `%s`. Zips kept only in scratch, removed; nothing uploaded; source map untouched." % ("YES" if cen["build_only"]["built_twice_identical_all"] else "NO", len(arts), len(cen["functions_packaging_served_py"]), cen["build_only"]["command"]))
w("")
w("| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |")
w("|---|---|---|---|---|---|---|")
for a in arts:
    w("| `%s` | %s | %s | %s | `%s` | %d | `%s` |" % (
        a["name"], "`%s`" % a["built_sha256"], "`%s`" % a["built_sha256_hex"][:16] + "...",
        a["built_bytes"], a["live_before"], len(a["changed_members"]), ROLLBACK[a["name"]]))
w("")
w("`live_before` = `aws lambda get-function-configuration` CodeSha256, read 2026-10-09; each equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip`, which is the rollback version in the last column.")
w("")
w("## Changed members and their owners (every one owned)")
w("")
for a in arts:
    w("**`%s`** -- %s" % (a["name"], "; ".join(a["census_summary"])))
    for m in a["changed_members"]:
        w("- %s `%s` (built `%s`, live `%s`): %s" % (m["status"], m["member"], m["built_sha256_prefix"], m["live_sha256_prefix"], short_owner(m) if m["owner_commits"] else m["owner_commit"]))
    w("")
w("`served.py` is owned by `%s` (ALL never admits, this amendment), `b4b544fb15` (IB-pr-387) and `7e0bfc3222` (IB-pr-385); in 49f-reporting-read and directory-search and export-render the live blob also predates `fff1b0395a` (IB-pr-366, the served CREATE guard) and `db8161f46e` (IB-pr-357), which ride in (row S7). "
  "Grouping for the signer: **clean (served.py only):** 49f-reporting-read, directory-search, export-render. **Carry other unreleased cells:** performance-adapter (`holdings_gold.py`, `loaders.py`), status (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`), ycharts-generate (`generate_installed.py` IB-yr-761 and four added custody/holdings members). "
  "**The svc subject needs export-render (custody-report-persist, submit-export) AND ycharts-generate (analysis-requests).**" % cen["code_pin"][:10])
w("")
w("## What the release does")
w("")
w("- **IB-pr-385.** `verified_internal_subject` admits ONE firm-bound service subject, `svc-custody-statement` (sub, `userType` service, edge-verified, not renderer, verified `x-firm-id` == `lookup('cottonwood')['long']` from `lib/opal_naming.py`). `Entry.handle` keeps it out of the any-firm selection and `global`, puts it on the Opal roster for its own firm only, and refuses it NOT_AUTHORIZED on every operation but `custody-report-persist`, `analysis-requests`, `submit-export`. A zip without the registry refuses it (fail closed).")
w("- **IB-pr-387.** An internal caller selecting another firm is narrowed by its profile row's `allowedFirmIds`: a non-empty list narrows; no row, no attribute or an empty list is unchanged; a non-list value or any read error is FIRM_BINDING. **Amendment 1: `ALL` (the string, or a list member) is a FIRM_BINDING refusal, never an unrestricted spelling.**")
w("")
w("## Writers of each changed property")
w("")
w("- **Admission of `svc-custody-statement` on the Opal roster (the property IB-pr-385 widens, for ONE named subject and ONE firm).** Writers of a request's Opal roster: 3 code sites (N=3, all read): `served.py` `Entry.handle` (`principals = frozenset([email]) if subject is not None`, the ONLY one this release changes), `_scope/custody.py:74` and `reports/generate_installed.py:158` (each rosters the verified custody principal for its own path; unchanged). Its inputs: the verified claims written by the edge authorizer (`portal-authorizer`, a signed token; the token itself is minted by the applier under the K2 mint pair `NEVER_WIDEN_PAIR_SVC_CUSTODY_STATEMENT_MINT.md`, DRAFT, not signed -- so no live token of this subject exists to admit). Both branches covered: cottonwood claim admitted, any other firm claim not admitted (replay arms below).")
w("- **A caller's selectable firms (the property IB-pr-387 narrows).** Writers of `allowedFirmIds` on a profile row: 0 code writers found in non-test code (17 files mention it; the authorizer and readers derive or read it; the rows are maintained data, not written by a Lambda in this repo) -- the rule that reads it is `Entry._internal_allowed_firms` (1 rule, read). Live rows: 83 scanned, 2 carry the attribute (above). Blast radius of the narrowing today: 0 internal callers lose a firm.")
w("")
w("## Every route this change admits (pair of admitted and another-firm-refused)")
w("")
w("Source of the route set: `docs/contracts/investor-reporting/v1/routes.json` at P -- 23 routes (21 DECLARED + 2 ROUTED_ELSEWHERE); its `_denominator` now reads declared 21, routed_elsewhere 2, total 23 (row S2 fixed, `71e9aacf27`, no route changed). **21 of the 23 are replayed below (the 6 released hosts); the other 2 are the held-out hosts' and are listed as NOT YET NARROWED.** The narrowing applies on every route, because every route runs `Entry.handle` and the narrowing fires when a caller selects a firm other than its verified one. Each route below is replayed through its HANDLER's built zip. Columns: **A** = internal row `[cottonwood]` selecting cottonwood (admitted); **B** = the same caller selecting inflection (refused FIRM_BINDING built; the live zip admitted it); **C** = no-row Opal caller selecting inflection (identical built and live); **ALL** = internal caller whose row is the string `ALL` / a list holding `ALL`, selecting inflection (refused FIRM_BINDING built). svc rows: **S1** svc cottonwood claim (admitted on built, not on live); **S2** svc inflection and 49financial claims (not admitted, built and live identical); **S3** svc cottonwood selecting inflection (FIRM_BINDING).")
w("")
w("| route | operation | handler | A | B (built / live) | C | ALL (str / list, built) | svc S1 / S2 / S3 |")
w("|---|---|---|---|---|---|---|---|")


def adm(c, firm):
    return c["reached_firm_check"] == firm


for p in rep["routes"]:
    A = p["internal_row_cottonwood_selecting_cottonwood"]
    B = p["internal_row_cottonwood_selecting_inflection"]
    C = p["internal_no_row_selecting_inflection"]
    if "svcCot" in p["svc"]:
        s = p["svc"]
        svc = "S1 %s/%s; S2 %s; S3 %s" % (
            "built admitted" if "svc-custody-statement" in (s["svcCot"]["built"]["roster"] or []) else "built NOT admitted",
            "live refused" if "svc-custody-statement" not in (s["svcCot"]["live"]["roster"] or []) else "live admitted",
            "not admitted (equal built/live)" if s["svcInf"]["built"] == s["svcInf"]["live"] and s["svc49"]["built"] == s["svc49"]["live"] else "DIFFERS",
            s["svcCotSel"]["built"]["code"])
    else:
        svc = "n/a (svc: %s)" % p["svc"]["svcOther"]["built"]["code"]
    AS, AL = p["internal_row_ALL_string_selecting_inflection"]["built"], p["internal_row_ALL_list_selecting_inflection"]["built"]
    allc = "%s / %s" % (AS["code"] if AS["reached_firm_check"] is None else "ADMITTED", AL["code"] if AL["reached_firm_check"] is None else "ADMITTED")
    w("| %s | %s | `%s` | %s | %s / %s | %s | %s | %s |" % (
        p["route"], p["operation"], p["function"],
        "admitted" if adm(A["built"], "cottonwood") and adm(A["live"], "cottonwood") else "CHECK",
        B["built"]["code"] if B["built"]["reached_firm_check"] is None else "ADMITTED", "admitted" if B["live"]["reached_firm_check"] == "inflection" else "refused",
        "identical" if C["built"] == C["live"] else "DIFFERS", allc, svc))
w("")
w("The non-svc `svc: UNEXPECTED` entries for `irpt-directory-search` mean the subject is not recognised at all there (its tree has no `lib/opal_naming.py`), so it is an ordinary service principal with an empty Opal roster; elsewhere it is NOT_AUTHORIZED. Tests cited as the second cover of each pair: `_authz/tests/test_svc_custody_statement.py` (23, incl. `test_svc_custody_statement_cottonwood_admitted_on_each_route`, `..._other_firm_claim_refused`) and `_authz/tests/test_allowed_firm_ids.py` (12: listed firm admitted, unlisted firm refused).")
w("")
w("## NOT YET NARROWED -- the routes of the two held-out hosts")
w("")
w("`irpt-holdings` and `irpt-narrative` are NOT in this release (their source-map rows are not restaged, nothing here builds or replays them). **Until they are released, an internal caller selecting another firm on these routes is NOT narrowed by its profile row and the svc subject is not admitted there:**")
w("")
w("| route | operation | handler | status | why held out |")
w("|---|---|---|---|---|")
for h in rep["held_out_routes_not_replayed"]:
    w("| %s | %s | `%s` | **NOT YET NARROWED** | %s |" % (h["route"], h["operation"], h["function"], HELD[h["function"]]))
w("")
w("**Follow-up cell: none is cut at this pin** (decomposition section 90 carries IB-pr-390 and IB-pr-391 only). It is for the issuer 2.0.0_SA_COO~P2 to cut, one cell for both hosts or one per host: (a) `irpt-holdings` -- clear the ADHC_DRIFTD.002 parity gate (`holdings_publication_port.py` is in `source_dir` and not in `files[]`), then restage `served.py` at the code pin and build/replay/sign; (b) `irpt-narrative` -- restage its `errors.py` to one carrying `public_line(admitted=)` (and its 27 `served.py` commits of drift), then the same. Rows `IRPT_BCKEND-D2-W201-S5` and `-S6` are the evidence.")
w("")
w("## The replay (offline; live versus built artifacts; `IB97-3_release_replay.json`)")
w("")
w("The replay drives the real `served.Entry.handle` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layers extracted beside it), with the profile row injected and `enforcer_for` stubbed: **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the Opal roster; **refused** = a FIRM_BINDING / NOT_AUTHORIZED reply, or the subject absent from the roster (the real enforcer and the persist writer then refuse a non-Opal principal; the stub does not run them). `UNEXPECTED` in a record is the stub's own stop after admission.")
w("")
w("| arm | verdict | negative control | detail |")
w("|---|---|---|---|")
for a in rep["arms"]:
    w("| %s | %s | %s | %s |" % (a["name"], a["verdict"], "yes" if a["negative_control"] else "no", a["detail"].replace("|", "/")))
w("")
w("`lib/opal_naming.py` `lookup('cottonwood')` (row D2-S26): resolves from the built tree of 5 of the 6 released functions, including both svc hosts (`irpt-export-render`, `irpt-ycharts-generate`); `irpt-directory-search` carries no `lib/opal_naming.py`, so the subject is simply not recognised there (fail closed, and it hosts no svc route). Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in, row S7); the two held-out hosts' routes; a live token of the subject (none exists until the mint pair is applied).")
w("")
w("## Branch A (released)")
w("")
w("Precondition: none to restage -- the real map already pins `%s` for the 6 released hosts (commit `c2bb612234`); the applier does not restage. Build from a clean tree at P or a descendant. For each of the 6 functions in the signed set (`irpt-holdings` and `irpt-narrative` are NOT in it):" % cen["code_pin"][:10])
w("")
w("1. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<key>.zip`, `<key>` = the function name, except 49f-reporting-read = `irpt-reporting-read-lambda`).")
w("2. The Terraform deploy path of the function's module (`infra/aws/terraform/investor-reporting/<tf file>`: %s); no IAM, route, schedule or environment change. Effect on served bytes: svc-custody-statement becomes admissible on the three routes for a cottonwood token (none exists yet); internal callers with a list row are narrowed and an `ALL` row is refused (0 such rows today); `served.py`'s IB-pr-366/357 changes also land." % "; ".join("`%s` %s" % (k.replace("irpt-", ""), v) for k, v in sorted(TF.items()) if k in cen["functions_packaging_served_py"]))
w("3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.")
w("")
w("## Branch B (rolled back)")
w("")
w("Per function, redeploy the prior artifact through the same Terraform path (never a console edit): the S3 object version in the table's last column (its CodeSha256 is the `live_before` value). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest. The restage of the source map reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).")
w("")
w("## The replay arm for the applier (rerun before the ledger)")
w("")
w("From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> <pin> <out.json>` (reads the live zips and layers from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`; if the svc arm is not `expected-diff` on all 3 routes; if arm B or the ALL arm is not refused on every counted route; if the no-row arm is not identical; or if the no-registry negative control admits the subject. Delete the scratch directory afterwards.")
w("")
w("## The after-read")
w("")
w("One live `svc-custody-statement` persist read, and one internal caller's narrowed read, after the apply:")
w("")
w("1. **svc persist (refusal-or-admission).** The applier, holding the minted token (K2 mint pair; not yet applied), POSTs `/api/scoped/investor-reporting/custody-report` once with a cottonwood-bound body. Expected: admitted to the writer (status per the writer's contract); a body bound to another firm: refused. If the token does not exist yet, this read is UNEXERCISED -- say so; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.")
w("2. **Internal caller, narrowed.** Use an existing internal caller whose profile row carries a non-empty list and select a firm outside it: expected FIRM_BINDING. Measured today: the only internal row with a list covers all four firms, so no such caller exists; the read is then the unrestricted arm (the same caller selecting a listed firm still reads through) and the narrowing stays UNEXERCISED live. Do not write a profile row to make one: that is a WORLD write this packet does not ask for.")
w("")
w("## Rows")
w("")
w("Dispositioned by AMENDMENT 1: `IRPT_BCKEND-D2-W201-S1` (amendment code committed, `%s`), `-S2` (routes.json denominator fixed, `71e9aacf27`), `-S3` (svc test fixture re-pointed to a no-row caller, same code commit), `-S4` (source map restaged, `c2bb612234`). Still open and ARMED: `-S5` (irpt-holdings parity gate) and `-S6` (irpt-narrative errors.py) -- both held out; `-S7` (IB-pr-366/357 ride in)." % cen["code_pin"][:10])
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK: packet", len("\n".join(L)), "chars")
