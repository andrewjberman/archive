# IRPT_BCKEND: remediations, round 117 (workstream ~P) -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T03:53:39Z. L8 input: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)`.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order in the workstream is not terminal
(`TO-IB-pr-420`, round 118, is issued). These 5 rows land in `surprise-channel/remediations/`, with the L10 slug, when it is.
OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: TO-IB-pr-420 terminal.

```text
[
 {
  "id": "IRPT_BCKEND-D2-S60",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "ARMED",
  "mechanism": "The live irpt-status, irpt-performance-adapter and irpt-narrative zips carry keyword splits between served.py and the packaged modules. The calls fail closed with a TypeError; IB-pr-419 read irpt-performance-adapter as failing on performance-report. Round 117 rebuilt all three and applied none.",
  "evidence": [
   "investigation rows IRPT_BCKEND-D2-S60, D2-S61, D2-W281-S1",
   "this seat's live reads 2026-10-11T03:53:39Z: irpt-performance-adapter CodeSha256 o/643qVE... LastModified 2026-10-09T07:41:59Z; irpt-narrative iEwSFL34... 2026-10-09T14:48:05Z; irpt-status t6OJTCcm... 2026-10-09T18:02:51Z -- none applied since round 117",
   "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)"
  ],
  "remedy": "IB-pr-420 applies the adapter and the narrative under the IB-pr-416 pair, and 2.0.0_SA_COO~Y2 applies irpt-status. The close is the live-call arm at each apply, read by this seat on the served function.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S3",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The live irpt-status zip reads 1 name-limb mismatch; rev 5's RetentionPolicy.reference split is a method call that only the new method-call limb reads.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S3",
   "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)"
  ],
  "remedy": "Closes with D2-S60 at the irpt-status apply. The method-call limb joins the standing closure check so the next split is read before a release.",
  "owner": "2.0.0_SA_COO~Y2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~Y2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S4",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "narrative/entry.py declares no prospect or owner-read modes, so two served handlers are unreachable today; their lazy import of interactive_access would raise ModuleNotFoundError if either mode were configured.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S4"
  ],
  "remedy": "The cell that first configures either mode on irpt-narrative ships interactive_access in the bundle, or the handlers are removed from this host.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S5",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The attribute limb reports an unknown keyword (path_ids) on the live irpt-narrative, cleared in the built zip; pytest _contracts at the pin reads 2 failed against the 9 of IB-pr-409's packet.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S5"
  ],
  "remedy": "The live mismatch closes with D2-S60 at the narrative apply. The issuer states which 2 contract tests fail at the pin and whether the release pair accepts them.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-S62",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "IB-pr-418's AC1 grades against the 49F-only set, so it passes while the all-firm served-id hash list still hits tracked files: 5 in the project tree (3 of them named in the order's paths) and 7 in the investor-reporting Lambda tree, one of which is the shipped seam data file with 10,713 ids.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-S62",
   "this seat's run of the served account-id hash list (29,587 hashes, client-data-check's token rule) at HEAD: IRPT_BCKEND project tree 5 of 2,070 text files hit (1 each: 3 under checks/r19, 1 under checks/r19e, 1 battery file); infra/aws/lambda/investor-reporting 7 of 633 files hit (10,725 hits: _ids/data/custodian_key_seam.json 10,713, _ids/raw_keys.json 2, and 5 test files 10)"
  ],
  "remedy": "A containment cell graded against the all-firm hash list for the 5 project files and the 5 test files. A CTO ruling on the two data files (_ids/data/custodian_key_seam.json, _ids/raw_keys.json): excepted as shipped Lambda data, or moved out of the repo.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v118"
  },
  "closed": false
 }
]
```

## Update at the round 118 compile (2026-10-11T04:42:13Z)

