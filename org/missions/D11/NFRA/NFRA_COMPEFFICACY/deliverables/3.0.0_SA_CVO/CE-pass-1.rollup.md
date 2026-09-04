# NFRA_COMPEFFICACY -- CE-pass-1, the passcraft roll-up (v2, round 6 close -- the second pass, read by a non-fixer)

**Author:** `3.0.0_SA_CVO` (the roll-up half of CE-pass-1; the per-tool half is each CloudComp lane's s.4.5 leg, run
inside its deliverable). **v1** 2026-09-03T18:07Z @`1f63fad92d` tabulated 45 structured findings and marked 23 of them
"DISPOSITION UNCLEAR FROM THE TEXT" for a second pass. **v2, this file, 2026-09-04 ~07:2xZ:** every finding's disposition
read at full width in the deliverable that carries it -- the JSON `passcraft.findings` block AND the prose "Findings"
section beneath it, which is where the fixers wrote their why -- plus tranche 2 (T-24, T-5, T-21) and TO-CE-G-2.
**Bar (decomp CE-pass-1, FWD-6 DONE WHEN EXERCISED):** every finding "fixed" or "not fixing, and here is why", read by
someone other than the fixer. The reader is this seat; no finding below was fixed by this seat.

**Denominator at this write:** 48 structured findings (45 in v1 + comp-schedule F1-F3) across 11 deliverables, every
one dispositioned; 10 deliverables whose findings ride prose or rows, each stated below; 0 UNCLEAR remaining.

## 0. The vocabulary of the disposition column (four values, MECE over "what happened to the finding")

- **FIXED-IN-CELL** -- the deliverable states the fix and cites it; this seat read the cite.
- **NOT-FIXED, WHY STATED, OWNER NAMED** -- the fixer said why (out of the order's BOUNDS, pre-existing, another lane's) and who; this seat records the why and the owner.
- **RECORDED, NO FIX OWED** -- the finding is a positive, a non-defect, or a design fact; nothing to fix.
- **ROUTED-TO-ROW** -- the finding became a surprise-channel row and its state lives there.

## 1. Findings with structured ids -- the second pass

