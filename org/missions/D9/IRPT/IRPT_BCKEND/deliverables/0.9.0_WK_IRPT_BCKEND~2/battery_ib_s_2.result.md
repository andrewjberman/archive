# IB-s-2 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-2`

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, second order) | **Branch:** `wk-irpt_bckend-1-2`
**Worktree:** `/c/tmp/wk-irpt-1-2`, re-cut from CLOUD at `313659c29c` (carries the merged IB-s-1
directory cell and the `a2e5071940` face amendments).
**Deliverable source pinned at:** `33351469c2` (the build) and `c51108918b` (the strict-mode
reason repair). **Nothing in this cell touched the world:** it ships a library, and the face says
so -- *"No deploy in this cell"*. No apply, no ledger entry, no S3 write, no vendor call.

---

## S2-AC1 -- 7 OF 7 ARMS PASS

```
  ARM (a) PASS: 9 of 9 injected headers traced to source lines; Opal principal NOT distinguishable (firmRole read at :205, never injected)
  ARM (b) PASS: 3 of 3 partial cases resolve to the exact allowed subset or an explicit UNSUPPORTED; 0 of 3 returned the requested whole; control case carries partial_reason None
  ARM (c) PASS: fingerprint identical across 2 of 2 identical runs; differs on a removed account and on an entitlement-revision change with an identical set
  ARM (d) PASS: 8 rows -> 6 unique accounts (2 duplicates collapsed, 0 double counted); 2 of 2 unmatched ownership ids carry a reason; 3 of 3 reason kinds exercised
  ARM (e) PASS: 6 forged headers dropped, resolved set/fingerprint/class IDENTICAL; a trusted-header change DOES move the set (positive control); 0 of 8 partner role keys (read from 3 of 3 real files) appear in the resolver
  ARM (f) PASS: 6 of 6 resolved objects schema-VALID; browser-safe view carries 0 of 9 vendor-id-shaped keys while the server view trips the same census at 3
  ARM (g) PASS: type ["string", "null"] ; account-only entry VALIDATES against the amended schema and is REFUSED by the pre-amendment text; 0 of 3 leaf diffs outside the one token
  7 of 7 arms PASS
IBS2-SCOPE-RESOLVED
```

### Every arm's control, in one table

An arm that asserts an absence and cannot be made to go non-zero is a constant, not a measurement.

| arm | the absence it asserts | the control that makes the same instrument go non-zero | observed |
|---|---|---|---|
| (a) | every header claim matches its line | a header name that is NOT injected, checked at `:383` | `False` -- the check can fail |
| (b) | `partial_reason` set on every partial case | a WHOLLY permitted request | `partial_reason` is `None` -- not a constant |
| (c) | fingerprint stable | one account removed; and the entitlement revision moved with an IDENTICAL set | both fingerprints differ |
| (d) | every gap carries a reason | a custodian-shaped id (the third reason kind); and a MATCHED account | `UNPROJECTED-ID`; `0` gap rows |
| (e) | a forged header changes nothing | changing a TRUSTED header (`X-Advisor-Id` -> advisor B); and the role-key matcher on a synthetic line | set moves, fp differs; matcher hits `2 of 8` |
| (f) | browser view carries no vendor id | the SERVER view, which does carry `vendor_ids`; and a `SUPERUSER` principal class | `3` hits; schema refuses |
| (g) | the amended schema accepts `null` | the PRE-AMENDMENT schema text, kept verbatim | `REFUSED -- None is not of type 'string'` |

### (a) The trace -- 9 of 9, verified against the source line each claims

```
    x-user-email       :383  from payload.sub          VERIFIED in source
    x-user-name        :384  from payload.name         VERIFIED in source
    x-user-tier        :385  from payload.tier         VERIFIED in source
    x-user-role        :386  from payload.role         VERIFIED in source
    x-firm-id          :387  from payload.firmId       VERIFIED in source
    x-user-type        :388  from payload.userType     VERIFIED in source
    x-advisor-id       :389  from payload.advisorId    VERIFIED in source
    x-advisor-role     :390  from payload.advisorRole  VERIFIED in source
    x-origin-verify    :391  from CONSTANT 'cloudfront' (not a claim)   VERIFIED in source
  9 of 9 header claims verified against index.mjs at HEAD
```

Full trace with the quoted lines, the rejected candidates and the fixture-provenance table:
`/c/tmp/wk-irpt-1-2/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/ib_s_2_validator_trace.md`.

**The Opal-principal answer the order asks for: NOT DISTINGUISHABLE.**

```
      :205  if (payload.firmRole === "admin") return null;
      :203  // remains reserved for Opal-platform admins per the firmRole framework
      :184  //   - Any jwt.role === 'admin' bypasses (null return) -- Opal staff AND
      :185  //     partner-firm admins (e.g. Travis at 49financial, role=admin)
    census: `firmRole` injected as a header anywhere in the file? False
    same admin headers -> without roster: FIRM_OPERATIONS | with roster: OPAL_GLOBAL
```

