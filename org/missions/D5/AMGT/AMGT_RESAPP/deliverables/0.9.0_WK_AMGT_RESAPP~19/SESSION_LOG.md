# AMGT-rj-4 session log -- `0.9.0_WK_AMGT_RESAPP~19`

Worktree `C:/tmp/wk-amgt-11-2`, branch `wk-amgt_resapp-11-2`, cut from SITEZ @`fa72663c56`.
2026-09-15 07:40Z - 08:4xZ. Round 11, chain B, order 1 of 3.

1. **07:40Z the bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-2`; `org/`,
   `.tools/`, `lib/research/identity/`, `lib/opal_data_harvest/` all present. TREE-OK.
2. **07:41-07:46Z re-grounded the premises.** Read `resolver.py`, `build_universe.py`, the
   coverage list (89 folders, 34 MEASURED), the `~1` model blocks (8 files, `<KEY>_Equity`),
   the CRO's identity brief, `lib/opal_data_harvest/{__main__.py,config.json,storage.py}`.
   Measured the ETF plane (AC1) and found its layout is DATE-partitioned, not book-
   partitioned -> row `W19-S1`; measured the harvest bucket (71 objects) and found
   `security-<16 hex>` persisted nowhere -> row `W19-S3`.
3. **07:46Z verified the harvester's key rule by a DISCRIMINATING control** before relying
   on it: `security-` + `sha256('Alibaba BABA')[:16]` = `security-b05e0ccdc9868504`, equal
   to the value `4.0.0_SA_CRO~W` measured independently from the loader and a SQLite read.
4. **07:44Z the SEC fetch** under the session egress word (Andrew-direct ~05:42Z
   @`dfa63b6d92`): the ticker-to-CIK table carries no form type, so `form_expected` was
   MEASURED from each issuer's own EDGAR submissions history -> row `W19-S4`. The join's
   name-agreement guard was designed after seeing three live collisions in the table
   (Rocket/RKT, Rogers/ROG, Sensata/ST).
5. **07:50-08:05Z built** `crosswalk.py` (X-1), extended `build_universe.py` with the union
   mode (U-1) leaving the legacy coverage pass untouched, wrote both schemas and 34 unit
   arms. Ran AC2-AC5.
6. **08:06Z AC6 failed its own discriminator on the first run:** the head-object
   `document-sha256` did not equal the local sha256 of the dry-run bytes. Cause: this
   device's text-mode stdout CRLF-translates the payload (191,481 bytes written where
   188,380 were uploaded), so the dry run was not a dry run of the same object. Fixed both
   emitters to `sys.stdout.buffer`; re-ran AC2-AC6 and the shas match exactly. The
   criterion's readback is what caught it.
7. **08:10Z filed rows** `W19-S1..S6`, committed the code, schemas, tests and rows
   (`282d3f769b`).
8. **08:15-08:25Z AC7**, the AFTER control: `gold/` identical on all three fields. AC7's
   `snapshots/` count has no AC1 before-value, and the bucket has a LIVE PRODUCER (7 of
   1518 objects written under `bbg/` at 07:52:34Z, inside this worker's window) -- so the
   stronger, prefix-scoped control was run instead and is recorded: no object under any
   prefix this cell reads carries a LastModified inside the window. Row `W19-S7`.
9. **08:3xZ** deliverables, proof instance, `<status>` flip, commit 2.

**Bounds honoured.** `s3://opal-data-etfs` READ-ONLY (`list_objects_v2` + `get_object`
only; 0 delete sites, 0 put sites against that bucket in `lib/research/identity/*.py`).
No Bloomberg call. `universe.json` read, never written. Nothing deployed (`rj-10`'s).
Only the two pool objects `crosswalk/v1/2026-09-15.json` and `universe/v1/2026-09-15.json`
were written, each with `Metadata {document-sha256, schema-version}` and a head-object
readback compared against the local bytes. No push, no merge, no rebase, no deletes.
