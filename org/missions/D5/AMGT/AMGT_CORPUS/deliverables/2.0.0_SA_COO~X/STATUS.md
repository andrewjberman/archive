# AMGT_CORPUS current state

Owner `2.0.0_SA_COO~X` (Claude seat, site Z); 2026-09-24 ~21:1xZ. Canonical flow (R-26). PRD v0.6 @`031c3a3a3e`, both L4-R
halves SIGNED current. Round 1 TERMINAL at `b4a8638eeb` (11 of 11); analysis @`031c3a3a3e`.

## BLOCKED ~23:0xZ -- the Bloomberg terminal will not sign in (needs a human at the box)

Bloomberg's updater ran 22:26Z and the terminal restarted 22:50-22:52Z, signed out. Two supervised sign-ins (fill, screenshot
verified 12-char login + 9 dots, submit) left the login window filled and no 8194 listener (a 120 s port poll between them);
per READ_HERE s.2 that is the one retry, so this seat STOPPED. Attempt ledger: 23 total, 3 today (20:46Z ok, 22:5xZ x2).
`0.0.3_BG_BBGTerminal` is not registered. Held behind it: the corrected FWD-12 re-pull + derive (CTO ruling msg 25799: R-21
covers it, pair @2a3319e5ae covers the derive) and the re-mint of the 4 + AMD (pairs @ae79d37b0c / CTO @35e4cb93ef), which
also waits for the running production sequence (step 9 dossier since 21:49Z). Served state is safe: the 31 keys restored
(Z-S26 @c25c5207a8), 58 new keys serve an honest empty block (0 figures).
The production sequence (started 21:35Z after the ingest read resolved_folders 73) ran steps 1-8 and was
KILLED by this seat's own 7200 s timeout at ~23:35Z inside step 9 (dossier, running since 21:49Z; rc 124); step 10 never ran;
no corpus process remains; write-once objects mean nothing partial was served. RESUME ORDER once the terminal is signed in:
corrected FWD-12 pull (identifiers with spaces) + derive, content-verified (FY rows > 0 per key); the re-mint; `ingest --write`
(expect resolved_folders 94); then `production_sequence --run` with no 2 h ceiling (dossier alone exceeds 1 h 45 m).

## ROUND 3 -- ALL 5 CELLS DRAINED (~20:4xZ); the 40-name FIRE held on ONE limb

Drains, each re-graded at the worker's tip on this seat's run: e-2 @`bb6b1f2f25` (22 mnemonics), e-3 @`1266b834ec` (sector
template re-mints once, 218 reports), e-4 @`5637be19e9` (production-sequence runner), e-1 @`21e624a003` (curated evidence
table), e-5 @`dae976b3b0` (served-as-empty-shell: 94 folders = 44 + 9 + 41). All five instances VALID. Worktrees
`/c/tmp/wk-crps3-{1..4}` removed and branches deleted. Eight ARMED rows owed by this seat disarmed by carrier Z-S22
@`2b3c2761e8`.

THE FIRE: pre-flight VERDICT PASS on `2.0.0_SA_COO~Z`'s builder fix @`9ec1226a01` (UNRESOLVED 40 -> 0, twins 0,
multi-claimed 0, 214 of 214 prior keys; `evidence/preflight_40_fire_20260924T210247Z.log`). Pair: COO half
`NEVER_WIDEN_ROUND3_FIRE40_HALVES.md` @`8bd8ba7e2b`, corrected @`498c9aeb01`; CTO half
`ledger/NEVER_WIDEN_ROUND3_FIRE40_CTO_HALF.md` @`af08f78a9b` signs every limb but the VENDOR limb. Asked of
`1.0.0_SA_CTO~Z` (21:05Z): does Andrew-direct R-21 @`b390c36444` release it; the CTO is also asking Andrew. `2.0.0_SA_COO~Y`
agreed the run is this producer's (msg 25747); its 94-folder proposal agrees on 37 of the 40, and the 3 differences sit on its
own not-document-confirmed list with no US-line record in the pool, so the home listings stand. Bloomberg terminal signed in
20:4xZ (one ledger attempt), health OK. After the fire: the production sequence through the runner, then the FWD-12 pull.

## ROUND 3 (history) -- EXECUTING (~19:1xZ)

