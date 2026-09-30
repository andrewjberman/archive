# AMGT_RESAPP round 53 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.61, issuance `cb37037d95`, on the CTO's round-52 analysis `5d3052d8d7`. Four orders, all
terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| ac-1 FWD-30's grader reads the displayed figure | LOCAL | ~190 | drain `99fd9d8dad` | `round45/checks/sweep.py` skips `role="tooltip"` / `data-figure-tooltip` subtrees inside the header figure. Plant: a tooltip change leaves the read unchanged. Control: a change to the visible `tabular-nums` span moves it. VALID |
| ac-2 a D-1 regeneration keeps every served sentence | LOCAL | ~191 | drain `4b472c8249` did NOT carry the branch (safe-merge exit 5; its tree equals the first parent, so nothing was reverted); re-landed by the worker, drain `8b56a93755` | The worker STOPPED per the cell's clause (row Z-W191-S1): ASML's 8 dropped sentences are stored with `quoted_spans []`, are not verbatim, and were served vacuously before C-VERBATIM-GATE HOLD. CTO msg 27185: HOLD working as designed (Z-S316). AMENDMENT 1 `cd70547173` re-scoped AC1 to span-carrying sentences: 2 of 2 kept, 8 held by design. 134 passed. VALID; no code change |
| ac-3 the slash-key window | WORLD | `0.7.0_AE_CloudOps~A` | entry opened `f4f9da33f7`, exec `e1367c77ba`, issuer close `f3f0e2167b` | COO half `bae8e66201`, CTO half `02eb2c5f9f`, pin `cd70547173` (8 CHANGED of 344). Leg (a): 40 CopyObject calls, raw kept. Leg (b): CodeSha256 `nKWCfQRQ...` -> `/QP4upEVzTjnHV2bAeIXIud0k0DgjDDGrlMgtm0uo7o=` (15:22:01Z). AMENDMENT 2 re-scoped AC3 after it failed (see section 3); the CTO accepted it on its half (AMENDMENT 1 `05a090d804`, msg 27252). No rollback |
| ac-4 the filings reader through slash_safe_key | LOCAL | ~192 | drain `63c369c734` | AMENDMENT 1 `e0d123d490` before spawn (CTO msg 27175). `fetch.pool_key` now routes `security_key` through `crosswalk.slash_safe_key`, with its docstring updated. 134 passed. VALID |

Worktrees `C:/tmp/r53-190..192`: branches merged; checkouts KEPT pending Andrew's go.

## 2. THE RESULT -- the issuer's real runs on the deployed function, at close

All re-run by the issuer on the served plane after the act, true exit codes 0:
- **ac-3 AC1:** `ac_3_copies.py` reads 40 of 40 objects at their encoded keys, byte-equal, raw kept.
- **ac-3 AC2:** `/timeline` for AMZN: 273 of 273 series entries carry `publishers_found_codes` (the HARVST q-5 rider). This unblocks
  DSGN round 13's found-codes wording.
- **ac-3 AC3 (AMENDMENT 2):** the BP/_LN and NG/_LN overlay, peers and thesis bodies are 6 of 6 equal to the pre-act capture, with 12
  read-path strings rewritten.
- **ac-3 AC4:** the one build landed.
- **FWD-30, the full served sweep at `/QP4upEV`:** **equal 95 of 96, values 95 of 96, unidentified 0, CAPTURE_FAILED 0, cases 288 of 288**; 32,145 value facts
  compared, 1 differs, 0 scale-unchecked; sweep exit 1 (E != I) (`round53/captures/fwd30_close_sweep_served_20260930T161018Z.{log,tsv}`).
  The one: TSM_US_Equity, 1 of 246 values. Same name and count as the 13:29Z re-grade on the fixed grader, which named it HEADER
  CURR_ENTP_VAL: page 'unit not resolved -- raw figure 71,993,494.73 (TWD)' vs export '71993494.73205896 UNRESOLVED-ON-TSM'. Both
  sides state UNRESOLVED; the grader reads the page's leading words as the value. The close log does not name the fact, so the
  identity at close is inferred from the count, not re-read. The ac-3 build moved no FWD-30 grade.

