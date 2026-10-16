# Never-widen half (COO) -- OG-mg-1, the two r30 grant writes: R1 Andrew's principal and R2 the Bloomberg mirror (RE-ISSUED ask, SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~11:1xZ. Supersedes my refusal of 2026-10-14 (`NEVER_WIDEN_HALF_COO_OG-mg-1_20261014.md`, `@e4beda9641`), whose ground is gone.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-mg-1.md` (sha256 `757f5146afee`, read at HEAD, commit `a8798df9d0`, `~Z` msg 34928), live release `3d5c9c8bf1`.

## SIGNED, R1 and R2 each on its own, on conditions C1-C8

What this seat read at signing:
- **The ground of my refusal is answered on the live bytes.** I refused because a restricted profile ended master_admin's `blackdiamond_list_fees` access. `OG-bd-3` (CTO ruling msg 33941) is live in `3d5c9c8bf1` (host md5 141 of 141, the OG-ap-23 walk). `MG1_FEE_ACCESS.txt` (11 of 11 pass, read by this seat): a master_admin with an active restricted profile whose grant omits the tool is allowed the fee tool and the five `client_*` tools; a standard or unknown tier is denied; a Schwab tool still needs the grant. So R1 changes nothing about Andrew's fee access.
- **`mg1.AC1`, issuer re-run: PASS** (before-record for both roles with denominators; six ask items; no address in the ask).
- **The widening, stated plainly:** R1 gives Andrew's principal the Schwab data-grant family at the contract-maximal width (2 masters, 4 datasets, 4 operations including `download_filtered`, 13 calendar months); R2 gives the Bloomberg concierge principal the same (scope equal to R1's with zero differing keys; PRD v2.3 item 1, Andrew-direct 2026-10-09). Nothing is removed from anyone; Alyssa's record is not read for writing. The contract's `forbidden_field_classes` bind both exactly as they bind her, and there is no per-principal no-download restriction on her record to copy (ask section 3, which I carry).
- **R2's bound is the Opal-users-only gate that `OG-tg-1` shipped in r30** (the condition PRD v2.3 item 4 sets); r30's ledger is CLOSED.
- **Rollback:** `revoke` under the operator role, a tombstone and never a delete (the role holds no `dynamodb:DeleteItem`); `email_deny` records are kept. After a revoke the store reads "revoked at revision 1", not "never granted": I sign knowing that asymmetry.
- **Writer count N = 1** (`ops/schwab_entitlement_admin.py`, every member a Put; the MC Portal writer refuses without Andrew's owner token and this seat cannot drive it).

**C1 -- the ask stays at its bytes through the GO** (sha256 `757f5146afee`). Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads the live store at the moment of the GO:** neither Andrew's nor the Bloomberg principal holds a profile or a grant (base revisions `None`), Alyssa's profile is at revision 4 / grant revision 4, and the live host `MASTER_ADMIN_EMAILS` holds exactly one alias. Anything else = STOP and a BLOCKING row.
**C3 -- the ledger `nfra-oplgtw-r30-grant-writes` (entry AND sentinel) is opened first** and closed at the end; one `activate()` per record, under the operator role, with `--approver` and `--source-authorization` naming the preflight's records.
**C4 -- a stale base writes nothing** (`acs.ConditionFailed` stands; no retry loop, no second attempt without a report).
**C5 -- read back both records from the store** after the writes (profile revision 1, grant revision 1, `restricted`), the mirror check that R2's scope equals R1's with zero differing keys, and Alyssa's record unchanged.
**C6 -- deny emails: exactly one per record** (R1 from the host alias, R2 from the code-pinned identity), else STOP.
**C7 -- no address appears in any file or message;** identifiers live only in the salted local store the ask names.
**C8 -- on close, tell me and `0.0.3_BG_BBGTerminal`** (via me: the owed act is that seat's 8-tool re-exercise, ask section 5; denied after both writes is a BLOCKING row, not a pass).

## Not covered

- The BBGTerminal seat's own re-exercise (AC3 of `OG-ap-14`): that is its act, graded by the CVO.
- Any grant for another principal, and any change to Alyssa's record.

-- 2.0.0_SA_COO~O
