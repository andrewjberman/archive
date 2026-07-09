# SCTY_MCPGUARD — NO-BYPASS perimeter attestation (m365-mcp-gateway :443)

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-09T19:05Z · **Archetype:** VALIDATE
**Authority:** CTO ruling 190127Z — *"GO on the perimeter re-attestation… it is now a **standing
condition** of the NO-BYPASS gate, not a one-off… Any future defeat-everything claim on this host
cites `describe-rules` output or it is `INFERRED` and non-actionable (22a)."*

## The doctrine this artifact exists to serve

> **"Two independent agents agreeing does not fix a shared blind spot when both look at the same
> layer. The corroboration was real; the LAYER was the gap."** — adopted verbatim as fabric doctrine, CTO 190127Z

The prior NO-BYPASS attestation (0.7.0's enum + 0.8.0's independent corroboration) enumerated
`server.py` **routes**. Routes are what the app *implements*. The ALB listener is what *decides*.
A defeat-everything gate must be attested at the **enforcement boundary**, not at the layer beneath it.
Redundancy across observers at one layer does not cure a shared layer assumption — it launders it into consensus.

## Attestation — live, `aws elbv2 describe-rules`, 2026-07-09T19:05Z

Listener: `…:listener/app/m365-mcp-gateway/62a54b61dc4634dd/4751a29f69442c23`

| prio | `authenticate-oidc`? | paths |
|---|---|---|
| 10 | no | `/mcp/*`, `/mcp`, `/authorize`, `/register`, `/token` |
| 20 | no | `/.well-known/oauth-authorization-server`, `/callback`, `/.well-known/oauth-protected-resource`, `/.well-known/jwks.json` |
| 30 | no | `/otp/fetch`, `/otp/health` |
| 31 | no | `/ms/site_children`, `/ms/onedrive_children`, `/ms/health`, `/ms/sites`, `/ms/search` |
| **default** | **YES** | catch-all — everything not matched above |

### The bearer-gated-not-OIDC perimeter set — 16 paths

These reach the app with **no** perimeter authentication; the app-layer guard is the *only* gate:

```
/mcp/*  /mcp  /authorize  /register  /token
/.well-known/oauth-authorization-server  /.well-known/oauth-protected-resource
/.well-known/jwks.json  /callback
/otp/fetch  /otp/health
/ms/site_children  /ms/onedrive_children  /ms/health  /ms/sites  /ms/search
```

Per-path gate (app layer): `/mcp*` → RS256 JWT + audience guard + GuardMiddleware · `/authorize`,
`/register`, `/token`, `/callback`, well-knowns → OAuth-AS + PKCE-S256, unauthenticated **by design**
(they *are* the auth surface) · `/otp/*` → static capability bearer, constant-time compare
(exercised 2026-07-09: wrong-bearer→401, no-auth→401, real→200) · `/ms/*` → `MS_INGEST_BEARER`,
read-only by construction.

### `/teams/poll` is NOT in the set

No non-default rule matches it → falls to the default rule → `authenticate-oidc` → unauthenticated
caller receives **302** to the IdP and never reaches the handler. Confirmed by probe (opaque bearer → 302)
**and** by the rule table above. Its app-layer bearer check is therefore defense-in-depth, not the live gate.

**Consequence for the prior gate:** the *"3 REST bypasses, all read-only"* finding is app-layer-true
and perimeter-layer-wrong. The real perimeter set is the 16 paths above. Severity: **not a
vulnerability** — the drift runs fail-safe (the route is *more* restricted than believed).
Bounded: no in-repo consumer exists (`teams-watch.sh` is absent); absence-in-repo is weaker evidence
than an access-log read, so an off-repo consumer, if any, is 302ing today.

## How to re-attest (the standing condition)

```bash
aws elbv2 describe-rules --listener-arn <listener-arn> --output json
# Reach, not rules: for each path, does its matched rule carry authenticate-oidc?
# A path whose ONLY gate is an app-layer bearer belongs in the bypass set. Enumerate it there.
```

Cite this output — not `server.py` routes — on any future defeat-everything claim for this host.

**Open coverage gap (CTO-approved build, route via COO):** no comp-tool answers *"which
principal-classes can reach this path, at the perimeter?"* `comp-routes` models CloudFront→origin;
nothing models ALB-listener-rule → `authenticate-oidc`-vs-`forward`. This drift was found by a curl
that happened to return 302 — **and a curl that happens to work is not a control.** Design note from
CTO: the tool must answer *reach*, not *rules* — rules are the config; reach is the property.

## Record corrections landed with this attestation

- `app/server.py` `teams_poll` docstring — removed *"so a shell watcher can curl it"*; added the perimeter note.
- `app/audit.py:75` — no longer calls `/teams/poll` *"the read-only REST bypass"*.

Comments only, **zero behavior change**. `commit-gate.sh` clean (2 files).

> **Deploy note (deliberate, flagged):** this creates a *comments-only* delta between the deployed
> gateway and repo HEAD. I did **not** restart the live gateway to land a comment: the m365 gateway
> is a crown-jewel host and `oauth_as.py:67-77` falls back to **generating an ephemeral RSA signing
> key** when the key env is absent, so a restart is not a zero-thought operation. The change rides the
> next scheduled gateway deploy. Until then, an `otp.py`-style sha256 parity check on `server.py`/`audit.py`
> will show a benign comments-only diff — recorded here so it is not later mistaken for drift.
