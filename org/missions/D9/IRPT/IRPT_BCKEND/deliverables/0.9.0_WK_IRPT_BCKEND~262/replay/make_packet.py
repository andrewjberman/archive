"""IB-pr-394 packet writer (modelled on IB-pr-390's): renders NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md from
IB99-1_release_census.json and IB99-1_release_replay.json. ASCII only.
    python <this file> <deliverables_dir>
"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
cen = json.loads((D / "IB99-1_release_census.json").read_text(encoding="utf-8"))
rep = json.loads((D / "IB99-1_release_replay.json").read_text(encoding="utf-8"))
pin = cen["pin"]
arts = {a["name"]: a for a in cen["artifacts"]}
TF = {"irpt-narrative": "infra/aws/terraform/investor-reporting/narrative/lambda.tf",
      "irpt-holdings": "infra/aws/terraform/investor-reporting/holdings/lambda.tf"}
L = []
w = L.append


def owners(m):
    return ", ".join(o["commit"] for o in m["owner_commits"][:6]) + (" +%d" % (len(m["owner_commits"]) - 6) if len(m["owner_commits"]) > 6 else "")


w("# Never-widen sign-off packet -- IB-pr-394: the two hosts IB-pr-390 held out -- irpt-narrative (TypeError on the served error path) and irpt-holdings (ADHC_DRIFTD.002 parity gate)")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~262 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 2690 via ~V2 msg 2691; rows `IRPT_BCKEND-D2-W201-S5`, `-S6`). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. "
  "Files beside this packet: `IB99-1_release_census.json`, `IB99-1_release_replay.json`, `replay/` (the scripts). Model: `0.9.0_WK_IRPT_BCKEND~201/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-390.md`.")
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **Unlike IB-pr-390, the artifacts below are built at the REAL source map** (`infra/aws/lambda/ci/lambda-source-map.json` at the pin, no `BAU_SOURCE_MAP_OVERRIDE`): both hosts' `served.py` rows are restaged in this cell, so a build at HEAD carries the change. Compare the printed sha256 to the table before any upload.")
w("2. **irpt-holdings is a small release** (2 changed members: `served.py` and the registered `holdings_publication_port.py`). **irpt-narrative is a wide one** (22 changed members, 8 of them added; live runs a boundary 28 `served.py` commits old). The release of narrative also **adds internal firm selection to a function whose live boundary does not honour it** (replay arm below, row `IRPT_BCKEND-D2-W262-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2). The signer can sign holdings alone: the two functions release independently.")
w("")
w("## Root cause and fix, per host")
w("")
w("- **irpt-narrative (row W201-S6).** The shared `_authz/served.py` calls `errors.public_line(..., admitted=BOUNDARY_REASONS)` in `_record`, at every error site. The `admitted` keyword exists in `_authz/errors.py` from `4fffe13f01`; narrative staged `errors.py` at `bc3727b3a3` (blob `784ee313ed70`), which does not take it, so every refusal that records an internal error raised TypeError. "
  "**Fix: restage narrative's `errors.py` row to `%s` (blob `b60f25ccaa70`, the current one) and its `served.py` row to the same pin (blob `87d9ecc49747`, IB-pr-390's).** The smaller change: two staged rows of ONE function, against editing the shared `served.py` (which moves the bytes of all 8 hosts, 6 of them already restaged and released under IB-pr-390) or restaging all 21 members. No other host's bytes move: every other function's `errors.py` row is untouched (holdings' is already the current blob). "
  "Tests: `narrative/tests/test_served_error_path.py`, 4 tests (`-k served_error_path`): an internal caller and a service caller each reach the error site of the real `entry.ENTRY` in a flat `python -I` tree built the way the builder builds it (staged blobs read at their pin, sha256-verified) and each get the staged `errors.py` public line and a refusal envelope, no TypeError; the staged `errors.py` takes `admitted`; and a negative control puts the old blob back and must see TypeError." % pin[:10])
w("- **irpt-holdings (row W201-S5).** `holdings/holdings_publication_port.py` (added by `73075a9048`, IB-m35-351) is in `source_dir` and not in `files[]`, so the ADHC_DRIFTD.002 parity gate refused every BUILD_ONLY. **Fix: `holdings_publication_port.py` added to holdings' `files[]` (owned by `73075a9048`),** and holdings' `served.py` row restaged to `%s` (blob `87d9ecc49747`). The member is then in the zip, as it is in `irpt-ycharts-generate`'s, which already registers it." % pin[:10])
w("")
w("## The pin and the builds")
w("")
w("- **Release pin P: `%s`** (branch `wk-IRPT_BCKEND-262`): the commit that holds both restages, the `files[]` member and the narrative tests. `served.py` at P is blob `87d9ecc49747` (IB-pr-390's code commit `74a62fb46c`).")
w("- Census: `infra/aws/lambda/ci/release-census.py <function> --pin P` for each of the two functions, live zip read from AWS (read only), diffed by member and sha256.")
w("- BUILD_ONLY from a clean tree (porcelain %d lines before and after every build), each function built twice, byte-identical: **%s** (2 of 2 built). Command: `%s`. Zips kept only in scratch; nothing uploaded; source map untouched." % (
    cen["build_only"]["porcelain_lines_before"], "YES" if cen["build_only"]["built_twice_identical_all"] else "NO", cen["build_only"]["command"]))
w("")
w("| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |")
w("|---|---|---|---|---|---|---|")
for a in cen["artifacts"]:
    w("| `%s` | `%s` | `%s`... | %s | `%s` | %d | `%s` |" % (a["name"], a["built_sha256"], a["built_sha256_hex"][:16], a["built_bytes"], a["live_before"],
                                                      len(a["changed_members"]), a["s3_rollback_version"]))
w("")
w("`live_before` = `aws lambda get-function-configuration` CodeSha256, read 2026-10-09; each equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip` (checked: %s), which is the rollback version in the last column." % (
    ", ".join("%s %s" % (a["name"], "yes" if a["s3_is_live_zip"] else "NO") for a in cen["artifacts"])))
w("")
w("## Changed members and their owners (every one owned)")
w("")
for a in cen["artifacts"]:
    w("**`%s`** -- %s" % (a["name"], "; ".join(a["census_summary"])))
    for m in a["changed_members"]:
        w("- %s `%s` (built `%s`, live `%s`): %s" % (m["status"], m["member"], m["built_sha256_prefix"], m["live_sha256_prefix"], owners(m) if m["owner_commits"] else m["owner_commit"]))
    w("")
w("Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). `served.py`'s owner list is IB-pr-390's code commit `74a62fb46c` first; the rest are the earlier `served.py` commits live narrative predates (28) / live holdings predates (5), including IB-pr-385/387 (the svc subject and the profile-row narrowing), IB-pr-366 and IB-pr-357. "
  "Narrative's `errors.py` is owned by `4fffe13f01`; holdings' `holdings_publication_port.py` by `73075a9048`. Narrative's other 20 members are the map's existing staged pins and source files, which no cell of this order changes; they release with it because live narrative was last built 2026-09-21.")
w("")
w("## Writers of the changed property")
w("")
w("- **The firm an internal caller's request is bound to (the property narrative's release widens: from the caller's own firm to a firm it selects).** Writers of the bound firm in `served.py`: **N=2**, both read: `verified = header(headers, 'X-Firm-Id')` (the edge-verified claim, unchanged) and `verified = selected` after the selection checks (internal caller only; `bucket_for(selected)` must accept it; a service principal needs its row's `allowedFirmIds`; an internal caller is narrowed by its profile row, and a bare `ALL` never admits, CTO msg 2569). Both branches are covered in the replay: with a row, narrowed; with NO row, any registered firm (the IB-pr-387 \"no row = unchanged\" rule) -- and on narrative that is NEW, because the live boundary never honoured `selected_tenant`.")
w("- **The Opal roster handed to `enforcer_for`:** 3 writers (N=3: `Entry.handle` and the two custody paths), only `Entry.handle` is in these zips and it is unchanged by this cell.")
w("")
w("## Every route of the two hosts: admitted and another-firm-refused")
w("")
w("Route set: `docs/contracts/investor-reporting/v1/routes.json` at P, handlers `irpt-narrative` and `irpt-holdings`: 2 routes (1 each). Columns -- **U-own** a plain firm user (x-firm-id cottonwood) with no selection: admitted for its own firm; **U-other** the same user selecting inflection: refused; **U-claim** the same user restating firm_id=inflection: refused; **A** an Opal internal caller with profile row `[cottonwood]` selecting cottonwood: admitted; **B** that caller selecting inflection: refused; **C** an unrelated Opal internal caller with no row, selecting inflection (built / live); **S** svc-custody-statement on the route's operation.")
w("")
w("| route | operation | handler | U-own | U-other (refused) | U-claim (refused) | A (built / live) | B (built / live) | C (built / live) | S |")
w("|---|---|---|---|---|---|---|---|---|---|")
for p in rep["routes"]:
    def bd(c):
        return "bound %s" % c["reached_firm_check"] if c["reached_firm_check"] else c["code"]
    w("| %s | %s | `%s` | admitted (%s) | %s (live: %s) | %s | %s / %s | %s / %s | %s / %s | %s |" % (
        p["route"], p["operation"], p["function"], p["userOwn"]["built"]["reached_firm_check"],
        "refused " + p["userSelOther"]["built"]["code"], bd(p["userSelOther"]["live"]),
        "refused " + p["userClaimOther"]["built"]["code"],
        "admitted " + str(p["rowCotCot"]["built"]["reached_firm_check"]), bd(p["rowCotCot"]["live"]),
        "refused " + p["rowCotInf"]["built"]["code"], bd(p["rowCotInf"]["live"]),
        bd(p["noRow"]["built"]), bd(p["noRow"]["live"]),
        "not on roster (" + str(p["svcOther"]["built"]["code"]) + ")"))
w("")
w("Reading: for a plain firm user both functions admit the user's own firm and never reach another (narrative's LIVE boundary ignores the selection and stays on the caller's firm; the built one refuses it). For an Opal internal caller, **holdings is unchanged except where a profile row narrows** (C identical, B newly refused); **narrative changes in C**: live binds an internal caller to `opal-capital` whatever it selects, built binds it to the selected firm with the Opal roster. Tests cited as the second cover: `_authz/tests/test_allowed_firm_ids.py`, `_authz/tests/test_svc_custody_statement.py`, and the four `served_error_path` tests.")
w("")
w("## The replay (offline; live versus built artifacts; `IB99-1_release_replay.json`)")
w("")
w("The replay drives the real `served.Entry.handle` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer `irpt-common:5` extracted beside it), profile row injected and `enforcer_for` stubbed to raise, so EVERY admitted case also crosses `served._record` (the error path under repair). **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the roster; **refused** = a FIRM_BINDING / NOT_AUTHORIZED reply. `UNEXPECTED` in a record is the stub's own stop after admission, now answered through the staged `errors.py` instead of TypeError.")
w("")
w("| arm | verdict | negative control | detail |")
w("|---|---|---|---|")
for a in rep["arms"]:
    w("| %s | %s | %s | %s |" % (a["name"], a["verdict"], "yes" if a["negative_control"] else "no", a["detail"].replace("|", "/")))
w("")
w("Not replayed: IB-pr-366's on-behalf create guard and IB-pr-357's envelope field (they ride in with `served.py`; neither route is a create route); a live token of svc-custody-statement (none exists until its mint pair is applied; neither host serves one of its three operations).")
w("")
w("## Branch A (released)")
w("")
w("For each function in the signed set (narrative and holdings are independent; sign either alone):")
w("")
w("1. From a clean tree at P (or a descendant whose `lambda-source-map.json`, the host trees and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` and compare the printed sha256 to the table (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip`).")
w("2. The Terraform deploy path of the function's module: %s; no IAM, route, schedule, layer or environment change. Effect on served bytes: the two functions answer through `served.py` `74a62fb46c`'s boundary; holdings gains `holdings_publication_port.py`; narrative gains the members listed above and honours internal firm selection (row W262-S1)." % "; ".join("`%s` (`%s`)" % (k, v) for k, v in TF.items()))
w("3. Per-family image/layer: none touched. The ledger entry names every function in the signed set.")
w("")
w("## Branch B (rolled back)")
w("")
for a in cen["artifacts"]:
    w("- `%s`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `%s` (its CodeSha256 is the `live_before` value `%s`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest." % (a["name"], a["s3_rollback_version"], a["live_before"]))
w("")
w("The source-map restage reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).")
w("")
w("## The replay arm for the applier (rerun before the ledger)")
w("")
w("From the repo root, scratch directory OUTSIDE the worktree holding `zips/<function>.1.zip` (the zips to be uploaded): `python replay/run_replay.py <scratch> P <out.json>` (reads the live zips and the layer from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if the negative control does not raise TypeError (the harness then is not reaching the error site). A `WIDENS` verdict is expected for irpt-narrative only. Delete the scratch directory afterwards.")
w("")
w("## The after-read")
w("")
w("1. **holdings.** One `GET /api/scoped/investor-reporting/holdings/{accountSetId}` as a plain firm user: expected the same answer as before (the member `holdings_publication_port.py` is not on this route's path); CloudWatch shows no `TypeError`.")
w("2. **narrative.** One refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line with the public reason code and no `TypeError` in the function's log group; an Opal internal caller selecting a firm now binds to it (the widening, row W262-S1). Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W262-S1` (OBSERVATION, ARMED: narrative's release is wide and adds internal firm selection). Closes by this cell: `IRPT_BCKEND-D2-W201-S5` and `-S6` (the code and restage; the release itself stays with the signed pair).")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK: packet", len("\n".join(L)), "chars")
