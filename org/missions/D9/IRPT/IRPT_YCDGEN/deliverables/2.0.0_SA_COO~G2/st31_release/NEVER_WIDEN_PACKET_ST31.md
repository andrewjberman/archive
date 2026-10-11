# The dead-letter release -- never-widen packet: st31 = the whole tree at trunk pin 19b02b2971, installed over st30

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11. **Operator:** `0.7.0_AE_CloudOps~YC2`. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
**Ledger:** `irpt-resident-st31-20261011`, opened at the first host act. **Rulings:** CTO msgs 4957 and 4971 (ship the
dead-letter record now, unbound, in the st30 form; the attach release is its own four cells). **Cells:** IRPT_YCDGEN
`YCD-a-12` (`decompositions/IRPT_YCDGEN_DECOMP_R12.md` @f6668485a7). **Census:** `CENSUS_ST31_AGAINST_ST30_20261011.md`.

**ONE group changes what the resident does: a generation job that fails its fifth delivery records why. No binding is
added. Everything else that moves is inert on the resident or changes no served answer.**

## 1. The act

- **Pin:** `19b02b2971`, a commit of box/dell2 itself. **No scratch branch and no cherry-pick**: every commit the host will
  run is on the trunk, which is the rule of the round-12 analysis section 3 item 3. (st30's pin carried one commit the
  trunk lacked; it was landed @177f315007 before this pin was cut.)
- **Build:** st30's recipe, unchanged: the whole tree at the one pin, `--research`, `--opal-map`, the same 2 `--member`s.
- **Gate:** `resident_package_gate.py` PASS in WHOLE-TREE mode against the running st30 (the gate was repaired @d7ae7d0f2b,
  row D2-S46). G1 294 of 294; G2 292 of 292 (2 generated members not compared); G3 117 of 117 compile; G4 0 unserved;
  G5 added 0, removed 0, changed 21, identical 273.
- **Tests on the trunk, with 0 packaged source files changed between the pin and the tree they ran on:** `ycharts/generate`
  507 passed, 0 failed (1 expected failure); `ycharts/research` 281 passed; the resident factory file 19 passed.
- **Artifacts** (`C:/dev/irpt-release-st31/`, local only, NOT staged):
  - tar `19b02b2971-st31.tar.gz`, sha256 `00532ad07e3e250b4a136b32585f4244ca25c6bf7108c850dc1af600118c4b99` (1,004,820 B);
  - `resident_host_install_19b02b2971-st31.sh`, sha256 `40207530c2c2b547d4502bea56260291be2752160321ffa8dae6985e1c410c64`.
- **Scripts** (this folder, derived from st30's): `pre_read.sh` (P1), `install_st31.sh` (D2 + V1),
  `remove_st31_to_st30.sh` (X1 + V2). The dead placeholder line of st30's script (row D2-S47) is not carried.

## 2. The one served change, the line it answers to, its consumers

| change | the ENDPOINT line | consumer, and one read through it | state after the install |
|---|---|---|---|
| D1: a generation job whose handler raises on its fifth receive records `FAILED` with code `DELIVERIES_EXHAUSTED`, the exception's CLASS as cause, and the receive count; then the exception propagates as before and the queue dead-letters the message | No ratified line speaks of a failed job's record: I looked and found none, and I do not stretch one to fit. The nearest is `IRPT_BCKEND_PRD.md` line 45, FWD-4, this project's share "the chain from validated input through captured request, job and result". The change was ordered by the CTO round-11 analysis @457305b604 section 3 item 2 on row IRPT_YCDGEN-D2-S49 | (1) The status route: by the worker's read of `ops/owned_status.py`, a FAILED job answers state FAILED, reason ANALYSIS_FAILED, with no actions, and the new detail is NOT passed to a caller. One read through it: the status of a request whose job this branch wrote. (2) The job row itself and the host journal, read by seats | APPLIED, UNEXERCISED: it fires only on a job that raises five times, and no seat drives one. V1 prints the packaged limit constant |

Both branches of D1, read from the code: a job that raises below the limit is untouched; a job at the limit whose state
is already READY, ATTENTION or FAILED keeps it; if writing the state itself fails, one journal line names that failure's
class and the original exception still propagates.

**What it changes for the eight existing dead letters: nothing.** They are already past delivery. Reconciling them by
record is a later act under a pair naming each (row D2-S45 stays ARMED). No dead letter is redriven.

## 3. What else moves, and why it is not a served change (census groups D2 to D7)

- **The packager's own-store pre-check (AR-g-32): INERT.** No `commentary_ready_queue_url`, no `analysis_ready_queue_url`
  and no `packager` key is in the built bindings. This release ADDS NO BINDING. The logical id under which a package is
  retained changes in the code; nothing is retained under the old one because the packager has never run (CTO msg 4922).
- Generated headers, the naming builder (129 of 129 and 17 of 17 answers identical), two other-project registry rows,
  five tightened schemas the resident does not validate against, fixtures and a test.

## 4. Blast radius

Host `i-0167fd745ad906a66`: one new root `/opt/irpt-resident/19b02b2971-st31`, the ExecStart, the receipt, ONE restart.
The capture library and wrapper are byte-equal to st30's (`857d90b81960d69a`, `55ddb8f7947cba7c`). No IAM, data, Lambda,
queue or portal change. The Opal allow list is unchanged: Andrew's sign-in only.

Writers of "what a job's row says after its last delivery fails": before, 0 (nothing wrote it); after, 1 (this branch).

**The vendor session is not touched and no request is submitted.** CTO msg 4917 stands: no seat sends a request down the
YCharts path until IRPT_BCKEND reads the session failure. Whether a restart of the resident by itself touches the vendor
session was NOT read in code. What is measured: st30's own install and restart at 10:32Z printed no session, eviction,
capture or vendor-request line (0 such lines in D2_V1_INSTALL_20261011.txt), and st31's installer is the same script form.
If the CTO wants that read in code before a restart while the session is failing, it is one read and I hold the order.

## 5. Order, STOP and rollback

1. **U2 stage** the tar and the install script; each key 404 before the put; read both sha256 back.
2. **P1 pre-read** (read only). **STOP:** `P1 STOP-READ PASS` (`IRPT_ANALYSIS_READY_QUEUE_URL` reads 0 three ways), st30
   running. On FAIL nothing is installed.
3. **D2 + V1 install.** The installer refuses unless `irpt-generation` reads 0 and 0, and rolls back itself on a failed
   start.
4. **Rollback (X1 + V2):** `remove_st31_to_st30.sh` restores the st30 receipt and root; st30 stays on the host. Rollback
   package: `37210c771a-st30.tar.gz`, sha256 `e5a6b6251b0e5e971cf73d785770965d4c2f407a6b4d79286508b50a853da241`.

Rollback is run on a failed V1, any I3 send or send failure, or a resident that stops polling.

## 6. Not established

Nothing here was exercised on the host. D1 has no after-read a seat can drive. The three host scripts pass `bash -n` and
have not run. Three of the four response-schema diffs were read by their size and shape, not line by line.

## COO HALF

**COO half SIGNED** -- `2.0.0_SA_COO~G2`, at trunk pin `19b02b2971` and the tar above, on the gate result, the census of
21 moved members, the one served change with both its branches, no binding added, and P1 as a STOP.

## CTO HALF

(owed)
