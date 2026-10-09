"""IB-pr-416 packet writer (form of IB-pr-409's make_packet.py). From the worktree root:
    python <this file> <deliverables_dir>
Reads IB117-1_signature_census.json, IB117-1_replay.json, IB117-1_red_list.json and IB117-1_adapter_refusals.json from <deliverables_dir>
and writes NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md there. irpt-performance-adapter is FIRST (AMENDMENT 1). Counts, sha256 and reason
codes only: no account id, balance, fee or flow. ASCII only.
"""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
cen = json.loads((D / "IB117-1_signature_census.json").read_text(encoding="utf-8"))
rep = json.loads((D / "IB117-1_replay.json").read_text(encoding="utf-8"))
red = json.loads((D / "IB117-1_red_list.json").read_text(encoding="utf-8"))
ref = json.loads((D / "IB117-1_adapter_refusals.json").read_text(encoding="utf-8"))
F = {r["function"]: r for r in cen["functions"]}
ORDER = ["irpt-performance-adapter", "irpt-narrative", "irpt-status"]
PIN = cen["pin"]
TREE = cen["tree_pin_of_staged_rows"]
DIR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278"
ATTR = cen["instruments"]["name_and_attribute_limbs"]
ORIG = cen["instruments"]["original"]
L = []
w = L.append


def own(m):
    c = m.get("owner_commits") or []
    return ", ".join(x["commit"] for x in c[:4]) + (" +%d" % (len(c) - 4) if len(c) > 4 else "") if c else m["owner_commit"][:40]


w("# Never-widen sign-off packet -- IB-pr-416: irpt-performance-adapter, irpt-narrative and irpt-status rebuilt from one tree so every served.py call fits its packaged callee")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~278 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO (CTO half), on row `IRPT_BCKEND-D2-S60` (ruled by `IRPT_BCKEND-D2-S61`; "
  "TO-IB-pr-416 AMENDMENT 1 orders the adapter first). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a clean tree, offline replays against "
  "SYNTHETIC data, AWS reads only (the live zips, their layers, CodeSha256, S3 version, CloudWatch counts). No client data is in this packet or its files: counts, sha256 and reason codes only.")
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **irpt-performance-adapter is the FIRST apply, and it is FAILING live now.** Its `Enforcer(load_report_owner=)` call raises `TypeError` (the packaged `enforce.py` predates "
  "that parameter) on every `performance-report` request that reaches the Enforcer, and the request fails closed. CloudWatch, `/aws/lambda/irpt-performance-adapter`, "
  "every page counted client-side, window %s to %s: **%d performance-report requests refused** (%d `irpt_error` lines, all public reason code %s; %d `irpt_internal` lines "
  "with exception_type TypeError), first %s, last %s (%d pages read). Counts only (`IB117-1_adapter_refusals.json`)." % (
      ref["window_start"], ref["window_end"], ref["refused_requests_irpt_error"], ref["refused_requests_irpt_error"],
      ", ".join("%s x%d" % kv for kv in ref["refusals_by_public_reason_code"].items()), ref["irpt_internal_typeerror_events"], ref["first_event"], ref["last_event"], ref["pages_read"]))
w("2. **No rollback branch for the adapter restores the older `5nyq8P6v`** (it would undo IB-pr-395's narrowing). The adapter's Branch B is **hold on the current live version "
  "`o/643qVE...`** (CodeSha256 `%s`)." % F["irpt-performance-adapter"]["live_sha256"])
w("3. **irpt-status's apply WAITS on IRPT_ANLREQ release 1** (2.0.0_SA_COO~Y2 is rolling it back). The built status zip carries release 1's `status_installed.py` "
  "(`3e59dc5d6e`, AR-y-21 AMENDMENTS 4, 6, 7) co-staged with `composition.py` and `repository.py` at `%s`; it must not be applied until the release-1 pair has cleared." % TREE[:10])
w("4. **The source map is NOT edited** (outside this order's grant). The three zips are built from `%s/candidate_source_map.json` (a map holding only these three functions, every other "
  "key verbatim), via `BAU_SOURCE_MAP_OVERRIDE`; the apply amendment must land those three entries into `infra/aws/lambda/ci/lambda-source-map.json` first, or the real-map build "
  "reproduces the split and its sha256 will differ (row `IRPT_BCKEND-D2-W278-S2`, ARMED, disarm owner 2.0.0_SA_COO~P2)." % DIR)
