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

## SURPRISES FILED

`IRPT_BCKEND-W1-S28` (OBSERVATION, ARMED, `disarm_owner` `1.0.0_SA_CTO`) -- the consumer
obligation itself, arm (c)'s own row; not a defect in this cell, the artifact the ruling's
condition 2 requires.
