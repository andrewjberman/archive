# B08 corpus-to-consumer join: proposed additive interface

Mandate: CONTRACT v1.0 / COO_X_CORPUS.md at `0e33cea24b`; trace B08 at
`fd51c46d81`. Producer owner `2.0.0_SA_COO~X`; Served Runtime / Experience
sole writer `2.0.0_SA_COO~Z`. This packet is an interface publication and a
proposed owner patch, not an applied runtime change or independent acceptance.

Call `lib.research.corpus.report_input.read_report_input(resolved_security_key,
client=authorized_s3_client)`. The key must come from the existing route's
resolved identity. No alias normalization, new permission context or writer
is introduced. The existing five-member `substrate()` response is unchanged.

| Producer fields | Proposed destination in actual `read_thesis_bundle` |
|---|---|
| `interface_version`, `security_key`, `observed_at` | `bundle.corpus` same names; observation time is not source vintage |
| `state`, `reason`, optional `error_type` | `bundle.corpus` same names; CURRENT / STALE / ABSENT / FAILED |
| existing `substrate` response | `bundle.corpus.substrate`; all five original members and `current`/`absent` values retained |
| `prior_reports` | `bundle.corpus.prior_reports`; original bronze key / extraction `sha256` plus explicitly named extraction URI, extraction-byte hash, bronze-byte hash, period absence reason |
| `documents` | `bundle.corpus.documents`; exact parsed selected derived documents, or named absence |
| `member_states`, `member_hashes` | same keys under `bundle.corpus`; exact sibling invalidation comparison |
| `input_manifest`, `input_manifest_sha256` | same keys under `bundle.corpus`; actual object URIs/byte hashes, optional semantic hash/method version and storage `last_modified` |

The current pinned Runtime function consumes none of these fields. The proposed
patch consumes this exact field set through one whole `corpus` object; it does
not claim the current frontend renders it. The Experience owner must explicitly
carry typed `corpus` fields through the existing thesis client/query and render
prior reports/context or named states. No additional route is proposed.

`observed_at` is this read's UTC time. `last_modified` is returned S3 metadata,
or null if unavailable; neither is a report's declared period. The input manifest
hash binds security identity, member states and referenced object bytes; it
excludes observation time and storage metadata. Semantic `content_sha256` is
carried from the producer, distinct from the independently measured byte hash.
References cover the artifacts delivered as report inputs, not a claim to capture
every transitive read or an atomic cross-object S3 snapshot.

CURRENT means admitted reports exist and every present derived member is current;
optional derived absence remains visible. ABSENT means no admitted prior reports,
even if the global typecast exists. STALE retains the old artifact with `current=false`.
FAILED has no substrate or partial manifest and exposes only a safe error type.
The report writer must not replace the last accepted revision on FAILED/STALE.
This read-only adapter neither persists nor independently proves revision-store
preservation; that is the Runtime publication boundary. A stale before-rebuild
observation and rebuilt observation have distinct manifests; unchanged sibling
member hashes remain equal.

## Exact owner patch and proof

`I4_RUNTIME_JOIN.patch` targets `lib/research/api/scoped_amgt.py` at
`1b1244cecf`. It adds only the corpus input at the end of `read_thesis_bundle`,
after identity resolution. All other top-level ASTs are byte-independent AST
equals. Base, patched source and patch SHA-256 values are recorded in
`evidence/I4_CONSUMER_JOIN_OFFLINE.json`. It has NOT been applied to any
Runtime source file. The owner should review/rebase against its actual pin.

`prove_consumer_join.py` compiles the actual pinned function plus the proposed
insertion in memory and calls the real corpus adapter against producer-written
fixtures under external-operation poison. Six cases pass: positive, absent,
stale-before-rebuild, rebuilt, missing retained extraction, unresolved identity.
After rebuild exactly prior_reports and continuation hashes change; siblings
remain equal. Other thesis helpers and identity are explicitly fixtures.

Deployment prerequisite for the Runtime owner: include the new module AND the
existing corpus/harvest/naming/PyArrow dependency closure and required read
permissions in its reviewed target package. Existing API source explicitly says
harvest.store/naming were outside its deployed closure; the patch alone is not
a deployable package. Preserve existing auth, no-span gating and never-widen
controls. Account for measured read fanout; no caching policy is silently added.
No cloud permission, served write or deployment authorization is supplied here.

## Real retained-input observation and populations

`evidence/I4_REPORT_INPUT_RETAINED.json` exercises the new adapter on
`IMB_LN_Equity`: CURRENT, 15 prior reports, 33 manifest references; continuation,
fund form and typecast current, sector template ABSENT because labels conflict
between consumer-non-cyclicals and technology. Its substrate equals the earlier
retained observation. 142 GETs / 9 LISTs / zero writes; explicit write-refusal
control passes. This is a backend retained-data read, not an authenticated API
or browser trace.

Population remains **123 admitted of 351 files; 228 excluded; 93 folders, 33
resolved and 60 unresolved** at the recorded C02 census vintage, carried in the
real-read evidence. A one-security read did not recompute that population.
America Movil AXMB/AMXB remains unresolved; its READY request must not execute.

**C1-C3 remain NOT_EVALUATED until B00/E0 and independent live acceptance.**
The existing c-11 read-only evidence is folded into B08/FWD-9; its historical
order is not rewritten or silently declared complete. No new order is cut.
