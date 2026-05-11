<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY</id>
    <project>ADVI_INFNNA</project>
    <title>Silver layer canonical ID dtype enforcement — eliminate cross-dim drift at the source; convert gold coerce_id_columns from load-bearing to belt-and-suspenders</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>medium</priority>
    <estimated_effort>~2-4h (audit + helper + builder updates + partial rebuild)</estimated_effort>
    <actual_effort>~2h (audit + helper + builder updates + in-place migrate via Option A pivot + Step 5 cascade)</actual_effort>
    <authorized_by>Andrew direct 2026-05-11 (follow-up to ACCOUNT-ID-COERCE root-cause analysis)</authorized_by>
    <closed_date>2026-05-11</closed_date>
    <closed_by>0.4.0_DS_ClientPlatform~A</closed_by>
    <closed_via>RAVC4 to COO 17:36Z. Gates 1-10 ✅ per CTO+COO pragmatic close (35/37 OK + 2 documented transient S3 SSL failures on 2019-stale-era keys ratified as Gate 1; INF_C02_C03_TLS_HARDEN authoring as separate follow-up TO). In-place dtype migrate executed (9,296/9,296 ok, 6.8min wall, ~50x faster than full bronze rebuild). Int64 sample-validation 12/12 PASS. Wall +6.9% vs ACCOUNT-ID-COERCE baseline (within ±10% tolerance). Commits f6b7238a9 + 8b4c59861. Memory entry shipped with dtype-only-fix vs transformation-change taxonomy.</closed_via>
  </metadata>

  <references>
    <ref type="parent_analysis">COO root-cause analysis 2026-05-11 — cross-dim ID dtype drift identified as architectural inconsistency (not Orion drift, not deprecation, not historical artifact)</ref>
    <ref type="empirical_evidence_1">silver/transactions/{date}.parquet — account_id, rep_id = object (str)</ref>
    <ref type="empirical_evidence_2">silver/api_dims/accounts_v2/snapshot_date=…/data.parquet — account_id = object (str) via explicit astype(str) line 425</ref>
    <ref type="empirical_evidence_3">silver/api_dims/positions_mv/snapshot_date=…/data.parquet — account_id = Int64 (no explicit cast, parse_int helper passthrough)</ref>
    <ref type="parent_to">ACCOUNT-ID-COERCE `5287179fb` (in flight) — gold-side defensive coerce_id_columns(df, cols=('account_id', 'rep_id')) closes immediate symptom in 6 affected scripts</ref>
    <ref type="ds_a_widening">2026-05-11 — DS~A discovered rep_id has same drift class as account_id; widened helper to coerce both</ref>
  </references>

  <context>
    The ACCOUNT-ID-COERCE fix closes the **symptom** at the gold-write boundary. The **architectural inconsistency** lives in the silver builders themselves — different `build_*` functions write the same logical column with different dtypes:

    - `build_accounts_v2` (commit `c3ba33c18`): **explicit** `astype(str)` on account_id (line 425 of convert_orion_api_to_silver.py)
    - `build_positions_mv` (commit `496ad4afc`): **implicit** Int64 via parse_int helper passthrough
    - `build_transactions` (commit `33180d972`): **implicit** str via CSV parse passthrough (no explicit cast)

    No documented canonical convention exists. Each builder was written separately, at different times. This is accumulated tech debt — latent until the first full instrumented cascade exposed the cross-dim concat dtype mismatch on 2026-05-08.

    **Canonical decision — Int64 (nullable):**
    - Type-correct for numeric IDs (all Orion IDs are integer values)
    - Smaller parquet column size
    - Aligns with gold-side `coerce_id_columns` direction (already Int64)
    - Matches `positions_mv` current behavior (less migration there)
    - Nullable Int64 (capital-I) accommodates missing/null ID values without falling back to object dtype

    **Net architectural goal:** every silver builder writes every logical ID column as `Int64` (nullable). The gold-side `coerce_id_columns` helper becomes **belt-and-suspenders defense** rather than load-bearing — same outcome on parquet write, but redundancy across both layers.
  </context>

  <scope>
    <step>
      **ID column audit.** Survey all silver builders in `data/orion/scripts/silver/convert_orion_api_to_silver.py` (and `_orion_api_silver_lib.py`). Enumerate every column ending in `_id` written by any builder. Build a matrix:

      | Column | Builders writing it | Current dtype per builder | Target dtype |
      |---|---|---|---|
      | account_id | transactions, accounts_v2, positions_mv, performance, billing, activity, ... | str/str/Int64/...  | Int64 |
      | rep_id | (likewise) | ... | Int64 |
      | household_id | ... | ... | Int64 |
      | client_id | ... | ... | Int64 |
      | registration_id, custodian_id, etc. | ... | ... | Int64 |

      Output: comprehensive table committed to session log + propose final canonical column list.
    </step>

    <step>
      **Add canonical silver-side coerce helper.** Build `coerce_silver_ids(df, cols=None)` at `data/orion/scripts/silver/_orion_api_silver_lib.py` (or appropriate location next to other silver helpers).

      Default cols: the canonical ID column set identified in Step 1. Idempotent. Same internal mechanism as gold-side `coerce_id_columns` (`pd.to_numeric(errors='coerce').astype('Int64')`).

      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/silver/*.py`.
    </step>

    <step>
      **Update all silver builders.** Add a `coerce_silver_ids(df)` call immediately before each builder's `return df[cols]` line. Remove any conflicting explicit casts (e.g., `accounts_v2`'s `astype(str)` line 425 — replace with the helper).

      Document the convention in a header comment in `convert_orion_api_to_silver.py`:
      ```
      # SILVER ID DTYPE CONVENTION (2026-05-11, ADVI_INFNNA.SILVER-ID-DTYPE-UNIFY):
      # All columns ending in _id MUST be Int64 (nullable). Use coerce_silver_ids()
      # before return df[cols] in every build_* function. Gold layer has a
      # belt-and-suspenders coerce_id_columns helper that defends against
      # cross-dim merges; silver-side enforcement is the canonical source.
      ```

      Pre-commit gate on every file touched.
    </step>

    <step>
      **Full silver rebuild — Andrew directive 2026-05-11.** Andrew's read: "the whole Inflection data set isn't even that big, which means that even if we do full rebuilds of all this stuff, it shouldn't really take a meaningful amount of time."

      Rebuild ALL silver dims with the new canonical Int64 enforcement applied uniformly. Use the existing per-date dispatcher pattern (mirror PERFDIM-CREATOR ThreadPoolExecutor 64-worker pattern). Per-dim:

      - `silver/transactions/` — 1,510 partitions
      - `silver/api_dims/accounts_v2/` — all snapshot dates (currently 7 — backfill to frontier if SILVER-ACCOUNTS-HIST hasn't yet)
      - `silver/api_dims/positions_mv/` — all snapshot dates
      - `silver/api_dims/performance/` — all snapshot dates
      - `silver/api_dims/tax_realized/` — all per-date partitions
      - `silver/api_dims/billing/` — all
      - `silver/api_dims/activity/` — all
      - `silver/api_dims/household/` — all
      - `silver/api_dims/assets_v2/` — 1 snapshot
      - Any other dim discovered in Step 1 audit

      Rationale for full rebuild over surgical:
      - Eliminates any latent inconsistency in dims we haven't audited at column level (other than ID cols, other columns may have undetected drift)
      - Establishes a single uniform-shape silver corpus
      - Inflection data volume is small enough that wall-clock is tolerable
      - Subsequent SILVER-ID-DTYPE-ENFORCEMENT pre-commit gate can be validated against a clean baseline

      Document each rebuild's partition count + wall-clock + soft-fail rate.
    </step>

    <step>
      **Validation cascade.** Re-run full INF gold cascade (mirror ACCOUNT-ID-COERCE's cascade pattern). Telemetry path `.runtmp/telemetry/{YYYY-MM-DD}/inf-gold-layer-runner/`.

      Verify:
      - Cascade still 37/37 OK (gold-side `coerce_id_columns` is now redundant defense, not load-bearing)
      - Wall-clock baseline preserved (silver-side coerce adds negligible overhead — &lt;5% expected per builder)
      - No new errors in any gold script

      If a gold script breaks: gold reads non-ID-column data with wrong dtype expectations — surface in RAVC, don't auto-patch.
    </step>

    <step>
      **Deprecation decision for gold-side coerce.** After 1 week of stable cascade runs with silver-side enforcement active:

      **Option A — Keep gold coerce permanently** (belt-and-suspenders): defends against future silver inconsistency reintroduction. Recommended.

      **Option B — Remove gold coerce** after silver is canonical: trims the helper layer. Risky if a future silver builder forgets the convention.

      Default to Option A. Surface in RAVC for COO ruling.
    </step>

    <step>
      **Memory entry.** Once cascade stable post-migration, propose memory entry:
      `feedback_silver_id_dtype_convention.md` — documents canonical Int64 convention + reasoning. Path under `.../memory/`. Defends future agents from re-introducing drift.
    </step>

    <step>
      **Commit + push + RAVC.** Bundle:
      - Helper file
      - All silver builder edits
      - Header comment in convert_orion_api_to_silver.py
      - Any session-log rebuild documentation
      - Author: `0.4.0_DS_ClientPlatform~A`

      RAVC payload:
      - Step 1 audit matrix
      - Step 4 rebuild counts + wall-clock
      - Step 5 cascade validation (37/37 OK + wall-clock vs ACCOUNT-ID-COERCE baseline)
      - Step 6 keep-vs-remove gold coerce recommendation
      - Step 7 memory entry draft
    </step>
  </scope>

  <acceptance_criteria>
    1. **ID audit matrix** delivered in session log with every silver builder × every ID column → current/target dtype.
    2. **Silver-side helper** `coerce_silver_ids` exists at canonical location + idempotent + tested.
    3. **Header convention comment** in `convert_orion_api_to_silver.py`.
    4. **All silver builders** call `coerce_silver_ids` before return; conflicting explicit casts (e.g., accounts_v2 astype(str)) removed.
    5. **Pre-commit gate** PASS on every file edit.
    6. **ALL silver dims rebuilt** with canonical Int64 enforcement (Andrew directive 2026-05-11 — full rebuild over surgical). Documented partition counts + wall-clock + soft-fail rates per dim.
    7. **Validation cascade** 37/37 OK with wall-clock within ±10% of ACCOUNT-ID-COERCE baseline.
    8. **Gold-side coerce_id_columns** disposition documented (recommendation: keep as belt-and-suspenders).
    9. **Memory entry** drafted (canonical Int64 convention + reasoning).
    10. **RAVC delivered** with audit matrix + cascade evidence + memory-entry path.
  </acceptance_criteria>

  <blocking>
    **Blocked by:** ACCOUNT-ID-COERCE TO completion (do not touch silver while gold cascade is in flight). After cascade `bdjyofvvo` lands clean, this TO unblocks.

    Adjacent gates:
    - LEADERBOARD-JOE-ABSENT may execute or close-resolved-by-cascade before this TO picks up — does not block.
    - SILVER-PERFORMANCE-HIST + SILVER-ACCOUNTS-HIST are independent — can run before, after, or in parallel.

    No Andrew gate beyond initial 2026-05-11 GO. Bandwidth-gated only.
  </blocking>

  <notes>
    This is the architectural follow-up to ACCOUNT-ID-COERCE. Gold-side closes the symptom; silver-side eliminates the source.

    **Why Int64 over str:**
    - Orion source values are integer-valued (no observed non-numeric IDs)
    - Smaller parquet footprint
    - Type-correctness for numeric joins/comparisons
    - Aligns with gold-side fix direction (consistency)
    - Nullable Int64 accommodates missing values without object-dtype fallback

    **Why not rebuild ALL silver partitions:**
    - Many dims already write Int64 correctly (positions_mv, etc.)
    - Rebuild cost scales with partition count × wall-clock per dim
    - Surgical rebuild matches the affected dims only — same outcome, lower cost

    **Why keep gold helper:**
    - Belt-and-suspenders defense against future silver inconsistency
    - Negligible runtime overhead (&lt;1% per Friday's empirical)
    - Removes a re-introduction risk if a new builder forgets the convention

    **Pattern note:** ACCOUNT-ID-COERCE + this TO together demonstrate a clean defense-in-depth pattern: enforce canonical convention at the data layer + defensive coerce at the consumer boundary. Worth documenting as an architectural pattern in addition to the memory entry for the specific ID-dtype rule.
  </notes>
</task_order>
