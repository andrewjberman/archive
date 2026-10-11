"""IB-pr-416 packet writer (form of IB-pr-409's make_packet.py; TO AMENDMENTS 1, 2 and 3). From the worktree root:
    python <this file> <deliverables_dir>
Reads IB117-1_signature_census.json, IB117-1_replay.json, IB117-1_red_list.json and IB117-1_adapter_refusals.json from <deliverables_dir>
and writes NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md there. irpt-performance-adapter is FIRST (AMENDMENT 1). Counts, sha256 and reason
codes only: no account id, balance, fee or flow. ASCII only.
"""
import hashlib
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
METHOD = DIR + "/method_call_limb_416.py"
L = []
w = L.append


def own(m):
    c = m.get("owner_commits") or []
    return ", ".join(x["commit"] for x in c[:4]) + (" +%d" % (len(c) - 4) if len(c) > 4 else "") if c else m["owner_commit"][:40]


def sha(rel):
    return hashlib.sha256((Path(rel)).read_bytes()).hexdigest()[:16]


a = F["irpt-performance-adapter"]
s = F["irpt-status"]
w("# Never-widen sign-off packet -- IB-pr-416: irpt-performance-adapter, irpt-narrative and irpt-status rebuilt from ONE commit so every served.py call fits its packaged callee")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~278 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO (CTO half), on row `IRPT_BCKEND-D2-S60` (ruled by `IRPT_BCKEND-D2-S61`; "
  "TO-IB-pr-416 AMENDMENTS 1, 2 and 3). Nothing here was uploaded, deployed or applied: BUILD_ONLY from a committed tree, offline replays against "
  "SYNTHETIC data with in-memory fakes, AWS reads only (the live zips, their layers, CodeSha256, S3 version, CloudWatch counts). No client data is in this packet or its files: counts, sha256 and reason codes only.")
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **irpt-performance-adapter is the FIRST apply, and it is FAILING live now.** Its `Enforcer(load_report_owner=)` call raises `TypeError` (the packaged `enforce.py` predates "
  "that parameter) on every `performance-report` request that reaches the Enforcer, and the request fails closed. CloudWatch, `/aws/lambda/irpt-performance-adapter`, "
  "every page counted client-side, window %s to %s (re-run at the time of writing, so the window ends at the current time): **%d performance-report requests refused** "
  "(%d `irpt_error` lines, public reason code %s; %d `irpt_internal` lines with exception_type TypeError), first %s, last %s (%d pages read). Counts only (`IB117-1_adapter_refusals.json`)." % (
      ref["window_start"], ref["window_end"], ref["refused_requests_irpt_error"], ref["refused_requests_irpt_error"],
      ", ".join("%s x%d" % kv for kv in ref["refusals_by_public_reason_code"].items()), ref["irpt_internal_typeerror_events"], ref["first_event"], ref["last_event"], ref["pages_read"]))
w("2. **No rollback branch for the adapter restores the older `5nyq8P6v`** (it would undo IB-pr-395's narrowing). The adapter's Branch B is **hold on the current live version "
  "`o/643qVE...`** (CodeSha256 `%s`)." % a["live_sha256"])
w("3. **irpt-status's apply WAITS on IRPT_ANLREQ release 1** (2.0.0_SA_COO~Y2). Live irpt-status is rev 3 (`%s`, last modified %s); rev 5 (`DZOdwUOG`) was rolled back after its R3 read caught "
  "`RetentionPolicy.reference() takes 3 positional arguments but 4 were given` (CTO half AMENDMENT 7). **This build is the ONE-TREE release that ruling orders for irpt-status**: it carries release 1's line "
  "(`status_installed.py` 3e59dc5d6e, `composition.py` and `repository.py`, `resident_installed.py`) with every sibling taken from the same commit, so no member is out of step with the one that calls it. "
  "It must not be applied before the release-1 pair has cleared." % (s["live_sha256"], s["live_last_modified"]))
w("4. **The source map is NOT edited** (outside this order's grant). The three zips are built from `%s/candidate_source_map.json` (a map holding only these three functions, every other "
  "key verbatim), via `BAU_SOURCE_MAP_OVERRIDE`; the apply amendment must land those three entries into `infra/aws/lambda/ci/lambda-source-map.json` first, or the real-map build "
  "reproduces the split and its sha256 will differ (row `IRPT_BCKEND-D2-W278-S2`, ARMED, disarm owner 2.0.0_SA_COO~P2)." % DIR)
