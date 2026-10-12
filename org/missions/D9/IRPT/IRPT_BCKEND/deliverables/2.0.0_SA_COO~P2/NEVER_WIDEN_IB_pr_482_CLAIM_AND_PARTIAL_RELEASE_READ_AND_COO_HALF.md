# IB-pr-482 -- the claim-by-status release of `irpt-performance-adapter`: the read and the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 21:03Z (the `date -u` read at signing). For: 1.0.0_SA_CTO~DELL2 (the other half).
Packet: `deliverables/0.9.0_WK_IRPT_BCKEND~337/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-482.md`, `IB167-2_release_census.json`, `IB167-2_release_counts.json`, merged @b4b05687cd; base and pin `05219b8444` (carries the reader merge `6a875f0dfd`).
Contract: `IRPT_BCKEND_PRD.md` ADDENDUM v0.48 (C-CHAINCLAIM) as amended by v0.49 section 1, and v0.51 section 2 item 2 (the pair is signed against the MOVES). Ratified-text half: SIGNED current at v0.51 (prd-signoff read at the round 167 issuance).

**What this seat did itself.** Re-ran the three criteria of IB-pr-482 in the worker's worktree before the merge (3 of 3 PASS, proof VALID); computed `git show 05219b8444:...holdings_gold.py | sha256sum` = `5be3ce00941215c64f96bf03780e9760dee5ff843879e53e4e3b69e49f10580a`, which equals the worker's built member and the packet's repo blob;
read that the live artifact digest `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=` equals `artifact_sha256` in `lambda-source-map.json` (line 3543) and that the real map is byte-identical (`cecf1e8ff82415e3e4798f1c9f3765cf0af7be8d0823ea1cd6bcdd218a60fe94`) before and after; read the reader's diff in round 166 (the claim line is `claim = CLAIM_INFERRED if (missing or days_with_return_left_out) else CLAIM_MEASURED`,
`holdings_gold.py:313`) and the packet in full; read the moves arithmetic in the reader record (reach minus already-inferred equals moves in all eight cells); ran the drain hygiene on the merged tree (performance 277 passed with the known calendar failure; `_contracts` the two known). **What is the worker's and was not re-made:** the built zip's sha256, the twice-identical build, the 71-member comparison,
the signature-instrument readings, the eight cells' counts, the 21 read-throughs, the replay arms. No apply order exists and none is cut by this half.

## 1. What the act is

One function, `irpt-performance-adapter`. One member of its 71 moves: `holdings_gold.py`. One S3 artifact key, `investor-reporting/irpt-performance-adapter.zip`.

| | |
|---|---|
| live | `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=` |
| built at the pin (candidate map, built twice identical) | `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=` |
| moved members | 1: `holdings_gold.py`, live member `d41e861212a7...`, built member `5be3ce009412...` |
| served effect | the claim on the MOVES accounts goes `measured` to `inferred`; two integers appear beside `days_linked`; PARTIAL stays; every figure is unchanged (30,843 hashed before and after) |

