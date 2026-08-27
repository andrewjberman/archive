# `POSN_TENANCY.TO-2-DS` — Cottonwood Positioning presence, measured

**Seat:** `0.4.0_DS_ClientPlatform~L` · **Issuer:** `2.0.0_SA_COO~Z` · **Date:** 2026-08-27T21:0xZ
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/POSN_TENANCY.TO-2-DS.cottonwood-home-and-empty-vs-missing.md` @`f1c83161bd`
**Read-only TO. No S3 object was written — stated as a measured inventory in AC4, not as an intention.**

---

## VERDICT

**AC1 PASS · AC2 PASS · AC3 PASS · AC4 PASS. ACCEPTED 4/4 by `2.0.0_SA_COO~Z` @`e4b264c7c4`.**
**Cottonwood Positioning presence at the served key: ABSENT — established as a MEASUREMENT, with
three positive controls, not inferred from the absence of a pipeline.**

✅ **Proof instance `rc=0 VALID`, `violations=0`, 4 rows — re-verified at this seat after the issuer
fixed the TO.** It first returned INVALID, and the cause was markdown backticks in the TO's
`<decomp_ref>`, not the instance; `2.0.0_SA_COO~Z` diagnosed that at their own seat and owned it. §5.
**I did not work around it, and the record of why is kept rather than tidied away.**

## 1. THE SERVED KEY — resolved on the rail, then measured live

The served key was **not** read out of a record. `comp-find` surfaced `compproof` reports of past
investigations (laptop paths) naming `opal-data-portal-v2`, which **conflicts** with the PRD's
*"substrate `opal-data-assets` TODAY"*. That conflict is exactly why the key was resolved on
`comp-routes` and then measured on the live plane:

```
comp-routes trace '/api/general/positioning/positioning_data.json'
  behavior /api/general/*  ->  origin S3-opal-data-portal-v2-json
  rewrite  /api/general/   ->  json/
  S3 URI   s3://opal-data-portal-v2/json/positioning/positioning_data.json
```

`comp-routes` declares its own plane: **DESIRED** — parsed Terraform + committed router source,
never a live `describe-distribution`. So it names the key; it does not establish presence. Presence
below is `s3api` on the **LIVE** plane.

## 2. AC1 — COMPLETE listings, exhaustion PROVEN

⛔ **Why manual pagination.** The CLI's auto-paginate **merges pages and drops `IsTruncated`/
`NextToken`** — the very field this criterion asks me to show is the one auto-paginate removes, and
`KeyCount` reads absent for every prefix. So each page is fetched with `--no-paginate` and the loop
terminates **only** on `IsTruncated == False`. `--max-items` and `head` appear nowhere.

| probe | prefix | pages | terminal `IsTruncated` | keys |
|---|---|---|---|---|
| AC1-a | `opal-data-portal-v2/json/positioning/` | 1 | **False** | **3** |
| AC1-b | `opal-data-portal-v2/json/` | 1 | **False** | **954** |
| AC1-c | `opal-data-cot/` (Cottonwood's home) | 7 | **False** | **6,599** |
| AC2-b | `opal-data-49financial/` | 12 | **False** | **11,847** |

The served Positioning prefix holds exactly three keys — `allocation_summary.json`,
`holdings_attribution_data.json`, `positioning_data.json`. **There is no firm dimension in any key**;
the artifact is a single unscoped object, which is the PRD's own *"served on `api/general/` to every
authenticated user of every firm."*

Across all **954** served keys: **0** contain `cotton`, `cot/`, `/cot`, `tenant` or `scoped`.
Account census: **31 buckets**, `opal-data-cottonwood` **ABSENT**, `opal-data-inflection` **ABSENT**
— independently reproducing the PRD §2a measurement at my own instrument.

⛔ **SUBSTRING TRAP, caught not counted:** token `firm` returned 2 hits, both **false** — it matched
inside `mullin-confirmation-hearing.json`. A case-folded substring census is not a census of the
concept.

## 3. AC2 — three positive controls, because the verdict is an ABSENCE

**A failed retrieval and a true absence are byte-identical.** So:

1. **Same probe finds keys** — the identical `list_all()` call returning 0 Cottonwood keys returns
   **3** on the served prefix.
2. **Works at firm-bucket scale** — `opal-data-49financial` returns **11,847** keys over **12
   pages**, so multi-page exhaustion is *exercised*, not assumed from a one-page case.
3. ⭐ **The control that matters most — Cottonwood's own home is NON-EMPTY.** `opal-data-cot`
   returns **6,599** objects over 7 pages: `gold` 3535 · `platinum` 1125 · `forwardfill_v2` 695 ·
   `silver` 596 · `logs` 424 · `code` 150 · `bronze` 73 · `blackdiamond` 1. **The absence is not an
   empty bucket and not a blind credential — one instrument reads 6,599 objects out of that exact
   bucket and 0 of them are Positioning.** `PT-b-3`'s *"a data HOME but NO Positioning data in it"*
   is measured on both halves by the same probe.

Plus a **head-object discriminating pair** on one bucket, one prefix, one command form:
`json/positioning/model.json` → **rc=254, HTTP 404**; `json/positioning/positioning_data.json` →
**rc=0**, ContentLength **8088**, LastModified `2026-08-27T11:05:20+00:00` (**`s3api`, UTC**).

⛔ **GRAIN TRAP, and it would have inverted the answer.** Token `position` matches **922 of 6,599**
keys in Cottonwood's home — `positions_cube.py`, `canonical_positions.py`, `0_composition.json`.
Those are the **canonical positions** pipeline, a different grain from the portal's **Positioning**
page artifact. A naive token census returns 922 and concludes Cottonwood *has* Positioning data. The
measured tokens are `positioning` → **0**, `allocation_summary` → **0**, `holdings_attribution` → **0**.

## 4. AC3 — the consumer DOES distinguish, incidentally, and the MISSING branch is lossy

**All citations @ portal `4a52439cbe`; every line number re-derived by `grep` at that commit, and
each cited file confirmed clean vs HEAD with a negative control that shows the one dirty path.**

```
MISSING key   portal-proxy.ts:94   if (!response.ok) {
              portal-proxy.ts:112    throw new Error(`API request failed: ${response.status} ...`)
              -> React Query ERROR state (queryFn at ModelPortfolioModal.tsx:134, Attribution.tsx:36)

EMPTY artifact portal-proxy.ts:115  return response.json()        -> resolves
              portal-proxy.ts:1133  canonicalizeCodeKeys(resp.portfolios)
              portal-proxy.ts:42    if (!rec) return rec          -> does NOT throw
              -> React Query SUCCESS state, no data
```

**Answer: YES, they land in different consumer states today.** ⛔ **The qualification is the part
worth reading:** the discrimination is a **byproduct of `!response.ok`**, not a designed contract.
The MISSING branch collapses into one undifferentiated `Error` string that also carries auth
failure, expired token and edge errors — nothing downstream can tell *"this firm has no data"* from
*"your token expired."*

⚠ **RELAYED, NOT RE-DERIVED BY ME:** a served-plane control recorded at `portal-proxy.ts:1099-1100`
says a **nonexistent path returns 401, not 404** (auth enforced before path resolution), which would
make MISSING indistinguishable from UNAUTHENTICATED. That is `0.0.0_AB_MSTR~Z`'s measurement, and a
docstring gives sufficient not necessary conditions. Re-measuring needs a live bearer against the
distribution — outside a read-only substrate TO. Carried with its caveat rather than folded in.

## 5. ⛔ PROOF-OF-SPEC: **RESOLVED @`e4b264c7c4`** — was alignment-INVALID, cause was the TO

> ✅ **RESOLVED, and re-verified at THIS seat rather than accepted on report.** `2.0.0_SA_COO~Z`
> found the cause at their own seat, named it as theirs — *"I wrapped the path in markdown backticks
> … your instance was correct the whole time and my formatting failed it"* — and fixed it in all
> three TOs carrying the construction. **Re-run here after the fix:** `rc=0 VALID`, `violations=0`,
> 4 rows; `alignment-forward-1` 4/4 criteria carry cell_refs; `alignment-forward-2` 4/4 cell_refs
> resolve; **negative control `rc=1`, fires**; the extractor now reads
> `workflows/…/DECOMP.md` → resolves **True**. The section below is kept as the record of what the
> failure looked like from the executor's side, **not** as an open blocker.
>
> ⚠ **One residual the checker discloses on its own face and it is the issuer's field:**
> `alignment-backward` reads **2 of 5** declared cells reachable, because the `<decomp_ref>` is
> UNDELIMITED and its wide harvest picks up `PT-b-2`, `PT-b-4`, `PT-inv-7` — the three ids this TO's
> scope_fence **explicitly EXCLUDES**. The tool says so itself: *"an EXPLICIT EXCLUSION CLAUSE reads
> here as a claim … NOT asserted as a violation. Add `<owned_cells>` to make this enforceable."*
> **An exclusion and an ownership claim are indistinguishable to the harvest**, so the 2/5 is not a
> coverage gap in this work. Not my artifact to amend.

```
proof-of-spec-check ... T2DS-AC1,T2DS-AC2,T2DS-AC3,T2DS-AC4   -> rc=1, violations=2
  structural=jsonschema | acceptance rows=4        <- the INSTANCE is well-formed
  VIOLATION decomp_ref.doc: instance names '<path>' but the governing TO names '`<path>'
  VIOLATION decomp-resolution: '`<path>' does not resolve to a file
```

The checker extracts the TO's decomp path **with a leading backtick**. **Proven by a one-variable
test on the extractor itself**, same path both times:

| `<decomp_ref>` notation | extracted | resolves |
|---|---|---|
| prose + backticks (this TO) | `` `workflows/…/DECOMP.md `` | **False** |
| bare path (the `TO-F3-DS` precedent) | `workflows/…/DECOMP.md` | **True** |

**This is the same class as the `<issued_to>` prose-notation defect documented in `org/XXX.md`** —
a machine-read field written for a human reader, where the tool then reports zero/unresolvable and
the reader blames the instance. **Fix is one notation change in the TO; that is the issuer's write.**
⛔ **I did not make my instance match the broken extraction** — adding a backtick to my path would
satisfy the string-compare and still fail resolution, i.e. it would loosen a gate that is firing
correctly. *A criterion that fires is right.*

## 6. `cell_status` — from states OBSERVED, never synthesized from criterion verdicts

⚠ **This block lives here and not in the instance because `PROOF_OF_SPEC.schema.json` has NO SLOT
for `cell_status` and its root is `additionalProperties:false`** — putting it there makes the
instance invalid. See §7.

| cell | `cell_status` | basis |
|---|---|---|
| `PT-b-3` | **OBSERVED** | Home present (6,599 objects, exhaustion proven) **and** Positioning absent (0 of 6,599; 0 of 954 served keys), one instrument, three positive controls. Both halves measured at the served key, not inferred from the absence of a pipeline. |
| `PT-c-2` | **PARTIALLY OBSERVED** | The **consumer** half is observed (§4, cited at `file:line @ 4a52439cbe`). The **producer** half **does not exist** — no producer emits a per-firm artifact, so there is no explicit-empty behaviour to observe. Exactly the honest close the TO predicted; I am not upgrading it because three criteria passed. |
| `PT-inv-1` | **OBSERVED (held)** | No render, screenshot, browser or Playwright call was made. Every verdict rests on bytes: object listings, head-object metadata, source lines at a named commit. Held **by construction of the method**, not by assertion. |
| `PT-inv-4` | **MEASURED NO-OP** | Read-only TO, so other firms are byte-identical **by construction**. Reported as a no-op, **not as a verification performed** — the TO asks for exactly that distinction and I did not run a cross-firm comparison. |

## 7. SURPRISE-CHANNEL ITEMS — all OBSERVATION / INERT, to `3.0.0_SA_CVO~Z` cc `2.0.0_SA_COO~Z`

**(a) A served key referenced by client code does not exist — LATENT, not live.**
`portal-proxy.ts:1381` fetches `/api/general/positioning/model.json`; `comp-routes` resolves it to
the same S3 origin and rewrite as its neighbours; `head-object` → **404** against a control → **200**.
⛔ **I almost reported this as a live breakage.** `getModelData` has **zero call sites**: 2 code
occurrences across **1,069 tracked portal files**, both in `portal-proxy.ts` (definition `:1379`,
barrel export `:2450`); every other hit is a doc. Negative control on `getPositioningData` returns
many. The portal's own docs record the call being **deliberately removed** for performance —
`etl/OPTIMIZED_JSON_STRUCTURE.md:387` and `etl/IMPLEMENTATION_SUMMARY.md:414` both say *"Remove
`getModelData()` call"* against a 16 MB PKL costing 5+ seconds. Consumer retired on purpose, key went
with it, exported wrapper left behind. **Not a defect today; it becomes one the moment anything calls
the export.** The docstring's *"Lambda: Checks X-User-Tier header"* would have explained the absence
benignly — that rival was **checked and excluded**, not assumed away.

**(b) The TO mandates a field the schema forbids.** `cell_status` appears nowhere in
`PROOF_OF_SPEC.schema.json` and the root is `additionalProperties:false`. Same class the schema's own
comment documents at `:41` for `decomp_ref` — *"the schema forcing a free-text workaround."* A TO
requiring a field the schema forbids yields either an invalid instance or unjoinable prose; I took
the prose knowingly and say so.

**(c) The shared checkout moved under me twice mid-task.** Workspace HEAD advanced between two
consecutive calls (a `find` for the TO returned nothing, then the file was there); the portal
submodule advanced `8b8a2cc775` → `4a52439cbe` between reading `portal-proxy.ts` and citing it. Every
`file:line` in §4 was **re-derived at the current commit** rather than carried forward. **A citation
whose vintage moved is not a citation, and on a ~12-seat shared tree the vintage moves with no signal.**

**(d) `PT-b-4` touched, not acted on** (TO's standing block). The AC2-b sweep of
`opal-data-49financial` necessarily traversed the two-prefix condition. Reporting only that it was
seen; three seats have measured it and a fourth measurement is not what it needs.

## 8. SCOPE HELD

No producer named (`PT-c-1` fenced, BLOCKED by the uncertified `PT-b-2`). No empty-contract designed
or built. No S3 object written — the complete verb inventory was `sts get-caller-identity`,
`s3api list-buckets`, `s3api list-objects-v2`, `s3api head-object`; **4 of 4 read-only, 0 write
verbs.** No alarm/monitor proposed (`PT-inv-5`). No gate loosened.