w("5. **The one tree (AMENDMENT 2) is commit `%s`.** Every staged row of the three functions whose repo path is under `infra/aws/lambda/investor-reporting/` (and the two gold `data/assets/scripts/gold/investor_reporting/` scripts "
  "of the adapter, whose blobs are identical at the old and new pin, so that move changes no byte) is re-pinned to it, its sha256 recomputed from `git show`; each re-pin (member, old pin, new pin, sha256 prefixes) "
  "is named per function below and in the census (`repins`). The investor-reporting tree at that commit is byte-equal to box/dell2's at the time of writing (`git diff 361c44fa9d box/dell2 -- infra/aws/lambda/investor-reporting` is empty), so it "
  "holds release 1's rows as IRPT_ANLREQ shipped them. Rows OUTSIDE investor-reporting (`lib/`, `org/standards/`, `infra/logic/registry/`, silver scripts, `firm_registry.json`, `_vendor`, `jwt_freshness.py`) keep the map's pins and are listed under "
  "`_kept_IB_pr_416` in the candidate map. No member is held at an older pin for a reason in a packet (row `IRPT_BCKEND-D2-W278-S1`)." % TREE)
w("6. **What rides, said plainly.** One commit means the members that lagged now arrive with the commits in between. The census names every changed member with its owning commits. Beyond the three split callees "
  "(`interactive_access.py`, `prospect.py`, `enforce.py`) this includes `served.py` at its HEAD blob (IB-pr-405 adds `analysis-request-read` to svc-custody-statement's operations), "
  "irpt-status's `repository.py` and `retention.py` at their HEAD blobs (3fc99be70f, the commits IRPT_ANLREQ AMENDMENT 9 had chosen to drop) and `resident_installed.py`, `owned_report.py`, `entry.py`, `durable_job.py`. "
  "The CTO half signs these as one tree (CTO half AMENDMENT 7) and the replay below is the grade, not a member-count limit.")
w("")
w("## The closure limbs and the zip census")
w("")
w("Instruments (each reads the zip's own bytes; run at its own path, `python <instrument> <zip>`; the packet carries ALL of them beside the zip census, CTO msg 3732):")
w("- `%s` -- ~Y2's original, untouched: the name limb (`from <packaged module> import f`; `f(...)`)." % ORIG)
w("- `%s` (sha256 prefix `%s`) -- the same with the ATTRIBUTE limb added: `module.f(...)` / `module.Cls(...)` where `module` is a packaged module, and a `**name` unpack resolved statically "
  "when `name` is a local dict literal with constant-key stores (this is what reads the adapter's `Enforcer(**render)` split). Last line ends `attr_checked=<k> attr_mismatched=<m>`." % (ATTR, sha(ATTR)))
w("- `%s` (sha256 prefix `%s`) -- the METHOD-call limb (AMENDMENT 2; CTO half AMENDMENT 7): `obj.method(...)` checked against EVERY packaged class method of that name; "
  "last line `method_call checked=<k> ... mismatched=<m>`. Its negative control is the rev-5 pairing (HEAD `repository.py` 2aa217ec58 with the older `retention.py` 80a79a7462): **2 mismatches, "
  "`.reference(4 positional)` against `RetentionPolicy.reference(owner,family,logical_id)`**, exactly the live rev-5 failure." % (METHOD, sha(METHOD)))
w("- `replay/method_call_runner_416.py` -- the dynamic METHOD-call arm, in the replay section below; `replay/live_call_runner_416.py` -- the call sites row D2-S60 names.")
w("- the LIVE-CALL arm of the release-1 half AMENDMENT 5 (one GET answering 200 within a minute of the promote), in its own section below.")
w("")
w("| function | pin / tree | built sha256 (CodeSha256 form) | live sha256 | built twice identical | live: name / attr / method mismatches | built: name / attr / method mismatches | attr calls checked (built) | untested import pairings live -> built | bytes |")
w("|---|---|---|---|---|---|---|---|---|---|")
for fn in ORDER:
    r = F[fn]
    w("| `%s` | `%s` / `%s` | `%s` | `%s` | %s | %d / %d / %d | **%d / %d / %d** | %d | %d -> %d | %d |" % (
        fn, PIN[:10], TREE[:10], r["built_sha256"], r["live_sha256"], "YES" if r["built_twice_identical"] else "NO", r["live_signature_mismatched"],
        r["live_attribute_mismatched"], r["live_method_mismatched"], r["built_signature_mismatched"], r["built_attribute_mismatched"], r["built_method_mismatched"],
        r["built_attribute_checked"], r["live_untested_import_pairings"], r["built_untested_import_pairings"], r["built_bytes"]))
w("")
w("Last lines of the instruments on each built zip:")
for fn in ORDER:
    w("- `%s`: `%s` | `%s`" % (fn, F[fn]["built_last_line"], F[fn]["built_method_last_line"]))
