# IB-s-2 PHASE 1 -- THE VALIDATOR TRACE

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` | **TO:** `IRPT_BCKEND.TO-IB-s-2` | **Cell:** `IB-s-2`
**Object traced:** `/c/tmp/wk-irpt-1-2/infra/aws/lambda-edge/auth-validator-edge/index.mjs`
(449 lines) at branch `wk-irpt_bckend-1-2` HEAD `313659c29c`.
**Instrument:** direct source read, line-addressed. Every line number below was re-read from the
file at that HEAD, and the resolver's own unit test
`test_every_trusted_header_is_actually_injected_at_the_line_it_claims` re-asserts each one on
every run -- so if the file moves, the test fails instead of this document lying.

---

## 1. THE INJECTED HEADER SET -- DENOMINATOR 9 OF 9

The validator is the single auth gate and the origin's only identity source:

> `:7` -- `* Downstream Lambdas never parse JWTs -- they read the injected X-User-* headers.`

The injection is one contiguous block, `:383-391`. Each header is assigned unconditionally
(`request.headers[...] = [...]`), so for these nine names a browser-supplied value CANNOT survive
-- the assignment overwrites it whether or not the client sent one.

| # | header | injected at | source claim | note |
|---|---|---|---|---|
| 1 | `X-User-Email` | `:383` | `payload.sub` | `\|\| ""` -- empty string when the claim is absent |
| 2 | `X-User-Name` | `:384` | `payload.name` | `\|\| ""` |
| 3 | `X-User-Tier` | `:385` | `payload.tier` | `\|\| "unknown"` -- the ONLY default that is not empty |
| 4 | `X-User-Role` | `:386` | `payload.role` | `\|\| "user"` -- absent role reads as a non-admin user |
| 5 | `X-Firm-Id` | `:387` | `payload.firmId` | `\|\| ""` -- the verified request firm |
| 6 | `X-User-Type` | `:388` | `payload.userType` | `\|\| ""` |
| 7 | `X-Advisor-Id` | `:389` | `payload.advisorId` | `\|\| ""` -- the .004a scoping identity |
| 8 | `X-Advisor-Role` | `:390` | `payload.advisorRole` | `\|\| ""` -- added by v12 (`:31`) |
| 9 | `X-Origin-Verify` | `:391` | **NOT A CLAIM** -- the constant `"cloudfront"` | the edge's own marker |

**Denominator: 9 headers found, 8 of them claim-derived, 1 a constant.**

**A stale carrier, found while tracing and reported rather than smoothed over.** The file's OWN
header comment at `:11-12` enumerates the injected headers and lists **EIGHT**, omitting
`X-Advisor-Role`:

> `:11-12` -- `* Injected headers: X-User-Email, X-User-Name, X-User-Tier, X-User-Role,`
> `*   X-Firm-Id, X-User-Type, X-Advisor-Id, X-Origin-Verify`

The v12 changelog entry at `:30-31` says `X-Advisor-Role` is injected, and the code at `:390`
does inject it. So the file carries two enumerations of one set and the summary one is short by a
member. **This trace is built from `:383-391`, the CODE, not from `:11-12`, the SUMMARY** -- and
that choice is why the count here is 9 and not 8. (The order's own Phase-1 note cites `:31` for
`X-Advisor-Role`; `:31` is the changelog line, `:390` is the injection.)

## 2. WHAT THE VALIDATOR DOES **NOT** DO -- the fact the resolver is built on

**It strips nothing.** There is no delete, no allow-list filter and no `X-` sweep anywhere in the
file: v7 (`:19`) records that it deliberately STOPPED stripping even `Authorization`. The nine
names above are overwritten; **every other header a client sends arrives at the origin untouched.**

That single fact is the whole reason `_scope/resolve.py` works from an ALLOW-LIST rather than a
deny-list, and why arm (e) exists. A resolver that read "any `X-User-*` header" would be reading
the browser on every name the validator does not happen to overwrite.

## 3. THE GATE THE VALIDATOR ITSELF ENFORCES

> `:188` -- `//   - Users with no advisorId claim AND no admin role cannot hit advisor-scoped paths`

implemented at `:199-207`:

