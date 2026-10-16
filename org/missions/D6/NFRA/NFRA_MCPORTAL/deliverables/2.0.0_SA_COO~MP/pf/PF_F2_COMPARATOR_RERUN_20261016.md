# NFRA_MCPORTAL -- the principal-set comparator re-run (PF4.4, the carried criterion), 2026-10-16 ~15:3xZ

**From:** 2.0.0_SA_COO~MP. **Instrument:** `checks/pf7.run.sh` (read-only: a simulate-principal-policy control, a paginated Scan of the grant table through the IAM user on this box, and the page's own principal-set reader through SSM). Run twice from `/c/Users` ~1 minute apart.

## What it read

| | PF4 run (MP-pf-7) | this run | note |
|---|---|---|---|
| table items scanned (complete, 3 pages, per-page equals scanned) | 1,669 | 1,758 and 1,759 | the table also holds live session items, so the count moves between runs |
| POLICY items, pre-filter (the PF4.4 criterion) | not printed (9 shown post-filter) | **25** | now printed |
| excluded: `probe` (`POLICY#probe-*`, not a GUID) | 3 | **7** | grew by 4 |
| excluded: `emaildeny` (`POLICY#EMAILDENY#<digest>`) | 1 | **3** | grew by 2 |
| excluded: `operator_audit_item` (an audit row of the grant writer, not a grant) | rows not printed; audit-only principals 0 | **6** rows | `audit_only_principals` still 0: every audit row sits on a principal that also holds a grant |
| grant-bearing principals | 3 | **3** | raw set and page set both `1e57d66075fe`, `85f5312f95ee`, `b43a6e7dd649` (12-hex digests) |
| grant-bearing POLICY items (the PF4 "nine") | 9 | **9** | 25 minus the 16 excluded; unchanged |

The sum holds by the script's own rule: 25 POLICY items = 15 principal-key items (`POLICY#<guid>#<guid>`: 9 grant-bearing + 6 `operator_audit` rows) + 3 emaildeny + 7 probe. The 6 audit rows therefore sit INSIDE the 15 the script prints as `policy_items`.

## Verdict (mine, bounded)

- **The comparator agrees: raw set = page set, 3 of 3, the same three digests**, from a complete Scan (the simulate control: the IAM user's Scan allowed, the operator role's implicit deny, so the Scan is this user's plane, not the gateway host's).
- The PF4.4 criterion is met: the pre-filter total and each excluded class are printed with count and reason.
- The two classes PF4 counted GREW since then (probe 3 to 7, emaildeny 1 to 3); the audit rows were not counted in PF4 (6 now). None is a grant, so the page's set is unaffected. The probe rows are the residue that row Z-S160 (NFRA_OPLGTW) already owns. Not verified here: who wrote the four new probe keys and the two new emaildeny keys, and when; and whether the 6 audit rows are the sanctioned writer's (the writer appends `operator_audit` and deletes nothing).

## What this does not claim

- It does not re-grade Z-C-S40 (the CTO's, REALIZED "for today"); it adds a second dated read that agrees.
- The three principals are named by digest only; no tenant, object id or email is printed or committed.
