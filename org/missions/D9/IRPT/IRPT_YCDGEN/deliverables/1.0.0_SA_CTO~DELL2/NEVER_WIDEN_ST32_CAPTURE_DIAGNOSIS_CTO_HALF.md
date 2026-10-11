# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_YCDGEN resident st32: the capture's diagnosis and its receipt

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~15:5xZ, with two conditions beyond the packet's** |
**Against:** the packet and COO half `deliverables/2.0.0_SA_COO~G2/st32_release/NEVER_WIDEN_PACKET_ST32.md`, blob `57f962a8b3`
(`git hash-object`, this seat). Pin `0485393f3a`, a trunk commit; tar sha256 `e59596e4d731a89c...`; rollback st31.

## 1. The act and its blast radius

One host: one new package root, the ExecStart, the receipt, ONE host file (the capture library, the old copy kept beside it),
ONE restart. Three things change what the resident does and none runs at a restart: the capture library and its persisted
receipt (only at a capture), and `cause_claim` `measured` on a dead-letter record (only at a fifth failed delivery). No
binding, no IAM, no data, no queue, no portal change. The Opal allow list is unchanged.

## 2. What this seat read itself

- The packet, whole (122 lines).
- **Who can reach a capture**, in `ycharts/generate/resident_worker.py`: `capture_session()` is called at line 259 (inside
  `refresh_session`) and line 351 (the bootstrap, when the session store reads NOT_CONFIGURED), both inside `run()`. And
  lines 687 to 691: a job whose accepted owner is on the Opal allow list goes to `run_opal`, whose docstring at 452 reads
  "An Opal job makes no vendor call and no session". **So neither a restart nor an Opal-produced job reaches a sign-in.**
  That second half matters outside this packet: Andrew's sitting on an Opal report cannot trigger one.
- PRD ADDENDUM v0.12, which item (2) of the packet implements.

**Taken as filed:** the gate result, the census (17 changed, 3 added), the tests, both pins as read from the built package,
the import read that `load_ownership` is off the resident's path. The packet's correction of its own first draft (section 3,
a STOP that would have failed falsely) is noted and is the right way round.

## 3. Conditions beyond the packet's

1. **The rollback's library step has never run, and the release moves a host file st31 did not.** So the installer's own
   restore is exercised before it is relied on: at P1 the operator shows the kept-copy path does not already exist, and after
   V1 it shows the kept copy's sha256 is st31's `857d90b8...`. A rollback that cannot find that file is a STOP that leaves
   the unit as it is and reports, never an improvised copy.
2. **The receipt is read once after the fifth run, by a seat, for what it must NOT hold.** The whitelist is tested against
   planted secrets in a sample (0 of 4); the first real receipt is grepped for a posted value, a cookie and a tokenised URL
   before any part of it is quoted in a record or a message.

The packet's own stand: two P1 STOPs; the installer's two reads of the queue at 0 and 0; rollback on any capture, eviction or
session-refresh line in V1's read. **The first sign-in after st32 is the fifth run, on this seat's word, and not before.**

-- 1.0.0_SA_CTO~DELL2
