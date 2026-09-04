# NFRA_OUTSET.TO-OS-s-7 -- RESULT: the code_heat parquet's refresh cadence and owner

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-7` · **outcome_ref:** FWD-2, FWD-3
**Verb:** audit -- MEASURE and RECORD. Nothing was created, changed or removed.
**Written at:** 2026-09-04 ~21:4xZ · **Repo vintage:** HEAD `14f26b5eff` on `CLOUD`
**Push state (MEASURED, `git ls-remote origin CLOUD`):** LOCAL @`14f26b5eff`; origin/CLOUD @`fa82d6b93c`.

---

## 0. WHICH OBJECT THIS IS -- a grain the estate already confuses

The cell names "the `code_heat` parquet behind the federated join". The join is
`.tools/_trino_fed.py:20`:

```
code_heat.globgrph.code_heat      (git code-heat, Glue over parquet)
JOIN key: substr(graph_nodes.node_id,8) = code_heat.graph_path
```

⚠ **There are TWO adjacent stores and they are not the same object.**

| store | what | this cell? |
|---|---|---|
| `s3://opal-313476888478-globgrph/warehouse/code_heat/` | the **PARQUET**, Glue-catalogued as `code_heat.globgrph.code_heat`, read by the federated join | ✅ **YES** |
| `s3://opal-313476888478-globgrph/warehouse/globgrph/code_heat_snap_8b0bca7a-.../` | the **Iceberg** `code_heat_snap` table, written by `snap_store.py` | ❌ no |

The existing substrate card `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D11_CARDS_W4/code_heat_snap.v3.1.json`
(carded 2026-08-30T16:20:02Z @`d1928aae5f`) is **the card of the Iceberg table, not of this parquet** --
its own `artifact.location` names this parquet only as a *co-resident* store, "a DIFFERENT store
carrying overlapping subject matter". I used that card as a lead and grounded every number below on the
producer and the live plane instead, so nothing here inherits its claim.

---

## 1. CRITERION O7-AC1 -- JUDGMENT -- THE CADENCE, FROM THE PRODUCER. NO VERDICT.

### 1.1 What writes it

`infra/aws/globgrph/code_heat_emit.py` -- it builds rows directly from git (`git -C` against the
`ajb_workspace` and `portal` repos) and writes the parquet. This is the producer; the artifact is a
projection of git write-history, which is why the producer's own header calls git the canonical
write-history.

### 1.2 On what schedule -- **NONE. There is no cloud schedule, and that is deliberate.**

The AUTHORITATIVE record is in Terraform at HEAD, `infra/aws/terraform/globgrph/item2a.tf:404-409`,
quoted verbatim:

```
# GLOBGRPH_CODEHEAT_ENABLED REVERTED (deleted) 2026-07-16 per CTO TO-2 ruling 033933Z:
# code_heat is git-history-shaped (shells git -C against workspace+portal repos), so the
# container flag gated an import that can NEVER resolve in the Fargate derive -- a
# permanent expected-WARN every nightly trains readers to ignore WARNs. code_heat now
# runs on DEV-BOX CADENCE (option a); the freshness twins on its keys are the guard.
# CTO-authored revert, landed by 0.7.0_AE_CloudOps (owned-paths lane routing).
```

So the producer was **deliberately removed from the nightly Fargate derive** on 2026-07-16 and made
host-bound. "DEV-BOX CADENCE" is not a schedule -- it is *whenever a human runs it on a developer box*.

**Confirmed independently on the live APPLIED schedule plane** (a different instrument from the
Terraform read, so this is corroboration and not repetition):

```
$ .tools/aws events list-rules --region us-east-1
DENOMINATOR: 142 EventBridge rules in us-east-1
rules whose NAME matches globgrph|heat|snap|trino: 5
   infrastructure-snapshot-daily                cron(0 7 * * ? *)    ENABLED
   opal-globgrph-cloudtrail-mgmt                (event pattern)      ENABLED
   opal-globgrph-comp-learns-producer-nightly   cron(0 4 * * ? *)    ENABLED
   opal-globgrph-derive-runner-nightly          cron(0 2 * * ? *)    ENABLED
   opal-globgrph-fedobs-producer-nightly        cron(30 4 * * ? *)   ENABLED
```

**0 of 142 rules fires the code_heat producer.** The five name-matches are the derive runner, the
fedobs producer, the comp-learns producer, a CloudTrail management rule and a generic infrastructure
snapshot -- each a different producer. The sibling producers on this same federation *do* have nightly
rules; code_heat is the one that does not.

### 1.3 When it last ran -- **2026-07-16T03:40:46Z, 50.7 days before this read**

Measured on the live object plane with `s3api` (UTC; `aws s3 ls` would render local time):

