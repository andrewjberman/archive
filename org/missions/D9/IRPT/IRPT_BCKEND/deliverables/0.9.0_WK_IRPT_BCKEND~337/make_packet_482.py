"""IB-pr-482 packet writer (form of IB-pr-409's and IB-pr-416's). From the worktree root:
    python -I <this file> <scratch_dir>
Reads IB167-2_release_census.json, IB167-2_release_counts.json and the scratch pytest/red-list text, writes IB167-2_red_list.json and
NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md beside it. Counts, sha256 and reason codes only: no account id, balance, fee or flow. ASCII only."""
import json
import sys
from pathlib import Path

S = Path(sys.argv[1])
D = Path("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~337")
cen = json.loads((D / "IB167-2_release_census.json").read_text(encoding="utf-8"))
cnt = json.loads((D / "IB167-2_release_counts.json").read_text(encoding="utf-8"))
F = cen["functions"][0]
CH = F["changed_members"][0]
BASE = cen["base_commit"]
PIN = cen["pin_commit"]
red_text = (S / "red_list.txt").read_text(encoding="utf-8")
failed = [ln.split("FAILED ", 1)[1].strip() for ln in red_text.splitlines() if ln.startswith("FAILED ")]
summary = [ln for ln in red_text.splitlines() if " passed" in ln or " failed" in ln][-1].strip()
TARGETS = ["infra/aws/lambda/investor-reporting/_contracts/", "docs/contracts/investor-reporting/"]
RED_OPS = ["analysis-request-original"]
members = [CH["repo_path"]]
deliv = sorted(str(p).replace("\\", "/") for p in D.iterdir() if p.is_file())
touch = [p for p in members + deliv if any(p.startswith(t) for t in TARGETS)]
naming = [p for p in members + deliv if any(o in p for o in RED_OPS)]
red = {"pytest_command": "from infra/aws/lambda/investor-reporting/ at the pin: python -m pytest _contracts -rf -q", "pytest_summary": summary, "failed_node_ids": failed,
       "failed_count": len(failed), "red_test_operations": RED_OPS, "target_prefixes": TARGETS, "pin_commit": PIN,
       "changed_member_source_paths": members, "paths_this_cell_changed_vs_base": deliv,
       "changed_paths_touching_a_target": touch, "member_paths_touching_a_target": [p for p in members if any(p.startswith(t) for t in TARGETS)],
       "paths_naming_a_red_operation": naming, "stop": bool(touch or naming),
       "same_two_failures_as": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json (2 failed at 361c44fa9d)"}
(D / "IB167-2_red_list.json").write_text(json.dumps(red, indent=1) + "\n", encoding="utf-8", newline="\n")

W = ("SI", "YTD", "QTD", "1Y")
L = []
w = L.append
BUILT, LIVE = F["built_codesha256_b64"], F["live_codesha256_b64"]
w("# Never-widen sign-off packet -- IB-pr-482: irpt-performance-adapter rebuilt from one pin so the claim follows the excluded day's status (C-CHAINCLAIM)")
w("")
w("Prepared by 0.9.0_WK_IRPT_BCKEND~337 for 2.0.0_SA_COO~P2 (COO half) and 1.0.0_SA_CTO~DELL2 (CTO half), on TO-IB-pr-482 (CTO msg 6517, PRD ADDENDUM v0.51 section 2 item 2; contract C-CHAINCLAIM, ADDENDUM v0.48 as amended by v0.49 section 1). "
  "**Nothing here was uploaded, applied or deployed**: BUILD_ONLY from a committed tree, offline replays on SYNTHETIC frames, AWS reads only (the live zip through `get-function`, and S3 list/get of the served holdings gold up to the cap day 2026-10-08). "
  "No Lambda was invoked, nobody signed in, no vendor was called. No client data is in this packet or its files: counts, sha256 and reason codes only.")
w("")
w("**READ THIS FIRST.**")
w("")
w("1. **The served change, in words.** The holdings-basis reader (`performance/holdings_gold.py`, merged at `6a875f0dfd` by TO-IB-pr-476) now sets `value_facts.claim` by the STATUS of the day left out of the chain, wherever the day sits in the window. "
  "`NO-PRIOR-HOLDINGS`, and `NON-POSITIVE-BASE` on a day whose prior day held no position row (`held_count` 0), are days with no base: a figure chained across them keeps `measured`. "
  "Every other non-OK day (`ALL-HOLDINGS-EXCLUDED`, `IMPLAUSIBLE-RETURN`, `FOLLOWS-DISCONTINUITY`, a `NON-POSITIVE-BASE` day whose prior day held a position row or whose count the gold does not carry, and any status the rule does not name) leaves a return out, and the claim reads `inferred`. "
  "A missing trading day still reads `inferred`, as before.")
w("2. **Two integers are added beside `days_linked`** in `report.optional_facts.value_facts`: `days_without_base` and `days_with_return_left_out`; they sum to `days_excluded` on every account read (%d of %d figures in the eight cells). "
  "The contract admits them (value_facts is an object or null with open members)." % (cnt["figures_compared"], cnt["figures_compared"]))
w("3. **The figures do not move.** The eight cells below were read with the live reader and the reader as built over the same cached partitions: %d figures compared, every cell's figure hash equal before and after (`figures_unchanged` = %s). "
  "Only the claim, and the two new integers, change on the wire." % (cnt["figures_compared"], str(cnt["figures_unchanged"]).lower()))
w("4. **PARTIAL stays.** All three absences (accrual basis, fees and income, money-weighted return) hold on every holdings-basis answer, so `entry.py` keeps choosing PARTIAL from the absences list alone; no byte of `entry.py` changes. The claim and the two integers, not the state, tell a window with a left-out return from one without.")
w("5. **One member changes.** Built against live: 71 members each, **%d member differs: `holdings_gold.py`**; no member is only in one zip; the changed member's built sha256 equals the repo blob at the pin." % len(F["changed_members"]))
w("6. **The source map is NOT edited** (outside this order's grant). The zip is built from `%s` (a map holding only this function, every other key verbatim, ONLY the `holdings_gold.py` pin moved to the pin below) via `BAU_SOURCE_MAP_OVERRIDE`. "
  "The apply order must land that one re-pin into `infra/aws/lambda/ci/lambda-source-map.json` first, or the real-map build reproduces the live bytes and its sha256 will differ from the one signed (row `IRPT_BCKEND-D2-W337-S2`, ARMED, disarm owner `2.0.0_SA_COO~P2`)." % cen["candidate_map"])
w("")
w("## Base, pin and the two zips")
w("")
w("| item | value |")
w("|---|---|")
w("| base_commit | `%s` |" % BASE)
w("| pin_commit (the tree built from, carries `6a875f0dfd`) | `%s` |" % PIN)
w("| function | `irpt-performance-adapter` (the only function whose `staged_from` lists `holdings_gold.py`) |")
w("| built sha256 (CodeSha256 form) | `%s` (hex `%s`, %d bytes) |" % (BUILT, F["built_sha256"], F["built_bytes"]))
w("| live sha256 (CodeSha256 form, `$LATEST`, last modified 2026-10-12T14:11:01Z) | `%s` (hex `%s`, %d bytes; the downloaded `Code.Location` zip hashes to it) |" % (LIVE, F["live_sha256"], F["live_bytes"]))
w("| built twice, byte-identical | %s (second build hex `%s`) |" % ("YES" if F["built_twice_identical"] else "NO", F["second_build_sha256"]))
w("| real `lambda-source-map.json` sha256 before / after the builds | `%s` / `%s` (%s) |" % (cen["real_source_map_sha256_before"], cen["real_source_map_sha256_after"], "byte-identical" if cen["real_source_map_sha256_before"] == cen["real_source_map_sha256_after"] else "CHANGED"))
w("| changed members vs live | 1 of %d: `holdings_gold.py` |" % F["members_built"])
w("")
w("| changed member | built member sha256 | repo blob sha256 at the pin | live member sha256 |")
w("|---|---|---|---|")
w("| `%s` | `%s` | `%s` | `%s` |" % (CH["name"], CH["built_member_sha256"], CH["repo_blob_sha256_at_pin"], CH["live_member_sha256"]))
w("")
w("Signature instrument `deliverables/0.9.0_WK_IRPT_BCKEND~278/signature_closure_attr.py` (both limbs, run at its own path on each zip's own bytes):")
w("- built: `%s`" % F["built_instrument_last_line"])
w("- live (the negative-control context): `%s`" % F["live_instrument_last_line"])
w("Both zips read 0 signature and 0 attribute mismatches, which is expected: only one non-signature member differs, and no call into it changed shape. The tests of the pin: `test_chain_claim.py` with `test_partial_only_when_absence_holds.py` 23 passed.")
w("")
w("## The MOVES, with the REACH beside them (per firm and window; cap day %s; counts taken at the pin `%s`)" % (cnt["latest_landed_day"], PIN[:10]))
w("")
w("The REACH is the accounts the new rule applies to (`days_with_return_left_out` above 0). The MOVES are the accounts whose served claim actually goes `measured` to `inferred` (measured with the live reader, inferred with the reader as built). "
  "The difference is accounts already `inferred` at base for a missing trading day (row `IRPT_BCKEND-D2-W319-S1`); for those the figure and the claim read the same before and after. "
  "**The pair is signed against the MOVES (column 4), not the reach.**")
w("")
w("| firm entry | window | REACH (rule applies) | **MOVES (measured -> inferred)** | already inferred at base | accounts with a figure | partitions read |")
w("|---|---|---|---|---|---|---|")
for e, nm in (("49F", "49F entry"), ("orion", "Orion (Inflection) entry")):
    for win in W:
        w("| %s | %s | %d | **%d** | %d | %d | %d |" % (nm, win, cnt["rule_reach"][e][win], cnt["claim_moves"][e][win], cnt["already_inferred_at_base"][e][win],
                                                          cnt["figures_compared_per_cell"]["%s/%s" % (e, win)], cnt["partitions_read"][e]))
w("")
w("These equal the CTO's numbers (v0.49 reach; v0.51 moves: 49F 23, 19, 2, 20; orion 750, 76, 7, 106) in all 16 cells. Partitions: 49F listed 567, 566 used (<= 2026-10-08); orion listed 1620, 1619 used. "
  "Accounts the reader refuses are the same before and after in every cell (`refusals_differ` 0). No `inferred` -> `measured` move occurs (%d). The claim counts per cell, base then after, are in `IB167-2_release_counts.json` (`claim_at_base`, `claim_after`)." % cnt["accounts_inferred_to_measured"])
w("")
w("## Branch A -- land it (digest-gated, never a mint)")
w("")
w("1. Open the NEVER-2 ledger entry first (`.tools/deploy_ledger.py open ...`) and commit its `.open_deploys` sentinel at once; it names EVERY task family that pulls this artifact (`irpt-performance-adapter` only, one `describe-task-definition`-style sweep of `staged_from` users: no other function lists `holdings_gold.py`).")
w("2. **START READ:** `get-function-configuration` CodeSha256 must equal the live value above (`%s`); anything else: STOP, no apply." % LIVE)
w("3. Land the single re-pin (`holdings_gold.py` -> `%s`, sha256 `%s`) into `infra/aws/lambda/ci/lambda-source-map.json` (the candidate map's `_repins_IB_pr_482` row is the exact edit), from a clean tree at the pin or a descendant whose `performance/` tree is unchanged." % (PIN, CH["built_member_sha256"]))
w("4. `BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-performance-adapter` and compare the printed sha256 to `%s`. **ABORT on any difference: never upload a different digest than the one signed, never mint a new artifact in place of it.**" % BUILT)
w("5. Then the same without BUILD_ONLY (upload), then the module's Terraform path (`infra/aws/terraform/investor-reporting/performance`, `s3_object_version` + `source_code_hash` only, plan to a planfile showing 1 change and 0 to destroy, apply with `bash .tools/safe-apply.sh`). No IAM, route, schedule, layer, environment or table change.")
w("6. **After:** live CodeSha256 equals `%s`; re-plan shows 0 changes; the census for the function shows `changed_members=0`; the direct-invoke proof below; close the ledger entry." % BUILT)
w("")
w("## Branch B -- restore the live version")
w("")
w("- **What is restored:** the live code, CodeSha256 `%s` (hex `%s`), last modified 2026-10-12T14:11:01Z. It equals the `artifact_sha256` of the source map at HEAD." % (LIVE, F["live_sha256"]))
w("- **Named and re-read at apply:** the S3 object version of `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-performance-adapter.zip` whose `content-sha256` metadata equals that CodeSha256 is NOT read here (an S3 version listing of the artifact bucket is outside this order's allowed AWS calls). "
  "The apply worker names it at step 1 of Branch A, BEFORE any upload, writes it into the ledger entry, and re-reads at restore time that `get-function-configuration` CodeSha256 is still the built value and that version is still addressable.")
w("- **Rollback per key:** one key, `investor-reporting/irpt-performance-adapter.zip`: redeploy that S3 version through the same Terraform path (`s3_object_version` + `source_code_hash`), never a console edit and never `aws lambda update-function-code`; then CodeSha256 equals the live value above and the re-plan is 0 changes. "
  "Nothing else is moved by the apply, so nothing else is restored: no table, route, IAM or layer.")
w("- **What the restore does to served values:** the claim on the MOVES accounts reads `measured` again; the figures never moved. **Stored revisions stay as stored**: a retained report's revision is the sha256 of the whole record (`repository.py:202`), so a record written with the new claim is a new revision and overwrites nothing; the restore removes none and needs none removed.")
w("- **Trigger:** a 5xx or `TypeError` in the function's log group after the apply, a direct-invoke arm below that fails, or a figure that differs from its before-read: restore at once.")
w("")
w("## The ADDENDUM 18 red list")
w("")
w("`pytest _contracts -rf` from `infra/aws/lambda/investor-reporting/` at the pin: **%s**. The FAILED node ids (%d):" % (red["pytest_summary"], red["failed_count"]))
for nid in failed:
    w("- `%s`" % nid.replace("\\", "/"))
w("")
w("Same two as `0.9.0_WK_IRPT_BCKEND~278/IB117-1_red_list.json` (2 failed at `361c44fa9d`). Their targets are the response contract and fixture of `%s`. This cell's changed member is `%s`; this cell changed %d paths vs its base, all under its deliverables folder. "
  "Intersection with the red tests' target surface (%s) and with any path naming a red operation: **%d changed, %d member, %d naming** -- STOP = **%s**. The packet does not cite \"suite green\"." % (
      ", ".join(RED_OPS), CH["repo_path"], len(deliv), ", ".join("`%s`" % t for t in TARGETS), len(touch), len(red["member_paths_touching_a_target"]), len(naming), "yes" if red["stop"] else "no"))
w("")
w("## The replay arms (offline, SYNTHETIC; the four frames of `performance/tests/test_chain_claim.py`; built zip's `holdings_gold.py` against the live zip's, each imported from its extracted zip)")
w("")
w("| arm | built claim | live claim | built days_without_base / days_with_return_left_out | figure built = live | verdict |")
w("|---|---|---|---|---|---|")
for a in F["replay_arms"]:
    w("| %s | %s | %s | %s / %s | %s | %s |" % (a["arm"], a["built_claim"], a["live_claim"], a["built_days_without_base"], a["built_days_with_return_left_out"], "yes (%s)" % a["figure_built"] if a["figure_verdict"] == "identical" else "NO", a["verdict"]))
w("")
w("The figure of every arm is `identical`; the claim arms 2 to 4 are `expected-diff` (live `measured`, built `inferred`); arm 1 keeps `measured` and differs only by the two new integers on built. Instrument: `deliverables/0.9.0_WK_IRPT_BCKEND~337/replay_arms_482.py`.")
w("")
w("## The consumers of the claim and the state, each with one read-through (%d)" % len(cnt["consumers_read_through"]))
w("")
w("The 11 backend consumers of `IB166-1_reader_record.json`, the backend and portal readers of `IB166-4_value_facts_readers.json`, and what the census here added (the narrative's own claim strings, the 49F gold's own `days_linked`, the portal tile and the holdings snapshot's claim). Cites resolve at the pin; the full text is in `IB167-2_release_counts.json`.")
w("")
w("| cite | reads | read-through |")
w("|---|---|---|")
for c in cnt["consumers_read_through"]:
    w("| `%s` | %s | %s |" % (c["cite"], c["reads"].replace("|", "/"), c["read_through"].replace("|", "/")))
w("")
w("No consumer reads the claim to change a decision: `entry.py` reads the absences only, the portal reads value_facts only for the window and the two value members, and every other path carries the claim as data.")
w("")
w("## Direct-invoke proof, to run AFTER the apply (by `0.7.0_AE_CloudOps~IB2`, not by this worker)")
w("")
w("The instrument is the one already signed for this function family: a direct `aws lambda invoke` of the DEPLOYED function with an API-shaped event for an Opal principal, using the function's own role (CTO ADDENDUM 3 path 1, as TO-IB-pr-368 used it), no new grant, a READ operation only. The same four arms:")
w("1. an account whose only excluded days are no-base days (`NO-PRIOR-HOLDINGS` or `NON-POSITIVE-BASE` with `held_count` 0): claim `measured`, `days_without_base` > 0, `days_with_return_left_out` 0;")
w("2. an account with an `ALL-HOLDINGS-EXCLUDED` day: claim `inferred`, `days_with_return_left_out` > 0;")
w("3. an account with a `NON-POSITIVE-BASE` day whose prior day held a position row: claim `inferred`;")
w("4. an unnamed status: claim `inferred`. The served gold may carry no account with an unnamed status; if none, arm 4 stays the offline replay above and the packet reads it UNEXERCISED against the served gold (ABSENT != EXERCISED-AGAINST).")
w("Each arm is read BEFORE the apply (same shape, persisting nothing) and AFTER: the **figure of each is unchanged from before** (equal to the last digit; record the sha256 of the figure, not the figure), and the claim moves as stated. Account ids stay in the invoker's scratch and out of the repo. "
  "The apply order must name which read operation the invoke uses and whether it persists: the fresh path persists a retained report (`retained.py:318`), a persisted record carrying the new claim is a new revision and overwrites nothing, and a persist is a write the signer must see named, not assumed absent.")
w("")
w("## Blast radius")
w("")
w("- **Function:** `irpt-performance-adapter` only; no other function, layer, IAM, route, schedule, environment or table changes. **Member:** `holdings_gold.py` only (1 of %d)." % F["members_built"])
w("- **Served effect:** on the MOVES accounts the claim reads `inferred` where it read `measured`; the two integers appear on every holdings-basis answer; PARTIAL stays; every figure is byte-for-byte the same number.")
w("- **Never-widen:** this MOVES a served value (the claim), so it ships only under the pair below. It widens nothing: no account is added to any set, no firm gains a read, no state changes.")
w("")
w("## The pair")
w("")
w("Both halves sign the same facts: built `%s`, live `%s`, one changed member `holdings_gold.py`, and the MOVES table above (the table the pair is signed against). A half that signs a different sha256 or different moves counts is void." % (BUILT, LIVE))
w("")
w("- **COO half -- `2.0.0_SA_COO~P2`:** signs that the moves counts equal the CTO's v0.51 item 2 and that the apply order will carry the Branch A digest gate and the Branch B restore named above. Signed: ______________________  at: ____________")
w("- **CTO half -- `1.0.0_SA_CTO~DELL2`:** signs the served change in words, the red list reading, and the choice of Branch A. Signed: ______________________  at: ____________")
w("")
w("## Rows")
w("")
w("`IRPT_BCKEND-D2-W337-S1` (the order names a READ file beside the reader record; the folder holds none; INERT), `IRPT_BCKEND-D2-W337-S2` (the source map's `holdings_gold.py` pin is stale until the apply order lands the re-pin; ARMED, disarm owner `2.0.0_SA_COO~P2`).")
w("")
w("Files beside this packet: `IB167-2_release_census.json`, `IB167-2_release_counts.json`, `IB167-2_red_list.json`, `candidate_source_map_482.json`, and the writers (`make_candidate_map_482.py`, `replay_arms_482.py`, `make_records_482.py`, `make_packet_482.py`).")
(D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("OK:", D / "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md", len("\n".join(L)), "red", summary, "stop", red["stop"])