```
function getAllowedAdvisorIds(payload) {
  if (payload.role === "admin") return null;        // :200  bypass
  if (payload.firmRole === "admin") return null;    // :205  bypass
  if (!payload.advisorId) return [];                // :206  deny everything
  return [payload.advisorId];                       // :207  locked to own advisorId
}
```

The resolver mirrors this at the DATA layer rather than re-deciding it: no `advisorId` and no
admin role resolves `UNKNOWN` with that line quoted as the reason, and an empty permitted set.

**Entitlement source.** The validator's own account/relationship gate (.004c) does not read a
header for the permitted set either -- it reads an S3 artifact:

> `:135-136` -- `a single S3 GetObject to opal-data-{alias}/platinum/{firmId}/ownership_map.json`
> `:153-154` -- `const bucket = FIRM_BUCKET_MAP[firmId] || ...; const key = "platinum/${firmId}/ownership_map.json"`
> `:162-163` -- `if (map.schema_version !== 1) { ... throw }`
> `:359-362` -- `entry.accounts` / `entry.relationships`, membership-checked

That artifact is the third input this cell's face does not name, and taking it is filed as row
`IRPT_BCKEND-W2-S7` (with its key-space seam) rather than assumed.

## 4. THE OPAL-PRINCIPAL QUESTION -- **NOT DISTINGUISHABLE**, and the line that settles it

The order asks for this explicitly: *"record how an Opal (non-firm) principal is distinguishable
from that header set, or that it is NOT, as a finding -- IB-s-15 builds on your answer."*

**ANSWER: NOT DISTINGUISHABLE from the injected nine.** Two independent reasons, both measured:

**(i) The discriminating claim is read but never injected.** The validator itself separates the
two populations using `firmRole`:

> `:202-204` -- `// are authorized to view all advisors within their firm. Master 'role'`
> `//   remains reserved for Opal-platform admins per the firmRole framework`
> `:205` -- `if (payload.firmRole === "admin") return null;`

`firmRole` is **not** among the nine injected headers. It exists inside the edge function and dies
there. A downstream Lambda cannot see it at all.

**(ii) The file contradicts itself about whether `role` alone carries the distinction.** `:202-204`
says master `role` is *reserved for Opal-platform admins*. Forty lines earlier the .004a semantics
say the opposite in a concrete case:

> `:184-185` -- `//   - Any jwt.role === 'admin' bypasses (null return) -- Opal staff AND`
> `//     partner-firm admins (e.g. Travis at 49financial, role=admin)`

A named partner-firm user at 49financial carries `role=admin`. So `X-User-Role: admin` is
**shared by Opal staff and firm admins** and cannot separate them. The two carriers are in one
file and they disagree; this trace does not pick a winner, it reports that neither can be relied
on and takes the narrower branch.

**Candidates considered and rejected, by subtraction from the printed denominator of 9** (not
from a forward list of what came to mind):

| header | why it cannot carry the answer |
|---|---|
| `X-User-Role` | shared by both populations -- `:184-185` |
| `X-Advisor-Role` | v12 TIER vocabulary for advisor-intelligence gating (`:32-36`), not an org boundary; `admin` here is one of its bypass values too |
| `X-User-Tier` | `tier === 'internal'` appears in the v12 admin bypass (`:243`) and is the closest thing to an Opal marker -- but it is an UNENUMERATED free-text claim with no registry anywhere in the repo, and its own default is `"unknown"` (`:385`). A value with no closed domain cannot be an authorization boundary. |
| `X-User-Type` | same shape: `userType === 'Dev'` is a bypass value (`:244`), free text, no registry |
| `X-Firm-Id` | empty for a user with no `firmId` claim -- but "empty" is ALSO what a misconfigured firm user gets (`\|\| ""`, `:387`), so absence is ambiguous in exactly the direction that would grant |
| `X-User-Email` | a domain (`@opalinvest.dev`) would be a heuristic on a string a JWT issuer controls; a name never authorizes |
| `X-User-Name`, `X-Advisor-Id`, `X-Origin-Verify` | carry no org-boundary information at all |

**9 of 9 headers examined; 0 can distinguish an Opal principal from a firm admin.**

