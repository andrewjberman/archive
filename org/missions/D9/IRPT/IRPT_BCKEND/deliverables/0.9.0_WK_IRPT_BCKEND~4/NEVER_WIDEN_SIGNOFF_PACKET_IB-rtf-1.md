# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtf-1

Cell `IB-rtf-1`. Two DIFFERENT classes of CANONICAL-ABSENT finding are in this packet -- kept
separate because their evidence and their remedy differ (see each section).

---

## CLASS A -- pre-existing, no true source anywhere, ever (rows W4-S34/W4-S35)

A content-addressed search of the whole reachable git object graph (`git hash-object --no-filters`
then `git cat-file -e` / a full `git rev-list --objects --all` index, not a path guess) found the
exact served bytes committed nowhere, ever, at ANY point in this repository's reachable history.
NOT deployed, NOT committed as source by this order. Same content and same absence as rows
`IRPT_BCKEND-W4-S34`/`W4-S35` (re-verified fresh this run, identical oids to those rows' own).

### irpt-intake-poller :: firm_registry.json

- **Blast radius:** the full served content (5229 bytes) is `present-only-in-served`; no canonical exists to diff against (0 of 0 canonical keys/lines).
- **Rollback:** the served bytes themselves -- `blob cc3f2c63bb2d8c14a3d65b2bb2215b4089e5e776718a307660a253eebfbd25e3` (sha256), fetched fresh each run from the LIVE DEPLOYED Lambda's own code (`aws lambda get-function --function-name irpt-intake-poller --query Code.Location`).
- **Writer census (N=1):** a scoped search of `infra/aws/lambda/investor-reporting/**`, `data/**`, `infra/logic/**` and `lib/**` for the literal string `firm_registry.json` (22 candidate files) found exactly ONE producer: `lib/opal_naming.py generate --target data/firm_registry.json`, reading `infra/logic/registry/scopes.json` (`data/firm_registry.json:2` @ HEAD, its own `_generated` header names this exactly). Every other hit is a READER or documentation. See `R58-AC2_judgment.md` s.1-2.
- **Disposition:** NOT deployed by this order; NOT committed as source. The member's row stays ARMED, `disarm_owner: 2.0.0_SA_COO~B to route`, per the existing investigation row.

### irpt-ycharts-generate :: firm_registry.json

- **Blast radius:** the full served content (5229 bytes) is `present-only-in-served`; no canonical exists to diff against (0 of 0 canonical keys/lines).
- **Rollback:** the served bytes themselves -- `blob cc3f2c63bb2d8c14a3d65b2bb2215b4089e5e776718a307660a253eebfbd25e3` (sha256), fetched fresh each run from the LIVE DEPLOYED Lambda's own code (`aws lambda get-function --function-name irpt-ycharts-generate --query Code.Location`).
- **Writer census (N=1):** same as `irpt-intake-poller`'s row above -- one producer, `lib/opal_naming.py generate`, no producer specific to this function.
- **Disposition:** NOT deployed by this order; NOT committed as source. The member's row stays ARMED, `disarm_owner: 2.0.0_SA_COO~B to route`, per the existing investigation row.

### irpt-ycharts-generate :: settings.json

- **Blast radius:** the full served content (9815 bytes) is `present-only-in-served`; no canonical exists to diff against (0 of 0 canonical keys/lines).
- **Rollback:** the served bytes themselves -- `blob a05bcea4d3cdfda972a35bf3bf088c6794728b426d924cbd2069a94ab33aed44` (sha256), fetched fresh each run from the LIVE DEPLOYED Lambda's own code (`aws lambda get-function --function-name irpt-ycharts-generate --query Code.Location`).
- **Writer census (N=0):** a scoped search of `infra/aws/lambda/investor-reporting/ycharts/**` and `infra/aws/lambda/investor-reporting/intake/**` for the literal string `settings.json` found 4 candidate files, all READERS or the tracked config itself -- ZERO producer/write scripts found. `intake/settings.json` is a hand-authored tracked config, unlike `firm_registry.json`; see `R58-AC2_judgment.md` s.1 for the served bytes' own (now-stale) self-declared provenance pointer.
- **Disposition:** NOT deployed by this order; NOT committed as source. The member's row stays ARMED, `disarm_owner: 2.0.0_SA_COO~B to route`, per the existing investigation row.

---

## CLASS B -- NEW, caused by a sibling worker's in-flight commit landing mid-census (row W4-S41)

`irpt-directory-search` was **redeployed at `2026-09-19T05:29:38Z`** (measured this run:
`aws lambda get-function --query Configuration.LastModified`), 29 seconds before this order's own
final battery run started (`run at 2026-09-19T05:30:07Z`) -- **during this order's own execution
window, by someone else.** Its `enforce.py` and `served.py` DO resolve to a NAMED canonical path
(the existing `_authz/enforce.py` / `_authz/served.py` staged_from declaration this order did not
touch) but the CONTENT now differs (DELTA != 0, NOT canonical-absent -- the canonical is KNOWN, the
served bytes just no longer match it as of this branch's `HEAD`). A follow-up, out-of-band check
(this worker, same turn, NOT part of the graded battery run) found the exact served bytes ARE
reachable in the shared git object database at the SAME paths, via commit
`b3a148044fa5699073e110126d0e6fc7d6b4fed5` ("L7 (IRPT_BCKEND.TO-IB-rtf-2 first pass,
0.9.0_WK_IRPT_BCKEND~1): the ordering inversion + the disclosure field + the consumer-obligation
row"), a SIBLING worker's own commit on cell `IB-rtf-2`, **not yet merged into this branch**.
`data/custodian_key_seam.json`'s new served content (oid
`8ac499ce7f9e24b443f67f29ebddee418addb4cd`) remains genuinely ABSENT from the shared object graph
even under this follow-up check -- a different, unexplained finding, not this same cause.

### irpt-directory-search :: enforce.py

- **Blast radius:** canonical IS named (`_authz/enforce.py` @ pin `28ccac62c9eed361c669dada2aa36eee5d2a65c8`, 567 lines); the diff (line-by-line, printed before any label): `only-in-served=59 of 567 lines; only-in-canonical=19 of 567 lines` -- a real, bounded content difference, not an absence.
- **Rollback:** the served bytes themselves -- `blob d1c8e7e094676526050309a90e4035084a3365e32435feb1b759458781804e93` (sha256).
- **Writer census (N=1, out-of-band):** the ONE writer this run identifies is `0.9.0_WK_IRPT_BCKEND~1`'s own commit `b3a148044fa5699073e110126d0e6fc7d6b4fed5` on cell `IB-rtf-2`, editing `infra/aws/lambda/investor-reporting/_authz/enforce.py` directly. NOT this order's writer, NOT this order's cell.
- **Disposition:** NOT deployed by this order; NOT committed as source (this order's own declaration for `enforce.py` on this function is left UNCHANGED at its pre-existing, rte-4-era pin -- repointing it to HEAD would not help, since HEAD ALSO does not match the live served bytes). Expected remedy is NOT a packet-forever item: once `IB-rtf-2`'s branch merges to `CLOUD` and this project's manifest is next re-declared against the merged HEAD, `enforce.py` should re-resolve to `TRACKED-ELSEWHERE-VERIFIED` with no further action. Filed as row `IRPT_BCKEND-W4-S41` (ARMED), `disarm_owner: 2.0.0_SA_COO~B` (the round's issuer, owning cross-cell sequencing on a shared pipeline).

### irpt-directory-search :: served.py

- **Blast radius:** canonical IS named (`_authz/served.py` @ pin `28ccac62c9eed361c669dada2aa36eee5d2a65c8`, 606 lines); the diff: `only-in-served=42 of 606 lines; only-in-canonical=5 of 606 lines`.
- **Rollback:** the served bytes themselves -- `blob ba0cea6d42461caf7df14c2e3dfe0317d3be4a3a5b0b90cb6ee1214f6a96d73d` (sha256).
- **Writer census (N=1, out-of-band):** same commit as `enforce.py` above, `b3a148044fa5699073e110126d0e6fc7d6b4fed5`, editing `infra/aws/lambda/investor-reporting/_authz/served.py`.
- **Disposition:** same as `enforce.py` above (this order's own declaration for `served.py` on this function is left at its pre-existing pin, unrepointed, for the same reason). Row `IRPT_BCKEND-W4-S41`.

### irpt-directory-search :: data/custodian_key_seam.json

- **Blast radius:** the full served content (197344 bytes) is `present-only-in-served`; no canonical exists to diff against (0 of 0 canonical keys/lines). NOTE: this is a DIFFERENT byte count than the 191120-byte `_ids/data/custodian_key_seam.json` blob every other function's served copy matches -- 6224 bytes larger, consistent with a CRLF checkout (row W4-S38's class) rather than a content change, but NOT yet confirmed either way this run.
- **Rollback:** the served bytes themselves -- `blob 8b077581adea24797940c290441acdee5a802a87710ee3c7e6ed66db591ea97e` (sha256).
- **Writer census (N=0, out-of-band):** unlike `enforce.py`/`served.py`, this exact oid (`8ac499ce7f9e24b443f67f29ebddee418addb4cd`) is ABSENT from the shared object graph even under the follow-up check -- no writer identified anywhere. Genuinely unresolved, not merely "not yet merged".
- **Disposition:** NOT deployed by this order; NOT committed as source. Filed as row `IRPT_BCKEND-W4-S41` (ARMED), `disarm_owner: 2.0.0_SA_COO~B`.