w("5. **`served.py` is held at its staged pin `74a62fb46c` in all three** (the byte-identical live member). HEAD's carries IB-pr-405's addition of `analysis-request-read` to "
  "svc-custody-statement's operations, which this order does not own (row `IRPT_BCKEND-D2-W278-S1`, ARMED, disarm owner 2.0.0_SA_COO~P2). Both closure limbs read 0 against that served.py.")
w("6. **What the fix is.** The tree at HEAD agrees with itself; each zip was built from mixed members. Every staged row naming a shared authorization module "
  "(`_authz`, `_scope`, `_ids`, `_keys`, `_render_identity`, `data/firm_registry.json`) other than `served.py` is re-pinned to the one commit `%s`, its sha256 recomputed from "
  "`git show`; irpt-status also takes `reports/composition.py` and `reports/repository.py` from it (the closure needs exactly those two; row `IRPT_BCKEND-D2-W278-S3`). "
  "Members held at their own pins for reasons stated elsewhere (irpt-status `ops/entry.py`, `ops/owned_report.py`, `resident_installed.py`; the `performance/` and `reports/` "
  "members not named above) are NOT callees of served.py and are not moved." % TREE)
w("")
w("## The two closure limbs and the zip census")
w("")
w("Instruments (both read the zip's own bytes; run at their own paths, `python <instrument> <zip>`):")
w("- `%s` -- ~Y2's original, untouched: the name limb (`from <packaged module> import f`; `f(...)`)." % ORIG)
w("- `%s` -- the same with the attribute limb added: `module.f(...)` / `module.Cls(...)` where `module` is a packaged module, and a `**name` unpack resolved statically "
  "when `name` is a local dict literal with constant-key stores (this is what reads the adapter's `Enforcer(**render)` split). Last line ends `attr_checked=<k> attr_mismatched=<m>`." % ATTR)
w("")
w("| function | pin / tree | built sha256 (CodeSha256 form) | live sha256 | built twice identical | live: name / attribute mismatches | built: name / attribute mismatches | attr calls checked (built) | bytes |")
w("|---|---|---|---|---|---|---|---|---|")
for fn in ORDER:
    r = F[fn]
    w("| `%s` | `%s` / `%s` | `%s` | `%s` | %s | %d / %d | **%d / %d** | %d | %d |" % (
        fn, PIN[:10], TREE[:10], r["built_sha256"], r["live_sha256"], "YES" if r["built_twice_identical"] else "NO", r["live_signature_mismatched"],
        r["live_attribute_mismatched"], r["built_signature_mismatched"], r["built_attribute_mismatched"], r["built_attribute_checked"], r["built_bytes"]))
w("")
w("Last lines of the instrument on each built zip:")
for fn in ORDER:
    w("- `%s`: `%s`" % (fn, F[fn]["built_last_line"]))
w("")
w("Negative control (the live zips): ")
for fn in ORDER:
    w("- `%s`: `%s`" % (fn, F[fn]["live_last_line"]))
w("")
w("The adapter's Enforcer split reads on the attribute limb alone (name limb on the live adapter reports only `InteractiveAccess(profile_reader=)`); the live narrative also reads "
  "`enforce.Request(path_ids=)` on the attribute limb (row `IRPT_BCKEND-D2-W278-S5`). The built zips were built twice with `TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` "
  "from a clean tree (porcelain 0 lines before and after) and are byte-identical; the zips stay in scratch, outside the worktree.")
