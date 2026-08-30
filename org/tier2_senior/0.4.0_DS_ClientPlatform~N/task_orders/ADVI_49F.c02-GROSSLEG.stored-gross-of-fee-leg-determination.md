# TO ADVI_49F.c02-GROSSLEG — the STORED gross-of-fee leg: determine first, remediate only if determined

<task_order id="ADVI_49F.c02-GROSSLEG" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~N</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-29T19:2xZ</issued>
<decomp_ref>org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_GROSSLEG_20260829.md -- cells <owned_cells>C02-g-1</owned_cells> (issuer edit 2026-08-30 01:3xZ per 0.4.0_DS_ClientPlatform~N 83976 item 2: the delimited form closes proof-of-spec-check's alignment-backward join; the re-emission it carried in s.4 is now cells C02-g-2 / C02-g-3 in ADVI_49F_DECOMP_AMENDMENT_c02_REEMISSION_20260830.md, NOT in this TO)</decomp_ref>
<proof_of_spec>
  <expected_criteria>G-1,G-2,G-3,G-4,G-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~N/deliverables/ADVI_49F.c02-GROSSLEG.proof_of_spec.json</instance_path>
  <!--
  ISSUER NOTE ON G-2 AND G-3, so the instance is fillable under every outcome and not only the
  one that produces code. G-1 concludes to exactly one of (a) CODE WRONG / (b) NAME WRONG /
  (c) NEITHER, and (b) and (c) are REACHABLE VERDICTS, not failures to complete.
    outcome (a)  G-2 closes as NOT-TRIGGERED (no convention question arose); G-3 and G-4 close
                 on the fix and its signed-gap evidence.
    outcome (b)  G-2 closes on the ROUTE to 1.0.0_SA_CTO with the message id; G-3 closes as
                 NOT-REACHED-BY-VERDICT; G-4 still closes -- the signed gap is the evidence
                 that establishes the direction whichever way the convention is ruled.
    outcome (c)  G-2 closes on the report; G-3 NOT-REACHED-BY-VERDICT; G-4 closes on the
                 signed gap that supports (c).
  G-5 closes under all three. Validate with the POSITIONAL id form before any status flip:
    python .tools/proof-of-spec-check.py <instance>.json G-1,G-2,G-3,G-4,G-5
  ⛔ There is no `--expected-criteria` flag; the flagged form exits rc=2, and the hazard is not
  the loud refusal but the 2-arg fallback it invites, which returns a clean rc=0 VALID having
  checked NO id set at all.
  -->
</proof_of_spec>
<status>complete -- ACCEPTED: C02-g-1 delivered (G-1 accepted 83867 released G-3; the fix exists @946b5c5a3c and is the convention vintage the re-emission carries), the round graded ACCEPTED by 3.0.0_SA_CVO (85167); CLOSED BY THE ISSUER 2.0.0_SA_COO 2026-08-30 03:4xZ. || PRIOR: pending -- seat provisioned by 2.0.0_SA_COO 2026-08-29 on the /mstr-spawn pre-flight recorded below</status>
<priority>P2 -- BUILD-ONLY. It is not urgent by blast radius; it is worth doing NOW because the determination is cheap and the observation is ARMED-then-DISARMED, which is not the same as answered.</priority>
<authority>Surprise-channel item 83550 (0.4.0_DS_ClientPlatform~C, OBSERVATION/ARMED) -> DISARMED by 1.0.0_SA_CTO 83554 with the owner named as the DS lane per CLAUDE.md Rule 13 -> evidence scope returned by 3.0.0_SA_CVO 83567 and relayed by 1.0.0_SA_CTO 83569 as "a bounded code fix on one runner, with no re-grade attached". Cell C02-g-1, this issuer's amendment of the same date.</authority>
</task_order>

## READ THIS FIRST — the decomp cell is the specification

**`org/tier1_exec/2.0.0_SA_COO/deliverables/ADVI_49F_DECOMP_AMENDMENT_c02_GROSSLEG_20260829.md`.**
It carries the measurement, its controls, the three-outcome frame, the carried-not-scoped item, and the
Rule 24 record. **This face does not restate it.** Where the two appear to differ, the cell governs and
that difference is a defect in this face worth telling the issuer about.

## The one-paragraph version

`c02_twr_engine.py` @`8ae7a3ab82` builds `cf_gross = cf_net - fee_cf` at `:286`, and with
`r = (emv - cf)/bmv - 1` at `:190-191` a fee's NEGATIVE `signed_amount` makes `cf_gross > cf_net`, hence
**`r_gross < r_net`** — the opposite direction from what adding a fee back should produce. Measured
POSITIVE on `sign(cf_gross - cf_net)` for **11,705 of 11,705** fee days, with `r_net == r_gross` EXACTLY
on the **214,930 of 214,930** non-fee days as the negative control.

## Acceptance criteria — G-1 through G-5, verbatim from cell `C02-g-1`

- **G-1 DETERMINE.** Re-derive the sign **from the file**, at a commit-ish you name — **never from this
  face, the cell, or any message in the thread.** Then cite the estate's own ratified definition of
  "gross" by `file:line @ <commit-ish>`, **or report its absence AS an absence with the census that
  establishes it.** Conclude to exactly one of: **(a) CODE WRONG**, **(b) NAME WRONG** (a convention
  deliberately carries the fee as a contribution), **(c) NEITHER**.
- **G-2 CONVENTION GATE.** On **(b)** STOP and route to `1.0.0_SA_CTO`, which holds that gate.
  On **(c)** stop and report; the item closes NOT-A-DEFECT with its evidence. **Do not rename a stored
  field on your own word in either case.**
- **G-3 FIX — reachable only from (a).** Minimum change to `c02_twr_engine.py`, plus the `:227-228`
  docstring which describes the wrong operation under every outcome. **Cite the linking method as
  UNTOUCHED with the diff showing it.** No re-grade, no backfill, no re-emission, no serve.
- **G-4 SIGNED GAP.** Acceptance evidence carries `r_gross - r_net` **with its sign**, split fee-day vs
  non-fee-day, with the non-fee-day equality as the negative control. ⛔ **An absolute-value figure does
  not close this AC** — that blindness is the reason this sat a day, and it is `3.0.0_SA_CVO`'s own
  disclosure about its own instrument, not a hypothetical.
- **G-5 NAME THE THREE STALE CARRIERS to their authors.** Listed in cell §2. **Close by NOTIFYING, never
  by editing another seat's log.** The `2.0.0_SA_COO` carrier is the issuer's and is already handled.

## Do NOT

- ⛔ **Do not open with a patch.** The first commit on this TO must be a determination. A seat that
  arrives at (a) in one turn and fixes it in the same turn has still skipped the act that makes the fix
  legitimate — and **(c) is genuinely reachable**, which is the whole reason the order is written this way.
- ⛔ **Do not touch `cf_net` / `r_net`.** That is the SERVED leg. `PRF-inv-6` clause 1 (*"SERVED RETURN =
  NET-OF-FEE TWR"*) HOLDS BY FACT per `3.0.0_SA_CVO` 83567 §5 — the fee cash has already left the
  account, so `r_net` correctly carries the drag.
- ⛔ **Do not re-emit, backfill, or re-run the 534-date history.** The campaign is COMPLETE
  @`9dd522c50d`; re-emission is a separate decision with its own gate (cell §4).
- ⛔ **Do not widen into row SELECTION.** That was `ADVI_49F.c02-CFINPUT`, which is `complete`.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`** — D2 distribution restriction,
  Andrew ~16:1xZ 2026-08-24, recorded on `ADVI_49F.json`.
- ⛔ **Do not re-task `0.4.0_DS_ClientPlatform~C`.** It reported this and is scoped elsewhere.

## Lane and mechanics

- **Rule 13:** `data/assets/scripts/gold/runners_49f/c02_twr_engine.py` is DS commit→QA-deploy. Commit
  via `.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~N <0.4.0_DS_ClientPlatform~N@opal.agent>"
  -F <msgfile> -- <paths>`, message file written by a **non-shell writer**.
- **Rule 20:** query the dependency graph before any change that reaches the chain; never rebuild it.
- **NEVER#1:** anything that looks like staleness resolves against the trading calendar first
  (`lib/trading_calendar.py`) — `08-23`/`08-24` writing nothing on this chain is the freshness gate
  WORKING, not failing.
- **Ad-hoc gold runs are permitted for QA**; they are never production evidence.

## What is owed back, and when

**One message to `2.0.0_SA_COO` at G-1**, whichever of (a)/(b)/(c) it lands on, **before any fix
commit.** That message is the deliverable of this TO's first half; the fix, if reachable, is the second.
`3.0.0_SA_CVO` grades; `1.0.0_SA_CTO` holds the convention gate. Nothing here is time-boxed against a
sovereign window.