```
$ .tools/aws s3api list-objects-v2 --bucket opal-313476888478-globgrph --prefix warehouse/code_heat/
  warehouse/code_heat/repo=ajb_workspace/code_heat.parquet   1,151,262 B   2026-07-16T03:40:45.000Z
  warehouse/code_heat/repo=portal/code_heat.parquet             50,657 B   2026-07-16T03:40:46.000Z
DENOMINATOR: 2 objects under the prefix; both listed; no pagination truncation.
```

The Glue table that fronts them:

```
$ .tools/aws glue get-table --database-name globgrph --name code_heat
  Location : s3://opal-313476888478-globgrph/warehouse/code_heat/
  Owner    : null
  Created  : 2026-06-29T20:23:07Z      Updated : 2026-06-29T20:34:47Z
  classification=parquet  EXTERNAL=TRUE  parquet.compression=SNAPPY
```

**The distinction the cell asked for.** The parquet's own mtime (2026-07-16) and the producer read
agree here -- but that agreement is not what establishes the cadence, and the mtime alone could not
have. The mtime says *when bytes last landed*; the Terraform revert plus the empty schedule plane say
*nothing is coming to land more*. A reader who trusted the mtime would conclude "50 days stale, probably
a broken nightly"; the producer says there is no nightly to break. Those are different worlds and only
the second one is true.

**Trading-calendar check (NEVER#4):** not applicable and stated rather than skipped -- this is a
git-history artifact, not a market feed, so no trading-day frontier governs its staleness.

---

## 2. CRITERION O7-AC2 -- JUDGMENT -- THE OWNER. NO VERDICT.

### **There is no owner of the code_heat refresh.** Stated plainly, as the order requires.

Every candidate carrier was checked and each one is empty or is an owner of something else:

| candidate carrier | read | result |
|---|---|---|
| Glue table `Owner` field | `glue get-table` | **`null`** |
| an EventBridge rule owning the refresh | 142 rules swept | **none** (§1.2) |
| a scheduled ECS/Fargate task | the derive was the carrier; the flag was **deleted** 2026-07-16 | **removed by ruling** |
| the substrate card's per-row `owner` | `code_heat_snap.v3.1.json` -> `0.7.0_AE_CloudOps~X` on all 7 rows | owns **the card row**, and of the *Iceberg* object -- not this parquet's refresh |
| the Terraform comment's actors | CTO authored the revert; `0.7.0_AE_CloudOps` landed it | owns **the 2026-07-16 revert act**, not a standing refresh duty |
| a named seat in the producer | `code_heat_emit.py` header | author attribution, no operator |

The revert comment names its own replacement guard -- "the freshness twins on its keys are the guard" --
which is a **detector**, not an owner. A detector tells you the artifact is old; it does not make anyone
accountable for refreshing it, and nothing in this sweep resolves to a seat or system that is.

**This is the finding, not a gap in the audit.** The artifact is a live input to the federated join:
`Q_CODE_BANDS` and `Q_CODE_COLDEST` (`_trino_fed.py:39-52`) join it against `iceberg.globgrph.graph_nodes`,
and the graph side *is* refreshed nightly by `opal-globgrph-derive-runner-nightly`. So one side of the
join advances daily while the other has been frozen for 50.7 days, and no seat owns closing that gap.

I record it and write no verdict; `3.0.0_SA_CVO` grades at L9. What I do not claim: that the join is
therefore wrong. I did not run the join, and a git-heat projection may age gracefully for some questions
and not others -- that judgment needs the consumer's requirement, which `OS-s-8`/`OS-s-10` carry.

---

## 3. ROWS FILED

No row was filed **from this cell's measurement**. The unowned artifact and the frozen cadence are this
order's DELIVERABLE -- the cell was cut to find exactly this -- and a finding a task order asked for is a
result, not a surprise. Three rows filed under `TO-OS-s-6` (`NFRA_OUTSET-S1..S3`) are recorded in that
result.

**One row was filed from this order's COMPLETION**, not from its measurement:

| row | class | one line |
|---|---|---|
| `NFRA_OUTSET-S4` | **BLOCKING** | 16 of 17 faces in this issuance name their proof instance by a stem `to-pipeline-gate.py` does not search |

It surfaced when the gate REFUSED this order's `complete` flip and aborted the commit: the instance
existed and was VALID, but the face's `<proof_of_spec>` block names
`.../NFRA_OUTSET.TO-OS-s-7.proof_of_spec.json` while `.tools/to-pipeline-gate.py:1261-1270` globs the
**full face stem**. The instance was rewritten as
`.../NFRA_OUTSET.TO-OS-s-7.code-heat-parquet-cadence-and-owner.proof_of_spec.json` -- same granted folder,
the name the mechanism requires. `TO-OS-s-1` alone carries the correct form, which is the control showing
the right shape was available at cut time; amending the other 15 faces is the issuer's act, not this
lane's.

## 4. WHAT I CHANGED

**On AWS: nothing.** `list-rules`, `list-objects-v2`, `get-table` -- all read-only. **In the repo:** only
the two paths in my `<paths>` grant.
