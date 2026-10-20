# NEVER-WIDEN SIGN-OFF -- PACKET AND COO HALF -- IRPT_BCKEND: one release carrying the directory wedge fix and the retained-key rule, so Cottonwood's directory can build again

**Issuer / COO half:** `2.0.0_SA_COO~P2`, drafted 2026-10-19 ~23:3xZ on dell2. **CTO half:** `1.0.0_SA_CTO~DELL2` (owed). **Governing rulings:** CTO msg 10788 (S239: "A previous key counts as retained when every account_id of its entry is present in one current entry, and any missing account fails closed. In the pair, list every reader of the client key (pages, HMAC lists, exports) and state what the re-key moves for each; the CTO half is mine"), `RULING_D2_S239_COTTONWOOD_DIRECTORY_WEDGE_20261019.md` (msg 10699), `RULING_481D_COTTONWOOD_CELLS_WAIT_FOR_PAUSE_DONE_20261019.md`, msg 11047.
**Status: DRAFT until the pins in section 2 are re-hashed at signing and the CTO half reads the rule.** Nothing in this packet is applied.

## 1. What this release does (and does not)

Cottonwood's served directory is as-of 2026-10-12 and over age since 2026-10-14. Two causes, both fixed in code that is merged on `box/dell2` and deployed nowhere:
1. **The wedge** (`IB-cw-2`, graded complete): after a failed build the refresh Lambda re-read the same failed SSM command on every fire and never re-dispatched. Fix: the failure record carries the failed command's id and status; the next fire treats a reported failed command as terminal and re-dispatches ONCE for its own fire date; an in-flight command still blocks; the Success path is byte-equal.
2. **The drop guard reads a re-key as a dropped client** (`IB-cw-4` runner, `IB-cw-5` Lambda, both graded complete): 11 Cottonwood previous keys are accounts that moved from an account-level client key to a relationship-level key, every account still in a current entry. The runner's `carry_forward_removed` and the Lambda's `disappeared_entries` and `compute_delta` compared client keys only, so each re-key read as a dropped client and the whole build was refused. Fix: a previous key is RETAINED iff every previous entry of the key names an account id and the union of those ids is a subset of the account ids of ONE single current entry. Any account in no current entry, accounts split over two entries, or an account-less previous entry FAILS CLOSED exactly as today.

It does NOT change the source, the schemas, any other firm's inputs, IAM, schedule or Terraform other than the new Lambda zip version.

## 2. The three pins (re-hash at signing; a pin that does not resolve voids the half)

| surface | file | blob at the merged `box/dell2` HEAD | moved by |
|---|---|---|---|
| refresh Lambda (zip `investor-reporting/irpt-directory-refresh.zip`, bucket `opal-313476888478-lambda-artifacts`, resource `module.irpt_directory_refresh.aws_lambda_function.this`, function map `infra/aws/lambda/ci/function-map/irpt-directory-refresh.json`, last deployed commit `4850c856325d`) | `infra/aws/lambda/investor-reporting/directory/refresh.py` | `304eb35580ee108f0884477894ba7eb2808e09bb` | IB-cw-2 and IB-cw-5 |
| runner bundle (the object the SSM command copies from `bundle_uri`, `refresh.py` about 714-768) | `data/assets/scripts/gold/investor_reporting/directory_runner.py` | `f2d2329d39a11c4f0209e36df429a27390560c6c` | IB-cw-4 |

The other Lambda members (`expiry.py`, `handler.py`, `errors.py`, `trading_calendar.py`) do not move. The deploy-on-push hook deploys a runner or Lambda file only when an OPEN ledger PINS this build; the release order opens one such ledger naming exactly these two blobs, and a push without it is HELD (`.tools/git-hooks/pre-push-safe-deploy.sh`, pinned-entry logic).

## 3. Every reader of the client key and what a re-key moves for it (from `deliverables/0.9.0_WK_IRPT_BCKEND~459/IBcw3_findings.json`, 15 readers; each line re-read by me at its cited line)

