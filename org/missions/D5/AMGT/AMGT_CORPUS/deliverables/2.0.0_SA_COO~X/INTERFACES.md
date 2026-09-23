# I4 corpus substrate: version 1 examples

Existing callable: `lib.research.corpus.substrate.substrate(security_key, client=None)`.
This packet documents the existing interface; it does not amend its schema.

The response contains `security_key` and five members: `prior_reports`,
`continuation`, `sector_template`, `fund_form`, `typecast`.

| Member | Present shape | Absence / failure |
|---|---|---|
| prior_reports | List of bronze URI, extraction-byte `sha256`, period and class | Empty list for no typed reports; store errors propagate |
| four derived members | `uri`, `content_sha256`, `method_version`, `inputs_count`, `current` | `{absent: reason}` for absent artifact or unresolved subject; failed reads raise |

**Hash units must not be conflated.** `prior_reports[i].sha256` hashes the
extraction JSON bytes although the adjacent key is `bronze_key`. It is NOT
the bronze-file byte checksum. The C02 manifest pairs the actual bronze URI,
bronze-byte SHA-256, extraction URI and extraction-byte SHA-256 explicitly.
The derived `content_sha256` is the producer's semantic-document hash before
that field is added, using that producer's canonical serializer. The stored
JSON includes the hash field: its retained-byte SHA-256 is a different unit.
Use `retained_byte_sha256` in the examples when populating R's byte manifest.

Full derived `inputs` are in each referenced gold document, not inline in the
substrate response. Load those documents through the existing reader with
the consuming caller's permissions; retain key, byte hash, semantic hash and
method version separately. A failed read must not become `{absent: ...}`.

`current` compares the stored inputs to inputs recomputed by the owning
producer. A new OTHER-class report changes prior_reports immediately and
makes continuation stale. After rebuilding continuation, exactly those two
members' hashes change; sector, fund and global typecast stay unchanged.
Absent security does not imply absent global typecast.

- `evidence/I4_EXAMPLES_v1.json`: poisoned offline exercise with present,
  absent, stale, rebuilt and failed-read controls. Uses the actual corpus
  writers over synthetic inputs; no claim about real report quality.
- `evidence/I4_RETAINED_EXAMPLE.json`: actual retained example for
  `IMB_LN_Equity`, with full referenced documents and distinct hashes.
- `evidence/C02_RECONCILIATION.json`: every one of 351 source files counted;
  123 admitted sources match bronze bytes and extraction lineage; 228 excluded.

Scope qualifiers: 93 folders = 33 resolved + 60 unresolved; admitted PDFs
remain a subset of 184 library PDFs. Preserve the L9 sector denominator
(49 labeled reports, 72 other exclusions, two unmapped out of 123) and
23 evidenced induction candidates of 60, with only one selected. America
Movil AXMB/AMXB remains UNRESOLVED and must not be executed into a served identity.

CTO 24824 period policy is implemented in the candidate: declared year first,
within-year sequence only for comparable granularities, no invented fiscal
close date. Incomparable/equal periods use explicit filing date when available,
otherwise stable input order. The independent validator checks every comparable
pair, including pairs separated by incomparable rows. C02 period_order records
renderer tie decisions separately; the I4 response schema stays unchanged.
The planted 2026-before-FY2025 reversal fails validation; FY2025-before-2026
is the correct ascending order. Raw lexical sorting and its old self-check
cannot establish this property.

R owns the consuming report, common API and shared page. S owns identity
resolution and induction. C owns corpus parsing/substrate and makes no
vendor or model calls. Independent interface acceptance remains CVO's.