w("")
w("`symbol_closure.py` (name resolution, ~Y2 r71) on the built irpt-status zip reads `missing=0`, PASS.")
w("")
w("## Per function")
w("")
for n, fn in enumerate(ORDER, 1):
    r = F[fn]
    w("### %d. `%s`%s" % (n, fn, "  -- THE FIRST APPLY (failing live)" if n == 1 else ("  -- apply waits on IRPT_ANLREQ release 1" if fn == "irpt-status" else "")))
    w("")
    w("- **Live sha256** (CodeSha256): `%s`, last modified %s; it equals the `content-sha256` metadata of the LATEST S3 version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/%s.zip`: **%s**." % (
        r["live_sha256"], r["live_last_modified"], fn, "yes" if r["s3_is_live_zip"] else "NO"))
    w("- **Built sha256** (CodeSha256 form): `%s` (hex `%s`, %d bytes), built twice identical: %s." % (r["built_sha256"], r["built_sha256_hex"], r["built_bytes"], "YES" if r["built_twice_identical"] else "NO"))
    w("- **Changed members vs live: %d** (live %s members, built the same count):" % (len(r["changed_members"]), r["census_summary"][0].split("live_members=")[1]))
    for m in r["changed_members"]:
        w("  - %s `%s` (built `%s`, live `%s`): %s" % (m["status"], m["member"], m["built_sha256_prefix"], m["live_sha256_prefix"], own(m)))
    w("- **Branch A (land it):** %s" % (
        "from a clean tree at P `%s` (or a descendant whose `narrative/`, `ops/`, `performance/`, `reports/`, `_authz/` ... trees and the three candidate entries are unchanged) with the three candidate entries landed in the source map, "
        "`BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting %s` and compare the printed sha256 to `%s` (ABORT if different), then the same without BUILD_ONLY, then the module's Terraform path "
        "(`s3_object_version` + `source_code_hash` only). No IAM, route, schedule, layer or environment change." % (PIN, fn, r["built_sha256"])))
    if fn == "irpt-performance-adapter":
        w("- **Branch B (hold):** there is no rollback to restore. **Hold on the current live version `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=`** (S3 version `%s`, re-read at apply: "
          "`get-function-configuration` CodeSha256 and the version still the latest). `5nyq8P6v` is NOT a rollback target (IB-pr-395's narrowing)." % r["s3_rollback_version"])
    else:
        w("- **Branch B (rolled back):** redeploy the prior artifact through the same Terraform path (never a console edit): S3 object version `%s` (its CodeSha256 is the live value above). "
          "Re-read at apply: `get-function-configuration` CodeSha256 unchanged and the version still the latest." % r["s3_rollback_version"])
    if fn == "irpt-status":
        w("- **Order:** this apply waits on IRPT_ANLREQ release 1 (2.0.0_SA_COO~Y2 is rolling it back). The built zip IS the release-1 member set made self-consistent, so apply it only with or after that pair.")
    w("")
w("## Blast radius")
w("")
w("- **Functions:** irpt-performance-adapter, irpt-narrative, irpt-status; no other function, layer, IAM, route, schedule, environment or table changes.")
w("- **Members:** the per-function lists above; `served.py` is unchanged in all three. Shared code in the repo is unchanged by this cell (the cell edits no product source).")
w("- **Effect on served bytes:** the adapter's `performance-report` stops failing on `Enforcer(load_report_owner=)` (it reaches the Enforcer with the retained-owner port, as IB-pr-293 intended); "
  "the narrative's prospect path stops raising on `guard_prospect(authorize_owner=, resolve_owner=)` and `enforce.Request(path_ids=)` fits; the status internal-caller CREATE path stops raising on "
  "`InteractiveAccess(profile_reader=)`. Authorization decisions on the arms below are identical live vs built.")
w("")
w("## The ADDENDUM 18 red list")
w("")
w("`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **%s**. The FAILED node ids (%d):" % (red["pytest_summary"], red["failed_count"]))
for nid in red["failed_node_ids"]:
    w("- `%s`" % nid.replace("\\", "/"))
w("")
w("Their targets are the response contracts / fixtures of `%s` and the declared-route response refs. This cell changes %d paths vs its base (all under its deliverables folder); the packaged members' source paths number %d. "
  "Intersection with the red tests' target surface (`infra/aws/lambda/investor-reporting/_contracts/`, `docs/contracts/investor-reporting/`) and with any path naming a red operation: "
  "**%d changed, %d member, %d naming** -- STOP = **%s**. `analysis-request-original` is a route irpt-status declares; none of its changed members is that route's contract, fixture or handler. "
  "This packet does not cite \"suite green\"." % (", ".join(red["red_test_operations"]), len(red["paths_this_cell_changed_vs_base"]), len(red["packaged_member_source_paths"]),
                                                  len(red["changed_paths_touching_a_target"]), len(red["member_paths_touching_a_target"]), len(red["paths_naming_a_red_operation"]), "yes" if red["stop"] else "no"))
