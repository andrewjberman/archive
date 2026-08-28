# `T7AE-AC2` cross-firm negative control -- EXHIBITED, not asserted

**Seat:** `0.4.0_DE_ClientPlatform~S` · **Measured:** 2026-08-28T02:5xZ, live plane
`https://opalinvest.dev`

`T7AE-AC2` requires: *"a request for a firm the caller is not entitled to must not return
another firm's object -- **exhibit the refusal, do not assert it**."* This exhibits it.

## Why this test and not the cottonwood one

`3.0.0_SA_CVO~Z` (12277) ruled against minting a self-signed `firmId=cottonwood` bearer, on the
argument that **a forged firm claim would manufacture the premise the test exists to check** --
it would verify the router honours a firm claim while *assuming* the claim, and say nothing about
whether the auth layer would **issue** it. Its §5 then said to take the free half.

**This is the free half, and it tests the exact property the forged test could not.** The
`49financial` credential is committed, real, and issued by the live auth layer -- so this
exercises **issuance AND resolution together**, forging nothing.

## The two arms

```
1 NEGATIVE  49financial -> /api/scoped/satellites/registry.json
            403 application/json 127 B
            {"error":"artifact_forbidden","uri":"/platinum/satellites/registry.json",
             "firmId":"49financial","status":403,"request_id":null}

2 POSITIVE  49financial -> /api/scoped/advisor-intelligence/platinum/firm/header_metrics.json
            200 application/json 1919 B   (its OWN firm's artifact)
```

**Arm 2 is what makes arm 1 mean anything.** A 403 from a dead, expired or malformed bearer proves
nothing about the boundary. The *same* bearer returning 200 on a route this firm IS entitled to
shows the token is live and accepted -- so the 403 is a **real refusal of a real, authenticated,
non-entitled caller**, not an artifact of a broken credential.

**Cottonwood's bytes were not returned.** The response sha256 is not
`0989650ab6a7541d...`; a direct comparison was made rather than inferred from the status code.

## What it establishes, and what it does not

- **ESTABLISHES:** an authenticated caller from a different firm cannot read cottonwood's
  satellites registry. `49financial` resolves to `opal-data-bd` (`_shared/firm-config.mjs:66`) --
  a different bucket -- and the refusal names the firm back (`"firmId":"49financial"`), so the
  router resolved the caller's own identity and then refused, rather than leaking across.
- **DOES NOT ESTABLISH:** that a *cottonwood* caller succeeds. That rung stays open and honestly
  labelled -- no cottonwood credential exists on this device, and the forged-claim substitute was
  ruled out. Two different claims; only one is measured here.
- **DOES NOT TOUCH `Z-S16`.** Staff still see a pill that 400s.

⚠ The `artifact_forbidden` shape is an **artifact-level** refusal naming the URI and firm. Whether
that is the S3 layer or an explicit router arm is **not measured here** and is not this lane's
surface -- surfaced, not chased.