Input: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_118_P_DRAIN_END_20261011.md @6eaa44414b (msg 4085)`. TO-IB-pr-420 is terminal; the gate still refuses while 2 IRPT_BCKEND orders read pending. UN-PARKS ON: every
IRPT_BCKEND order terminal. Changes to the rows above when they land:

- **D2-S60** narrows to irpt-status. The adapter and the narrative are repaired on the refusal path (this seat's live reads: digests
  equal the map; TypeError before each apply, typed NOT_AUTHORIZED after). Still open on those two: no ADMITTED request has run on
  the new bytes, and the three widenings on the adapter are applied and unexercised. The close is `2.0.0_SA_COO~Y2`'s irpt-status
  apply plus the first admitted request on each function.
- **D2-W278-S5**: the live attribute mismatch on irpt-narrative is closed by the apply. The 2 failing contract tests at the pin stay.
- **D2-W278-S3, D2-W278-S4, D2-S62**: unchanged.
- **New, to ride the same slug:** the source map's `last_deployed_commit` and `last_deployed_at` for the two applied functions still
  read 2026-10-04 (row D2-S70). Owner `2.0.0_SA_COO~P2`: the apply's ledger or the map records the 2026-10-11 deploy.

## Update 2026-10-11 ~06:5xZ: irpt-status is applied

This seat's live read: irpt-status carries `6idtFvAm` (revision 6), modified 2026-10-11T04:44:47Z; 30 invocations to 06:22Z with
0 TypeError, 0 Traceback, 0 RetentionRefused. All three functions of row **D2-S60** are now repaired, and irpt-status has served an
admitted read (IRPT_YCDGEN round 7's run). When this file lands, D2-S60 graduates as INERT with one residual: no admitted request has
run on the adapter or the narrative. D2-W278-S3 closes with it. New for the same slug: the source map's `artifact_sha256` for
irpt-status reads `E7VKvhg3`, not the live digest (IRPT_ANLREQ row D2-S32 carries it).

## Update 2026-10-11 ~07:0xZ: row D2-S62 does not graduate

`1.0.0_SA_CTO~DELL2` msg 4327 relays Andrew's word of 2026-10-09 (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_192xZ_CLIENT_DATA_IN_PRIVATE_GIT_NOT_WORTH_TIME.md`): no further moving,
redacting or renaming of tracked files for account ids. **D2-S62** (the containment cell passed on the 49F set while the all-firm list
still hits 12 tracked files) is dismissed on that word when this file lands, not graduated. No ruling on the two Lambda data files is
asked. The same word closes the containment follow-ons this seat named for ADVI_COTBKF.

---

## Added at rounds 119 to 121, 2026-10-11T09:39:12Z (input: msg 4591)

Held with the rows above, on the same condition (IB-pr-404 and IB-pr-413 terminal):

- **D2-W282-S2** (owner `2.0.0_SA_COO~P2`): an identical repeat of a vendor performance request is refused once the first is
  retained. Remedy: the repeat serves the retained figure, or the refusal is the stated behaviour the page handles. It will show on
  the first re-walk that repeats a request.
