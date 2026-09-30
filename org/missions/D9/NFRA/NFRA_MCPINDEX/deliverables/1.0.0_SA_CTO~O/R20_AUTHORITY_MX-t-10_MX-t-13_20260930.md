# R20 AUTHORITY -- NFRA_MCPINDEX MX-t-10 (X11) and MX-t-13 / MX-r-7 (X12): entries NFRA-MCPINDEX-R20-01 .. -08

**Issuer:** `1.0.0_SA_CTO~O`, 2026-09-30 ~16:4xZ. It is the CTO role that authors the `NAMING_LEGACY_READS.json`
carrier (`.owned-paths.yaml` lane NAMING_LEGACY_READ_AUTHORITY), under 3.0.0_SA_CVO~O's issuer verdict @9c9fa60bc8.

**Acknowledgement:** Andrew-direct 2026-09-30 ~13:0xZ, VERBATIM: "yes thats fine on naming exception". Record:
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260930_13xxZ_R20_ETFS_BDFEES_YES_SCHWAB_GRANT_YES_ADVI_LIFTED.md`
@1eba868308.

**Register rows:** `infra/logic/06_CONFORMANCE_LEDGER.md` section 6, X11 and X12, written by 4.0.0_SA_CRO @3ddc6b3519.
Both are GRANTED CONDITIONAL.

**Gate kind:** `read_context.kind = r20_exception` (`.tools/naming-gate.py` @cb4296f508). It is the only kind that
reaches a NEW literal. It grades naming only: it advances no remediation and proves nothing about reads versus writes.

**Entries:** computed by 2.0.0_SA_COO~MI against the frozen bytes with the gate's own `r20_exception_ok`, in
`deliverables/2.0.0_SA_COO~MI/round5/R20_ENTRIES_MX-t-10_MX-t-13.json` @b9d1b053bc.

## The entries this record authorizes (exactly these, and no others)

| id | file | literal | register | occurrences |
|---|---|---|---|---|
| NFRA-MCPINDEX-R20-01 | `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` | `platinum/etfs/positioning_data.json` | X11 | 1 |
| NFRA-MCPINDEX-R20-02 | `workflows/atom_decomposition/emit_catalog_v02.py` | `platinum/etfs/` | X11 | 3 |
| NFRA-MCPINDEX-R20-03 | `workflows/atom_decomposition/emit_catalog_v02.py` | `platinum/etfs/positioning_data.json` | X11 | 1 |
| NFRA-MCPINDEX-R20-04 | `infra/aws/ec2/opal-gateway/app/integrations/blackdiamond/integration.py` | `opal-data-bd` | X12 | 3 |
| NFRA-MCPINDEX-R20-05 | `infra/aws/ec2/opal-gateway/app/integrations/blackdiamond/integration.py` | `silver/fees/` | X12 | 4 |
| NFRA-MCPINDEX-R20-06 | `infra/aws/ec2/opal-gateway/app/integrations/blackdiamond/integration.py` | `49financial` | X12 | 5 |
| NFRA-MCPINDEX-R20-07 | `infra/aws/terraform/opal-gateway/blackdiamond_reader_iam.tf` | `opal-data-bd` | X12 | 1 |
| NFRA-MCPINDEX-R20-08 | `infra/aws/terraform/opal-gateway/blackdiamond_reader_iam.tf` | `silver/fees/` | X12 | 1 |

**Remediation fields:**
- X12 entries name `ADVI_FIRMBKTS` (the owner of the `opal-data-bd` alias).
- X11 entries name `ETFS_CANON` (the `platinum/etfs/` remediation row @fd3b3b7bf2).

**`as_of_cutoff`:** `2026-10-07` (inclusive, UTC). It covers the commit window. A re-touch after it needs a new record,
never an edit of the date.

## Scope limits

- READ-ONLY at these keys, where the data lives today. No write, no other key, bucket, file or occurrence count.
- A changed count, or the literal in any other file, is refused by the gate. That is the intended behaviour.
- The owning migrations stay LIVE, and nothing here advances or closes them.
- X11 and X12 end when their migrations move the keys onto the builder grammar.

## Landing order

1. The entries land in `org/standards/NAMING_LEGACY_READS.json`, in this seat's own commit.
2. That commit comes only after site-Z CLOUD carries naming-gate @cb4296f508 and X11/X12, because the gate reads the
   carrier and the kind from HEAD.
3. The commit must come BEFORE MX-t-10's and MX-t-13's commits.
