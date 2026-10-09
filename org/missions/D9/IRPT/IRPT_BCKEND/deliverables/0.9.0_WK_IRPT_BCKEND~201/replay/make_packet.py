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
arts = cen["artifacts"] + cen["unbuilt_census_only"]
L = []
w = L.append


def short_owner(m):
    return ", ".join(o["commit"] for o in m["owner_commits"][:6]) + (" +%d" % (len(m["owner_commits"]) - 6) if len(m["owner_commits"]) > 6 else "")


w("# Never-widen sign-off packet -- IB-pr-390: release of IB-pr-385 + IB-pr-387 (`_authz/served.py` hosts) -- svc-custody-statement admitted on three routes, internal callers narrowed by their profile row")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~201 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO. Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. "
  "Files beside this packet: `IB97-3_release_census.json`, `IB97-3_release_replay.json`, `lambda-source-map.candidate.json`, `amendment1_ALL_never_admits.patch`, `replay/` (the scripts). Model: `0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`.")
w("")
w("**READ THIS FIRST -- this packet is PRE-AMENDMENT and the order is left OPEN.**")
w("")
w("1. **Amendment 1 (ALL never admits an internal caller, CTO msg 2569) is NOT in this pin.** The lane gate refused the code commit (row `IRPT_BCKEND-D2-W201-S1`, BLOCKING): "
  "`served.py` and two test files are in no order's `<paths>` until the drain. The change is written, tested and saved as `amendment1_ALL_never_admits.patch` (_authz suite: 303 passed, 1 failed -- row S3: `test_svc_custody_statement.py` is outside the grant). "
  "At this pin an internal caller whose row is the string `ALL` is still treated as unrestricted. Measured live: of 83 `opal-users-v2` profile rows, 2 carry `allowedFirmIds` -- one internal `Dev` row with a LIST of six ids that covers all four firms, and one service row `cottonwood`; **0 internal rows hold `ALL`**, so the amendment changes no live caller today. "
  "Do not sign the final pair on this pin: re-run `replay/make_census.py`, `replay/run_replay.py`, `replay/make_packet.py` at the amendment's commit.")
w("2. **A build at the real source map does not carry this change** (row S4, ARMED). All 8 functions pin `served.py` at older blobs. The artifacts below are built from `lambda-source-map.candidate.json` (8 `staged_from` rows differ) through `BAU_SOURCE_MAP_OVERRIDE`. The applier must land that restage in `lambda-source-map.json` first, or the release is a no-op that reads green.")
w("3. **`irpt-narrative` must stay OUT of the pair** (row S6, ARMED): the new `served.py` raises `TypeError` on its error path against that function's staged `errors.py`, and its live boundary is 27 `served.py` commits behind. **`irpt-holdings` has no built artifact** (row S5): the builder refuses on a parity gate that fails at the real map too.")
w("")
w("## The pin and the builds")
w("")
w("- **Release pin P: `%s`** (branch `wk-IRPT_BCKEND-201`). Code pin `dea0f53252` (box/dell2 HEAD as the worktree carries it) holds IB-pr-385 `7e0bfc3222` and IB-pr-387 `b4b544fb15`; P is the next commit, which adds the candidate map. `served.py` at P is blob `e1db29d5eb5b`." % pin)
w("- **Census of EVERY function that packages `_authz/served.py`: 8 of 8** in `lambda-source-map.json` (a token census of `served.py` in `files[]` and `staged_from` over all 229 functions): %s. The layer map carries no copy (0 hits)." % ", ".join("`%s`" % f for f in cen["functions_packaging_served_py"]))
w("- BUILD_ONLY from a clean tree (porcelain 0 lines before and after every build), each function built twice, byte-identical: **%s** (7 of 7 built). Command: `%s`. Zips kept only in scratch, removed; nothing uploaded; source map untouched." % ("YES" if cen["build_only"]["built_twice_identical_all"] else "NO", cen["build_only"]["command"]))
w("")
w("| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |")
w("|---|---|---|---|---|---|---|")
for a in arts:
    w("| `%s` | %s | %s | %s | `%s` | %d | `%s` |" % (
        a["name"], ("`%s`" % a["built_sha256"]) if a.get("built_sha256") else "NOT BUILT (row S5)", ("`%s`" % a["built_sha256_hex"][:16] + "...") if a.get("built_sha256_hex") else "-",
        a.get("built_bytes", "-"), a["live_before"], len(a["changed_members"]), ROLLBACK[a["name"]]))
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
w("`served.py` is owned by `b4b544fb15` (IB-pr-387) and `7e0bfc3222` (IB-pr-385); in 49f-reporting-read, directory-search, export-render and holdings the live blob also predates `fff1b0395a` (IB-pr-366, the served CREATE guard) and `db8161f46e` (IB-pr-357), which ride in (row S7). "
  "Grouping for the signer: **clean (served.py only):** 49f-reporting-read, directory-search, export-render. **Carry other unreleased cells:** performance-adapter (`holdings_gold.py`, `loaders.py`), status (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`), ycharts-generate (`generate_installed.py` IB-yr-761 and four added custody/holdings members). "
  "**The svc subject needs export-render (custody-report-persist, submit-export) AND ycharts-generate (analysis-requests).**")