w("")
w("Negative control (the live zips): ")
for fn in ORDER:
    w("- `%s`: `%s`" % (fn, F[fn]["live_last_line"]))
w("")
w("The adapter's Enforcer split reads on the attribute limb alone (the name limb on the live adapter reports only `InteractiveAccess(profile_reader=)`); the live narrative also reads "
  "`enforce.Request(path_ids=)` on the attribute limb (row `IRPT_BCKEND-D2-W278-S5`). The live irpt-status (rev 3) reads the `profile_reader` split on the name limb. "
  "**The untested import pairings column is `pin_coherence.py`'s skew count** (`%s`, run on the real map at box/dell2 for the live column, on the candidate map for the built column; "
  "live irpt-status: %d): a pairing nobody has run is a skew; one tree leaves %d, %d and %d." % (
      "IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/checks/r2/pin_coherence.py", s["live_untested_import_pairings"], a["built_untested_import_pairings"],
      F["irpt-narrative"]["built_untested_import_pairings"], s["built_untested_import_pairings"]))
w("")
w("The built zips were built twice with `TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate> BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>` "
  "from a tree whose investor-reporting paths are committed, and are byte-identical across the two runs; the zips stay in scratch, outside the worktree.")
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
    rp = r.get("repins") or []
    w("- **Re-pins (%d rows; %d change the packaged bytes):**" % (len(rp), sum(1 for x in rp if x["bytes_changed"])))
    for x in rp:
        w("  - `%s`: %s -> %s (`%s` -> `%s`)%s" % (x["member"], x["old_pin"][:10], x["new_pin"][:10], x["old_sha256_prefix"], x["new_sha256_prefix"], "" if x["bytes_changed"] else " [pin only, same bytes]"))
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
        w("- **Order:** this apply waits on IRPT_ANLREQ release 1 (2.0.0_SA_COO~Y2). Apply it only with or after that pair.")
        w("- **Two after-reads for the apply leg (AMENDMENT 3), both run by `~G2` in an sr1 window, with the 5xx and TypeError counts of the R3 read printed beside them:**")
        w("  1. REQ-5e4149d2's owner read (status-job + analysis-report) answers with **no RetentionRefused and no TypeError**;")
        w("  2. one GET `.../analysis/requests/{id}/original` answers, and **the count stays 1** (the read does not write).")
        w("- **Release 1's last two irpt-status reads are deferred to this build** (they cannot run on rev 3, which lacks the reader members).")
    w("")
w("## Blast radius")
w("")
w("- **Functions:** irpt-performance-adapter, irpt-narrative, irpt-status; no other function, layer, IAM, route, schedule, environment or table changes.")
w("- **Members:** the per-function lists above. Shared code in the repo is unchanged by this cell (the cell edits no product source); the packaged bytes are the blobs of commit `%s`." % TREE[:10])
w("- **Effect on served bytes:** the adapter's `performance-report` stops failing on `Enforcer(load_report_owner=)` (it reaches the Enforcer with the retained-owner port, as IB-pr-293 intended); "
  "the narrative's prospect path stops raising on `guard_prospect(authorize_owner=, resolve_owner=)` and `enforce.Request(path_ids=)` fits; the status internal-caller CREATE path stops raising on "
  "`InteractiveAccess(profile_reader=)`; irpt-status serves the owned-history readers of release 1 on one consistent set. Authorization decisions on the arms below are identical live vs built "
  "except where an arm is marked expected-diff and names the live TypeError.")
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
w("AMENDMENT 2 grades each build by a REPLAY OF EVERY ROUTE plus the LIVE-CALL arm plus a METHOD-call arm. Each tree is extracted (`python -I`, flat layout, the function's live layers beside it) and the zip's own "
  "`entry.ENTRY` is driven by IB-pr-409's `authz_case_runner.py` (unchanged: every route of the function, six binding cases each), `replay/scope_runner_416.py` (row D2-S48's method, route per host), "
  "`replay/live_call_runner_416.py` (the three split call sites: the LIVE-CALL arm at the code level) and `replay/method_call_runner_416.py` (the METHOD-call arm: the real Entry's `handle` called for EACH route, "
  "two principals, synthetic event, in-memory fake clients, a `sys.settrace` hook that records every call-arity TypeError raised in the zip even when the code catches it). The NEGATIVE CONTROL tree is the built tree with "
  "`interactive_access.py`, `prospect.py` and `enforce.py` put back to the LIVE bytes. Verdicts are exactly `identical` or `expected-diff`: %d arms, none UNEXPECTED." % len(rep["arms"]))
