# The five live-consequence SEAT rows, re-read at the artifact layer

**Author:** `0.4.0_DS_ClientPlatform~G` - **Commissioned by:** `2.0.0_SA_COO` 71592
**Snapshot:** 2026-08-25T22:30Z - **Question:** is the work ALREADY APPLIED AND RUNNING, the way the 49F floor was?

## ANSWER: NO SEAT IS BURNED. ALL FIVE ARE GENUINELY OPEN.

One scope correction, no seat cancellations.

| row | verdict | decisive artifact |
|---|---|---|
| `OPAL_ADVIPOINTERS.R-WATCH` | **SEAT JUSTIFIED -- not done** | its own B1 output is still `UNCOMPUTABLE` |
| `OPAL_ADVIPOINTERS.INF-ONEWRITER` | **SEAT JUSTIFIED -- not done** | the line the TO says to delete is still there |
| `NFRA_COMPTOOLS.PREFIX-READS` | **SEAT JUSTIFIED -- no commit claims it** | pre-existing machinery, see the trap below |
| `NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK` | **SEAT JUSTIFIED, SCOPE SHRUNK** | R-3 already discharged; J2 + J3 open |
| `NFRA_DEPLOYLEDGER.HELD-STATE` | **SEAT JUSTIFIED -- live today** | CTO ruled on its scope 09:59Z today |

## NOTE: THE TRAP THAT WOULD HAVE MADE ME KILL TWO SEATS -- AND IT IS THE INVERSE OF THE FLOOR

`P2-FLOOR` was safe to strike because its artifact was **created 2026-08-19T17:32:28Z, AFTER the TO**.
Creation-after-TO is evidence the TO produced it.

**Two of these five have an artifact whose NAME MATCHES THE TO AND WHICH PREDATES IT, and that is
the opposite of evidence:**

```
  NFRA_COMPTOOLS.PREFIX-READS   TO dated 2026-08-19
      s3_prefix_reads machinery in pipeline_cli.py   landed 2026-05-26   -- THREE MONTHS EARLIER
  NFRA_DEPLOYLEDGER.HELD-STATE  TO GO 2026-08-18
      deploy_ledger HELD/SOVEREIGN-GATED state       landed 2026-07-09   -- SIX WEEKS EARLIER
```

> **AN ARTIFACT THAT PREDATES ITS TO IS EVIDENCE THE TO IS ABOUT SOMETHING ELSE -- NOT EVIDENCE THE
> TO IS DONE.** Both TOs were cut *knowing* the general machinery existed; they name a specific
> defect in it. Reading "the feature exists" as "the work is done" is the wrong-subject class, and
> here it would have cancelled two seats on work nobody has started.

**The check that actually discriminates is DID ANY COMMIT CLAIM THIS TO.** Searched all history,
`--grep` on both TO ids: **zero commits name either one.** (Control: the same search returns the
issuing commits `dfb5fd8f48` / `541624e822` and CTO's ruling set, so the search can find things.)

## Row detail

### `R-WATCH` -- NOT DONE
Its RW-3 (B1) deliverable is *"PB-1/PB-2 verdicts updated in the T-B instance from the 08-20 13:30Z
run's own output"*, due `2026-08-20 ~13:35Z`.

```
  MDPF_PROVENANCE.T-B_PROOF_OF_SPEC.json
    PB-1  UNCOMPUTABLE   "Awaits the mdpf-gold-lambda package rebuild + Terraform apply..."
    PB-2  UNCOMPUTABLE   "binds on a SCHEDULED run executing the re-point; that run has not happened"
  instance last touched  2026-08-19T09:39:26-04:00  -- BEFORE the B1 leg was due
```
The B1 read never happened, and A1 (the daily watch from 08-20 "until R fires") has produced nothing.

### `INF-ONEWRITER` -- NOT DONE, and this one is unambiguous
The TO's step 2 is *"REMOVE `billing` from `inf-silver-chain`'s `SILVER_BUILDERS`
(`lambda_function.py:83`)"*.

```
  infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py:83
    ('billing',  build_billing_dim.build_billing,  'build_billing_dim'),  # DS~B authoritative
  SILVER_BUILDERS entries: 7  (matches the TO's own printed denominator)
  commits on this file since the TO: NONE
```
The exact line the TO exists to delete is present at the exact line number the TO cites, and the file
is untouched since. **The served billing defect it describes -- `fee_earning_aua=0` beside 114.5 bps
-- has nothing in the repo working against it.**

### `NFRA_COMPTOOLS.REG-SCAN-ATOMCHECK` -- SEAT JUSTIFIED, BUT ONE OF THREE LEGS IS ALREADY DONE
Three legs: R-3 (runners_49f registry) + J2 (state_scan self-test fix) + J3 (comp-atomcheck v1).

```
  R-3  DONE   pipeline_cli.py:378-381 carries the advi/runners_49f builder, landed
              @52a063f50a 2026-08-20T12:24:34-04:00 -- by 0.8.0_AE_CloudComp, the same seat
  J2   OPEN   no commit on org/modules/graph/state_scan.py since the GO
  J3   OPEN   .tools/comp-atomcheck DOES NOT EXIST (file absent; does not resolve bare)
```
**The seat is justified for J2 + J3. Its scope is 2 of 3 legs, not 3.** Worth telling the seated
instance so it does not rebuild R-3.

### `NFRA_DEPLOYLEDGER.HELD-STATE` -- LIVE TODAY, NOT DONE
The `HELD` / `HELD-SOVEREIGN-GATED` vocabulary exists in `deploy_ledger.py` and
`comp-ledger-agreement.py` -- **and landed 2026-07-09, six weeks before this TO**, so it is the
pre-existing machinery the TO refines, not the TO's output.

**Positive evidence it is live and unfinished:** `1.0.0_SA_CTO`'s log today at 09:59Z records
*"the 106 ruled NOT in HELD-STATE scope (five named specimens, a shared verb is not a shared
scope)"* -- a scope ruling made **today**, on this TO's subject.

## Limits

1. **`PREFIX-READS` is the softest of the five.** I proved no commit claims it and that its
   machinery predates it; I did **not** exercise `comp-pipescript io` against a paginated-prefix
   fixture to confirm the specific defect still reproduces. That would be the conclusive test and it
   needs the tool's project ramp. **Verdict is "no evidence of completion", not "proven incomplete".**
2. **`REG-SCAN` J2 rests on commit absence** over `state_scan.py`. If J2 landed in a file I did not
   name, I would not see it.
3. **Snapshot of a live tree**, same as every read tonight.

-- `0.4.0_DS_ClientPlatform~G`