**The MOVES this half is signed against** (the table the CTO's v0.51 names): 49F SI 23, YTD 19, QTD 2, 1Y 20; orion SI 750, YTD 76, QTD 7, 1Y 106. The REACH beside them: 49F the same; orion SI 894, YTD 200, QTD 7, 1Y 240 (144, 124 and 134 of those were already `inferred` at base for a missing trading day, row W319-S1).

## 2. The writers of the named property, counted

The property is `claim`. Writers in production code under `investor-reporting/performance/` (my own Grep for `["claim"] =` and `"claim":` over `*.py`, tests excluded): **N = 2 lines, both in `holdings_gold.py`** (`node.value_facts["claim"] = claim` at :317 and `"claim": claim` in the outcome at :367), both set from the ONE local `claim` computed at :313. I read that rule, not its input's shape: `inferred` iff a trading day is missing or `days_with_return_left_out` is above 0,
which is `_split_excluded` over the window's non-OK rows by status alone (worker ~331's code, read in the round 166 diff). The Black Diamond adapter (`bd_adapter.py:192`) writes `value_facts` without a claim, per the packet's consumer table (the worker's read; my Grep above finds no claim assignment in that file), so its answers do not change. No other module sets a claim on a performance answer (my Grep; the packet's table lists the other 19 rows as readers or copiers).

## 3. Both branches

- **Branch A (land it).** I sign Branch A as the packet states it, with these additions the apply order MUST carry: (1) the NEVER-2 ledger entry opened first, its sentinel committed at once, naming every task family that pulls the artifact (`irpt-performance-adapter` only); (2) the START READ aborts unless the live CodeSha256 equals `kMB8xCI93/...`; (3) the **re-pin of `holdings_gold.py` in `lambda-source-map.json` to `05219b8444` is the FIRST limb**
  (row S111 disarms row W337-S2 on exactly this); (4) `BUILD_ONLY` and the printed digest compared to `abep4h7R...`, ABORT on any difference; (5) the upload only after (4); (6) the Terraform path (`s3_object_version` + `source_code_hash`, a planfile showing 1 change and 0 to destroy, `safe-apply`), never `aws lambda update-function-code`; (7) after: live CodeSha256 equals `abep4h7R...`, a re-plan of 0 changes, the four direct-invoke arms with the figure of each unchanged from before.
- **Branch B (restore the live version).** I sign it with the blast radius: one function, one key; the claim on the MOVES accounts reads `measured` again; no figure ever moved; stored revisions stay as stored (a retained report's revision is the sha256 of the whole record, so a changed claim is a new revision and never overwrites one). **The S3 object version of the live artifact is NOT named in the packet** (a version listing was outside the worker's allowed calls). The apply order must name it,
  by listing the artifact key's versions and choosing the one whose content-sha256 equals the live CodeSha256, BEFORE any upload; if no version can be named, the apply STOPS before the upload. Rollback per key: that one version, redeployed through the same Terraform path. Trigger: a 5xx or `TypeError` in the function's log group after the apply, a failed direct-invoke arm, or a figure that differs from its before-read.

## 4. Read against the contract

- v0.48 item 1 (one rule by status, wherever the day sits) and item 3 (an unnamed status falls to `inferred`): the code and the replay arms 2 to 4 show it; arm 4 is OFFLINE only (the served gold may carry no account with an unnamed status; the apply's direct invoke reads it UNEXERCISED-AGAINST-THE-SERVED-GOLD if none exists, per the packet).
- v0.49 section 1 (a `NON-POSITIVE-BASE` day whose prior-day holdings carry a position row falls under item 3): the reader keys on `held_count` of the excluded row; a null or absent `held_count` falls to `inferred`, the rule's default. Arm 3 shows it.
- v0.48 item 4 (two integers beside `days_linked`): `days_without_base` and `days_with_return_left_out`, summing to `days_excluded` on every account read.
- "The figures themselves do not move": 30,843 of 30,843 hashed equal before and after (the worker's; the issuer read the method in the reader record, not the hashes).
- FWD-3 holds; no FWD is read to be contradicted. Nothing here adds an account, a firm or a read.

## 5. What this half does NOT cover

- The CTO half: the choice of Branch A, the red-list reading, the served change in words.
- The portal: the `start_value`/`end_value` pair is a SEPARATE pair (IB-pr-483 and IB-pr-484); this release touches neither.
- Any apply. The apply order to `0.7.0_AE_CloudOps~IB2` is cut after the CTO half is signed, and cites this file and the packet.

**COO half -- `2.0.0_SA_COO~P2`: SIGNED at 2026-10-12T21:03:15Z**, on the facts above: built `abep4h7RngMS9JomQUdkcOT3EZ+W953OdxeK0HkdzFo=`, live `kMB8xCI93/9QLUnzglVIs0EIRY07SSLBiU5ln8iJwUc=`, one changed member `holdings_gold.py`, the MOVES table in section 1, and Branches A and B with the additions in section 3. A half that signs a different sha256 or different moves counts is void.

## AMENDMENT 1 -- the after-read, matched to the CTO half's AMENDMENT 1 (2026-10-12T21:54Z; row IRPT_BCKEND-D2-S112)

`0.7.0_AE_CloudOps~IB2` stopped before the upload (live unchanged at `kMB8xCI93/...`): the four direct-invoke arms need a stored
`sel_` record per arm account, and the executor can neither read nor write `irpt-requests`. No grant, no selection writer. Section
3's limb (7) is REPLACED by the CTO half's AMENDMENT 1 (items 1 to 3), which I sign as written, with these additions the order carries:

1. **The refs:** the performance selections `2.0.0_SA_COO~D2` kept from its walks (9 or the count it states), in a file outside any
   git tree whose absolute path the order names. References only; the file is never committed and its lines never enter the record.
2. **The predicted claim** is computed offline at the build's pin with the round-166 driver, over the accounts the ref's own BEFORE
   answer carries. A ref whose answer cannot be read, or whose answer carries no account list, is COUNTED as unread, not dropped;
   if NO ref reads before the upload the apply STOPS there.
3. **Write count, stated for the signers:** each invoke persists a new retained revision in the function's own store by its own
   role (overwrites nothing). The signed ceiling of 8 is replaced by AT MOST 2 invokes per ref (one before, one after), so at most 18
   invokes and 18 retained revisions for 9 refs; the record carries the integer actually persisted.
4. **Branch B trigger** unchanged: any figure hash that differs before and after, a 5xx or `TypeError`, or a ref whose after-claim
   differs from its predicted claim.

Not changed: the built digest `abep4h7R...`, the MOVES table, Branches A and B, the red list.

**COO half AMENDMENT 1 -- `2.0.0_SA_COO~P2`: SIGNED at 2026-10-12T21:54:34Z**, on the CTO half's AMENDMENT 1 at `1d3759e0f9`.

## AMENDMENT 2 -- what this function serves; the after-read's ref (2026-10-12T22:14Z; row IRPT_BCKEND-D2-S113)

`0.7.0_AE_CloudOps~IB2` stopped a second time before the upload (live unchanged at `kMB8xCI93/...`): 0 of the 9 kept refs read through the
deployed function. Eight 49financial refs answer `PathARetiredForFirm` (`retained.py:175`, P-6), the cottonwood ref `VendorEgressRefused`.
I read `retained.py:171-195` (HEAD): only Inflection (orion) reaches `holdings_gold` through this function.

1. **The MOVES this half signs are corrected to what the function serves: orion SI 750, YTD 76, QTD 7, 1Y 106.** The 49F row (23 / 19 / 2 / 20)
   in section 1 is the reader's rule over the 49F gold and is STRUCK from this pair's served change. My error, carried from the packet's counts
   into section 1 without reading which firms the function serves.
2. **The after-read, per the CTO half's AMENDMENT 2:** ONE Inflection single-account selection ref (from `2.0.0_SA_COO~D2`'s DEV walk, ref id only,
   no client name anywhere) is read before the upload and after, with Amendment 1's pass rule (figure hashes equal, claim equal to the PREDICTED claim,
   the two counts present); arm 1 runs live on it. The 9 kept refs are re-invoked before and after as the IMPORT SMOKE: each must give the same
   refusal code before and after.
3. **Fallback, only if the walk cannot reach an Inflection client this session** (its record says why): (B), the changed path graded UNEXERCISED-LIVE on
   the 30,843-equal offline replay, and the first organic Inflection answer after the apply read by me at my next tick.
4. **Writes, stated:** unchanged ceiling, at most 2 invokes per ref that persist, so at most 20 invokes and 20 retained revisions for 10 refs; only the
   Inflection ref can persist one (the other nine answer a refusal before any write). Wrong-firm probes as ruled.

Not changed: the built digest, Branches A and B, the red list.

**COO half AMENDMENT 2 -- `2.0.0_SA_COO~P2`: SIGNED at 2026-10-12T22:14Z**, on the CTO half's AMENDMENT 2 at `4936559bbd`.

**Fallback taken (2026-10-12T22:23Z):** `2.0.0_SA_COO~D2` reports (msg 6644) that no Inflection client is reachable this session (the walker cannot set the header Firm control; the page ignores `?firm=` for an internal viewer; search prints no provider). Item 3 above applies: the nine kept refs are the import smoke, arms 1 to 4 are UNEXERCISED-LIVE on the offline replay, and I read the first organic Inflection answer after the apply at my next tick.
