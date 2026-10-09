# SA-c-1 route census: firm reach of a one-firm test filer token (0.9.0_WK_TCKT_VNEXT~6)

Data: `SA_ROUTE_CENSUS.json` beside this file. Source-only, no AWS call. N = 117 routes on the portal API 7k3ed8px20
across 8 Terraform roots (116 declared in source + the console-only `$default`). The route set was cross-checked against a
second, independent parse of the same sources (116 of 116 match, 0 missing, 0 extra).

## Verdict counts (identical for both tokens)

| verdict | routes |
|---|---|
| ONE_FIRM | 36 |
| NO_FIRM | 51 |
| MORE_THAN_ONE | 27 |
| UNRESOLVED | 3 |

Why the tokens do not differ: the authorizer returns `allowedFirmIds = "opal-capital"` for both, because only `userType Dev`
or `tier internal` yields ALL and neither token has either (`portal-authorizer/index.mjs:293-322`). A regex search of `infra/aws`
for code that branches on `tier == service` found none, so `tier advisor` versus `tier service` changes nothing read here. `T_ADVISOR_OPAL` and `T_SERVICE_TIER_OPAL` are the same principal.

## 1. Is either token ONE_FIRM or NO_FIRM on every route?

No. Neither token is. 27 routes are MORE_THAN_ONE and 3 are UNRESOLVED.

## 2. Routes that break one-firm, and the smallest clamp

**A. Six ticket routes (opal-ticket-api, `ticket_center/lambda_function.py`).** INTERNAL (`firmId == opal-capital`, `:291-293`) is
admitted and none of these checks the ticket's firm: LIST `:1103`, METRICS `:1375`, GET `:1123`, CLAIM `:1145`,
COMPLETE `:1207`, REPORT `:1260`. A one-firm clamp is a code change in the `COMMENTARY_ALLOWED_FIRMS` pattern:

- Add env `FILER_ALLOWED_FIRMS` (JSON `{"<filer email>": ["49financial"]}`, empty or unset = no override).
- In `_firm_allowed` (`:310`) return `firm in map[email]` when the actor's email is in the map; otherwise unchanged. Real
  internal users carry `ALL`, so they are untouched.
- Call `_firm_allowed(actor, item.requester.firm)` in the six handlers: filter the LIST and METRICS items, and refuse
  GET, CLAIM, COMPLETE and REPORT (404) when it is false.

**B. The 21 investor-reporting routes created by the `api` root (21 MORE_THAN_ONE).** All share `_authz/served.py`
`Entry.handle`. An internal caller may name any tenant with `selected_tenant` (`:1124-1131`) and the `allowedFirmIds` clamp at
`:1134-1137` applies only to `x-user-type == service`. Reach is 3 of 3 enabled client firms (49financial, inflection,
cottonwood), no firm refused. The two `reporting/*` routes (created by the `reporting-read` root) are the exception and are
ONE_FIRM (49financial), because that function's bucket map holds one firm (`reporting-read/locals.tf:59`). Smallest clamp,
one condition: widen `:1134` to `service OR email in FILER_ALLOWED_FIRMS` and use the map's list as `allowed`. This needs no
new mechanism; it reuses the existing service branch. (`routes.json` `_denominator` says 19 declared; the file holds 21.)

**C. Three UNRESOLVED routes.** `trade-identifier-cache` (2 routes) has no repo source. The `$default` route (khcd4f1) is
console-only and its authorizer setting is not in source. These need a live read (AWS) to resolve, which this order barred.

Not breaks but worth stating: the 51 NO_FIRM routes include platform operations that read no firm at all. The data-refresh
routes (9) admit a caller whose `userType` is absent (`data_refresh/lambda_function.py:160-167`), so both tokens reach
`data-refresh/trigger` and `rollback`. See the surprise rows.

## 3. FWD-1 needs the ticket service to treat the filer as INTERNAL

| question | T_ADVISOR_OPAL | T_SERVICE_TIER_OPAL |
|---|---|---|
| resolves INTERNAL (`firmId == opal-capital`, `:291-293`) | yes | yes |
| ticket CREATE for firm `49financial` passes `_firm_allowed` | NO: refused 400 at `:1072-1073` | NO: refused 400 at `:1072-1073` |

`_firm_allowed` (`:310-315`) tests membership in `allowedFirmIds`, which is `opal-capital` for both. CREATE succeeds only
for a ticket whose `answers.firm` is `opal-capital`. So FWD-1 as designed (an Analysis Request for 49financial filed by this
filer) cannot pass for either token. The `FILER_ALLOWED_FIRMS` override in clamp A also fixes this, since it replaces the
membership set with `["49financial"]` for that one email.

The `service` tier claim does not make the filer a service subject. `principal_class` (`:283-290`) keys a service subject on
`userType == "service"` AND the email being one of three named `svc-*` subjects; an unlisted service email is UNRESOLVABLE.
