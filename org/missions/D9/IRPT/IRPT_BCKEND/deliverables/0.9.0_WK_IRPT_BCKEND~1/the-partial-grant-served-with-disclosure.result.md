# IRPT_BCKEND.TO-IB-rtf-2 -- FIRST PASS RESULT

Worker `0.9.0_WK_IRPT_BCKEND~1`. Cell `IB-rtf-2`. CTO ruling @61627f39f9.

## WHAT SHIPPED THIS PASS (arms a-c)

**(a) THE INVERSION.** `infra/aws/lambda/investor-reporting/_authz/enforce.py` `Enforcer.resolve_now`:
project first (`_scope.resolve` already computed `scope["permitted_account_set"]`), decide on the
RESULT. An EMPTY permitted set is refused -- `UNPROJECTED_GRANT` when EVERY granted id was
unprojected, `EMPTY_GRANT` otherwise. A NON-EMPTY permitted set is SERVED, with the gap disclosed
on the scope's census as `unprojected_grant: {count, denominator, kinds}`.

Tests, all real `Enforcer`, `infra/aws/lambda/investor-reporting/_authz/tests/test_enforce.py`:
  * `test_a_partial_unprojected_grant_is_served_with_the_gap_disclosed` -- 3 granted, 1
    unprojected, 2 permitted -> SERVED, `{"count": 1, "denominator": 3, "kinds":
    {"UNPROJECTED-ID": 1}}`.
  * `test_a_zero_unprojected_grant_is_served_with_count_zero_present` -- the ordinary case,
    `{"count": 0, "denominator": 3, "kinds": {}}`, PRESENT not omitted.
  * `test_an_unprojected_grant_is_refused_and_not_served_empty` (existing, unchanged assertion) --
    all-unprojected -> `UNPROJECTED_GRANT`.
  * `test_a_cross_firm_advisor_id_is_refused_empty_grant_not_unprojected` -- an advisor absent
    from the firm's roster entirely -> `EMPTY_GRANT`, never `UNPROJECTED_GRANT`.
  * `test_ordering_mutant_refuses_the_partial_case_the_real_code_serves` -- the DISCRIMINATOR:
    `infra/aws/lambda/investor-reporting/_authz/tests/mutant_ordering.py` AST-transplants the
    PRE-FIX order (row W1-S27: any unprojected id refuses the WHOLE grant, unconditionally) into
    a parsed copy of the REAL `enforce.py` source; the mutant refuses the exact partial case the
    real code serves.

`31 of 31` tests in `test_enforce.py` PASS (this run). The mutant is independently re-derived a
second time inside `battery_ib_rtf_2.py` arm (a), never trusted from the pytest assertion alone.