w("")
w("## What the release does")
w("")
w("- **IB-pr-385.** `verified_internal_subject` admits ONE firm-bound service subject, `svc-custody-statement` (sub, `userType` service, edge-verified, not renderer, verified `x-firm-id` == `lookup('cottonwood')['long']` from `lib/opal_naming.py`). `Entry.handle` keeps it out of the any-firm selection and `global`, puts it on the Opal roster for its own firm only, and refuses it NOT_AUTHORIZED on every operation but `custody-report-persist`, `analysis-requests`, `submit-export`. A zip without the registry refuses it (fail closed).")
w("- **IB-pr-387.** An internal caller selecting another firm is narrowed by its profile row's `allowedFirmIds`: a non-empty list narrows; no row, no attribute or an empty list is unchanged; a non-list value or any read error is FIRM_BINDING. (At this pin a bare `ALL` is still unchanged: amendment 1, row S1.)")
w("")
w("## Writers of each changed property")
w("")
w("- **Admission of `svc-custody-statement` on the Opal roster (the property IB-pr-385 widens, for ONE named subject and ONE firm).** Writers of a request's Opal roster: 3 code sites (N=3, all read): `served.py` `Entry.handle` (`principals = frozenset([email]) if subject is not None`, the ONLY one this release changes), `_scope/custody.py:74` and `reports/generate_installed.py:158` (each rosters the verified custody principal for its own path; unchanged). Its inputs: the verified claims written by the edge authorizer (`portal-authorizer`, a signed token; the token itself is minted by the applier under the K2 mint pair `NEVER_WIDEN_PAIR_SVC_CUSTODY_STATEMENT_MINT.md`, DRAFT, not signed -- so no live token of this subject exists to admit). Both branches covered: cottonwood claim admitted, any other firm claim not admitted (replay arms below).")
w("- **A caller's selectable firms (the property IB-pr-387 narrows).** Writers of `allowedFirmIds` on a profile row: 0 code writers found in non-test code (17 files mention it; the authorizer and readers derive or read it; the rows are maintained data, not written by a Lambda in this repo) -- the rule that reads it is `Entry._internal_allowed_firms` (1 rule, read). Live rows: 83 scanned, 2 carry the attribute (above). Blast radius of the narrowing today: 0 internal callers lose a firm.")
w("")
w("## Every route this change admits (pair of admitted and another-firm-refused)")
w("")
w("Source of the route set: `docs/contracts/investor-reporting/v1/routes.json` at P -- 23 routes (21 DECLARED + 2 ROUTED_ELSEWHERE); its own `_denominator` is stale (row S2). The narrowing applies on every route, because every route runs `Entry.handle` and the narrowing fires when a caller selects a firm other than its verified one. Each route below is replayed through its HANDLER's built zip (holdings: the would-be zip). Columns: **A** = internal row `[cottonwood]` selecting cottonwood (admitted); **B** = the same caller selecting inflection (refused FIRM_BINDING built; the live zip admitted it); **C** = no-row Opal caller selecting inflection (identical built and live). svc rows: **S1** svc cottonwood claim (admitted on built, not on live); **S2** svc inflection and 49financial claims (not admitted, built and live identical); **S3** svc cottonwood selecting inflection (FIRM_BINDING).")
w("")
w("| route | operation | handler | A | B (built / live) | C | svc S1 / S2 / S3 |")
w("|---|---|---|---|---|---|---|")