- **D2-W282-S3** (owner `2.0.0_SA_COO~P2`): one calendar-fallback test fails. "Pre-existing" is inferred until it is run on the
  tree before the change (the CTO half's condition 4).
- **D2-S72** (owner `1.0.0_SA_CTO~DELL2`, to place): `build-and-upload.sh` exits 0 when its restore of pinned members fails on a
  held index lock. A shared-tree build can leave a tracked file carrying staged content. Remedy: a failing exit on a failed restore.
- **D2-S71** (owner `2.0.0_SA_COO~P2`): a signed packet says the Dells cannot write IAM; an apply from dell2 shows otherwise.
  Wording only.

**For the slug:** the release is APPLIED, UNEXERCISED. The Performance hop is graded by the DSGN_IRPTV1 walk, not here.

---

## Added at round 122 (the rollback), 2026-10-11T10:35:01Z (input: msg 4726)

**Corrections to the section above.** The vendor performance release was a departure from the ENDPOINT and is rolled back (read live).
D2-W282-S2 is dismissed, not held: a refused repeat is the designed state again. The line "the release is APPLIED, UNEXERCISED" is
superseded: it was applied, served 3 figures, and was removed.

Held on the same condition (IB-pr-404 and IB-pr-413 terminal):

- **D2-S78** (owner `1.0.0_SA_CTO~DELL2`): 3 vendor-calculated returns were served in the 44 minutes; the use records and
  retained reports of that window are unread and kept. Remedy: read them (who, which account sets), and rule whether a retained
  vendor report can be served again by any path.
- **D2-S76** (owner `1.0.0_SA_CTO~DELL2`, to place): 13 seat-folder orders carry no round tag and are counted in every round by
  `round-close-check.py`; one has no proof instance at the expected name. Remedy: tag them, as TCKT_VNEXT's issuer did.
- **D2-W282-S3**: now measured as failing before the change (the applier's run on the restored tree). Still a failing test.

**For the slug, the lesson the issuer names and this seat shares:** a release was signed, applied and compiled on its blast radius
and bytes, and nobody read it against the outcome it serves. This seat reads the ENDPOINT on every served change it compiles.

---

## Added at rounds 123 to 128, 2026-10-11T13:11:57Z (input: msg 4965)

Held on the condition that no IRPT_BCKEND order is open (IB-pr-404, IB-pr-413, IB-pr-431, IB-pr-432 are):

- **D2-S82** (BLOCKING; owner `1.0.0_SA_CTO~DELL2`): ADDENDUM v0.34's ratified-text half is refused on two text defects. Remedy:
  the two repairs named in `org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_PRD_v0.34_RATIFIED_TEXT_REVIEW_20261011.md @3f67123932`, then this seat signs.
- **D2-S83** (owner `1.0.0_SA_CTO~DELL2`, the gate's owner): the sign-off hash does not see a contract change made by addendum.
  Remedy: the half's hash covers the addenda that say they change it, or such a change is written into the hashed section.
- **D2-W284-S1** (owner `2.0.0_SA_COO~P2`): the close-anchor instrument keeps one price per CUSIP while a CUSIP carries different row
  prices on 50 of 85 days. It bears on what the addendum's claims measure.
- **D2-W286-S1** (owner `2.0.0_SA_COO~P2`): two columns are absent from 49 of the 85 partitions.
- **D2-W285-S3** (owner `1.0.0_SA_CTO~DELL2`): two real S3 requests with a literal fake key left the box before the offline fake was
  installed; refused, nothing read or written. Disclosed by the worker. Remedy: the replay harness installs the fake before any import.
- **D2-W285-S2** (owner `2.0.0_SA_COO~P2`): the replay box lacks the PDF library, so the pin tests that need a real PDF cannot run.

---

## Added at rounds 127 (amended), 129, 130 and 132, 2026-10-11T14:58:13Z (input: msg 5175)

Row D2-S82 above is met: PRD v0.35 and v0.36 repaired the text and this seat signed both. It is dismissed at the slug.

Held on the condition that no IRPT_BCKEND order is open:

- **D2-W288-S2** (OBSERVATION, INERT; filed by `0.9.0_WK_IRPT_BCKEND~288`): Over the 85 graded days one non-cash row (Units zero, Market Value above zero) fits none of the five ungradeable kinds and has no price; it is counted as sixth_reason_rows 1 and not fitted to a kind.
- **D2-S85** (OBSERVATION, INERT; filed by `0.7.0_AE_CloudOps~IB2`): The capture's full receipt (login_submission, probe_pair, warmup, login_path, screen) is consumed in process by run_capture and written nowhere, so the only surviving host evidence is eight step lines in a per-run-truncated stderr file; and the library's explicit SIGNED_OUT_APP_CHROME diagnosis for 
- **D2-S86** (OBSERVATION, INERT; filed by `0.7.0_AE_CloudOps~IB2`): A send-command whose local shell quoting had already failed handed SSM the empty string; SSM accepted it, ran nothing, and reported Status Success with ResponseCode 0 and empty output, so a CommandId and a Success both existed for a read that never happened.
- **D2-S88** (OBSERVATION, INERT; filed by `0.7.0_AE_CloudOps~IB2`): A GetItem on the irpt-jobs lease row from this seat's own session is denied -- kms:Decrypt on the table's CMK is not granted to cloudops-dell2-agent-user -- so the lease and job rows that hold the capture cooldown and the refresh intent are unreadable from the operator side; the row was read through
- **D2-W292-S1** (OBSERVATION, INERT; filed by `0.9.0_WK_IRPT_BCKEND~292`): On IB-pr-434 the persisted probe_pair is null in exactly the case the new code SIGNED_OUT_APP_CHROME_AFTER_SUBMIT names, because probeSession returns before the discriminating pair when the browser holds no identity cookie; the pair only exists when an identity cookie was present, so for the 2026-10
- **D2-S84** (OBSERVATION, INERT; filed by `2.0.0_SA_COO~P2`): IRPT_BCKEND is named EXPIRY OWNER of a TRANSITIONAL live row in the routed 49 Financial bucket alias: dell1's ADVI_FIRMBKTS lets the IRPT readers and the two gold writers keep reading investor-reporting/directory/ there instead of copying it into the firm's canonical bucket; the row expires at IRPT_

**For the slug:**
1. **The cost of the date-basis rule is now measured: 57.3 percent of eligible Cottonwood account-days blank, 382 of 999 accounts
   never served.** The largest kind is a priced security the anchor does not carry (34,437 account-days). Cottonwood Performance
   stays UNAVAILABLE.
2. **The vendor sign-in was submitted and never confirmed** (the host read; claim inferred). The path is stopped for every seat
   until st32 carries the capture build.
3. The sections response contract admits the Opal-made report. That closes IRPT_YCDGEN rows W2-S13 and W6-S4 on the contract side.

---

## Added at rounds 133 and 134, 2026-10-11T15:36:53Z (input: msg 5234)

Held on the condition that no IRPT_BCKEND order is open:

- **D2-W293-S1** (OBSERVATION; filed by `0.9.0_WK_IRPT_BCKEND~293`): The store the order calls last read to 2026-10-06 holds rows to 2026-10-09 when read through the census module's own reader, so a coverage figure taken from the 2026-10-06 note would understate it by the last three trading days.
- **D2-W293-S2** (OBSERVATION; filed by `0.9.0_WK_IRPT_BCKEND~293`): The order and 2.0.0_SA_COO~C2 group the own-firm silver prices store with the custodian marks; the store's source column names yahoo_finance, linear_interpolation and transaction_observed, so its price_kind could as well be read as market_close, mixed or derived.
- **D2-W293-S3** (OBSERVATION; filed by `0.9.0_WK_IRPT_BCKEND~293`): ib429_claims_v035.py, copied unchanged into this folder, reads IB127-1_account_day_claims.json from the previous cell's folder in its measure mode (for the anchor landing-order timing block), which does not exist in this worktree, so only its functions and its --control mode are 
- **D2-W294-S1** (OBSERVATION; filed by `0.9.0_WK_IRPT_BCKEND~294`): IB-pr-436: the Yahoo reader returns no bars for FPNIX, one of the nine funds; its 85 fund-days are no_nav_found

**For the slug:** 734 securities sit outside the anchor; the blank share reads 58.2 percent with the cash rule as ruled. An
independent daily NAV agrees with the custodian's mark on every fund-day measured for eight funds (claim inferred, one source).
Whether an unofficial reader may anchor a served figure is a PRD question and is not decided.

---

## Added at rounds 135 and 136, 2026-10-11T16:04:13Z (input: msg 5271)

Held on the condition that no IRPT_BCKEND order is open:

- **D2-S92** (BLOCKING; owner `1.0.0_SA_CTO~DELL2`): ADDENDUM v0.37's ratified-text half is refused on two points; the first is
  that no mutual fund's date label was measured. Remedy: the repairs named in `org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_PRD_v0.37_RATIFIED_TEXT_REVIEW_20261011.md @5810d49063`, then this seat signs.
- **D2-W295-S2** (owner `1.0.0_SA_CTO~DELL2`): the Opal form's v2 references sit inside an always-true conditional because the
  portal's generator cannot render a v2 reference. Remedy: the generator learns v2 references and the wrapper is removed, or the
  encoding is ruled to stay and the contract says why at its head.

**For the slug:** a second witness would take the blank share from 58.2 to 37.0 percent by the round 136 sizing; nothing is stamped.
