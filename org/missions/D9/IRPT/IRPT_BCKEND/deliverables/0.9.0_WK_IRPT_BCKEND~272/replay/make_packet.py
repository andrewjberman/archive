"""IB-pr-409 packet writer: renders NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-409.md from IB110-1_release_census.json, IB110-1_release_replay.json
and IB110-1_red_list.json. ASCII only.
    python <this file> <deliverables_dir>
"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
cen = json.loads((D / "IB110-1_release_census.json").read_text(encoding="utf-8"))
rep = json.loads((D / "IB110-1_release_replay.json").read_text(encoding="utf-8"))
red = json.loads((D / "IB110-1_red_list.json").read_text(encoding="utf-8"))
pin = cen["pin"]
art = cen["artifacts"][0]
built = art["built_sha256"]
STOPPED = "QiNRKpaCoX5gIGmt8ypj34l3noLeroXqwWLprr68Pmw="
sc = rep["enforcer_scope"]
L = []
w = L.append


def owners(m):
    o = m["owner_commits"]
    return ", ".join(x["commit"] for x in o[:6]) + (" +%d" % (len(o) - 6) if len(o) > 6 else "")


def cell(side, name):
    c = sc[side]["cases"][name]
    return "%s / roster %s / permitted_account_set %d" % (c["principal_class"], c["roster"], len(c["permitted_account_set"] or []))


w("# Never-widen sign-off packet -- IB-pr-409: irpt-narrative -- a no-row Opal caller classes UNKNOWN as live does; the TypeError fix and the opal-capital binding kept")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~272 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO ADDENDUM 18.1, msg 3284, on row `IRPT_BCKEND-D2-S48`). "
  "Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays against a SYNTHETIC directory, AWS reads only (the live zip, its layer, "
  "its CodeSha256 and S3 version); no client-data enumeration. Files beside this packet: `IB110-1_release_census.json`, `IB110-1_release_replay.json`, "
  "`IB110-1_red_list.json`, `replay/` (the scripts). This packet SUPERSEDES `0.9.0_WK_IRPT_BCKEND~264/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-399.md`: its artifact "
  "`%s` is the build IB-pr-401 STOPPED on and is no longer the one to sign." % STOPPED)
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **The fix.** The shared `served.Entry.handle` hands `enforcer_for` the caller's own email as the Opal roster for every verified Opal internal caller; for a caller with "
  "NO maintained profile row that classes OPAL_GLOBAL (`enforce.py:790`: any advisor in its own firm), where the live irpt-narrative hands no roster and classes UNKNOWN. "
  "`narrative/entry.py` now drives the shared handle on a request-local copy of the entry whose `enforcer_for` passes the roster through `NarrativeEntry._live_roster`: "
  "a roster naming a caller with no profile row (`_internal_allowed_firms` -> None), or whose row cannot be read, is replaced by None, which is exactly what the live boundary hands. "
  "Only irpt-narrative changes, and only `narrative/entry.py` among its members relative to IB-pr-399.")
w("2. **The shared `_authz/served.py` is UNCHANGED**: `git diff bd9c06d2fb HEAD -- infra/aws/lambda/investor-reporting/_authz/` is empty (blob `12b0ac90c8` at the base and at the pin), "
  "and no other host's code is touched. The packaged `served.py` member is the STAGED blob `_authz/served.py@74a62fb46c` (sha256 prefix `87d9ecc49747`, the same as IB-pr-399's census), "
  "which the source map pins and this cell does not edit.")
w("3. **The enforcer-scope arm now reads IDENTICAL**, driven as in row D2-S48 (each tree's own `_scope.resolve` with the roster that tree's boundary hands `enforcer_for`): live and built both "
  "class the no-row caller UNKNOWN with nothing granted. Its NEGATIVE CONTROL, the stopped `%s` entry.py, reads OPAL_GLOBAL on the same arm and grants the whole synthetic firm population, "
  "so the harness is reaching the cell it measures." % STOPPED[:8])
w("4. **ONE difference remains, outside this order and stated rather than hidden (row `IRPT_BCKEND-D2-W272-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2):** a caller WITH a maintained profile row "
  "(`allowedFirmIds` non-empty) keeps the roster the shared boundary hands it, as the order says (\"a row-listed caller is unchanged\"), so it classes OPAL_GLOBAL on built where live classes it "
  "UNKNOWN. That is the same class change IB-pr-399 carried for that caller (built == stopped on the arm below); this cell does not change it and does not widen it. The signer decides it.")
w("")
w("## Root cause and fix")
w("")
w("- **Cause (row D2-S48).** The restaged `served.py` computes `principals = frozenset([email]) if subject is not None else self.opal_principal_ids` and calls `self.enforcer_for(verified, principals)`. "
  "The live boundary called `enforcer_for(verified)`. `resolve.classify_principal` puts the roster check (branch 2) before the advisor and admin branches, so a roster hit is OPAL_GLOBAL.")
w("- **Fix (`narrative/entry.py`, this cell's code commit `%s`).** `NarrativeEntry.handle` makes `view = copy.copy(self)` (the warm Entry is never mutated, and an `enforcer_for` stub installed on the instance is still the callee), "
  "installs a wrapper that calls the original `enforcer_for(tenant, self._live_roster(roster))`, and runs `served.Entry.handle(view, ...)`. The IB-pr-399 selection drop (`_held_to_verified_firm`) is unchanged. "
  "The roster is replaced only when it is a request-local email set whose caller has no profile row; a row read error grants nothing (fail closed to the live roster); None and the Entry's own roster pass through." % pin[:10])
w("- **Tests** (`narrative/tests/test_no_row_unknown.py`, 13 items, `-k no_row_unknown`): a flat `python -I` tree built the way the builder builds it (staged blobs at their pin, sha256-verified), "
  "the real `entry.ENTRY`, an enforcer stub that records the roster, then that tree's own `resolve.classify_principal`. No-row callers (no row, attribute absent, empty list, null list, selecting another firm, "
  "own firm, no selection) get roster None and class UNKNOWN; a read error, an `ALL` row and a service principal grant nothing; a row-listed caller and a plain firm user match the shared boundary; "
  "the warm Entry is not mutated; the CONTROL drives the shared `served.Entry` and must read OPAL_GLOBAL. With the fix reverted 9 of the 13 fail. The existing `-k served_error_path` and `-k opal_capital_binding` tests pass; narrative suite 69 passed.")
w("")
w("## The pin and the build")
w("")
w("- **Release pin P: `%s`** (branch `wk-IRPT_BCKEND-272`): the code commit. Everything committed after it is deliverables and rows; none touches `lambda-source-map.json`, the host tree or `_authz/`." % pin)
w("- The source map needed no edit (`entry.py` is already in narrative's `files[]`).")
w("- Census: `infra/aws/lambda/ci/release-census.py irpt-narrative --pin P --map infra/aws/lambda/ci/lambda-source-map.json`, live zip read from AWS (read only).")
w("- BUILD_ONLY from a clean tree (porcelain 0 lines before and after both builds), built twice, byte-identical: **%s**. Command: `TMPDIR=<scratch> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` "
  "(the REAL source map, no override). The zip is kept in scratch only; nothing uploaded." % ("YES" if art["built_twice_identical"] else "NO"))
w("- **Built sha256 (CodeSha256 form): `%s`** -- different from the stopped `%s`. 21 of the 22 changed members carry the same sha256 prefix as IB-pr-399's census; the one that differs is `entry.py` (`%s`)." % (
    built, STOPPED, next(m["built_sha256_prefix"] for m in art["changed_members"] if m["member"] == "entry.py")))
w("")
w("| function | built sha256 (CodeSha256 form) | hex | bytes | live_before (CodeSha256) | changed members vs live | S3 rollback version (live zip) |")
w("|---|---|---|---|---|---|---|")
w("| `irpt-narrative` | `%s` | `%s`... | %d | `%s` | %d | `%s` |" % (built, art["built_sha256_hex"][:16], art["built_bytes"], art["live_before"], len(art["changed_members"]), art["s3_rollback_version"]))
w("")
w("`live_before` = `aws lambda get-function-configuration` CodeSha256 (last modified %s); it equals the `content-sha256` metadata of the LATEST version of "
  "`s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`: **%s**, which is the rollback version." % (art["live_last_modified"], "yes" if art["s3_is_live_zip"] else "NO"))
w("")
w("## Changed members and their owners (every one owned)")
w("")
w("`irpt-narrative` -- %s" % "; ".join(art["census_summary"]))
for m in art["changed_members"]:
    w("- %s `%s` (built `%s`, live `%s`): %s" % (m["status"], m["member"], m["built_sha256_prefix"], m["live_sha256_prefix"], owners(m)))
w("")
w("Owners are the commits that touched each member's source path after the commit holding the LIVE blob, up to the commit holding the BUILT blob (an added member: the commit that introduced the blob). "
  "`entry.py` is owned by this cell's code commit `%s`." % pin[:10])
w("")
w("## Blast radius")
w("")
w("- **Function:** `irpt-narrative` only (one route, `GET /api/scoped/investor-reporting/narrative/{reportId}`). No other function, layer, IAM, route, schedule, environment or table changes.")
w("- **Members:** the %d changed members above vs live; relative to the stopped IB-pr-399 build, ONE member differs: `entry.py`." % len(art["changed_members"]))
w("- **Shared code:** `_authz/served.py` is unchanged (blob `12b0ac90c8`); the fix lives in `narrative/entry.py` only.")
w("- **Effect on served bytes:** a no-row Opal internal caller is bound to opal-capital (IB-pr-399) AND classed UNKNOWN as live (this cell); a row-listed caller is narrowed and classed as on IB-pr-399; the TypeError is fixed.")
w("")
w("## Writers of the changed property")
w("")
w("- **The Opal roster handed to `enforcer_for`.** Writers: **N=2**: `served.Entry.handle`'s `principals = ...` (shared, unchanged) and `NarrativeEntry._live_roster` (this cell). The second can only REPLACE a non-empty "
  "request-local roster with None; it cannot add a principal.")
w("- **The firm a request is bound to:** unchanged by this cell (IB-pr-399's `_held_to_verified_firm`).")
w("")
w("## The red list (CTO ADDENDUM 18, row D2-S46)")
w("")
w("`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **%s**. The FAILED node ids (%d):" % (red["pytest_summary"], red["failed_count"]))
for n in red["failed_node_ids"]:
    w("- `%s`" % n)
w("")
w("Their targets are the public-route count against the installed status handler, the upload route denominator, and the response contracts / fixtures of `%s`. This cell changes %d paths vs its base (%s); "
  "the packaged members' source paths number %d. Intersection with the red tests' target surface (`%s`) and with any path naming a red operation: **%d changed, %d member, %d naming** -- STOP = **%s**. "
  "No investor-reporting `_contracts` test about `narrative-packet` is red. This packet does not cite \"suite green\"." % (
      ", ".join(red["red_test_operations"]), len(red["paths_this_cell_changed_vs_base"]), ", ".join(red["paths_this_cell_changed_vs_base"]),
      len(red["packaged_member_source_paths"]), "`, `".join(red["target_prefixes"]), len(red["changed_paths_touching_a_target"]),
      len(red["member_paths_touching_a_target"]), len(red["paths_naming_a_red_operation"]), "YES" if red["stop"] else "no"))
w("")
w("## The enforcer-scope arm (row D2-S48's method)")
w("")
w("Driven with the resolver's OWN TRUSTED_HEADERS: x-origin-verify=cloudfront, x-user-email=ops@opalinvest.com, x-firm-id=opal-capital; x-advisor-id, x-user-role, x-user-type absent. Directory: SYNTHETIC "
  "(two opal-capital accounts, one account of another firm); ownership empty. One tree per process.")
w("")
w("| case | live (class / roster / permitted) | built (this cell) | stopped QiNRKpaC (negative control) |")
w("|---|---|---|---|")
for name in ("no_row_no_selection", "no_row_selecting_other", "row_listed_no_selection"):
    w("| %s | %s | %s | %s |" % (name, cell("live", name), cell("built", name), cell("stopped", name)))
w("")
w("The first two rows are the arm: built == live, UNKNOWN, nothing granted (`identical`). The stopped tree reads OPAL_GLOBAL with the whole synthetic firm population "
  "(negative control, `expected-diff`). The third row is the one remaining difference (item 4 above).")
w("")
w("## The replay (offline; live versus built artifacts; `IB110-1_release_replay.json`)")
w("")
w("The replay drives the zip's own `entry.ENTRY` out of each EXTRACTED ZIP (`python -I`, flat layout, the function's live layer extracted beside it), profile row injected and `enforcer_for` stubbed to raise. "
  "IB-pr-399's 13 arms re-run (same names, same verdicts) plus 3 new arms: `no_row_internal_enforcer_scope`, its negative control, and the row-listed caller against the stopped build. "
  "Verdicts are exactly `identical` or `expected-diff`; %d arms, no UNEXPECTED." % len(rep["arms"]))
w("")
w("| arm | verdict | negative control | detail |")
w("|---|---|---|---|")
for a in rep["arms"]:
    w("| %s | %s | %s | %s |" % (a["name"], a["verdict"], "yes" if a["negative_control"] else "no", a["detail"].replace("|", "/")))
w("")
w("## Branch A (released)")
w("")
w("1. From a clean tree at P `%s` (or a descendant whose `lambda-source-map.json`, `narrative/` and `_authz/` are unchanged): `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-narrative` "
  "and compare the printed sha256 to `%s` (ABORT if different), then the same script without BUILD_ONLY (S3 object `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-narrative.zip`)." % (pin, built))
w("2. The Terraform deploy path of the module `infra/aws/terraform/investor-reporting/narrative/lambda.tf`; no IAM, route, schedule, layer or environment change. Effect on served bytes: narrative answers through "
  "`served.py` `74a62fb46c`'s boundary (unchanged shared file) with the TypeError fixed, a no-row internal caller on opal-capital and classed UNKNOWN as live, a row-listed caller narrowed, and the members listed above added or changed.")
w("3. Per-family image/layer: none touched. The ledger entry names irpt-narrative.")
w("")
w("## Branch B (rolled back)")
w("")
w("- `irpt-narrative`: redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `%s` (its CodeSha256 is the `live_before` value `%s`). "
  "Re-read at signing: `get-function-configuration` CodeSha256 unchanged and the version still the latest." % (art["s3_rollback_version"], art["live_before"]))
w("")
w("The source-map state reverts with the commit. No other state: the change is code only (no table row, IAM or schedule written).")
w("")
w("## The replay arm for the applier (rerun before the ledger)")
w("")
w("From the repo root, scratch directory OUTSIDE the worktree holding `zips/irpt-narrative.1.zip` (the zip to be uploaded): `python <deliverables>/replay/run_replay.py <scratch> %s <out.json>` "
  "(reads the live zip and the layer from AWS, runs `replay/authz_case_runner.py` and `replay/enforcer_scope_runner.py` per tree). STOP the apply if `no_row_internal_enforcer_scope`, "
  "`no_row_internal_selects_other_firm` or `internal_error_refusal` is not `identical`, if any arm is `UNEXPECTED`, if the error-path arm shows a HARNESS_ code, or if a NEGATIVE CONTROL "
  "does not behave (the harness then is not reaching the cell it measures). The IB-pr-399 half's other conditions are unchanged. Delete the scratch directory afterwards." % pin)
w("")
w("## The after-read")
w("")
w("One request as an Opal internal caller selecting another firm: expected the answer bound to opal-capital (as before); one refused request (e.g. a firm user selecting another firm) logs one `irpt_error` JSON line "
  "with the public reason code and no `TypeError` in the function's log group. Either read is UNEXERCISED until the apply; the replay is the only evidence and ABSENT != EXERCISED-AGAINST.")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W272-S1` (OBSERVATION, ARMED, disarm owner 2.0.0_SA_COO~P2): a row-listed internal caller still classes OPAL_GLOBAL on built vs UNKNOWN on live (unchanged from IB-pr-399, per the order). "
  "`IRPT_BCKEND-D2-W272-S2` (OBSERVATION, INERT): the IB-pr-399 replay driver derived its pre-binding control from `pin^`, which at this pin is IB-pr-399's own entry; the control is now pinned to `cabad9008c^`.")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-409.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("OK: packet", len(L), "lines")
