# X-1 filer entitlement -- never-widen pair DRAFT (COO half): one Opal person files on behalf of the partner firms

**COO half SIGNED by** `2.0.0_SA_COO~Y2`, 2026-10-08 ~19:0xZ (drafted ~19:0xZ; CTO half GIVEN @7b8ba60fa9). **Authority:** Andrew-direct ~18:5xZ, VERBATIM "Alyssa can file on behalf of
all partner firms" (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_185xZ_ALYSSA_FILES_ON_BEHALF_OF_ALL_PARTNER_FIRMS.md`
@d78ef1df76; CTO msg 1436: an explicit list, never "ALL"; CTO signs its half). Separate from the E6 release pair (CTO msg 1444).
Both halves signed; written per section 5 (result in section 6). The person is named here only as the record names her; every key is an opaque id.

## 1. The row and its before-read (read ~19:0xZ, `scan` of `opal-users-v2` SK=PROFILE, 83 items scanned, 1 match)

| field | before |
|---|---|
| key | `PK = USER#usr_63f855c7e1da`, `SK = PROFILE` |
| `firmId` / `userType` / `tier` / `role` / `status` | `opal-capital` / `Dev` / `internal` / `admin` / `active` |
| `allowedFirmIds` | **ABSENT** |

## 2. The one write

`update-item` on that key: `SET allowedFirmIds = ["49financial", "cottonwood", "inflection", "opal-capital", "demo", "mockadv"]` (a DynamoDB list of strings, the shape
`interactive_access.py` and `uploads.py` read), with `ConditionExpression attribute_not_exists(allowedFirmIds)` so it cannot
overwrite a value written since the before-read. No other field. **Rollback:** `REMOVE allowedFirmIds` (back to ABSENT), read back.

## 3. Who reads this attribute (census: `allowedFirmIds` in *.py/ts/tsx/mjs/js/tf, 42 files)

- **The row attribute is read only by IRPT code:** `_scope/canonical_profile_reads.py` (projects it),
  `_scope/interactive_access.py`, `intake/uploads.py`, `_authz/served.py`, and `ycharts/generate/current_authority.py`.
- **Not by the token issuer:** `auth-handler/src/*.ts` has no reference.
- **Not by the portal or other APIs.** `portal-authorizer/index.mjs` computes its own context `allowedFirmIds` from the token: Dev or
  internal tier means `ALL`. `ticket_center`, `opal-partners-data` and the portal read that context, not the row. Her portal,
  ticket and partner-data access do NOT change.

## 4. Effects (STATE COHERENCE: what widens, what narrows, what does not move)

| effect | when | source |
|---|---|---|
| **WIDENS:** she may create an Analysis upload ON BEHALF of a verified advisor of 49financial, cottonwood or inflection; the record names her as actor | only once E6 (release 2) is live | E5 / uploads.py |
| **NARROWS (a):** an upload she creates for one of those three firms WITHOUT `advisor_email` is refused | once E6 is live | ~P2 msg 1442: "a filer listing the tenant must name an advisor" |
| **NARROWS (b):** an Analysis generation job she runs for any data firm NOT on the list (e.g. `opal-capital`, or the test firms `demo` / `mockadv`) is refused `ACTOR_FIRM_NOT_ALLOWED` | **immediately** on the write, on live release 1 | `current_authority.py:135-141` (a list restricts even an OPAL_GLOBAL row) |
| no change | -- | portal, tickets, partner data, every other principal |

**Open question for the CTO half (narrowing b):** Andrew's word grants filing; it does not ask to restrict her. Either (i) the list
also names the firms she generates for today (at least `opal-capital`; and `demo`/`mockadv` if she uses them), which
`uploads.py` still refuses as an on-behalf owner (`INPUT_ACCESS_DENIED` for opal-capital/global), or (ii) the narrowing is
accepted and recorded. This seat recommends (i) with `opal-capital` added, and holds the write until the CTO rules.

**RULED (CTO msg 1447, half @7b8ba60fa9): (i), widened.** The list is the six firms in section 2, so nothing she generates for
today narrows (narrowing b is removed). On-behalf reach stays the three partner firms: `uploads.py` refuses opal-capital as an
owner, and E6's grant excludes `demo`/`mockadv`. Narrowing (a) stands by design (E5).

**Registry pseudo-block check (~19:0xZ):** `data/firm_registry.json` `pseudo` holds one entry, `global` (kind `aggregate`, "NOT a
firm"; the mdpf all-firms channel). It is not a data firm she generates for, so it does not join the list. `firms` holds 5 enabled
entries (3 client, `mockadv` test, `demo` demo), all on the list.

## 5. Order and after-reads

1. Before-read again at write time (field ABSENT); if not ABSENT, STOP.
2. The conditional `update-item`.
3. Read back: `allowedFirmIds` equals the ruled list exactly; no other field changed (compare the projected fields of section 1).
4. If E6 is not yet live: no behaviour read beyond 3. Once E6 is live, its after-reads 4-6 (with this real principal in place of the
   test filer, by opaque id) are the behaviour proof, run under E6's ledger or a successor.
5. Rollback trigger: any read-back mismatch, or a CTO or Andrew word -> `REMOVE allowedFirmIds`, read back ABSENT.

**Executor:** this seat (dell2). `cloudops-dell2-agent-user` already reads and writes `opal-users-v2` (the round-65 test filer put
and delete, row W156-S1 evidence). That table's own key admits it.

## 6. Result (branch WRITTEN), 2026-10-08 ~19:0xZ, by `2.0.0_SA_COO~Y2` on dell2

| step | read |
|---|---|
| 1 before-read (consistent `get-item`) | `allowedFirmIds` ABSENT; firmId `opal-capital`, userType `Dev`, status `active`, role `admin`, tier `internal`; hash of the other projected fields `926c6297e0fa9c24` |
| 2 conditional `update-item` (`attribute_not_exists(allowedFirmIds)`) | rc 0; UPDATED_NEW = the six-firm list |
| 3 read-back (consistent `get-item`) | `allowedFirmIds` = `[49financial, cottonwood, inflection, opal-capital, demo, mockadv]` EXACT; other-field hash `926c6297e0fa9c24` (unchanged) |

No name or email was printed or stored; the hash covers the projected fields other than `allowedFirmIds`. Rollback (not triggered):
`REMOVE allowedFirmIds`. Behaviour proof is owed after E6: one on-behalf admit by this principal, and one opal-capital generation
as before (CTO msg 1447).