**A stale carrier found while tracing:** the file's own summary comment (`:11-12`) enumerates
`8 of 9` injected headers, omitting `X-Advisor-Role` -- which its own v12 note (`:31`) and its own
code (`:390`) both inject. Two enumerations of one set in one file. This trace is built from the
CODE, and that is why the denominator here is 9 and not 8.

### (b) A partly permitted relationship, three ways

```
  fixture: relationship r2... reaches 2 account(s); advisor A's grant covers 1 of those 2
  DEFAULT MODE  -> resolved ACCOUNT ['a3...'] ; partial_reason: ... 1 of them are outside the
                   viewer's permitted set and are NOT returned ...
  STRICT MODE   -> resolved UNSUPPORTED ; permitted set [] ; STRICT mode: resolved UNSUPPORTED
                   and NOTHING is returned, rather than the 1 permitted account(s) dressed as
                   the requested scope.
  WHOLLY UNPERMITTED -> resolved UNSUPPORTED (never an empty look-alike of the requested scope)
  the requested WHOLE was returned in 0 of 3 partly/unpermitted cases
```

### (d) The overlap and the gaps

```
    account ROWS across entries: 8 | UNIQUE after collapse: 6 | duplicates collapsed: 2
    a firm-operations viewer's permitted set: 6 == 6 unique in the population
    DENOMINATOR: 6 granted account(s); 4 matched; 2 unmatched
      a7... -> CROSS-FIRM: present in the directory under another firm_id ...
      a8... -> NOT-IN-DIRECTORY: no entry in this firm's directory holds this account ...
    2 of 2 unmatched accounts carry a reason; 3 of 3 reason kinds exercised
```

### (g) The contract amendment, and what did NOT move

```
  ids.relationship_id type: ["string", "null"]
  AMENDED schema -> account-only entry with relationship_id null: VALIDATES
  PRE-AMENDMENT schema text -> the SAME entry: REFUSED -- None is not of type 'string'
  ONE-TOKEN CHECK: 3 leaf difference(s) between the two schema texts, 0 of them outside
                   ids.relationship_id.type
  REGRESSION on the pair IB-s-18's battery grades: valid accepted True ; invalid refused True
```

Two shape decisions made so the amendment cannot break the battery that guards the contract:
the account-only entry is a **sibling key** (`instance_account_only`) because IB-s-18's arm (b)
reads `["instance"]`, which is byte-unchanged; and the pre-amendment copy lives under `fixtures/`
because that arm enumerates `*.schema.json` in `_contracts/` itself and asserts **11 of 11**, so a
twelfth schema at that level would have broken its count.

---

## ONE VACUOUS PASS CAUGHT BEFORE IT SHIPPED

Arm (e)'s partner-role census first printed **`0 of 0`** and PASSED. `portal/` is a **gitlink**,
and a linked worktree does not populate a submodule -- so the directory existed, contained nothing,
and the census over it returned an empty denominator that reads exactly like a clean result. The
arm now resolves the partner files at the primary checkout (reads only; no portal write is
granted), **prints which checkout answered**, and **FAILS rather than printing a zero** if neither
does. It now reads `0 of 8 ... read from 3 of 3 real files`, with a positive control proving the
matcher can hit.

## ONE PROSE-VS-FIELD CONTRADICTION CAUGHT IN THE OUTPUT

Strict mode returned `UNSUPPORTED` with an empty set while carrying the DEFAULT branch's reason
text -- *"The resolved scope is the exact allowed subset"*. Both halves were true of some branch
and the pair was false of that one. Repaired at `c51108918b`; no behaviour changed, because the
returned set was already empty and already correct.

---

## S2-AC2 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. Is the validator's header set sufficient to resolve firm-admin vs advisor vs Opal?

**ADVISOR: YES.** `X-Advisor-Id` (`payload.advisorId`, `:389`) is the identity the validator's own
`.004a` gate locks a non-admin caller to (`:199-207`). An advisor is resolvable, and the resolver
uses exactly that claim.

**FIRM-ADMIN vs ADVISOR: YES, with one caveat.** `X-User-Role: admin` separates an admin from a
non-admin. The caveat is that `X-Advisor-Role` **also** carries `admin` as a v12 tier bypass value
(`:35`, `:238-244`), so two different headers use one token for two different things; the resolver
treats either as the admin signal, which is the wider read of the two and therefore the safe one
**for this direction** (it can only move a caller from FIRM_ADVISOR to FIRM_OPERATIONS, both
firm-bounded).

**OPAL vs FIRM-ADMIN: NO. The header set cannot do it, and IB-s-15 must add a claim upstream.**
Two independent reasons, both measured at HEAD and printed by arm (a):

1. **The discriminating claim is read and never injected.** The validator separates the two
   populations with `firmRole` at `:205`, under a comment (`:202-204`) saying master `role`
   *"remains reserved for Opal-platform admins per the firmRole framework"*. `firmRole` is not one
   of the nine injected headers -- censused, `0` occurrences in any `request.headers` assignment.
   It exists inside the edge function and dies there.