w("")
w("| function | arm | verdict | negative control | detail |")
w("|---|---|---|---|---|")
for fn in ORDER:
    for x in rep["arms"]:
        if x["function"] == fn:
            w("| `%s` | %s | %s | %s | %s |" % (fn, x["name"].replace("|", "/"), x["verdict"], "yes" if x["negative_control"] else "no", x["detail"].replace("|", "/")))
w("")
w("Reading the arms: the **no-row-internal** arm (`no_row_internal_enforcer_scope`) is identical live vs built on all three hosts (the narrative classes UNKNOWN as on its live 409 build; the adapter and "
  "status class OPAL_GLOBAL on both sides, unchanged by this cell). The **prospect** arms show the live TypeError where the call site has the split and none on built; the narrative's "
  "internal-caller prospect arms read ModuleNotFoundError on BOTH sides because that zip packages no `interactive_access.py` (row `IRPT_BCKEND-D2-W278-S4`, INERT: the host declares no prospect or owner-read mode). "
  "The **enforcer build** arm shows the adapter's and the narrative's live TypeError on `load_report_owner` and the built Enforcer constructed. The **method-call** arms show 0 call-arity errors on every built route; "
  "the live narrative and adapter read arity errors there (the negative control), and the live irpt-status (rev 3) reads 0, as it carries no split of that class.")
w("")
w("**Limits of the method-call arm, stated:** the stores are in-memory fakes that answer empty or not-found, so the call goes as deep as an empty store lets it (`functions_entered` in each detail cell counts the distinct functions of the zip entered); "
  "the narrative and adapter built routes stop at `FIRM_BINDING` for the synthetic principals before compute, so their Enforcer build is covered by the `enforcer build` arm and the static limb, not by the route call. "
  "The static method-call limb (0 mismatches on every built zip, 2 on the rev-5 pairing control) is what catches the `.reference(...)` class without seeded data. ABSENT != EXERCISED-AGAINST: this packet does not claim the retained-record paths ran on real rows.")
w("")
w("## The live-call arm (IRPT_ANLREQ release 1 half AMENDMENT 5, CTO msg 3732)")
w("")
w("Carried beside the zip census, unchanged in meaning: *a LIVE-CALL arm sits before the ledger closes: ONE real GET answering 200 on a non-49F request within a minute of the promote; a 500 means "
  "immediate Branch B.* It is standard in the CTO seat's halves for every served Lambda release. Per function, rerun at apply (UNEXERCISED until then; ABSENT != EXERCISED-AGAINST):")
w("- `irpt-performance-adapter`: one GET `/api/scoped/investor-reporting/performance/{accountSetId}` as a caller outside the 49F case; expect a typed answer, never 500 and never `TypeError` in the group. "
  "Branch B is the hold above (there is no previous version to promote), so a 500 means STOP and escalate, not a re-promote.")
w("- `irpt-narrative`: one GET `/api/scoped/investor-reporting/narrative/{reportId}` as a firm user; expect 200 or a typed refusal, one `irpt_error` line at most and no `TypeError`; a 500 means immediate Branch B.")
w("- `irpt-status`: one GET `/api/scoped/investor-reporting/status` for a non-49F caller within a minute of the promote; a 500 means immediate Branch B; PLUS the two after-reads named in its section (REQ-5e4149d2's owner read; one GET `/original`, count stays 1). Do not start until IRPT_ANLREQ release 1 has cleared.")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W278-S1` (the one tree is 361c44fa9d; what rides is named; INERT), `-S2` (source map not edited, candidate map in deliverables; ARMED, 2.0.0_SA_COO~P2), "
  "`-S3` (live irpt-status is rev 3 and still carries the `profile_reader` split; the release-1 after-reads are deferred to this build; INERT), `-S4` (irpt-narrative packages no interactive_access.py; INERT), "
  "`-S5` (attribute limb also reads enforce.Request(path_ids=) on live narrative; the red list now reads 2 failed; INERT), `-S6` (the method-call arm is an instrument this order did not specify beyond one sentence; its limits; INERT).")
w("")
w("Files beside this packet: `IB117-1_signature_census.json`, `IB117-1_replay.json`, `IB117-1_red_list.json`, `IB117-1_adapter_refusals.json`, `candidate_source_map.json`, "
  "`signature_closure_attr.py`, `method_call_limb_416.py`, `pin_coherence_candidate_416.py`, and the writers (`make_candidate_map.py`, `make_census_416.py`, `make_packet_416.py`, `cw_refused_count_416.py`, `replay/`).")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK:", D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md", len("\n".join(L)))