Decomposition v3.0 @`d63cdd71ca` (five cells cut by write set, 15 checks as files dry-run at the base: 12 build checks FAIL,
3 bounds PASS); ONE issuance @`6108b0d804`; e-1 amended before its spawn @`c1437f9864` (the evidence table read against the
served pool: Bunzl -> BZLFY US and UMG -> UNVGY US attach to existing universe records; QXO associates; SLB registers; 35
register + 5 associate; Shopify SHOP CN agreed with `2.0.0_SA_COO~Y`). `2.0.0_SA_COO~Z`'s folder-onto-no-folder ENRICH landed
@`e640337205` first, so e-1 calls all 40. Workers spawned: `~1` e-4 (then e-5), `~2` e-1, `~3` e-3 (worker-light), `~4` e-2;
worktrees `/c/tmp/wk-crps3-{1..4}` at `c1437f9864`. Drain acts owed by this seat: the 40-name fire under a fresh pair; the
22-field pull under Andrew's V3 word (WORLD: change-management entry, batches of 3); the production sequence through e-4's runner.

## HOLD LIFTED ~18:10Z (CTO msg 25696: the pull landed at de839386bb / a1f085f2ef, every laptop-fabric add on origin). Round 2's
L10 is cut @`e05085196c` (FWD-19 NOT_REALIZED and moved; the 9 empty shells are NOT dossier-served; s.7 is round 3's list).
ROUND 3 IS BEING CUT from s.7 plus this seat's reconciled draft @`18f7a03a63`; two one-line asks out (CTO: the FWD-12 cell;
COO~Y: one registration run for the 40). Superseded hold text kept below for the record.

## (superseded) HOLD -- ALL AMGT OPS ON THIS FABRIC (Andrew-direct ~17:2xZ at the CTO terminal, relayed msg 25665, verbatim: *"Yes, tell
MSTR to ping you when ready, they need to coordinate with MSTR Base to know when all of the laptop fabric adds have made it to
the CLOUD so you can properly pull and only then continue with ops on this fabric as it petains to AMGT"*). This seat cuts,
drains, fires and analyses NOTHING on AMGT_CORPUS until `0.0.0_AB_MSTR~Z` pings the CTO that the laptop fabric is on
origin/CLOUD and the pull has landed. Already-landed work stands (round 2 TERMINAL, packet FINAL, the 40 measured, the
round-3 DRAFT and the FWD-12 sizing @`e510316e08`); round 3 is cut only after the pull, the CVO's slug and the CTO's analysis.

## Round 2 -- ALL 6 CELLS DRAINED (~15:0xZ); L8 handed to `3.0.0_SA_CVO~Z`

**d-4 drained @`809a89d8ff`** (worker close b011df6c7f; re-graded here: 8 of 8, package 260, checker VALID; `folders_read 93
dossier_served 53 resolved_no_prose 0 unresolved_with_reason 40 sum 93`, `never_prose_named 11`, scan vintage
`20260924T145816Z.json`; row W1-S4 on the shell-dossier reading of workbook-only folders). Packet FINAL:
`ROUND2_DRAIN_END_PACKET.md`. Owed now: L9 by the CVO (d-2 AC4, d-3 AC4 + the rows), then the CTO's round-2 analysis, then
this seat's round-3 cut (FWD-12 figures pull under Andrew's word; Z-S17; Z-S18; Z-S15). Slot ~1's worktree retired.

## Round 2 (history) -- EXECUTING, 5 of 6 cells drained (d-1, d-2, d-3, d-5, d-6)

Decomposition v2.0 @`df6798aebf`; ONE issuance @`7f48b997a9`. Drained into CLOUD: d-6 @`341bffca19`, d-1 @`c356bbff56`,
d-2 @`a419df8f9d`, d-5 @`7dc89c66c3` (after two issuer re-opens: amendment 1 the folder-vs-report disagreement refusal,
amendment 2 the call carries `--bloomberg "<root> <cc>"` beside `--folder`), **d-3 @`34a556c46e`** (the composed dossier:
33 of 33 names, written 20 / existed 13; census 825 fields, 286 cited, 539 ABSENT-with-reason, 0 neither; negative control
ABSENT; `read_dossier` @`bdfbd7ff6b`; `DOSSIER_INTERFACE.md` published to `2.0.0_SA_COO~Z` 09:22Z); corpus suite 254 PASS
on CLOUD. Pending: d-4 (the 93-of-93 census), behind the fire by design. Worker slots ~1, ~2, ~3 have drained every order
issued to them; slot ~1 is continued onto d-4 only after the corrected fire, the re-ingest and the production sequence.

Measured: extraction v2 123 of 123 (inline leads 22 of 52 PDFs); continuations 33 of 33 (with_pillars 10, PDF pillars 5;
4,580 of 4,580 citations; ASML_NA_Equity 2 pillars); scanner 0 library writes, 17 of 17 test sites fixture-rooted;
induction dry run on CLOUD: population 60, evidenced 20, ambiguous 2 (Copa, Uber collisions), disagreement 1 (America
Movil AXMB vs AMXB), other 37, 20 of 20 argv carry both flags, bloomberg_calls 0.