**What the resolver does with that.** `OPAL_GLOBAL` is **never minted from headers**. It requires
`opal_principal_ids`, an explicit server-side roster the caller supplies, **empty by default** --
so the capability is ABSENT rather than silently granted. A `role=admin` caller with a verified
firm resolves `FIRM_OPERATIONS`, the firm-bounded class. Bound 3 says Global is granted to an Opal
principal and **never** to a firm one; a signal that cannot tell them apart cannot be the thing
that grants Global.

**What IB-s-15 must add, with the file and the owner named.** The upstream fix is one line beside
`:390` injecting the claim that already decides this inside the function:

```
request.headers["x-firm-role"] = [{ key: "X-Firm-Role", value: payload.firmRole || "" }];
```

* **FILE:** `/c/tmp/wk-irpt-1-2/infra/aws/lambda-edge/auth-validator-edge/index.mjs`
* **LANE / OWNER:** `.owned-paths.yaml` has no rule for `infra/aws/lambda-edge/auth-validator-edge/**`;
  the longest match is `infra/aws/**` -> lane **`CLOUD_OPS_OR_ETL`**, *"Any AE agent -- infra/aws,
  pipeline Terraform, hook wiring"*. (The one edge function carved out of that lane is
  `public-data-router`, `.owned-paths.yaml:1870-1872`, and this is not it.) So the owning seat is
  an **AE seat** -- `0.7.0_AE_CloudOps` and its lanes, or `0.8.0_AE_CloudComp`.
* **NOT IN THIS ORDER'S `<paths>`.** This cell reads that file and does not write it. Editing it
  would be a BLOCKING row, never an override.
* **AND IT IS A SERVED-OUTPUT ACT, NOT A CODE EDIT.** Lambda@Edge is replicated to every
  CloudFront point of presence; the function sits on distribution `EVTSA9VEHNZVH` (`:4`) in front
  of **28 existing behaviors**. Adding a header there is a change to the auth path of every route
  on the distribution, so it carries the never-widen sign-off, not just a deploy.

**A cheaper alternative IB-s-15 should weigh first:** keep the roster server-side. The resolver
already accepts `opal_principal_ids`; a small Opal-principal list read from a server-only location
grants Global with **no change to the edge at all** and no blast radius on 28 behaviors. The
upstream claim is the cleaner long-run answer; the roster is the one that needs no sign-off.

## 5. WHICH FIXTURES COULD **NOT** BE CUT FROM REAL IDENTITY DATA

Stated here because the judgment criterion asks for it and because a fixture that cannot represent
the failure cannot score it.

| fixture | real data available? | why |
|---|---|---|
| the 201-group overlap | **YES, and it is the only one** -- IB-s-1 measured 201 groups, 29,907 memberships, 6,155 unique accounts. Modelled faithfully (one account under two relationships) but with synthetic ids. | using real opaque ids in a committed fixture would put a live account identifier in the repo for no gain -- the overlap is a SHAPE |
| a partly permitted relationship | **NO** | requires an ownership map that grants part of a relationship. No ownership map has been read by this cell at all, and the seam in row W2-S7 means the live one would not even join to the directory |
| a revoked entitlement | **NO** | there is no entitlement plane in production yet -- IB-s-1's directory emits `access.entitled: UNKNOWN` with a reason for every one of 5,062 entries |
| an Opal principal | **NO -- and this is the finding, not an inconvenience** | no Opal-principal roster exists anywhere on the DESIRED plane, and section 4 shows the header set cannot identify one. A "real" fixture would have to invent the very claim whose absence is the finding |
| a firm admin | **NO** | a real admin JWT is a credential; bound 6 forbids one in any fixture, log or commit |
| a forged header | **NO, BY CONSTRUCTION** | the forgery is a request that never happened. It is synthesised from the real header NAMES (section 1) so it is shaped exactly like the thing it must not be trusted as |
| the unmatched-ownership list | **NO at this vintage** | IB-s-1 measured INF unmapped at **0 of 874** -- the live population is EMPTY, so a live-cut fixture would pass vacuously (row `IRPT_BCKEND-W2-S3`). Constructed instead, with all three gap reasons exercised |

**1 of 7 fixture classes has a live population at this vintage.** Everything else is synthetic and
says so in `_scope/tests/fixtures.py`, with the shape's real source cited per item.
