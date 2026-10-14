# IRPT_ANLREQ release 28 ADDENDUM 1b -- the synthetic internal viewer carries NO allowedFirmIds -- CTO half

**Signed by:** 1.0.0_SA_CTO~DELL2, dell2, 2026-10-14 ~04:1xZ.
**Bound to:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release28/NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_ADDENDUM_1B_INTERNAL_VIEWER_NO_FIRM_LIST.md`,
git blob `fe221dfcf1`, read with `git hash-object` at signing. It amends Addendum 1 section 3 only (COO blob `909ca2c466`, CTO half @daf0a6043e).

## SIGNED, on these terms

1. **The reason is read at the code, not relayed.** `infra/aws/lambda/investor-reporting/_authz/served.py` `_create_owner` (:1063-1083):
   - a filer whose `allowedFirmIds` lists the tenant must name an advisor, or is refused;
   - any other internal subject keeps `access.prospect_owner()`.
   Addendum 1 as written would therefore stop at D1 and prove nothing.
2. **The blast radius is the ordinary Opal-staff path, held for at most 20 minutes.** It grants nothing an Opal staff login does not
   already hold. Its acts are bounded by `TO-EXERCISE-R28b` and the lane's script:
   - the door's route only, with `selected_tenant=49financial`;
   - four requests, and synthetic files only;
   - one token, never written and never logged;
   - the row deleted after `exp`, then read ABSENT.
   A request outside those bounds is a stop and a report, not a retry.
3. **Both branches (section 4):** a NOT_AUTHORIZED at D1 stops the sitting and removes the row, and no other identity is tried. A
   different answer follows Addendum 1 section 6.
4. **The two synthetic stored inputs** are now attributed to the internal viewer's prospect owner in 49financial. They are not deleted by
   the lane. Their delete is Andrew's act (CLAUDE.md Agent Autonomy, S3 deletes), listed once the report names the ids.
5. **Limit unchanged:** this proves the door's answers only. The partner-advisor run of FWD-1 stays owed on the ordinary-authorizer pair
   (row D2-S93).

-- 1.0.0_SA_CTO~DELL2
