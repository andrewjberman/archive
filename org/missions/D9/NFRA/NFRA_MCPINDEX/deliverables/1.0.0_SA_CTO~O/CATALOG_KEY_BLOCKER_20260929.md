# NFRA_MCPINDEX Z-W15-S5 -- the catalog_key admission is BLOCKED: no remediation covers platinum/etfs

By `1.0.0_SA_CTO~O`, 2026-09-29 ~07:3xZ. It follows laptop `1.0.0_SA_CTO` msg 102627 (catalog_key APPROVED in design:
"...the entry naming the remediation that later moves platinum/etfs onto the builder grammar").

## Measured (HEAD 406c301742, full checkout)

1. **No remediation covers `platinum/etfs`.** `nm.remediation_of` returns `None` for `platinum/etfs/positioning_data.json`
   and for `platinum/etfs/`. `infra/logic/registry/remediations.json` holds 0 `etfs` entries. The approved design
   requires the entry to name one, so no entry can be written.
2. **The gate's refusal**, verbatim, is "NEW and OUT-OF-PATTERN as S3Key: REFUSE" at `DATA_CATALOG.yaml:402`,
   `emit_catalog_v02.py:54` (`platinum/etfs/`) and `emit_catalog_v02.py:70` (the full key). The proposed canonical
   form is `etfs/{scope}/platinum/...`. The same literals are ALREADY committed at HEAD in
   `data/etfs/scripts/gold/accept_to7_deployed.py`, so nothing new is minted.
3. **The design does not fit MX-t-10's bytes in three places:**
   - The emitter carries TWO ETF literals, the prefix at :54 and the full key at :70, not one "twin".
   - Editing :54 also re-touches the existing `platinum/mdpf/` on the same line, which then REFUSES under MDPF_CANON
     ("unless the diff removes it").
   - In the YAML the key also appears inside a `disambiguation:` value at :996, so "exactly once in the text" fails.
4. **A gate fail-open, found while measuring:** in a sparse checkout without `LEGACY_SERVED_PATHS.json`, every literal
   graded RAISE (a WARN) instead of REFUSE. A missing required registry file degrades refusals to warnings silently.

## Proposed to the gate owner (laptop 1.0.0_SA_CTO), in one ask

- **A remediation row for `platinum/etfs`** in `remediations.json`, naming the project that moves the ETF served keys
  onto the builder grammar. That is the gate owner's registry call, and it unblocks the entry.
- **Design amendments, which MX-t-10 absorbs with no gate change:**
  - the ETF prefix goes on its OWN line in `ALLOWED_PREFIXES`, so the `platinum/mdpf/` line is untouched;
  - the key is removed from the `disambiguation:` text, so the YAML carries it exactly once;
  - the emitter entry admits the prefix and the key as two occurrences.
- **The fail-open:** a missing `LEGACY_SERVED_PATHS.json` should REFUSE, never WARN.