## 3. For your L8 read (CTO msg 27252 asks for it)

**ac-3 AC3 was re-scoped AFTER it failed.** Read it against its planted control:
- **Why it failed:** the body reports its own read path inside the `*_read` provenance subtrees (`posture_read`, `peer_read`,
  `scores_read`, `management_read`), and the act moves that path by design.
- **What AMENDMENT 2 does:** it rewrites the encoded name back to raw inside those subtrees only. Every other byte must equal the
  pre-act capture.
- **Evidence:**
  - Unamended check: 6 of 6 bodies moved.
  - Amended check: 0 of 6 moved.
  - A value planted outside `*_read` (NG/_LN peers): FAILS, exit 1.
  - A rejected wider rewrite that also touched citation `report_key` fields: FAILS on BP thesis, because those citations were
    stored encoded before the act.
- **Executor's same-plane control (row Z-S318):** both code versions were run in process on the same data. BP/_LN thesis has 13,621
  fields; 3 differ, all path strings.
- **Why the change is mine:** AC3 and the COO half's "byte-equal" wording were my instrument defect, the same class as Z-S311. It is
  the third check of this round span that could not see its own outcome.

## 4. Judgment criteria

None this round.

## 5. Rows this round (L8 input)

| row | source | standing | what it records |
|---|---|---|---|
| Z-W191-S1 | ~191 | BLOCKING; resolved by CTO msg 27185 and Z-S316 | ac-2's STOP: the dropped sentences are non-verbatim |
| Z-S316 | issuer | INERT | Z-S314 re-classified: the HOLD is working as designed. A live rebuild still removes served sentences, so it runs only under a pair |
| Z-S318 | AE~A | BLOCKING, INERT; ruled by Z-S320 (AMENDMENT 2) | AC3 cannot pass by the specified act |
| Z-S319 | AE~A | ARMED; ruled INERT for served output by Z-S321 | the build script's upload leg mangles a content-sha256 that starts with `/` (MSYS), at rc=0. yang-lambda deploys the S3 object VERSION, so only `source_code_hash` is corrupted |

## 6. Carried to the CTO's round-53 analysis

1. **Round 54's census and compliance pair** (CTO msg 27185): a census of non-verbatim served D-1 sentences, plus a WORLD compliance
   pair.
2. **The FWD-30 gap:** TSM `CURR_ENTP_VAL`. Both sides say UNRESOLVED, but the page cell leads with "unit not resolved --", a second
   grader reading gap (95 of 96 at close, section 2). AMGT_CORPUS round 25 (Z-S69, the TSM denomination census) is the
   upstream fix.
3. **The metadata repair (Z-S321), as round 54's repair cell:** three scripts under `infra/aws/terraform/harvest/` pass
   `content-sha256` bare: `build-and-upload-scoped-amgt.sh:742`, `build-and-upload-print-deps-layer.sh:79` and
   `build-and-upload.sh:29` (the HARVST research-pull-enqueue artifact). `build-and-upload-chatter-axis.sh:42-44` already has the
   fixed shape: no path conversion on the segment, plus a read-back that refuses on mismatch. Until round 54 lands, the COO half of any
   RESAPP build pair carries "head-object content-sha256 equals the local sha" as an act-start limb.
4. **Gate proposal, agreed earlier (Z-S311/Z-S312), now with a third instance:** a check whose comparand embeds the thing the act
   moves (here the read path) must show its positive arm before the cut.
5. **Parked (laptop-CTO ruling, msg 27166):** site Z's `test_seed_etf_constituents.py:201-203` must assert the conditional put once
   origin `9e4997d618` lands on site Z. It passes 8 of 8 today.
6. **Instrument note:** safe-merge exit 5 ("committed but branch not carried") happened once (ac-2). The re-land needs the worker's
   serial: the W-row gate and the TREE_DELIVERABLES lane refuse the issuer.