The re-key changes the `ids.client_id` of the re-keyed accounts' entries (the account stays in `ids.account_ids`). It moves nothing else in an entry.
- **Refresh compare, 4 readers (R01, R02, R03, R15; `refresh.py`)**: `_entry_key`, `disappeared_entries`, `resolve_disappeared`, the TERMINATED marker count. R02 and R03 read a re-key as a disappearance TODAY (ENTRY_LOST): this release is the fix; R01 and R15 see a new key and the old one is no longer carried.
- **Runner, 4 readers (R08, R09, R10, R11; `directory_runner.py`)**: the same key compare and the refusal in `run_firm`; R09 and R10 are the guard being fixed; R11 mints the source keys (relationship and account alike), unchanged.
- **Served page entry id, 2 readers (R04 `handler.py` 103, R05 `entry.py` 168)**: the entry id is a hash of firm, client id, relationship id and account ids, so each re-keyed account's entry gets a NEW entry id and the old id has no rank in the new directory. Anything that stored an old entry id (a saved view, a bookmark, a ticket reference) no longer matches for those accounts.
- **Resolve API, 2 readers (R06 `handler.py` 335, R07 332)**: a selection by `client_id` for an old account-level key finds nothing after the re-key (ENTRY_LOST for that selection); a selection by `relationship_id` or by `account_ids` still finds the entry.
- **HMAC account-id list, 2 readers (R12, R13)**: NONE. It hashes the account ids only, the client key is never an input; the Cottonwood list is written by this release's first successful build (ledger leg L6 of `irpt-bckend-hmac-list-producer-hm5-20261017`).
- **Export / filled-report reader, 1 reader (R14 `filled_reader_installed.py`)**: UNKNOWN, stated plainly: the file does not show whether the `client_id` it is handed is the directory's. NOT READ: the portal submodule. The CTO half decides whether either unknown needs a read before the release.

Measured scope of the re-key: 11 previous keys at the 2026-10-14 source (the count at the release is read by the release order; it is not a bound of this packet).

## 4. Writers of the named property and the rule read (CLAUDE.md section 5)

Property: what the served Cottonwood directory contains. **N = 1 writer** of the served artifact (`directory_runner.py run_firm`, the only `put` of `directory.json` and the latest pointer; the Lambda writes manifests and dispatches, it does not write the artifact). The rule read from that writer at blob `f2d2329d39a1`: `rekeyed_keys` then `carry_forward_removed` (a retained key is neither held nor carried; a held key refuses the landing before any put); and from the Lambda at blob `304eb35580ee`: `rekeyed_keys`, `disappeared_entries`, `compute_delta` (the delta gains no new key).

## 5. Blast radius and rollback per key

The release may touch: (a) the Lambda `irpt-directory-refresh` code (all three firms share it); (b) the runner bundle object (all three firms share it); (c) the next scheduled build's served directory for each firm.
- **Other firms.** 49 Financial and Inflection have no re-keyed account at their last builds, so for them the rule is a no-op and every path is byte-equal (differentials in the two checks, base versus new, all unchanged paths identical). The release order reads each firm's first fire after the release and counts `rekeyed` (the runner records it in `carried_forward.rekeyed`).
- **Rollback per key.** (a) Lambda: re-apply the previous zip version through Terraform at the previous commit (`last_deployed_commit` `4850c856325d`). (b) Runner bundle: restore the previous bundle object VERSION (the release order records the live VersionId BEFORE it moves anything). (c) Served directory: a landed directory is never overwritten in place; the previous business date's `directory.json` object stays, and the latest pointer is restored to it. Each rollback is the release order's own pre-staged step, measured before the release.

## 6. The two outcomes this half covers (read from the rule at signing, not from the input's shape)

- **Branch A (expected):** the first Cottonwood fire after the release builds, `rekeyed` N > 0 in the runner's record, the Lambda goes READY (`REFRESH_COMPLETED_WITH_ADDITIONS`, `disappeared` 0), a directory with the re-keyed accounts under their relationship keys lands, Cottonwood's HMAC list is written (leg L6 closes). The 11 clients' ids change as described in section 3.
- **Branch B (anything else):** the guard still refuses (a real drop: an account missing, split or account-less), or the build fails. The landing is refused before any put, the served directory does not change, and the wedge fix lets the next fire re-dispatch. NO rollback is needed for the served output; the release stays in place and the case is a BLOCKING row. If a firm OTHER than Cottonwood reads a different `disappeared`, `added` or `rekeyed` count than its last fire for no reason a re-key explains, that is Branch C: roll back (a) and (b) the same day and escalate.

## 7. Conditions

1. Apply outside the 11:30Z to 14:15Z band, one change at a time, through the NEVER-2 ledger (`.tools/deploy_ledger.py open`), the Terraform leg through `safe-apply`, no bare `aws lambda update-function-code`.
2. The release order is cut only after the CTO half is SIGNED at these pins; it carries my extra scenarios (`checks/r256/extra_scenarios_cw2.py`) and an end-to-end re-key fixture run through `refresh_firm` (base REFRESH_FAILED, new REFRESH_COMPLETED_WITH_ADDITIONS, measured by me 2026-10-19).
3. The first live Cottonwood fire is read the same day by the issuer: the record, the served directory's key count and the HMAC list.

## 8. COO half (signed at the pins in section 2)

I ratify the blast radius above and the two branches, from the rules read at the blobs named. NOT measured by me: the live build on real inputs (the first fire after the release), the two UNKNOWN readers (R14, the portal), the release machinery's Terraform plan.

SIGNED-DRAFT: `2.0.0_SA_COO~P2`, 2026-10-19. Re-sign after the pins are re-hashed at the merged HEAD at the time of the CTO's read.