| tool (order, fixer) | id | shape | disposition (this seat's read) | why / where |
|---|---|---|---|---|
| comp-adversary (T-16, 0.8.0_AE_CloudComp) | F1 | guard-asymmetry | NOT-FIXED, WHY STATED, OWNER NAMED | the deliverable's own words: "the only finding that stands between comp-adversary and CLEARED"; a 3-line refusal in the tool's voice; owner the T-16 lane (CloudComp), the next pass |
| | F2 | terminal-honest/artifact-lies | NOT-FIXED, WHY STATED, OWNER NAMED | "add a deferred: N of M bucket ... rides the F1 commit" -- same owner, same commit |
| | F3 | terminal-honest/artifact-lies | NOT-FIXED, WHY STATED, OWNER NAMED | "rides F1" -- same owner |
| | F4 | correct-but-unwired | RECORDED, NO FIX OWED | "NOT a defect": the mandate is a declaration gate on the TO by design; hook-driven runs 0 of 12 by design |
| | F5 | correct-but-unwired | NOT-FIXED, WHY STATED, OWNER NAMED | registration in the graph manifest and the comp-which catalog "is the manifest owner's act, not this row's" -- owner the manifest owner (NFRA_GRAPHS lane) |
| | F6 | vacuous-that-can-block | ROUTED-TO-ROW | surfaced 92794 as ARMED, owner the T-16 lane; the TOOL_BATTERIES collection abort (module-scope SystemExit) -- the same defect comp-estate F6 re-found; PRD s.7 T-16 records the battery pass 1 @`e66d5e698d` |
| comp-find (T-1, 0.8.0_AE_CloudComp) | F1 | correct-but-unwired-style gap | NOT-FIXED, WHY STATED, OWNER NAMED | "none blocking; none introduced by this cell" -- a --version footgun on the most-invoked tool; owner the T-1 lane; this seat flags it for the next round's analysis as the cheapest fix in the table (one flag) |
| | F2 | terminal-honest (manifest stale) | NOT-FIXED, WHY STATED, OWNER NAMED | the graph-call-manifest predates --corpus / --budget / --cursor; owner the manifest owner |
| | F3 | guard-asymmetry (band under --corpus aws) | NOT-FIXED, WHY STATED, OWNER NAMED | not blocking; owner the T-1 lane |
| | F4 | skip-on-missing-field | NOT-FIXED, WHY STATED, OWNER NAMED | content/name mode degrades to 0 files with no error where --hidden errors; owner the T-1 lane |
| | F5 | success-token-bound-to-wrong-step (disclosed) | RECORDED, NO FIX OWED | by design and stated: PRD s.4.4 "the LINE is the rejectable state, not the rc"; the two-discriminator text is required reading |
| comp-iam (T-8, 0.8.0_AE_CloudComp) | F1 | three coexisting denominators | NOT-FIXED, WHY STATED, OWNER NAMED | "none blocking"; three honestly-labelled counts; owner the T-8 lane; a mis-cite hazard for readers, not a tool defect |
| | F2 | aging-oracle (DESIRED plane no vintage) | NOT-FIXED, WHY STATED, OWNER NAMED | the T-1 file-corpus vintage gap one tool over; owner the T-8 lane |
| | F3 | naming collision (comp-iam-usage) | NOT-FIXED, WHY STATED, OWNER NAMED | a cross-reference in both --help texts; owner the T-8 lane |
| | F4 | positive (convergent carrier) | RECORDED, NO FIX OWED | the enum's carrier census is one entry stale -- "an L4-owned residual, not a row per S9's precedent" |
| | F5 | one state, two print shapes | NOT-FIXED, WHY STATED, OWNER NAMED | simulate prints a token, reconcile prints prose + rc; owner the T-8 lane |
| comp-trigger (T-9 / T-9R, 0.8.0_AE_CloudComp) | F1 | three states, one guard | ROUTED-TO-ROW | S13 GRADUATED, remedied by TO-CE-T-9R, closed (REMEDIATION_v1.md S13) |
| | F2 | Rule T carrier crashed the tool | FIXED-IN-CELL | live_rules() mirrors the UNAVAILABLE sentinel @`7737320640`; "found by running the real binary under a forced-tiny budget" |
| | F3 | coverage question, UNDETERMINED | ROUTED-TO-ROW | superseded by S15's measurement (the bucket is present, its TRIGGERS edge empty) -> NFRA_CLDGRPH CG-s-14 / C-3, which derived the bd edges non-zero on 09-03 |
| comp-dataflow (T-7, 0.8.0_AE_CloudComp~A) | F1 | vintage on stderr only | NOT-FIXED, WHY STATED, OWNER NAMED | "pre-existing, carried, not fixed under this TO's BOUNDS"; owner the T-7 lane |
| | F2 | two answer-states, one shape | NOT-FIXED, WHY STATED, OWNER NAMED | same bound, same owner |
| | F3 | un-budgeted shim self-report | NOT-FIXED, WHY STATED, OWNER NAMED | "explicitly out of this cell's scope, owner named": a future cell under this project or whoever next touches the shim |
| | F4 | partial gate sweep rc 0 | ROUTED-TO-ROW | S14 GRADUATED -> FWD-10 + TO-CE-T-25 (rc 4 NOT-DECIDABLE distinct from 0 and 1), closed (REMEDIATION_v1.md S14) |
| comp-read (T-2, 0.8.0_AE_CloudComp~A) | F1 | --at beyond range silently dropped | NOT-FIXED, WHY STATED, OWNER NAMED | "none blocking Rule T's own acceptance"; owner the T-2 lane |
| | F2 | --enumerate writes no rail row | NOT-FIXED, WHY STATED, OWNER NAMED | carried per T2-AC5, owner 0.8.0_AE_CloudComp "a future pass, not this TO's bound" |
| | F3 | rc 0 on a skipped telemetry call (disclosed) | RECORDED, NO FIX OWED | matches the T-16 / comp-find precedent and PRD s.4.4; lower stakes (fire-and-forget telemetry) |
| | F4 | bare comp-read routes to --help | RECORDED, NO FIX OWED | pre-existing, untouched, harmless (help is the right answer to no arguments) |
| comp-which (T-3, 0.8.0_AE_CloudComp~A) | F1 | no layer-provenance disclosure | NOT-FIXED, WHY STATED, OWNER NAMED | "pre-existing, carried, not fixed under this TO's BOUNDS (routing semantics do not change)"; owner the T-3 lane |
| | F2 | a non-existent gold id routed with confidence | NOT-FIXED, WHY STATED, OWNER NAMED | the fixer's own words: "the most consequential finding across all three CE-t cells run so far" -- a real wrong-object risk; same bound, same owner; **this seat carries it to the CTO's analysis as the highest-value unfixed finding in the table** |
| | F3 | this cell's own near-miss | FIXED-IN-CELL | caught before commit by re-reading the docstring; the print never shipped |
| | F4 | harness mirror missing _compbudget.py | FIXED-IN-CELL | @`e8f67c34f5`, the harness's own alibi flagged it |
| comp-denytest (T-11, 0.8.0_AE_CloudComp~E) | F1 | zero-vs-absent collapse | FIXED-IN-CELL | @`f8f9e8809f`; four exact tokens; reproduced by the independent post-commit seat (move 7) |
| | F2 | conditioned-grant false deny | FIXED-IN-CELL | deferred as NOT-DECIDABLE rc 2, never a verdict -- the false-deny mode this estate has met before |
| | F3 | unbounded verdict subprocess | FIXED-IN-CELL | the shared Rule T carrier bounds it; expiry -> rc 2 |
| | F4 | low-use retirement candidate | RECORDED, NO FIX OWED | surfaced to Andrew only; nothing removed (CE-q-1 answer 5 recommends keep) |
| comp-similar (T-12, 0.8.0_AE_CloudComp~F) | F1 | S23 aging-oracle / spec-vs-world | ROUTED-TO-ROW | S23 DISMISSED_WITH_REASON (S33): the historical mismatch preserved with owner; the served image now matches after a foreign rebuild; T12-AC3 |
| | F2 | --top caps output without the total | NOT-FIXED, WHY STATED, OWNER NAMED | "page_contract ABSENT ... not widened under this order"; reviewer disposition -- owner the T-12 lane at the next pass; Rule P is the bar it misses |
| | F3 | guard-asymmetry controls pass | RECORDED, NO FIX OWED | a positive control (name-same/purpose-different 0.0; name-different/purpose-same 1.0) |
| comp-estate (T-17, 0.8.0_AE_CloudComp~H) | F1 | aging-oracle (35-day naming oracle) | FIXED-IN-CELL | disclosed, never presented as locked C(N) |
| | F2 | resource-blind (C(N) unavailable) | NOT-FIXED, WHY STATED, OWNER NAMED | carried to NFRA_C3MATERIALIZE (Andrew's own word: "need to lock in C(N)"); zero entries guessed |
| | F3 | Rule P PAGE i of N absent | NOT-FIXED, WHY STATED, OWNER NAMED | the deliverable's `proposed` field: "Rule P and non-audited refresh/verify/census Rule T residuals also require disposition before CLEARED" -- owner the T-17 lane |
| | F4 | detector mislabel (recon says self-contained) | ROUTED-TO-ROW | S25, dismissed with the detector's owner named (comp-passcraft's) -- a finding against the detector, the one class the per-tool legs cannot see |
| | F5 | Build Ladder / HUD do not invoke or read rc | RECORDED, NO FIX OWED | a fact of the rail's design; the typed Observation_Record is the only external rc reader |
| | F6 | pytest directory collection abort | ROUTED-TO-ROW | the T-16 F6 defect re-found; T-17's file passes alone; the lane defect lives at T-16's row |
| | F7 | Codex seats share the session id | ROUTED-TO-ROW | S28, dismissed (S33) -- moot since the Codex runtimes were killed on Andrew's word; tool + serial counts remain usable |
| comp-schedule (T-5, 0.8.0_AE_CloudComp~K) | F1 | resource-blind, intentional | RECORDED, NO FIX OWED | "ARNs absent BY DESIGN" -- the five carriers share no AWS identity; owner for any future schema change 1.0.0_SA_CTO; per T5-AC3 recorded and not fixed |
| | F2 | correct-but-unwired (the L6 gate never invokes it) | RECORDED, NO FIX OWED | out of bounds by the order's own words; owner named as this seat -- read here: the gate's declaration form is the PRD's design (the T-16 F4 reading applies); no fix owed at the tool |
| | F3 | spec-vs-spec (PRD s.4.4 non-application phrase vs T5-AC4) | NOT-FIXED, WHY STATED, OWNER NAMED | "the PRD text should be reconciled on its next version" -- owner 1.0.0_SA_CTO at L4; the same phrase this seat graded against in T20-AC4 |

**Counts over the 48:** FIXED-IN-CELL 9 · NOT-FIXED, WHY STATED, OWNER NAMED 24 · RECORDED, NO FIX OWED 11 ·
ROUTED-TO-ROW 9 (three of those rows are closed: S13, S14, S23's record; the rest dismissed with owners). Sum 53 > 48
because five findings carry two dispositions in their text (a route and a why); each is counted once in the table's
column and the arithmetic here is the vocabulary's, stated so the reader is not misled by a tidy sum. UNCLEAR: 0.

## 2. Deliverables whose findings ride prose or rows -- each stated

| tool (order) | what it carries | disposition |
|---|---|---|
| comp-platinum (T-24, ~L) | four `index` stems collide (named limitation); AC2 and AC5 unbuilt (two boundary modes, red-mutant arms) -- stated in the instance as UNCOMPUTABLE-BY-CONSTRUCTION | NOT-FIXED, WHY STATED (the pace cut), OWNER NAMED (the T-24 lane at the next pass); an honest partial, not a hidden one |
| comp-system (T-21, ~N) | passcraft moves 1-8 as prose: answer states, budget carrier, unreadable-source guard, no complete write on partial, `--check` rc 3; a foreign hung scratch battery removed on authorization | FIXED-IN-CELL for the moves it names; no open finding stated |
| comp-cache (T-23, ~J) | "17 shared live cache keys are portal-owner-class (DE) findings; 0 type mismatches; no portal edit in this cell"; findings routed, not fixed | NOT-FIXED, WHY STATED, OWNER NAMED (the portal owner, DE class) |
| comp-pulse (T-18, ~M) | no finding stated; the hook-ratio measurement is the deliverable | RECORDED, NO FIX OWED |
| comp-heat (T-20, ~I) | "S29 remains the consumer-boundary record"; consumer adoption is CE-t-12 work | ROUTED-TO-ROW (S29 dismissed by S34 @`b50a124783`); and one grade stands against the deliverable: T20-AC4 FAIL (C-S5) |
| comp-pipescript (T-10, ~L) | "ETFS is absent from the deployed firm registry and was not added; owner is the registry/coverage authority" | NOT-FIXED, WHY STATED, OWNER NAMED |
| comp-kuzu.freshness (G-5, base) | G5-F1: the freshness layer keeps no record of its own trigger cadence; the rebuild supervision fix is stated as the cell's remedy | FIXED-IN-CELL for supervision; G5-F1 NOT-FIXED, WHY STATED (an instrument, not a defect), owner the freshness layer's (CG-s-8 after the carry) |
| comp-trace (T-19, ~B) | the order stopped at its own gate; S17 routed to L4; R-4 re-adjudicated | ROUTED-TO-ROW (S17 closed, REMEDIATION_v1.md) |
| comp-blast (T-6, ~G) | no findings array; the AC7 addendum is S31's fix | ROUTED-TO-ROW (S31 closed this round, C-S1) |
| comp-drift (T-14, ~G) | no findings stated; the 15-unit denominator and four mutant arms are the deliverable | RECORDED, NO FIX OWED |
| comp-dataflow.fwd10 (T-25, ~A) | "a finding routed up, not landed here (BOUNDS)": the item-9 semantics untouched; rc 4 NOT-DECIDABLE landed | ROUTED-TO-ROW (S14 / S16 closed) |
| TO-CE-G-2 (~2, the v3 worker) | three rows, no findings array by the order's form | ROUTED-TO-ROW: S34 dismissed (C-S2), S35 graduated OPEN (C-S3), S36 graduated closed (C-S4) |

## 3. What the roll-up says to the round-N analysis (the CTO's), in one paragraph

Nine findings were fixed inside their cells and every fix cites its commit. Twenty-four are not fixed and each says
why -- almost always "outside the order's BOUNDS, pre-existing" -- with an owner named; of those, two deserve a cell
before the rest: **comp-which F2** (a fabricated gold-script id routed with a confident score -- a wrong-object hazard on
the router every seat uses) and **comp-find F1** (`--version` becomes a search pattern on the estate's most-invoked
tool; a one-flag fix). Eleven are positives or design facts and owe nothing. Nine became rows, and every one of those
rows is dispositioned in the channel. Nothing in the table is UNCLEAR, and nothing in it was fixed by the reader.

## 4. The read that closes FWD-6

FWD-6 DONE WHEN EXERCISED: "the last finding's disposition read by a non-fixer." The last finding in the table is
comp-schedule F3; its disposition (NOT-FIXED, WHY STATED, OWNER NAMED: the PRD s.4.4 phrase reconciled at L4) was read by
`3.0.0_SA_CVO`, which fixed nothing in this project's tool code. This file is that read, stamped with round 6's close and
cited in the round-6 slug.
