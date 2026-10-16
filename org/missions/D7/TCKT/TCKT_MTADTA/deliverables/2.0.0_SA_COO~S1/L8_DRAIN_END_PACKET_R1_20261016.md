# L8 drain-end packet -- TCKT_MTADTA round 1 (2.0.0_SA_COO~S1, dell1, 2026-10-16 ~07:5xZ)

**For:** 3.0.0_SA_CVO (and the record for 1.0.0_SA_CTO~DELL1). **Decomposition:** `org/missions/D7/TCKT/TCKT_MTADTA/decompositions/TCKT_MTADTA_DECOMP.md`.
**Issuance:** @c9971df7ca (`fanout: 4 of 4 chains, cap 8`) on PRD v0.2 @86f3caec3a. **Round-close check:** `round-close-check.py --project TCKT_MTADTA
--round 1`: `orders=5 judgment=0 verdict=MAY-CLOSE` (proofs 5/5). Claim words: `measured` = read this session at trunk; `held` = cited from a record.

| cell | order | slot | risk | merged | criteria (worker run; re-run by the issuer in the worker tree) |
|---|---|---|---|---|---|
| MD-i-1 | TO-MD-i1 | ~2 | WORLD (path floor), nothing run live | @42e88e6af6 | `I1-APP-OK`, `I1-SUBS-OK`, `I1-TF-OK`; pytest 10 passed |
| MD-s-1 | TO-MD-s1 | ~4 | WORLD (path floor), nothing run live | @1398fc4fb1 | `S1-SILVER-OK rows=4`, `S1-READDAY-OK`; pytest 16 passed |
| MD-c-1 | TO-MD-c1 | ~3 | WORLD (path floor), nothing run live | @1d9a3c6893 | `C1-GUARD-OK kept=4 dropped={'SharePoint': 1}`, `C1-COVERAGE-OK`, `C1-COLLECT-OK bronze_objects=2`; pytest 11 passed |
| MD-h-1 | TO-MD-h1 | ~1 | WORLD (path floor), nothing applied | @77716ab496 | `H1-ROWS-OK targets=19`, `H1-R20-OK`, `H1-TF-OK`; `validate` OK 55 systems, 15 scopes |
| MD-a-1 | TO-MD-a1 | ~1 | WORLD (path floor), nothing applied | @c301aa1ad0 | `A1-HANDLER-OK calls_logged=7`, `A1-TF-OK`; pytest 20 passed |

Drain checks (measured, at trunk): `py_compile` OK; 57 pytest passed over `data/m365_metadata/scripts/tests` and the Lambda tests; `terraform fmt -check` clean on the
merged root except `collector.tf` (cosmetic alignment); `terraform init -backend=false` + `validate` on a scratch copy with the data-source patch and placeholder zips: Success.
The one real run of the round: `deliverables/2.0.0_SA_COO~S1/thread_trace_r1.py` -> `thread_trace_r1.out.json`, verdict `THREAD-TRACE-OK` (SYNTHETIC events, in-memory clients, no network).

## What the round established (measured)

- **FWD-1's thread exists in code end to end, and has not run on real data.** Collector (filter + levers) -> door `put` -> `derive_silver` -> `get_day` -> `read_day.render`
  produced one person's Eastern day in order (09:00, 10:05, 22:30; the 02:30Z event lands on the previous Eastern date). Real content waits on release acts 1-3.
- **FWD-7's guard held under a search of every stored object:** an outsider's event, an internal recipient outside the eight, an external domain, a subject, a raw IP, an
  unlisted source key and a file name were planted; 0 hits in bronze, state, coverage and the silver parquet bytes. The door refused a non-member and a bronze read.
  Not shown: parquet is compressed, so a byte search of the silver file is weaker than the bronze and column checks beside it.
- **FWD-8's first half is DESIRED, not exercised:** `access.tf` holds the group, role, function, a bucket policy denying the data actions to every principal but the role,
  and a key policy admitting the role alone. Whether an admin's direct read is refused is read only after release act 1.
- **Registry and R20:** rows `trino` (scope) and `m365-metadata` (system), root-map entry `trino`, R20 entry X18 (the drop at collection, PERMANENT; the KMS key's alias form),
  19 targets regenerated (8 of them already drifted at the cut, the hash line only).

## Seams the criteria did not catch (found at the drain)

1. `register_app.py` stored the bare client secret; the collector reads a JSON credential. Fixed by the issuer (`ed86ee4cf3`).
2. `collector.tf` reads the door and the two secret containers as data sources, which fail at plan until they exist. The issuer's lane may not write `infra/aws/terraform`; the
   exact patch is `collector_tf_direct_references.patch`, for the CloudOps seat that applies the root.

## Rows at this packet

Open and armed: `D1-S4` (the bucket policy denies `s3:ListBucket`; a Terraform refresh of the bucket needs it; ARMED, owner 1.0.0_SA_CTO~DELL1, **inferred from the S3 reference, not exercised**),
`D1-W3-S3` (a day's coverage object is overwritten by each hourly fire; INERT until a reader exists; carried to the repair cell). Open observations: `D1-S2` (object ids; the CTO agreed
@msg 6565), `D1-S3` (the issuer's dispositions), `D1-S5` (the collector role is a second invoker of the door; the PRD says group members only), `D1-W1-S2` (three portal targets regenerated and
uncommitted), the other worker rows as filed. Cleared: `D1-W3-S1`, `D1-W4-S1` (sparse cone), `D1-W3-S2` (keys equal builder output).

## Owed at the round-2 recut (on the CTO's round-1 analysis)

Release acts 1-4 of the decomposition (apply by a CloudOps seat with a change-management entry, Andrew's consent, the two secret values and the office egress addresses, the real
run); the `collector.tf` patch and the `ListBucket` decision before the apply; the repair cell (coverage per fire, content time from the listing, typed S3 prefixes); then the
enrichment list: FWD-9 coverage reads, FWD-8 statement, FWD-2 chains, FWD-3, FWD-4, FWD-6, FWD-5, FWD-10. Open at Andrew: the Entra consent; the C-FIELDS levers; external domains.