2. **The file contradicts itself about `role`.** `:184-185` states that `jwt.role === 'admin'` is
   carried by *"Opal staff AND partner-firm admins (e.g. Travis at 49financial, role=admin)"* --
   the opposite of `:202-204`. A named partner-firm user carries the claim that is supposedly
   reserved. Two carriers in one file, disagreeing; this cell picks neither and takes the narrower
   branch.

Every one of the nine was examined **by subtraction from the printed denominator**, not by recall.
The closest candidates are `tier === 'internal'` and `userType === 'Dev'` (both v12 admin-bypass
values, `:243-244`) -- and both are **unenumerated free-text claims with no registry anywhere in
the repo**, one of which defaults to the literal string `"unknown"` (`:385`). A value with no
closed domain cannot be an authorization boundary.

**WHAT THIS CELL DOES ABOUT IT.** `OPAL_GLOBAL` is never minted from headers. It requires
`opal_principal_ids`, an explicit server-side roster the caller supplies, **empty by default**, so
the capability is ABSENT rather than silently granted. A `role=admin` caller with a verified firm
resolves `FIRM_OPERATIONS`. Bound 3 grants Global to an Opal principal and **never** to a firm one;
a signal that cannot tell them apart cannot be the thing that grants Global.

**THE FILE AND THE SEAT, NAMED.**

* **FILE:** `/c/tmp/wk-irpt-1-2/infra/aws/lambda-edge/auth-validator-edge/index.mjs`, one line
  beside `:390`: `request.headers["x-firm-role"] = [{ key: "X-Firm-Role", value: payload.firmRole || "" }];`
* **SEAT:** `.owned-paths.yaml` carries **no** rule for `auth-validator-edge` -- the only
  `lambda-edge` carve-out is `public-data-router` at `:1870-1872` -- so the longest match is
  `infra/aws/**`, lane **`CLOUD_OPS_OR_ETL`**: *"Any AE agent"*. That is `0.7.0_AE_CloudOps` (and
  its lanes) or `0.8.0_AE_CloudComp`. **NOT in this order's `<paths>`; this cell read it and did
  not write it.**
* **AND IT IS A SERVED-OUTPUT ACT.** Lambda@Edge replicates to every point of presence and the
  function sits on distribution `EVTSA9VEHNZVH` (`:4`) in front of **28 existing behaviors**, so
  the change touches the auth path of every route on that distribution -- never-widen sign-off,
  not merely a deploy.
* **CHEAPER ALTERNATIVE IB-s-15 SHOULD WEIGH FIRST:** the server-side roster this resolver already
  accepts. It grants Global with **no edge change at all** and no blast radius on 28 behaviors.
  The upstream claim is the cleaner long-run answer; the roster is the one that needs no sign-off.

### 2. Which fixtures could NOT be built from real identity data, and why

**1 of 7 fixture classes has a live population at this vintage.** The full table with the
per-item reason is section 5 of the trace; the summary:

| fixture | live data? | why not |
|---|---|---|
| the group overlap | **YES** -- the only one (IB-s-1: 201 groups, 6,155 unique) | modelled faithfully, synthetic ids: committing real opaque ids buys nothing, the overlap is a SHAPE |
| partly permitted relationship | no | needs an ownership map that grants part of a relationship; none has been read, and the W2-S7 key-space seam means the live one would not join |
| revoked entitlement | no | there is no entitlement plane in production -- IB-s-1 emitted `access.entitled: UNKNOWN` for all 5,062 entries |
| an Opal principal | **no, and that IS the finding** | no Opal roster exists on the DESIRED plane and the header set cannot identify one; a "real" fixture would have to invent the very claim whose absence is the finding |
| a firm admin | no | a real admin JWT is a credential -- bound 6 |
| a forged header | no, by construction | the forgery is a request that never happened; synthesised from the real header NAMES so it is shaped exactly like the thing that must not be trusted |
| the unmatched-ownership list | no at this vintage | IB-s-1 measured INF unmapped at **0 of 874** -- a live cut would pass vacuously (row `W2-S3`) |

### 3. What I would want the CVO to look at hardest

* **The third input.** The face's signature is `resolve(headers, directory)`; neither object
  relates an advisor to an account. I took the ownership map -- the artifact the edge validator
  already trusts for the same question -- and made the permitted set an INTERSECTION so it can
  only shrink. That is a design decision inside a cell whose spec is frozen, filed as row
  `IRPT_BCKEND-W2-S7` rather than made quietly.
* **The seam is silent in the SAFE direction.** With no `id_projection`, the custodian/opaque key
  spaces do not join and the advisor sees NOTHING -- which reads as a correct revocation, not as a
  broken join. That is why the row is ARMED and why every census prints the unmatched count with
  its three reasons.
* **`FIRM_OPERATIONS` is a widening relative to an advisor**, deliberately: a firm-authorized
  viewer gets the firm population *under the same rules* (the face's own fixture list). It is
  bounded by `verified_request_firm_id` and by the single directory handed in, so it can never
  become a cross-firm aggregate -- but it is the branch where an ambiguous `admin` signal buys the
  most, and it is the one to challenge.
