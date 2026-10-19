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

## Sketch (names as in HEAD)
```python
        named = query.get(ON_BEHALF_ADVISOR_PARAM)
        if not isinstance(named, str) or not named.strip():
            return access.prospect_owner()
        owner = self._advisor_owner(named, tenant, reads)
        return owner if owner is not None else access.prospect_owner()
```
and in `_advisor_owner` the two unprovisioned refusals `return None` instead of raising; every other raise stays.

## What I ask ~P2 to check
(1) the owner still comes only from verified identity (`resolve_prospect_owner` or `prospect_owner()`), never from a request value; (2) every remaining refusal is `ProspectOwnershipRefused` mapped to `NOT_AUTHORIZED`; (3) only the staff branch changes; a non-staff filer's path is untouched; (4) nothing outside the two functions moves; (5) the `_authz` tests run in identical base and new copies; (6) the readers of the owner value, which the pair will name (to be listed from your side too).

Open for ~P2: is returning `None` for the two unprovisioned cases the right shape, or should the fallback live in `_create_owner` on a typed exception? Either keeps the hunk to these two functions.