**(b) THE DISCLOSURE FIELD, NON-OPTIONAL.** `infra/aws/lambda/investor-reporting/_authz/served.py`
`response_envelope()` (the ONE shape every scoped route answers in -- module docstring, "THE
ENVELOPE IS ONE SHAPE") now carries `unprojected_grant` as a top-level field, present at zero,
default `{"count": 0, "denominator": 0, "kinds": {}}`. `Entry.handle` (the one call site) feeds it
from `Served.census["unprojected_grant"]`, which `Enforcer.serve`/`submit_job`/`consume_job` now
carry. `7 of 7` `entry.py` (directory, export, holdings, narrative, ops, performance,
ycharts/generate) import the shared `served` boundary and share its ONE `response_envelope(`
call site (censused fresh this run via `comp-find`, and again inside the battery by reading
`served.py`'s source directly) -- so the field reaches every route through one construction, not
seven promises.

**(c) THE CONSUMER-OBLIGATION ROW.** `IRPT_BCKEND-W1-S28`, class `OBSERVATION`, `hazard_standing`
`ARMED`, `disarm_owner` `1.0.0_SA_CTO`, filed in
`org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md` (inside the
first json fence's array) BEFORE any deploy, naming the field, the routes that carry it and
IRPT_FNTEND's obligation to render a visible partial indicator whenever `count > 0`.

## WHAT DID NOT SHIP THIS PASS -- ARM (d), THE EXPECTED STOP

`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-2.md`
is written and committed this pass (the ACT's blast-radius description: the 7 keys' current
`CodeSha256` as the rollback baseline, both branches of the blast radius, `W=1` writer of the
served-behaviour property). At HEAD, `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` carry NO
`NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtf-2_*.md` naming this packet's `blob <hash>`
-- both ABSENT, exactly as the cell text says to expect ("the halves do not exist before the
packet does"). R59-AC1 arm (d) is graded FAIL, truthfully, in this pass's proof-of-spec instance;
arm (e) (the deploy) does NOT run. The order's `<status>` stays `pending`; the issuer re-hands the
same order once both halves exist at HEAD naming the packet's blob.

## SURPRISES FILED (first pass)

`IRPT_BCKEND-W1-S28` (OBSERVATION, ARMED, `disarm_owner` `1.0.0_SA_CTO`) -- the consumer
obligation itself, arm (c)'s own row; not a defect in this cell, the artifact the ruling's
condition 2 requires.

## SECOND PASS -- ARM (d) AND ARM (e) (this run)

**(d) THE HALVES.** Re-hashed the packet at HEAD: `git rev-parse HEAD:.../NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-2.md`
== `713a22a4d9b451ce78207a4ee647dc1fecd28c9d`, matching the CTO half's bound blob exactly (no
STOP). Both halves read at HEAD: COO half `org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-2_PARTIAL_GRANT_DISCLOSED.md`
@76db3f781e and CTO half `org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-2_PARTIAL_GRANT_DISCLOSED.md`
@b1f376845a, both naming `blob 713a22a4d9b451ce78207a4ee647dc1fecd28c9d`. The battery's own
`names_blob` check had a bug (bare substring `"blob " + hash`, which cannot match the halves'
actual `"blob \`<hash>\`"` markdown form) -- fixed to a regex tolerating the backtick/emphasis
between the word and the hash; this is my own instrument, not the halves, and is the fix, not a
widening.

**THE CTO HALF'S ONE CONDITION (tolerance read, before any deploy).** Read the shared portal
checkout at `C:\Users\AndrewBerman\Desktop\ajb_workspace\portal` (branch `DEV` @`be8cf218743af0c04a4d57b908b28cf7435e119d`;
the worker's own worktree gitlink at HEAD resolves to `2453a7b4c6b7ff91ea89db499890a9486265d1a0`,
a DIFFERENT, unreachable-from-here commit, so the shared checkout is what was read).
`portal/src/pages/InvestorReporting/contracts/envelope.ts:166-169` (`isEnvelopeShaped`) and
`:180-237` (`parseIrEnvelope`) @be8cf218743af0c04a4d57b908b28cf7435e119d: the parser reads named
properties (`contract_version`, `operation`, `firm_id`, `status`, `data`) directly off the parsed
JSON object by key access; it never enumerates or asserts the envelope's key SET, and no
`additionalProperties:false` runtime validator (no ajv/zod/schema `.strict()` call) runs over the
top-level envelope anywhere in `portal/src/api/api-client.ts` (`apiRequest` returns a plain
`response.json()`, line 175) or in `envelope.ts` itself -- the `additionalProperties: false`
language in both files' comments describes the SOURCE JSON SCHEMA / generated wire TYPE
(compile-time only; TypeScript's excess-property check applies to object literals, never to a
value received over the network), not a runtime enforcement. **VERDICT: TOLERANT.** An unknown
top-level key (`unprojected_grant`) is silently ignored by the parser and does not raise
`EnvelopeMismatch` or reject the response. Proceeded to (e).

**(e) THE DEPLOY.** Change-management ledger `irpt-bckend-ibrtf2-partial-grant-disclosure` OPENED
@a7c19015bb (8 legs: 7 activation + 1 verify), sentinel committed before any act. Built all 7 zips
fresh (`rte6_package_deploy.py build`; the two untracked-production-source-file fallbacks for
`irpt-status` and `irpt-ycharts-generate` were re-materialized this pass into `.scratch/ops_extracted/`
and `.scratch/ycharts_extracted/` by extracting them UNCHANGED from the currently-deployed zips,
since this worktree's own `.scratch/` does not carry the first pass's materialized copies).
Uploaded all 7 to `s3://opal-313476888478-lambda-artifacts/investor-reporting/`, each verified by
upload metadata (`content-sha256` == built). Applied via `.tools/safe-apply.sh` under
`.tools/terraform.exe` (provisioned), one root per function, each plan `-target`-scoped to the
function's own `aws_lambda_function.this` (the `directory/` root's UNSCOPED plan picked up an
UNRELATED, concurrently-changing `irpt-directory-refresh` resource -- a different, live sibling
cell's own work -- so every apply was narrowed to exactly the resource this order owns): `directory`
(1 changed, 0 destroy), `export` (1/0), `holdings` (1/0), `narrative` (1/0), `ops` (1/0),
`performance` (1/0), `ycharts` (1/0) -- 7 of 7, 0 to destroy anywhere. `rte6_package_deploy.py
verify`: 7 of 7 `served == built` CodeSha256. Ledger closed @db44bae990, all 8 legs proven,
committed before the grading read.

**LIVE PROOF**, through the REAL `served.Entry.enforcer_for` (`portal/../directory/entry.py`'s
own `ENTRY` object, imported unmodified): `abby_horton`/`49financial` now SERVED, `k=21` permitted,
`unprojected_grant={count:12, denominator:33, kinds:{UNPROJECTED-ID:12}}` -- self-consistent
(`k + count == denominator`). The cross-firm swap (`definitely-not-a-49f-advisor`) still REFUSED
(`EMPTY_GRANT`). The ACTUAL pre-deploy artifact bytes -- fetched fresh from S3 this run by content
hash (`investor-reporting/irpt-directory-search.zip` version `6gdufvGXDxvLc8SYLeQtS5osgwdrXeDm`,
verified `sha256(b64) == v0MMA3yUxIPNdCMXhE/2pSD9lU+5LgI945JqkuULH8U=`, the packet's own recorded
prior `CodeSha256`) -- read `UNPROJECTED_GRANT` on the identical real request: the genuine
pre-fix negative control, not a simulated mutant. `inflection` and `cottonwood` (empty ownership
maps) both REFUSED `EMPTY_GRANT`, the empty branch's own code.

**NUMERIC DRIFT FROM THE PACKET'S EXPECTATION (row W1-S30).** The packet/order text names
"k=21, count=22 (of 43)" from `battery_ib_rte_6.py`'s own prior measurement; this run measures
`k=21, count=12 (of 33)`. Confirmed by S3 version history: `opal-data-bd`'s
`platinum/49financial/ownership_map.json` was overwritten by a CONCURRENT, unrelated scheduled
refresh at `2026-09-19T05:10:38Z` (prior version at `00:09:01Z`, the packet's own window),
shrinking `abby_horton`'s account list from 43 to 33. The RELATIONSHIP the acceptance criterion
grades (`k>=1`, `count==denominator-k`) holds exactly; only the specific numeric constants from an
earlier vintage no longer match current live state (forward-looking-criterion bar).

## SURPRISES FILED (second pass)

`IRPT_BCKEND-W1-S29` (OBSERVATION, ARMED, `disarm_owner` `1.0.0_SA_CTO`) -- `irpt-holdings`
packages its OWN diverged local `enforce.py` (pre-fix order, never sets the disclosure field),
not the shared `_authz/enforce.py` this cell inverted; the build tool's `source_dir`-first
resolution ships the stale copy. Out of this cell's BOUNDS to fix; this order's own required live
proof targets `directory-search`, which correctly resolves `_authz/enforce.py`, so R59-AC1 is
unaffected.

`IRPT_BCKEND-W1-S30` (OBSERVATION, INERT) -- the numeric drift above (k/count/denominator vs the
packet's expectation), caused by a concurrent, unrelated scheduled refresh; not a defect, recorded
so a later reader does not mistake the difference for a deploy bug.
