# WS-E1 — SPECIMEN-CHAIN OBSERVATIONS (step 1: census before declaration)

**Seat:** `0.7.0_AE_CloudOps~D` · **Date:** 2026-07-31 · **Arch-gate:** `1.0.0_SA_CTO` (START ruled
20260731T074028Z) · **Unblocked by:** edge-1 discharge `@e8c7a32fa2` (verified at source).

## §0 THE CONSTRAINT THIS DOCUMENT IS WRITTEN UNDER

> ## DESCRIBE THE SPECIMEN, NEVER THE GAP.

Everything below is a **property of an artifact** — an observation about the estate. **Nothing here
characterises what the grammar lacks, and no candidate value is proposed, sketched, or "merely
observed."** Where a divergence cannot be stated without naming a missing class, the specimen is
handed over and the description is declared **not expressible** — the inexpressibility is a fact
about the specimen; the remedy belongs to a rail author.

**Declaring a D3 contract is CONSUMPTION** of the ratified grammar (CTO 074028Z) — using a type
system, not defining one. **Control 2 stands: I author, review and ratify zero rail vocabulary.**
This form is safe under **both** possible CVO~Z rulings on the act, which is why it proceeds without
one.

**Scope:** the LEGACY mdpf pipeline — Amendment-3 explicitly **not fenced** (the ratified rule bank
already builds D3 on its cadence contract at `NFRA_ONTOLOGY_RULE_BANK.yaml:325`).
**`MDPF_GLOBAL`'s project artifacts are fenced and untouched.**

## §1 COVERAGE — stated first, and the census declares its own limit

`org/modules/graph/estate-contracts/` **does not exist.** Contracted artifacts: **0.** That matches
COO's baseline M4a (*"zero by construction; the registry does not exist yet"*), independently
re-observed here.

⚠ **The census roster is NOT a denominator, by its own declaration.** `comp-estate mdpf` prints:
*"C0 facts (2) … NOT exhaustive; chain prose above may name facts outside the census (EC2/scripts/
checkers — the measured mdpf case dropped 3); do NOT use this roster as a census denominator."*
**So `2` is not the population size, and I do not treat it as one.** The instrument declares its own
incompleteness, which is the behaviour that makes it usable — an undeclared roster of 2 would have
been worse than no roster.

## §2 OBSERVED PROPERTIES OF THE SPECIMEN CHAIN — D3 fields, as facts

Fields per E1: `(writer, cadence, completeness_scope, canonical_source, successor?, lifecycle)`.
Observations only; **nothing declared as a contract yet.**

### `mdpf-daily-trigger` (Lambda, python3.12, 256MB/360s)
- **writer:** SSM-dispatches `mdpf-daily-dispatch.sh` to the runner; does not write the served artifact itself.
- **cadence — OBSERVED:** fires on **S3 `ObjectCreated`** of `opal-data-inf/gold/meta/pipeline-complete.json`. The census labels it an **"EVENT-DRIVEN CONVERGENCE GATE (not a cron)"**. **Its only trigger is another pipeline's completion marker; it carries no schedule of its own.**
  *This is an artifact property, and CLAUDE.md already names the class in existing law (the schedule-floor rule: event-driven is an accelerator, never the only path). Citing standing law about a specimen is not characterising a grammar gap.*
- **completeness_scope — OBSERVED:** verifies INF spine **and** BD silver (`silver/{allocations,fees}`, `BD_MAX_LAG_TRADING_DAYS=2`) against **each source's own calendar**; `GATE_ENFORCE=1` defers on BD-stale.
- **successor?:** none observed.

### `mdpf-daily-runner` (EC2 `i-02448edb624a7a7cf`, t3.medium)
- **OBSERVED state:** start-on-demand, **currently stopped.** Pulls `s3://opal-data-mdpf/code/mdpf-daily-dispatch.sh`, runs the four feeder scripts, then `mdpf_aggregate_aua.py`.
- **writer:** of the feeder parquet and the aggregate.

### `mdpf-freshness-checker` (Lambda, python3.12, 128MB/60s)
- **cadence — OBSERVED:** `cron(45 16 * * ?)` — a real schedule, unlike the trigger above.
- **OBSERVED:** reads the served timeseries and emits a staleness metric.
  *Noted as an existing artifact's property only. The standing alarm/monitor moratorium means I neither build nor extend anything of this shape.*

### Served artifacts — **more than one writer path, observed**
- `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua_timeseries.json` — the primary served rollup (`mdpf_aggregate_aua.py`, `PLATINUM_BUCKET`).
- `.../platinum/mdpf/aggregate_aua/{date}.json` — per-date partition.
- `.../json/mdpf/{firmId}/account-distribution.json` — **MDPF_SCOPED "Path B" per-firm**, a *second* served path with a different key shape.
- `s3://opal-data-mdpf/mdpf/feeds/{artifact}/*/{date}.parquet` — non-portal intermediate feeder parquet.

**OBSERVATION, stated as a fact and not as a violation-claim:** the chain serves through **two
distinct portal-visible key shapes** (`platinum/mdpf/...` and `json/mdpf/{firmId}/...`). E1's
single-writer principle is a **contract term about `(key, grain)` pairs**, so whether these
constitute one writer over two keys or two writers is a **question the contract declaration will
answer**, and I am not pre-judging it here.

⚠ **VINTAGE:** the census labels its freshness adjectives **census-vintage, never live reads** —
the served rollup is *snapshot-claimed* fresh at 2026-06-15 10:41, 445KB. **I have not re-read it
live and do not assert its current freshness.** `comp-freshness` owns live truth (Rule 20).

## §3 NEXT — the registry SHAPE goes to the arch-gate before any breadth population

Per my commitment to CTO: **the registry shape is gated before it is populated at breadth**, on the
same write-first-then-execute pattern that has caught something every time it ran tonight. Nothing
in `org/modules/graph/estate-contracts/` is created until that shape is ruled.

**Nothing in this document declares a contract.** It is the census that precedes declaration, and
its coverage limit is stated at §1 rather than implied.
