# TCKT_VNEXT round 19 -- register of global (every-firm) admissions

**Authority:** CTO ruling ADDENDUM 7 item 4 (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_IRPT_ANLREQ_FOUR_LANES_END_TO_END_20261015.md`, msg 8833): the two `OPAL_GLOBAL` admissions stand by design, for Opal staff only, and each is named here (route, principal, reason) so no global admission is implicit.
**Author:** `2.0.0_SA_COO~V2` (direct act of cell `R19-rg-5`, 2026-10-16). **Claim:** `measured` for the source lines (read at HEAD of `box/dell2`, line numbers as read, an edit moves them); `held` for the reasons (the ruling's words and the PRD's, not re-derived here).

| # | where (route / function) | principal | what it admits | reason | source at HEAD |
|---|---|---|---|---|---|
| G1 | the report side's interactive access: `authorize_current` in `_scope/interactive_access.py` | `OPAL_GLOBAL` (minted only from the caller-supplied Opal roster, never from headers) | an Opal principal may view another creator's custody or prospect record, any firm | "A view filter never narrows verified Opal authority" (the file's own comment): Opal staff read the original input creator's artifacts; the record's identity, contents, expiry and release stability are validated separately by the caller | `infra/aws/lambda/investor-reporting/_scope/interactive_access.py:115` |
| G2 | the resident's `make_authorize` in `reports/resident_installed.py` | `OPAL_GLOBAL` principal | the same rule on the resident path (no HTTP `current()` comparison there): any owner's record in scope | "the accepted dual-owner design: the actual submitter reads the original input creator's artifacts" (the function's docstring); an owner whose firm is empty, `global` or `opal-capital` is still refused | `infra/aws/lambda/investor-reporting/reports/resident_installed.py:248-260` |
| G3 | the ticket service's firm fence: `_profile_scope` (`lambda_function.py`) | an INTERNAL staff PROFILE row carrying the explicit marker `scope_all_firms = True` and no `allowedFirmIds` (contract item 3; built by `TO-R19-L3`, the marker written by `TO-R19-MIG`) | filing and listing for every firm | the ticket center is `requireInternal` (J7): Opal staff who file for any firm. Before round 19 a row with NO attribute meant every firm by omission; from the release it means no firm, and global is only this BOOL marker | `infra/aws/lambda/ticket_center/lambda_function.py:391-426` (the tail at :418-426 is replaced by `TO-R19-L3`) |

## Not global (named so the register is not read as complete by silence)

- **A named list, not a wildcard:** `svc-commentary` (`COMMENTARY_ALLOWED_FIRMS`, `lambda_function.py:82`), the packager (`PACKAGE_ALLOWED_FIRMS`) and, from this round, `svc-analyst-intake` (`ANALYST_INTAKE_ALLOWED_FIRMS`, `TO-R19-L2`). `ALL` is dropped in each.
- **Staff with a firm list** on the PROFILE row (`allowedFirmIds`): scoped to that list, as before.
- **The DL notice** (`TICKET_DL_MAP`, a `"*"` default row) is a recipient default, not a data admission; it is untouched by this round.

## Change rule

A new global admission is a row here in the same commit that adds it, or the commit is wrong. The owner of G1 and G2 is the report side's project (`IRPT_ANLREQ`); the owner of G3 is TCKT_VNEXT (`2.0.0_SA_COO~V2`).