def adm(c, firm):
    return c["reached_firm_check"] == firm


for p in rep["routes"]:
    if p["function"] == "irpt-narrative":
        w("| %s | %s | `%s` | EXCLUDED | EXCLUDED | EXCLUDED | - (row S6: built TypeError on the error path) |" % (p["route"], p["operation"], p["function"]))
        continue
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
    w("| %s | %s | `%s`%s | %s | %s / %s | %s | %s |" % (
        p["route"], p["operation"], p["function"], " (would-be)" if p["built_kind"] == "would_be" else "",
        "admitted" if adm(A["built"], "cottonwood") and adm(A["live"], "cottonwood") else "CHECK",
        B["built"]["code"] if B["built"]["reached_firm_check"] is None else "ADMITTED", "admitted" if B["live"]["reached_firm_check"] == "inflection" else "refused",
        "identical" if C["built"] == C["live"] else "DIFFERS", svc))
w("")
w("The non-svc `svc: UNEXPECTED` entries for `irpt-directory-search` mean the subject is not recognised at all there (its tree has no `lib/opal_naming.py`), so it is an ordinary service principal with an empty Opal roster; elsewhere it is NOT_AUTHORIZED. Tests cited as the second cover of each pair: `_authz/tests/test_svc_custody_statement.py` (23, incl. `test_svc_custody_statement_cottonwood_admitted_on_each_route`, `..._other_firm_claim_refused`) and `_authz/tests/test_allowed_firm_ids.py` (12: listed firm admitted, unlisted firm refused).")
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
w("`lib/opal_naming.py` `lookup('cottonwood')` (row D2-S26): resolves from the built tree of 6 of 8 functions, including both svc hosts (`irpt-export-render`, `irpt-ycharts-generate`); `irpt-directory-search` and `irpt-narrative` carry no `lib/opal_naming.py`, so the subject is simply not recognised there (fail closed, and neither hosts a svc route). Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in, row S7); the narrative route (row S6); a live token of the subject (none exists until the mint pair is applied).")
w("")
w("## Branch A (released)")
w("")
w("Precondition (row S4): the applier lands the candidate restage in `infra/aws/lambda/ci/lambda-source-map.json` (8 `staged_from` rows: pin `b4b544fb15...`, sha256 `e1db29d5...`; or the amendment's commit), commits, then builds from a clean tree. For each function in the signed set (recommended: every one but `irpt-narrative`; `irpt-holdings` only after the parity gate is cleared, row S5):")
w("")
w("1. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<key>.zip`, `<key>` = the function name, except 49f-reporting-read = `irpt-reporting-read-lambda`).")
w("2. The Terraform deploy path of the function's module (`infra/aws/terraform/investor-reporting/<tf file>`: %s); no IAM, route, schedule or environment change. Effect on served bytes: svc-custody-statement becomes admissible on the three routes for a cottonwood token (none exists yet); internal callers with a list row are narrowed (0 today); `served.py`'s IB-pr-366/357 changes also land." % "; ".join("`%s` %s" % (k.replace("irpt-", ""), v) for k, v in sorted(TF.items())))
w("3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.")
w("")
w("## Branch B (rolled back)")
w("")
w("Per function, redeploy the prior artifact through the same Terraform path (never a console edit): the S3 object version in the table's last column (its CodeSha256 is the `live_before` value). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest. The restage of the source map reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).")
w("")
w("## The replay arm for the applier (rerun before the ledger)")
w("")
w("From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> <pin> <out.json>` (reads the live zips and layers from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`; if the svc arm is not `expected-diff` on all 3 routes; if arm B is not refused on every counted route; if the no-row arm is not identical; or if the no-registry negative control admits the subject. Delete the scratch directory afterwards.")
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
w("`IRPT_BCKEND-D2-W201-S1` (BLOCKING: amendment 1 cannot be committed), `-S2` (the stale `_denominator` is in the contract file, not the granted path), `-S3` (BLOCKING: IB-pr-385's test collides with amendment 1), `-S4` (BLOCKING, ARMED: source map pins), `-S5` (BLOCKING: irpt-holdings parity gate), `-S6` (BLOCKING, ARMED: irpt-narrative), `-S7` (IB-pr-366/357 ride in).")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK: packet", len("\n".join(L)), "chars")
