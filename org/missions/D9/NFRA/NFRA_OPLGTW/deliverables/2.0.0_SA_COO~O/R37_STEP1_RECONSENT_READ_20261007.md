# R37 step 1 -- does a fresh `/login` consent alone drop the scoped concierge's earlier Graph scopes?

By: `2.0.0_SA_COO~O` (issuer, NFRA_OPLGTW), 2026-10-07 ~10:4xZ. For `ROUND_ANALYSIS.round24.md` @0e813364da, ruling R37, row
`NFRA_OPLGTW-Z-W28-S11`. No sign-in, no token acquired, no host run and no change was made for this file.

## Answer

**No. A fresh consent through `/login` alone does not drop them. The earlier consent must also be removed in Entra, and the
sign-in comes after that removal.**

## The two legs, each with its claim

| # | Statement | Claim | Source |
|---|---|---|---|
| 1 | The scoped identity's silent acquire asked for the 9 narrowed scopes and the token Entra returned listed the full earlier set (17 Graph scopes plus CallTranscripts.Read.All). | measured | row Z-W28-S11, r25 Phase A rehearsal, 2026-10-07T03:52Z. Not re-read here. |
| 2 | In Entra, delegated consent is ADDITIVE. A grant is stored per client and resource as one scope string. Asking for fewer scopes at `/authorize` never shortens that string. | held | Microsoft identity platform behaviour as this seat knows it. NOT fetched today: reading Microsoft's site is egress off Opal infrastructure. |
| 3 | A token issued for a resource carries every delegated scope already granted for that client and resource, so it can list more scopes than the request named. | held, and consistent with leg 1 | as leg 2. Leg 1 is the one measured instance. |
| 4 | So a new `/login` under the 9-scope request adds nothing and removes nothing. The token after it lists the same set as today. | inferred | from legs 1 to 3. |

Leg 1 already shows the mechanism at work on this tenant: a 9-scope request, a 17-plus-scope token. A re-consent is the same
request with a consent screen in front of it.

## What is NOT read, and decides the size of step 2

**Whether the earlier consent is the concierge's own grant or a tenant-wide admin grant.** This seat cannot read it: it is an
admin read of the gateway app's permission grants in Entra.

- **If it is the concierge's own grant** (granted for that one user): removing that one grant, then one `/login` under the
  9-scope request, leaves a 9-scope grant. The next token lists 9.
- **If it is a tenant-wide grant** (granted for all users by an admin): every user of the gateway app holds the 17 through it,
  the concierge included. No act on the concierge alone narrows its token. Narrowing it in Entra would need the tenant-wide
  grant itself cut down, which reaches every gateway user, or a separate app registration for the concierge. Until then the
  gateway's tool allowlist stays the only narrowing in effect, as R37 states it is today.

## Step 2, as this read shapes it (Andrew's acts; no agent performs them)

1. In Entra, open the gateway app's permissions and read which kind of grant carries the 17 scopes.
2. If it is the concierge's own grant: revoke it, then sign the concierge in through `/login` outside a send window.
3. If it is tenant-wide: a design call comes first, and `/login` alone changes nothing.

**The test is unchanged** (R37): a token acquired after the act lists only the narrowed scopes. The issuer re-reads the 9 Graph
probes then.

## Limits

- Legs 2 and 3 are this seat's knowledge, not a citation. A citation needs one fetch of Microsoft's documentation, which needs
  Andrew's word.
- Leg 1 is one run on one identity.
