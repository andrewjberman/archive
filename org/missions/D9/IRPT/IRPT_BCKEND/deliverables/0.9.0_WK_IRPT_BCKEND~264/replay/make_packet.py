"""IB-pr-399 packet writer (modelled on IB-pr-394's): renders NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-399.md from
IB102-3_release_census.json and IB102-3_release_replay.json. ASCII only.
    python <this file> <deliverables_dir>
"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
cen = json.loads((D / "IB102-3_release_census.json").read_text(encoding="utf-8"))
rep = json.loads((D / "IB102-3_release_replay.json").read_text(encoding="utf-8"))
pin = cen["pin"]
art = cen["artifacts"][0]
route = rep["routes"][0]
L = []
w = L.append


def owners(m):
    o = m["owner_commits"]
    return ", ".join(x["commit"] for x in o[:6]) + (" +%d" % (len(o) - 6) if len(o) > 6 else "")


def fc(c):
    return "%s/%s" % (c["reached_firm_check"], c["code"])


w("# Never-widen sign-off packet -- IB-pr-399: irpt-narrative -- the TypeError fixed while a no-row internal caller stays bound to opal-capital")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~264 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO half @7f294053f0, msg 2765, on row `IRPT_BCKEND-D2-W262-S1`; the TypeError is row `IRPT_BCKEND-D2-W201-S6`). "
  "Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays, AWS reads only. Files beside this packet: `IB102-3_release_census.json`, `IB102-3_release_replay.json`, `replay/` (the scripts). "
  "This packet SUPERSEDES the irpt-narrative half of `0.9.0_WK_IRPT_BCKEND~262/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md` (its artifact `NbzUcWz1...` is no longer the one to sign; holdings is unaffected).")
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **The fix.** IB-pr-394's restage (narrative's `errors.py` and `served.py` rows to `74a62fb46c`) is kept: it removes the TypeError. What changes is narrative's own `entry.py`: `ENTRY` is now a `NarrativeEntry` (a subclass of the shared `served.Entry`) whose `handle` drops `selected_tenant` before the shared boundary reads it, for ONE case only -- an Opal internal caller (`verified_internal_subject`, not the svc-custody subject, not `x-user-type: service`) that has NO maintained profile row (`_internal_allowed_firms` returns None: no row, no attribute, or an empty list). That caller stays on its verified `X-Firm-Id` (`opal-capital`), as it does on the live function, whatever it selects, including a firm the registry does not know. The shared `_authz/served.py` and every other host are untouched.")
w("2. **A caller with a profile row is narrowed as on the other hosts** (row-listed selection admitted and bound to the selected firm; unlisted refused FIRM_BINDING; a malformed row or `ALL` refused). Live narrative ignored the selection for such a caller too, so a row-listed caller selecting a listed firm now binds to that firm where live bound opal-capital -- the IB-pr-387 narrowing, narrower than the no-row reach this cell removes, and the same as every other host.")
w("3. **One difference remains and is NOT closed by this cell (row `IRPT_BCKEND-D2-W264-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2): the Opal roster.** The arm below is identical on the bound firm and the public code. The roster the boundary hands `enforcer_for` is not: live hands none, the built boundary hands the caller's own email, which `classify_principal` reads as OPAL_GLOBAL inside opal-capital. That is a property of the shared `served.py` the order does not let a worker edit, it rode in with IB-pr-394's restage, and its effect on what a narrative request may name was not measured. The signer decides it.")
w("")
w("## Root cause and fix")
w("")
w("- **TypeError (row W201-S6).** `served._record` calls `errors.public_line(..., admitted=)`; narrative's staged `errors.py` (`bc3727b3a3`) lacks the keyword. Fixed by IB-pr-394 (rows restaged to `74a62fb46c`), kept here unchanged; tests `-k served_error_path` (4) pass.")
w("- **Widening (row W262-S1).** The restaged `served.py` honours `selected_tenant`; with no profile row an internal caller was admitted for any registered firm. Fixed in `narrative/entry.py` (`NarrativeEntry._held_to_verified_firm`, `_drop_selection`) at the code commit `%s`. Any error reading the selection or the row falls through to the shared boundary, which refuses." % pin[:10])
w("- **Tests** (`narrative/tests/test_opal_capital_binding.py`, 12 test items over 14 cases, `-k opal_capital_binding`): a flat `python -I` tree built the way the builder builds it (staged blobs at their pin, sha256-verified), the real `entry.ENTRY`, an enforcer stub that records the firm it is asked for. No-row internal selecting inflection is bound to opal-capital via the query, a JSON body, a base64 body, a nested `selection`, a row without the attribute and an empty list; an own-firm selection and no selection are unchanged; a row-listed caller is admitted on its list and refused off it; `ALL` is refused; a plain firm user selecting another firm is refused; an unregistered firm is not refused wider; and a NEGATIVE CONTROL runs the shared `served.Entry` with the same event and must bind inflection.")
w("")
w("## The pin and the build")
w("")
w("- **Release pin P: `%s`** (branch `wk-IRPT_BCKEND-264`): the code commit. Everything committed after it is deliverables and the surprise row; none touches `lambda-source-map.json`, the host tree or `_authz/`." % pin)
w("- The source map needed no edit: `entry.py` is already in narrative's `files[]` and the `served.py`/`errors.py` rows are IB-pr-394's.")
w("- Census: `infra/aws/lambda/ci/release-census.py irpt-narrative --pin P --map infra/aws/lambda/ci/lambda-source-map.json`, live zip read from AWS (read only).")
w("- BUILD_ONLY from a clean tree (porcelain 0 lines before and after both builds), built twice, byte-identical: **%s**. Command: `TMPDIR=<scratch> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` (the REAL source map, no override). The zip is kept in scratch only; nothing uploaded." % ("YES" if art["built_twice_identical"] else "NO"))
w("")
w("| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |")
w("|---|---|---|---|---|---|---|")
w("| `irpt-narrative` | `%s` | `%s`... | %d | `%s` | %d | `%s` |" % (art["built_sha256"], art["built_sha256_hex"][:16], art["built_bytes"], art["live_before"],
                                                            len(art["changed_members"]), art["s3_rollback_version"]))
w("")
w("`live_before` = `aws lambda get-function-configuration` CodeSha256 (last modified %s); it equals the `content-sha256` metadata of the LATEST version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`: **%s**, which is the rollback version." % (art["live_last_modified"], "yes" if art["s3_is_live_zip"] else "NO"))
w("")
w("## Changed members and their owners (every one owned)")
w("")
w("`irpt-narrative` -- %s" % "; ".join(art["census_summary"]))
for m in art["changed_members"]:
    w("- %s `%s` (built `%s`, live `%s`): %s" % (m["status"], m["member"], m["built_sha256_prefix"], m["live_sha256_prefix"], owners(m)))
w("")
w("Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). `entry.py` is owned by this cell's code commit `%s` and `630de21b95`. The other 21 members are IB-pr-394's list unchanged: the map's staged pins and source files, which no cell of this order changes; they release with it because live narrative was last built 2026-09-21." % pin[:10])
w("")
w("## Writers of the changed property")
w("")
w("- **The firm an internal caller's request is bound to.** Writers of the bound firm in `served.Entry.handle`: **N=2**: `verified = header(headers, 'X-Firm-Id')` (the edge-verified claim) and `verified = selected` after the selection checks. This cell adds one gate BEFORE the second: `NarrativeEntry` removes the selection from the event for a no-row non-service internal caller, so the second writer never fires for it. Both branches are covered by the replay and the tests: with a row, narrowed; with NO row, bound to the verified firm.")
w("- **The Opal roster handed to `enforcer_for`:** unchanged by this cell and different from live (row W264-S1).")
w("")
w("## The route: admitted and another-firm-refused")
w("")
w("Route set: `docs/contracts/investor-reporting/v1/routes.json` at P, handler `irpt-narrative`: 1 route. Columns: **U-own** plain firm user (x-firm-id cottonwood), no selection; **U-other** that user selecting inflection; **U-claim** that user restating firm_id=inflection; **A** internal caller with row `[cottonwood]` selecting cottonwood; **B** that caller selecting inflection; **C** an unrelated Opal internal caller with NO row selecting inflection (built / live); **S** svc-custody-statement on this operation. Cells are `bound firm/public code`; UNEXPECTED is the stub's own stop after admission.")
w("")
w("| route | U-own | U-other | U-claim | A (built / live) | B (built / live) | C (built / live) | S |")
w("|---|---|---|---|---|---|---|---|")
w("| %s (`%s`) | %s | %s (live %s) | %s | %s / %s | %s / %s | **%s / %s** | %s |" % (
    route["route"], route["operation"], fc(route["userOwn"]["built"]), fc(route["userSelOther"]["built"]), fc(route["userSelOther"]["live"]),
    fc(route["userClaimOther"]["built"]), fc(route["rowCotCot"]["built"]), fc(route["rowCotCot"]["live"]),
    fc(route["rowCotInf"]["built"]), fc(route["rowCotInf"]["live"]), fc(route["noRow"]["built"]), fc(route["noRow"]["live"]), fc(route["svcOther"]["built"])))
w("")
w("Reading: C is the cell this order is about -- built and live both bind opal-capital; before this cell (negative control row below) built bound inflection. A is a real change against live (built binds the listed firm, live bound opal-capital) and is the narrowing the other hosts have. B is refused where live would have bound opal-capital. For a plain firm user the built boundary refuses another firm, and the live boundary never reaches it. Tests cited as the second cover: `_authz/tests/test_allowed_firm_ids.py`, `_authz/tests/test_svc_custody_statement.py`, the four `served_error_path` tests and the twelve `opal_capital_binding` test items.")
w("")
w("## The replay (offline; live versus built artifacts; `IB102-3_release_replay.json`)")
w("")
w("The replay drives the zip's own `entry.ENTRY` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer `irpt-common:5` extracted beside it), profile row injected and `enforcer_for` stubbed to raise, so every admitted case also crosses `served._record`. **admitted** = the boundary bound the request to the firm and handed `enforcer_for` the roster; **refused** = FIRM_BINDING / NOT_AUTHORIZED.")
w("")
w("| arm | verdict | negative control | detail |")
w("|---|---|---|---|")
for a in rep["arms"]:
    w("| %s | %s | %s | %s |" % (a["name"], a["verdict"], "yes" if a["negative_control"] else "no", a["detail"].replace("|", "/")))
w("")
w("`internal_error_refusal` (issuer ruling per CTO analysis ADDENDUM 14, msg 2804, row W201-S6; AMENDMENT 1 to the order, recorded by 2.0.0_SA_COO~P2 at the drain) replays an internal error through the BUILT zip's real `entry.ENTRY`: the staged `errors.py` shape, one `irpt_error` line, no TypeError; its NEGATIVE CONTROL puts the old `errors.py` back and the TypeError escapes.")
w("")
w("`no_row_internal_selects_other_firm` is **identical** on bound firm and public code; the roster is recorded in its detail and is the content of row W264-S1.")
w("")
w("## Branch A (released)")
w("")
w("1. From a clean tree at P (or a descendant whose `lambda-source-map.json`, `narrative/` and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` and compare the printed sha256 to `%s` (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`)." % art["built_sha256"])
w("2. The Terraform deploy path of the module `infra/aws/terraform/investor-reporting/narrative/lambda.tf`; no IAM, route, schedule, layer or environment change. Effect on served bytes: narrative answers through `served.py` `74a62fb46c`'s boundary with the TypeError fixed, a no-row internal caller still on opal-capital, a row-listed caller narrowed, and the members listed above added or changed.")
w("3. Per-family image/layer: none touched. The ledger entry names irpt-narrative.")
w("")
w("## Branch B (rolled back)")
w("")
w("- `irpt-narrative`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `%s` (its CodeSha256 is the `live_before` value `%s`). Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest." % (art["s3_rollback_version"], art["live_before"]))
w("")
w("The source-map state reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).")
w("")
w("## The replay arm for the applier (rerun before the ledger)")
w("")
w("From the repo root, scratch directory OUTSIDE the worktree holding `zips/irpt-narrative.1.zip` (the zip to be uploaded): `python replay/run_replay.py <scratch> P <out.json>` (reads the live zip and the layer from AWS, runs `replay/authz_case_runner.py` per tree). STOP the apply if `no_row_internal_selects_other_firm` is not `identical`, if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if either NEGATIVE CONTROL does not behave (the harness then is not reaching the cell it measures). Delete the scratch directory afterwards.")
w("")
w("## The after-read")
w("")
w("One request as an Opal internal caller selecting another firm: expected the answer bound to opal-capital (as before); one refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line with the public reason code and no `TypeError` in the function's log group. Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W264-S1` (OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2): the Opal roster. Closes by this cell: the firm-binding half of `IRPT_BCKEND-D2-W262-S1` (the roster half moves to W264-S1); the release itself stays with the signer.")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-399.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("OK: packet", len(L), "lines")