w("")
w("## The replay (offline; live zip against built zip; `IB117-1_replay.json`)")
w("")
w("Each tree is extracted (`python -I`, flat layout, the function's live layers beside it) and the zip's own `entry.ENTRY` is driven by IB-pr-409's `authz_case_runner.py` (unchanged), "
  "`replay/scope_runner_416.py` (row D2-S48's method, route per host) and `replay/live_call_runner_416.py` (the three split call sites). The NEGATIVE CONTROL tree is the built tree with "
  "`interactive_access.py`, `prospect.py` and `enforce.py` put back to the LIVE bytes. Verdicts are exactly `identical` or `expected-diff`: %d arms, none UNEXPECTED." % len(rep["arms"]))
w("")
w("| function | arm | verdict | negative control | detail |")
w("|---|---|---|---|---|")
for fn in ORDER:
    for a in rep["arms"]:
        if a["function"] == fn:
            w("| `%s` | %s | %s | %s | %s |" % (fn, a["name"].replace("|", "/"), a["verdict"], "yes" if a["negative_control"] else "no", a["detail"].replace("|", "/")))
w("")
w("Reading the arms: the **no-row-internal** arm (`no_row_internal_enforcer_scope`) is identical live vs built on all three hosts (the narrative classes UNKNOWN as on its live 409 build; the adapter and "
  "status class OPAL_GLOBAL on both sides, unchanged by this cell). The **prospect** arms show the live TypeError where the call site has the split and none on built; the narrative's "
  "internal-caller prospect arms read ModuleNotFoundError on BOTH sides because that zip packages no `interactive_access.py` (row `IRPT_BCKEND-D2-W278-S4`, INERT: the host declares no prospect or owner-read mode). "
  "The **enforcer build** arm shows the adapter's and the narrative's live TypeError on `load_report_owner` and the built Enforcer constructed.")
w("")
w("## The live-call arm (IRPT_ANLREQ release 1 half AMENDMENT 5, CTO msg 3732)")
w("")
w("Carried beside the zip census, unchanged in meaning: *a LIVE-CALL arm sits before the ledger closes: ONE real GET answering 200 on a non-49F request within a minute of the promote; a 500 means "
  "immediate Branch B.* It is now standard in the CTO seat's halves for every served Lambda release. Per function, rerun at apply (UNEXERCISED until then; ABSENT != EXERCISED-AGAINST):")
w("- `irpt-performance-adapter`: one GET `/api/scoped/investor-reporting/performance/{accountSetId}` as a caller outside the 49F case; expect a typed answer, never 500 and never `TypeError` in the group. "
  "Branch B is the hold above (there is no previous version to promote), so a 500 means STOP and escalate, not a re-promote.")
w("- `irpt-narrative`: one GET `/api/scoped/investor-reporting/narrative/{reportId}` as a firm user; expect 200 or a typed refusal, one `irpt_error` line at most and no `TypeError`; a 500 means immediate Branch B.")
w("- `irpt-status`: one GET `/api/scoped/investor-reporting/status` for a non-49F caller within a minute of the promote; a 500 means immediate Branch B. Do not start until IRPT_ANLREQ release 1 has cleared.")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W278-S1` (served.py held at 74a62fb46c; ARMED, disarm owner 2.0.0_SA_COO~P2), `-S2` (source map not edited, candidate map in deliverables; ARMED, 2.0.0_SA_COO~P2), "
  "`-S3` (the real irpt-status map pairs release-1 status_installed.py with an older composition.py; ARMED, 2.0.0_SA_COO~Y2), `-S4` (irpt-narrative packages no interactive_access.py; INERT), "
  "`-S5` (attribute limb also reads enforce.Request(path_ids=) on live narrative; the red list now reads 2 failed; INERT).")
w("")
w("Files beside this packet: `IB117-1_signature_census.json`, `IB117-1_replay.json`, `IB117-1_red_list.json`, `IB117-1_adapter_refusals.json`, `candidate_source_map.json`, "
  "`signature_closure_attr.py`, and the writers (`make_candidate_map.py`, `make_census_416.py`, `make_packet_416.py`, `cw_refused_count_416.py`, `replay/`).")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK:", D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md", len("\n".join(L)))
