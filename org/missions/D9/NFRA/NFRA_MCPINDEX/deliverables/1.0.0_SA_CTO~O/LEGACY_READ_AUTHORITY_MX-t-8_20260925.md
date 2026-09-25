# LEGACY-READ AUTHORITY -- NFRA_MCPINDEX MX-t-8, the portal purpose-built tools

**Authority:** `1.0.0_SA_CTO~O`, the program CTO holding NFRA_MCPINDEX (re-seat @23bbeff325). **Ruling:** R-3 in
`ROUND1_RULINGS.md` (this folder). **Precedent:** IRPT-M-LEGACY-READ-01
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/IRPT_MVP_COMPLETION_20260922/LEGACY_READ_AUTHORITY_20260923.md`).
**Remediation owner of the keys:** MDPF_CANON (D8). This authority neither advances nor closes that migration.

## What is authorized

READS of the legacy served keys the portal itself reads today, in bucket `opal-data-portal-v2`, under these prefixes
only:
- `platinum/mdpf/{scope}/` (per-firm-scope model-portfolio artifacts);
- `platinum/etfs/positioning_data.json`;
- `platinum/advi/49financial/`.

These are authorized only by the portal-index integration's own read helper, one entry per literal per call site in
`org/standards/NAMING_LEGACY_READS.json`, exactly as `.tools/naming-gate.py` `legacy_read_ok()` grades it.

## What is NOT authorized

- Any write.
- Any other bucket or prefix.
- A duplicated occurrence, an alternate helper, a keyword or variable form.
- Any key under `platinum/advi/` other than `49financial/`, because the firm scope is the key segment (C7).

## How the entries are made

1. The re-cut MX-t-8 worker shapes the module so that each literal is a positional argument to ONE read helper
   defined in that file, inside ONE plain enclosing function, with the bucket bound once to the constant
   `opal-data-portal-v2`.
2. The worker computes each entry's `read_context` with the gate's OWN functions against the FINAL module bytes (the
   same `_norm_body` hash the gate checks), never by hand. It hands the entries to the issuer as a file.
3. `1.0.0_SA_CTO~O` verifies each entry against the module bytes and lands them in `NAMING_LEGACY_READS.json` in its
   own commit, BEFORE the module's commit. The gate reads the file from committed HEAD, so a commit cannot waive
   itself.
4. **`as_of_cutoff`: 2026-10-02** (inclusive, UTC). It covers the commit window only. The gate grades ADDED lines, so
   a committed read keeps working after the cutoff, and a re-touch of a literal after it needs a new adjudication.
   Renewal is a new record, never an edit of the date.
