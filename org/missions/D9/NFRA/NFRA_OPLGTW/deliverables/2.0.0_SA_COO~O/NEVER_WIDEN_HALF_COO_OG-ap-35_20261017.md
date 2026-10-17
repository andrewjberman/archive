# Never-widen half (COO) -- OG-ap-35, narrowing one client's live grant by one key (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-17 ~03:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-35.md` (`~NFRA1` Phase A, commit `83dc896cad`), sha256 `224a80d88a5248397aa5617d40a3584832828c8d7523e12a5d996a631fe88249` (recomputed by this seat from the file: equal; 7296 bytes). Basis: the CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_OPLGTW_BD68_ALYSSA_DOWNLOADS_ENFORCE_HIS_WORD_20261017_Z.md` @aed4469fa6 (open call `sitez-20261016T111519Z-bd68`), Andrew's word of 2026-10-08, "no downloads needed yet".

## SIGNED, on conditions C1-C7

What this seat read at signing:
- **`ag1.AC1`, issuer re-run: PASS** (the before-record complete with `download_filtered` in her operations, the usage counts numeric, the hashes 10 hex, the denominator printed; the ask carries the three half headings and the four required items; no e-mail and no long digit run). The check was dry-run at the base (FAIL), on synthetic records (PASS) and with six control arms (FAIL) before it was relied on.
- **The narrowing, stated plainly:** her principal loses ONE operation, `download_filtered`; `describe`, `list`, `query` are unchanged; nobody gains anything. Changed keys: `operations` only (`prepare()` accepted the candidate and printed an 8-line diff). Her grant moves from revision 4 to 5.
- **Usage before the write (counts only; reported to the CTO for Andrew):** 0 `download_filtered` calls since her grant's activation, last use none; positive control seen (her 5 events and another principal's 1 download event). The general audit lake carries no record of her principal and is not relied on.
- **The side-write, disclosed by the applier and read by me:** `activate()` also puts her existing `email_deny` record again with the same tid, oid and status active, appends one `operator_audit` record, and writes the `data_entitlement` revision 5; four items of one principal's partition in one transaction, no delete. Her browser-route deny is unchanged by it (the record is identical).
- **What I did NOT read:** the live effect. The read-back is proven only in Phase B.
- **Rollback:** restore. The next revision (6) is the before scope, written through the same `activate`; never a delete or a tombstone.

**C1 -- the ask stays at its bytes through the GO** (sha256 above). Any change re-opens all three halves.
**C2 -- Phase B step 6 re-reads at the GO:** her profile and grant revisions still 4 and 4, and the other two principals' grant hashes equal to `AG1_BEFORE.json`. Anything else = STOP and report.
**C3 -- ONE write**, ledger `nfra-oplgtw-alyssa-no-download` (entry AND sentinel) first and closed at the end.
**C4 -- `ag1.AC2` is read by this seat** from the ledger, `AG1_AFTER.json` and `AG1_BEFORE.json` before `OG-ap-35` is flipped.
**C5 -- a failed read-back restores at once** (the download not refused, or another operation not answering): `activate` the before scope, re-read, close the ledger ROLLED BACK, report.
**C6 -- no tenant, object id, e-mail, account id or grant value** in any file or message; hashes, roles, operation names and counts only; no call is made as her principal; no seat contacts her or her firm.
**C7 -- the `email_deny` record is read before and after the write** and its attribute hash recorded in `AG1_AFTER.json` as `email_deny_hash_before` and `email_deny_hash_after` (10 hex each); they must be equal, since the side-write is meant to change nothing there.

## Not covered

- Lifting the rule: Andrew's one word, "Alyssa may download", restores the operation through the same writer.
- Any other principal, any IAM, Lambda, gateway or environment change.

-- 2.0.0_SA_COO~O
