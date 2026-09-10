# STORE_CONTRACT -- `s3://opal-data-research` key grammar

TO: `AMGT_RESAPP.TO-AMGT-s-6` (cell AMGT-s-6, outcome FWD-6, manifest row S6). Worker
`0.9.0_WK_AMGT_RESAPP~7`. Bucket created via `infra/aws/terraform/research/` through
`safe-apply` under change-management entry
`org/critical_paths/change_management/20260910T2059Z_amgt-resapp-opal-data-research-bucket_deploy_completion.md`.

This is a DATA CONTRACT, not new infrastructure. It defines the keyspace every later
cell writes into and reads from -- nothing here requires a second bucket, a second
prefix grammar, or any code. `AMGT-s-1` (raw landing) and `AMGT-s-14` (the input
ledger) are the two named consumers; both must be able to write/read correctly from
this document alone, without asking anyone.

## 1. The three prefixes

```
raw/<vendor>/<security_key>/<YYYYMMDDTHHMMSSZ>/<artifact>        vendor bytes, untouched
derived/<engine>/<security_key>/<YYYYMMDDTHHMMSSZ>/<artifact>    what an engine computed from raw
packs/<security_key>/<YYYYMMDDTHHMMSSZ>/pack.json                the assembled pack object
```

- **`raw/`** -- exactly what the vendor shipped, byte-for-byte, no reshaping (mirrors
  Rule 17a's bronze law: raw stays raw). `<vendor>` is the source name as the estate
  already spells it elsewhere (`bloomberg`, `seekingalpha`, `serp`, `brightdata`, ...).
  Example: `raw/bloomberg/AAPL_US_Equity/20260910T210824Z/model_block.json`.
- **`derived/`** -- what an engine (a parser, a mapper, a qualification-rule pass, a
  drafting step) computed FROM raw bytes already in this bucket. `<engine>` names the
  computing step, never the vendor. Example:
  `derived/model_block_mapper/AAPL_US_Equity/20260910T211500Z/mapped_fields.json`.
- **`packs/`** -- the assembled object a page or a downstream consumer actually reads:
  one JSON per security per stamp, built FROM one or more `derived/` (and where a
  field has no derivation step, `raw/`) records. Never a second place raw or derived
  bytes are copied into -- a pack REFERENCES its sources by key, it does not restate
  their bytes.

`C-RAW-BEFORE-DERIVED` (PRD section 3): raw vendor bytes land before anything derives
from them. In this grammar that is structural, not a convention to remember -- a
`derived/` or `packs/` writer reads an existing `raw/.../<stamp>/` key as its input;
there is nothing to derive from until a `raw/` write already exists.

## 2. `<security_key>`

The identity layer's key: the Bloomberg ticker with spaces replaced by underscores
(`AAPL US Equity` -> `AAPL_US_Equity`), until `AMGT-s-12` (THE IDENTITY LAYER --
Bloomberg ticker, SA symbol, IR domain, social account) states a different key or a
resolution step. Every prefix in section 1 uses the SAME `<security_key>` string for
the same security -- there is exactly one identity axis in this bucket, and it is
this one, until `AMGT-s-12` amends it. A vendor's OWN identifier (an SA `sa_id`, a
CIK, a CUSIP) is never used as `<security_key>`; it is data, and lands as a field
inside the artifact at that key, or as its own `raw/` write if the vendor ships it as
a distinct payload.

## 3. `<YYYYMMDDTHHMMSSZ>`

UTC, always. The instant the WRITE started (not the vendor's `as_of`, which is a field
inside the artifact, never the key -- the OPAL_ASSETS `run_date`-vs-`as_of` lesson
mirrored here). Every write under `raw/`, `derived/` or `packs/` mints its own stamp;
a multi-stage run (fetch, then map, then assemble the pack) produces at least three
DIFFERENT stamps, one per stage, because each stage is its own write and "a single
refresh under one timestamp is a violation" (`AMGT-s-14`'s own bar).

## 4. The two rules that make this a version store and not a log

1. **Nothing is ever written to a path that already exists.** Every write mints a
   fresh `<YYYYMMDDTHHMMSSZ>` prefix; an S3 `PutObject` to a key that already exists
   is never issued by a correct writer. Bucket versioning (this cell's AC2, `Enabled`)
   is the SAFETY NET for the case a writer gets this wrong -- an accidental overwrite
   becomes a new version instead of a loss -- it is not the mechanism a correct writer
   relies on to avoid collisions; the stamp is.
2. **A consumer reads the LATEST stamp under a prefix.** "Latest" for a given
   `<vendor-or-engine>/<security_key>/` (or `packs/<security_key>/`) prefix means the
   lexicographically-greatest `<YYYYMMDDTHHMMSSZ>` child -- which is also
   chronologically latest, because the stamp format is fixed-width and zero-padded.
   `aws s3api list-objects-v2 --bucket opal-data-research --prefix <prefix>/
   --delimiter /` returns the stamp directories as `CommonPrefixes`; the max string
   IS the answer. No index, no pointer file, no "latest" alias key is maintained --
   maintaining one would be a second place that can go stale against the keys
   themselves, and the stamp already sorts correctly.

## 5. Outcome, so `AMGT-s-14` never has to ask

`AMGT-s-14` (THE INPUT LEDGER) renders, per input class: source, last run, outcome,
and lets one class re-run alone while the others stay. This grammar gives it
everything it needs, read-only, from keys already defined above:

- **source** = the `<vendor>` (raw) or `<engine>` (derived) segment.
- **last run** = the latest `<YYYYMMDDTHHMMSSZ>` stamp under that source's
  `<security_key>` prefix (section 4, rule 2) -- or, across every `<security_key>` a
  source has ever written, the latest stamp under the bare `raw/<vendor>/` or
  `derived/<engine>/` prefix, for a source-level "last run" rather than a per-security
  one.
- **outcome** = every writer persists its own output alongside the artifact at the
  SAME stamp: a `_outcome.json` sibling key
  (`raw/<vendor>/<security_key>/<stamp>/_outcome.json`,
  `derived/<engine>/<security_key>/<stamp>/_outcome.json`) carrying at minimum
  `{"outcome": "success"|"failure"|"partial", "started_at": "<UTC stamp>",
  "finished_at": "<UTC stamp>"}`. A run that fails before producing any artifact
  still writes `_outcome.json` at its own fresh stamp with `"outcome": "failure"` --
  the write is the stage's own output either way ("every stage persists its own
  output", this cell's own wording), so a failed run is never invisible as a silently
  missing stamp indistinguishable from "never ran".
- **re-run alone** = a re-run of one input class writes new keys under ONLY that
  class's `<vendor>` or `<engine>` prefix. Because every other class lives under a
  disjoint `<vendor>`/`<engine>` segment and rule 1 (section 4) forbids overwriting
  an existing stamp, re-running one class is structurally incapable of touching any
  other class's keys -- there is no shared mutable state between classes for a re-run
  to disturb.

## 6. Deliberately not built here

No lifecycle expiration, no replication, no notification, no event rule on this
bucket (G-20, this cell's BOUNDS) -- this document is the grammar every future writer
follows by convention, not a policy this cell enforces mechanically. No IAM change and
no bucket policy (this cell's BOUNDS: which principal writes here is `AMGT-s-1`'s and
`AMGT-s-2`'s to establish when they land bytes). No second bucket and no parallel
prefix under another name (G-19).
