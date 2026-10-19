# O1 backend hunk, proposed for ~P2's review (2.0.0_SA_COO~Y2, 2026-10-19) -- NOT an order, NOT applied

Scope: `infra/aws/lambda/investor-reporting/_authz/served.py`, the functions `_create_owner` and `_advisor_owner` only (cited by name; ~P2's msg gives the HEAD lines `:1073` to the end of `_advisor_owner` `:1123`). Source of the change: PRD IRPT_ANLREQ v0.23/v0.24 (C-FIRM: Opal staff choose any firm and own the request through `prospect_owner()`; the typed advisor email becomes attribution only), brief O1, gaps G1 and G9.

## Today (HEAD)
- No advisor named and `tenant in actor["allowedFirmIds"]` -> `ProspectOwnershipRefused("an on-behalf upload must name the firm advisor")` (the `:1089-1091` refusal); otherwise `access.prospect_owner()`.
- Advisor named -> `_advisor_owner` raises `ProspectOwnershipRefused` for: blank email; firm not in `firm_ids()`; profile reads failing; no partner profile at the firm or an email/firm mismatch; user row absent, disabled or of another firm. Otherwise it builds the advisor's owner through `resolve_prospect_owner`.

## Proposed behaviour
1. **No advisor named** (key absent, or blank) -> `access.prospect_owner()`, whatever `allowedFirmIds` lists. The `allowedFirmIds` clause is deleted.
2. **Advisor named and PROVISIONED** (partner profile and active user row at the firm, as today) -> the advisor's owner through `resolve_prospect_owner`, unchanged.
3. **Advisor named and UNPROVISIONED** (the two refusals "no partner profile at the named firm" and "profile absent, disabled or of another firm") -> `access.prospect_owner()`. The typed email is attribution only and never becomes authority.
4. **Unchanged refusals**, still `ProspectOwnershipRefused` -> `NOT_AUTHORIZED`: lookup key unreadable (`queryStringParameters` not a dict); firm not a registered client firm; advisor profile reads raising. `access.prospect_owner()` itself still fails closed for a subject with no resolvable owner, and nothing is stored then.

## Sketch (REVISED after ~P2's review, broker msg of 2026-10-19 ~20:3xZ: a typed exception, not None)
```python
class AdvisorUnprovisioned(ProspectOwnershipRefused):   # the ONE line outside the two bodies, beside the base class in served.py
    """The named advisor has no partner profile / no active user row at the firm: attribution only."""

        named = query.get(ON_BEHALF_ADVISOR_PARAM)
        if not isinstance(named, str) or not named.strip():
            return access.prospect_owner()
        try:
            return self._advisor_owner(named, tenant, reads)
        except AdvisorUnprovisioned:
            return access.prospect_owner()
```
`_advisor_owner` raises `AdvisorUnprovisioned` for exactly two cases: no partner profile at the named firm, and user row absent / disabled / of another firm. A partner email or firm MISMATCH stays a plain `ProspectOwnershipRefused` (data damage, not "unprovisioned"). Any other caller of `_advisor_owner` still fails closed, since the subclass is still a refusal.

## Tests the order will name (no test in the repo pins the on-behalf branch today; baseline at HEAD: `_authz` 365 passed, owner composition 6 passed)
T1 staff, no advisor key, tenant in `allowedFirmIds` -> `prospect_owner()`; T2 staff, blank advisor key -> `prospect_owner()`; T3 advisor named and provisioned -> the advisor's owner; T4 advisor named, no partner profile -> `prospect_owner()`; T5 advisor named, user row disabled -> `prospect_owner()`; T6 partner email or firm mismatch -> `ProspectOwnershipRefused`; T7 unregistered firm -> refused; T8 unreadable query -> refused; T9 `prospect_owner()` unresolvable -> refused, nothing stored.

## Where the typed email is recorded
It is NOT recorded as attribution anywhere in this change: when the advisor is unprovisioned the typed value is dropped, and the portal stops sending it (O2). If attribution is wanted it is a separate contract, which I will raise with the CTO rather than invent here.

## What I ask ~P2 to check
(1) the owner still comes only from verified identity (`resolve_prospect_owner` or `prospect_owner()`), never from a request value; (2) every remaining refusal is `ProspectOwnershipRefused` mapped to `NOT_AUTHORIZED`; (3) only the staff branch changes; a non-staff filer's path is untouched; (4) nothing outside the two functions moves; (5) the `_authz` tests run in identical base and new copies; (6) the readers of the owner value, which the pair will name (to be listed from your side too).

Answered by ~P2: typed exception (above).
