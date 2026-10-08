# L8 drain end -- IRPT_BCKEND rounds 79 and 80, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~19:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD by path
floor; nothing was uploaded or applied in either round | **Drains:** round 80 @9a594e96a8 (branch 175), round 79 @038b35d676 (branch 174)

**Judgment criteria:** 0. Both orders are terminal (`complete`) with their proofs VALID. The issuer re-ran every mechanical criterion on
the worker's branch before the drain. `round-close-check` reads MAY-CLOSE for rounds 79 and 80.

## Round 79 -- IB-pr-366, slot ~174: the live guard resolves an on-behalf owner (E5, ADDENDUM 2)

- **STOP, then ruling.** The first run stopped under its refusal clause (row D2-W174-S1): no existing read yields an owner PRINCIPAL other
  than the filer. The CTO ruled option (c) (msg 1402; Andrew confirmed ~18:3xZ that on-behalf upload is wanted). AMENDMENT 1 @1e3ab5d454
  added four negative arms.
- **Fix fff1b0395a (`_authz/served.py`):**
  - The served CREATE wires the existing `get_user` read into `InteractiveAccess` (`allowedFirmIds`), read once per request.
  - An `advisor_email` query parameter is a lookup key only. It is verified by `get_partner_profile(email, tenant)` and `get_user(email)`
    on the registry-validated tenant: matching email, same firm, status `active`.
  - The owner is built by `resolve_prospect_owner` from that advisor's claims.
  - `uploads.py` and `interactive_access.py` are untouched.
- **Graded by the issuer:**
  - IB79-1-AC1 PASS (admit arm through served: 2 passed).
  - IB79-1-AC2 PASS (8 negative arms: 15 passed).
  - IB79-1-AC3 PASS (6 of 6 suites, each in its own process).
  - Control: the new tests fail 6 of 18 against the old `served.py`.
- **One behaviour to note:** a filer whose list names the tenant but who names no advisor is now refused NOT_AUTHORIZED with nothing
  stored. It was refused before too, by `uploads.py` (UPLOAD_CREATOR_MUST_BE_CURRENT_ACTOR / UPLOAD_ACTOR_ATTRIBUTION). Every other owner is
  today's.
- **For `~Y2`'s re-pin and new release-2 pair (E6):**
  - The email travels as the query parameter, because `uploads.py` rejects unknown body fields.
  - Row D2-W174-S3: the role grants no read on `opal-partner-<firm>`, so a deployed build refuses every on-behalf admit until an IAM grant
    lands. That grant is a laptop act.

## Round 80 -- IB-pr-367, slot ~175: repository.py repin for the CUSTODY_REPORT kind (E7 part 1, ADDENDUM 4)

- **Pin a0d8d4943f.** Two staged rows of `irpt-export-render` are repinned: `repository.py` to b13bab7495 (KINDS gains CUSTODY_REPORT),
  and `retention.py` to f60e6f1d2a.
  - The issuer verified `retention.py` is required: the packaged `reference()` takes 3 arguments, and the new repository passes 4
    whenever the revision is a string.
- **Census at the pin:** `changed_members=2`, both owned. BUILD_ONLY ran from a clean tree (rc 0, no residue); built
  `idanP8nX/mqaQ+FIGGY6AT4Xe/JxckOM3N0rWwivSh8=`.
- **Graded by the issuer:** IB80-1-AC1, AC2 and AC3 PASS.
- **Packet** blob aa9115a66f. COO half @764a0abf3c, CTO half @275e506034 (release first, plus a retained-read regression check).
  The release is round 81 (IB-pr-368, issued @fba505cec6 on branch 176, worker ~176 running).

## Rows

| row | status |
|---|---|
| D2-W174-S1 | Resolved by D2-W174-S2 (ruling (c), fix fff1b0395a). |
| D2-W174-S3 | Carried by D2-S5 to `~Y2`'s E6 pair (the IAM read grant, a laptop act). |
| D2-W175-S1 | Carried by D2-S5 to E8 (`~M2`) and E9 (IB-pr-369, round 82, issued @c1d9cdc323, worker ~177 running). |

## In flight in this lane

- Round 81: IB-pr-368, the IB-pr-367 release, with pre and post retained read-back.
- Round 82: IB-pr-369, E9 code. Its own release pair follows after IB-pr-368 is live (ADDENDUM 6 order).

**Push state:** LOCAL (dell2 CLOUD drain pending).