## INCIDENT Z-S13 (this seat's act) and the HELD re-fire

The 08:02Z fire (d-5 as first issued) made 0 Bloomberg calls and, through `add_security`'s per-name `write_pool`, replaced
`2.0.0_SA_COO~Z`'s signed `crosswalk/v1/2026-09-24.json` (MEASURED 194) with CLOUD's 36-shape plus 20 UNRESOLVED noise rows;
this seat's first grade used the wrong before-object. **Rollback CLOSED** 08:22:33Z by `2.0.0_SA_COO~Z` on the CTO's GO
(copy-object from the signed VersionId; verified 3 of 3 legs on three instruments; ledger `amgt-crosswalk-0924-rollback`
closed). Row Z-S13 condition 1 met.

**UPDATE ~14:1xZ -- THE CORRECTED CHAIN IS DONE; Z-S16 DISARMED (row Z-S19); d-4 CONTINUED.** `backlog --write` minted the
scan vintage `date=2026-09-24/20260924T130441Z.json` (93 = 53 resolved + 40 unresolved + 0 ambiguous); continuation `names 53
rebuilt 20 existed 33 (with_pillars 16, pdf 8)`; dossier `names 53 written 36 existed 17` (every one of the 20 new keys written at
as_of=2026-09-24; 16 of the old 33 rebuilt on changed inputs), 13:05-14:12Z. Andrew-direct ~13:2xZ ("open call approved, all
options approved do them in order", record @`16ee7f6373`, CTO R-70 confirms the reading): the FWD-12 figures pull's per-use
word is GIVEN -- spent by ONE cell at the round-3 cut (no scripted puller for the 22 mnemonics exists today; R-21 binds the how).
Options done in order: drain-end packet DRAFT @`75e4bc7e5c`; served-plane reads (AZN_LN, UBSG_SW MEASURED on the deployed
route) @`32bf98d750`; ten residue worktrees retired, merged branches deleted, slot ~1 kept. Z-S17's remedy fork settled by the
one query R-68 named (0 consumers of `total`; it leaves the body; c-7 cell next cut). NOW: worker ~1 continued onto d-4.

**UPDATE ~13:0xZ -- Z-S16 REMEDIED, RE-MINTED, RE-INGESTED; the production sequence found two more.** `2.0.0_SA_COO~Z`'s
builder fix (a registration RESOLVES its same-folder UNRESOLVED record in place) drained @`a5b9859e0a`; fresh pair (COO half
@`5de984f360`, CTO half #2 @`839b04a16c`, in force @`6236af5af4`); byte-identity HEAD == `a2b84a1b2a` (51,725 B, sha 200ec514;
pre-fix differs); ONE `crosswalk.main --write-pool` at 11:59:01Z: versions 23 -> 24, VersionId `BN_TiAyAX_EwRm_nP.PMymkiUnFBMA1N`,
560,881 B (the pre-built payload exactly), records 274 -> 254, MEASURED 214 with 214 of 214 keys present, UNRESOLVED 60 -> 40,
resolved_folders 20, multi-claimed forms 0 (evidence @`2c24cc867d`; CTO R-63 closes the pair). Re-ingest 12:00-12:04Z:
**resolved_folders 53, stored 218 (put_performed 94, existed 124), AMBIGUOUS 0** -- the 20 folders' 94 reports are in bronze.
Production sequence: extract --write and --run-v2 (v2_stored 218, put 95), typed (218 rows, 95 written), continuation,
fund_form, typecast (new scope=all-workbooks object) OK; **sector_template REFUSED (row Z-S17 ARMED: its gold object name
omits the corpus-wide total the body carries, so an unchanged type collides on a grown corpus; gold refused correctly)**;
dossier rebuilt 33 in 45 min. **Row Z-S18 (INERT, this seat's sequencing miss):** continuation and dossier enumerate names from
the latest research-backlog scan vintage (round 1's 33), which the decomposed sequence never re-minted, so the 20 new names got
no continuation or dossier on the first pass; the corrected chain (`backlog --write` -> continuation -> dossier) is RUNNING;
d-4 is continued after it. Z-S16 disarm carrier row follows the corrected chain.

**UPDATE ~11:3xZ -- FIRED ONCE, AND AN EXPOSURE BEHIND IT.** d-5 amendment 3 drained @`71e2409a43` (re-graded at the tip:
20 of 20, package 256, checker VALID); the pair completed (COO half @`4bbd43777c`, CTO half @`9a6472e58f` in the CTO's
folder); `bloomberg_health` OK; before-state re-measured identical (probe-2); the fire ran 11:09:45-11:11:01Z: **population
60 evidenced 20 ambiguous 2 disagreement 1 other 37 called 20 registered 20 already_registered 0 refused 0 errors 0
bloomberg_calls 20 batch_calls 1 pool_puts 1 sum 60**, rc 0. Discriminator (probe-3): versions 22 -> 23, latest VersionId
`tlVd1Cqrlhk93VurXE2jThhPNToWm0wA`, 583,272 B, sha 223264e2, MEASURED 194 -> 214, records 254 -> 274, registered 7 -> 27,
194 of 194 prior keys present, 20 new; raw bronze partitions 4 -> 24. registrations.json +20 @`b7819604e0`; evidence
@`911d09d153`; rows Z-S14 (disarm carrier for Z-S13, both conditions MET) and Z-S15 (the worker's committed batch file is a
test fixture -- `run()` writes into the hard-coded `DELIVERABLES_DIR` the tests share) @`b00b740d0c`.
**EXPOSURE, row Z-S16 ARMED (disarm owner this seat):** the re-ingest at 11:19Z resolved the SAME 33 folders (stored 124,
put_performed 1, existed 123) -- **0 of the 20 inducted folders ingested**, because the builder APPENDED each registration
beside the folder's still-UNRESOLVED coverage record (UNRESOLVED 60 -> 60), so 20 association forms are claimed by two
identities and `crosswalk.resolve()` reads them AMBIGUOUS. FWD-19 is REALIZED on identity, NOT on re-ingest. Remedy proposed
to `2.0.0_SA_COO~Z` (its surface): a registration resolves its same-folder UNRESOLVED record instead of appending; then ONE
re-mint under a fresh pair (no Bloomberg call); then this seat's re-ingest + production sequence; d-4 behind that.

**UPDATE ~10:5xZ -- all four preconditions HOLD (CTO R-51): the two clauses below were BUILT by `2.0.0_SA_COO~Z`
@`a125f8be8b` (`--batch` = one put per run; the universe input on every build) and drained onto CLOUD @`8c75f4f90d`
(byte-identical, R-51). R-49's count-first check, run here on the collision check's own in-memory object: 0 of 20
evidenced keys collide (positive controls ASML/AAPL present), so the ENRICH fork is moot. d-5 ISSUER AMENDMENT 3
@`e1014a7eb6` moves the induction to ONE `--batch` call; worker ~2 continued on it. COO half of the pair SIGNED
@`4bbd43777c` (`NEVER_WIDEN_ROUND2_D5_REFIRE_HALVES.md`; N = 2 writers printed; blast radius ONE conditional put;
before-state VersionId `aTOpDZTTPlIzLLoeTFumB8KHmv6A0txG`); CTO half owed. The fire runs after the amendment-3 cell
drains VALID and the CTO half lands.**

**Re-fire was HELD on two clauses, both on `add_security` (`2.0.0_SA_COO~Z`'s surface, taken on its Peers closer track):**
1. `write_pool` once per run (one put), not once per name (20 versions in 18 s was the partial-read window itself).
2. **Measured 09:0xZ, this seat's pre-flight:** `crosswalk.build_crosswalk("2026-09-24")` in memory on CLOUD returns MEASURED
   **36**, not 194 -- the universe/v1 source is an explicit `identity_universe`/`identity_source` argument the CLI passes
   and `add_security._persist_registration_and_pool` (`:175`) and its collision check (`:392`) never do. Without this clause
   the corrected fire re-creates the incident with one put. Reported to both seats (msg after 25353).
Then ONE re-fire under a never-widen pair whose halves print the key's writer count (two: the Peers producer, this
induction), state the blast radius as the puts actually made, and address the rollback to the version before the first.
Evidence of attempt 1: `induction_run_2026-09-24_fire_attempt1.json`, `evidence/induction_fire_attempt1_20260924T0802Z.log`,
`evidence/registrations_misfire_attempt1_20260924T0802Z.patch`.

## Interfaces owed outward

`DOSSIER_INTERFACE.md` (d-3) to `2.0.0_SA_COO~Z` when d-3 drains. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9: d-2 AC4,
d-3 AC4. The crosswalk stamp + registered count to `2.0.0_SA_COO~Z` after the corrected fire (its Peers trigger).

Bounds: AMGT only; no library write; no S3 delete; no self-granted access; no shared push (`0.0.0_AB_MSTR~Z`); no deploy;
no pool write from this seat until the hold lifts. Residue for the integrator: merged worker worktrees `wk-crps2-2`,
`wk-crps2-3` (branches merged), the round-1 closer worktree, the temp library copies. This file is current state.
