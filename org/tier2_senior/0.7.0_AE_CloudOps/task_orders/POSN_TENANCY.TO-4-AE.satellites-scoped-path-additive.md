<task_order>
<id>POSN_TENANCY.TO-4-AE.satellites-scoped-path-additive</id>
<title>THE SATELLITES SCOPED PATH — additive, firm-discriminated, and the three firms WITHOUT Satellites must get an EXPLICIT EMPTY rather than a refusal-shaped error</title>
<project>POSN_TENANCY</project>
<directive>POSN</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~Y</issued_to>
<issued_at>2026-08-27T22:2xZ</issued_at>
<status>complete -- CLOSED **SUPERSEDED** BY THE ISSUER 2026-09-01 ~14:3xZ (2.0.0_SA_COO, who issued it), routed by 0.0.0_AB_MSTR 91786 on ANDREW-DIRECT ~14:0xZ that D4 and POSN_TENANCY are DONE. ** SUPERSEDED, NOT ACCEPTED, AND THE DISTINCTION IS THE WHOLE POINT (0.0.0_AB_MSTR~Z's bound, adopted): 'THE WORK IS DONE IN THE WORLD' AND 'EVERY ACCEPTANCE CRITERION WAS SCORED' ARE DIFFERENT CLAIMS. MEASURED AT THE INSTANCE BY THIS SEAT, not taken from the routing message -- POSN_TENANCY.TO-4-AE_PROOF_OF_SPEC.json, DENOMINATOR 6: 3 PASS, 1 UNCOMPUTABLE-BY-CONSTRUCTION, 2 UNVERIFIABLE-BY-INSTRUMENT. THREE OF SIX ARE NOT PASS, so an ACCEPTED stamp would assert a scoring that did not happen. The sovereign's word closes the WORLD half; it does not retroactively score the criteria, and nobody re-runs them -- per /mstr-spawn 1d-ii, measure the artifact, close the face, NEVER re-execute; a re-execute of finished work is a REWIND. ** NO ACCEPTANCE WAS RE-RUN, NO CRITERION RE-STAMPED, NO DELIVERABLE TOUCHED. || PRIOR STATUS, VERBATIM: ACTIVE</status>

<decomp_ref>
workflows/atom_decomposition/runs/posn-tenancy/20260827T200734Z/DECOMP.md — stage-3 atom decomp,
authored by 2.0.0_SA_COO~Z. **Cells this TO discharges: PT-a-1, PT-a-3.**

⭐ **RE-CERTIFIED by `3.0.0_SA_CVO~Z` at pin `@4a1d7a5e3c`** — both cells verified **byte-identical
between pin and worktree by CELL HASH** (`PT-a-1` `1f7b8261159a`, `PT-a-3` `c7cbdbb0e60e`), so the
file's later movement does not touch them. **These are the restated cells, not the originals.**
</decomp_ref>

<basis>
**ANDREW-DIRECT ~22:1xZ, VERBATIM** (record `@834bfafebb`):
> *"I think it is better to just do a scoped api path for the satellites, that way we dont have to
> mess with the rest of the plumbing of the page and it is inobtrusive + if we decide later that it
> makes more sense to just handle this elsewhere, then doing so is not a massive effort."*

**ANDREW-DIRECT ~21:52Z, VERBATIM:** *"all of Positioning is general, it was always meant to be a
general page, but we are making an exception in the case of cottonwood here for the purpose of their
'Satellites' portfolios."*
```
SATELLITES payload      -> a NEW firm-scoped API path        <- THIS TO
positioning_data.json   -> UNTOUCHED. General, /api/general/, keeps serving four firms
MODELS / ETFS           -> UNTOUCHED. No re-plumbing, no migration, no re-point
```
⭐ **HIS SELECTION CRITERION, CARRIED BECAUSE IT OUTLIVES THIS DECISION:** he chose on
**REVERSIBILITY** — *"not a massive effort"* to undo — **not on which design is most correct today.**
**Prefer the option that is CHEAPEST TO BE WRONG ABOUT.** Any design choice inside this TO that
forecloses cheap reversal is off-spec.
</basis>

<payload_blocker>
⛔⛔ **`AC1`'s POSITIVE ARM AND `AC3` ARE BLOCKED — AND THE PRECISE STATE IS "DEFINED IN SHAPE,
UNPOPULATED, PRODUCER NAMED", *NOT* "nothing exists".** Measured by `0.7.0_AE_CloudOps~Y` BEFORE
writing any Terraform, which is why this cost nothing; **reframed by `3.0.0_SA_CVO~Z`, and the
difference decides what gets built.**

⭐ **THE PAYLOAD EXISTS AND ITS CONTRACT ALREADY DOES TOO — `satelliteAdapter.ts:1-4`:** *"synthesise
the `satellites` payload from **the ALREADY-SERVED models payload PLUS the declared registry**."*
```
market / holdings data  -> the ALREADY-SERVED general artifact. Every firm receives it.  COMMON
SATELLITE_REGISTRY      -> which books, which blends, which weights.        COTTONWOOD-SPECIFIC
```
>> ⛔ **SO THE FIRM-SPECIFIC OBJECT IS THE *REGISTRY READ*, NOT MARKET DATA — AND THE DECOMP'S HAZARD
   MODEL ASSUMED OTHERWISE.** What the scoped path must serve, and what must never reach another
   firm, is **membership/blends/weights**, not prices. **`SatelliteBook` is the declared shape, so
   the contract is not an open design question.** <<
⭐ **That makes the scoped payload SMALLER and already-shaped** — a registry read, not a data plane.
```
SWEEPS, every one terminal IsTruncated=None:
  opal-data-portal-v2      4,125 keys   'satellite' -> 0
  opal-data-cot            6,599 keys   'satellite' -> 0
  opal-data-bd           122,356 keys   'satellite' -> 0
  opal-data-49financial   11,847 keys   'satellite' -> 0
  TOTAL 145,927 keys, ZERO satellite artifacts anywhere
POSITIVE CONTROL, same sweep/bucket: 'gold' 3,738 of 6,599, 'silver' 681
  -> the instrument FINDS tokens, so the zero is a MEASURED ABSENCE, not a broken probe
```
**`satelliteSet.ts:93` — `SATELLITE_REGISTRY: readonly SatelliteBook[] = []` — EMPTY BY DESIGN**, its
own header naming **`ETFS_SATELLITES.TO-2` as the PRIMARY CARRIER** of the member set (shipped empty
deliberately to avoid a second carrier). **`satelliteAdapter.ts:98` derives Satellites CLIENT-SIDE
into positioning shape and performs NO fetch.**

>> ⛔ **THE CHAIN, EVERY LINK MEASURED:** a scoped path was commissioned for a payload that **has no
   server-side existence**; its member set lives in an **empty registry**; that registry's declared
   primary carrier is **`ETFS_SATELLITES.TO-2`**, held by **`0.4.0_DS_ClientPlatform~W` — A SEAT THAT
   DIED TONIGHT** — whose own status reads *"ACTIVE — unblocked; waiting on a SEAT"*; and the
   registry's **`REGISTRY_MAINTAINER` is `None`**, the one item standing open at Andrew. <<
⭐ **THE MAINTAINER QUESTION IS NOT HOUSEKEEPING. IT IS THIS PROJECT'S CRITICAL PATH.**

**WHAT STILL PROCEEDS, and it is most of the TO:** `AC2` (additive proof), `AC4` (cache key wiring),
`AC5` (`X-Firm-Id` survives), `AC6` (rung discipline) **need no payload.** ⛔ **Do NOT invent a
fixture payload to unblock `AC1`/`AC3`** — a scoped path proved against a manufactured artifact
proves the plumbing and nothing about the boundary.
</payload_blocker>

<additive_fence>
⛔⛔ **THIS TO IS ADDITIVE. NOTHING EXISTING CHANGES MODE.**
`0.7.0_AE_CloudOps~Y` measured the three Positioning modes UNIFORM on `/api/general/` and warned that
scoping one would CREATE a 2-of-3 split against Andrew's ~21:3xZ uniformity rule; `3.0.0_SA_CVO~Z`
measured Positioning as the exception to **47** live `/api/scoped/` uses. **Both are answered by
ADDING a path rather than MOVING one.**
>> **IF THE DESIGN REQUIRES TOUCHING `positioning_data.json`, THE GENERAL ROUTE, MODELS OR ETFS, STOP
   AND SURFACE IT.** That is a finding about his ruling, not a licence to proceed. <<
</additive_fence>

<cells>

| cell | what this TO owes it |
|---|---|
| `PT-a-1` | **The Satellites payload is served firm-discriminated on a NEW scoped path.** Oracle: **Cottonwood FETCHES its Satellites artifact and another firm CANNOT**, exercised **with BOTH arms**, verified **at the response bytes**. |
| `PT-a-3` | **The CDN cache key includes firm — ON THE EXCEPTION PATH ONLY.** ⛔ **NOT on the general artifact.** Measured: the firm-keyed policy **already exists and is applied to the scoped S3 behaviours** — so this is a **WIRING** question, not a build. |
| `PT-inv-1` | **THE BYTES, NOT THE PIXELS.** Binding on every criterion. |
| `PT-inv-2` | **`X-Firm-Id` STAYS JWT-INJECTED.** Already PASSED (`TO-3-AE` `AC2`, exercised) — **must SURVIVE this change.** |
| `PT-inv-4` | **OTHER FIRMS BYTE-IDENTICAL** where not the subject. |

⚠ **`PT-c-2` BINDS THIS BUILD BUT IS CITED IN ITS *ORIGINAL CERTIFIED* WORDING ONLY:** *"a firm with
no data emits an EXPLICIT EMPTY, never a missing key; a missing key and an empty artifact must be
distinguishable at the consumer."* ⛔ **My later amendments to that cell (the 3-of-4 promotion, the
client-seam measurement) are NOT CERTIFIED and are CONTEXT, not spec.** They are quoted in `AC3`'s
rationale so you know why it matters — **the requirement you are held to is the certified sentence.**
</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `T4AE-AC1` | **BOTH ARMS, AT THE BYTES.** Cottonwood obtains its Satellites artifact (200 + its own bytes) **and a non-Cottonwood identity attempting the same path is REFUSED**, status and body recorded for each. ⛔ **A single arm is not a PASS** — "Cottonwood got its data" is equally true in a world with no discrimination. | `PT-a-1` | |
| `T4AE-AC2` | ⛔ **ADDITIVE, PROVED NOT ASSERTED.** `positioning_data.json` is **byte-identical** before/after (hash or ETag, printed), and the general route, Models and ETFs are **unchanged**. **Denominator printed.** | `PT-a-1` `PT-inv-4` | |
| `T4AE-AC3` | ⛔ **THE THREE FIRMS WITHOUT SATELLITES GET AN EXPLICIT EMPTY, NOT A MISSING KEY.** ⚠ **THE CHEAP IMPLEMENTATION IS THE WRONG ONE AND WILL LOOK RIGHT:** a bare 404/403 for those firms lands them in the client's error branch. **Measured at portal `875182fc74`:** `:94 !response.ok` → `:108` a **401-only, LOGGING-ONLY** branch → `:112 throw`. **A 403 gets no branch at all.** The status **IS interpolated into the Error string — STRINGIFIED, NOT DESTROYED — so what is missing is a CONTRACT**, and ⛔ **parsing a status code out of an Error message is NOT a contract anyone may build on.** **ABSENCE PRESENTS AS A REFUSAL.** Exercise one no-Satellites firm and show what it receives. | `PT-c-2` (original certified wording) | |
| `T4AE-AC4` | **Firm-scoped cache key on the exception path, measured AT THE EDGE** (two firms, same path, distinct entries) — **and the GENERAL artifact's cache key is shown UNCHANGED.** ⛔ **Firm-keying the common artifact partitions IDENTICAL BYTES: a correct-looking control over an exposure that does not exist, doing nothing about the one that arrives with the data.** | `PT-a-3` | |
| `T4AE-AC5` | **`X-Firm-Id` remains JWT-injected and NOT client-assertable AFTER the change** — re-exercised, not inherited from `TO-3-AE`. | `PT-inv-2` | |
| `T4AE-AC6` | ⛔ **DESIRED ≠ APPLIED ≠ EXERCISED on every claim.** Terraform is DESIRED; a live policy read is APPLIED; a request that got a response is EXERCISED. **No `.tf` cited as evidence of force.** **No render, screenshot or UI state as evidence** (`PT-inv-1`). | `PT-inv-1` `PT-a-3` | |

</acceptance_criteria>

<undischarged_carried>
⛔ **`PT-inv-3` — `null` FIRM FAILS CLOSED — HAS NEVER BEEN EXERCISED, BINDS THIS BUILD, AND IS NOT A
CRITERION ON THIS TO.** `TO-3-AE`'s `AC5` returned UNVERIFIABLE-BY-INSTRUMENT: a firmless JWT needs
**signing-key use or a production identity mutation**, neither in that grant nor this one.
>> **IT IS A CREDENTIAL QUESTION, NOT A CODE QUESTION.** ⛔ **Do NOT claim it, do NOT infer it from
   source, and do NOT let its absence block the rest of this TO.** If your work makes it exercisable,
   say so — that is a finding. Carried at decomp `@6a07d17cbb`. <<
</undischarged_carried>

<reporting>
Deliverable + proof instance in this lane's own `deliverables/` (**verified to exist**), committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~Y <0.7.0_AE_CloudOps~Y@opal.agent>" -F <msgfile>`,
message file written by a **non-shell writer**, never a heredoc.
**Push state MEASURED** with a control, **or the words "push state UNMEASURED"**.
**`cell_status` per cell from observed states ONLY** — do not synthesize cell states from criterion
verdicts.
⛔ **DESTINATION NAMED, BECAUSE MY OWN SPEC HAS BEEN MANDATING A FIELD WITH NO HOME: put the
`cell_status` block in the MEASUREMENT RECORD (`.md`), NOT in the proof instance.**
`PROOF_OF_SPEC.schema.json` has **NO SLOT** for `cell_status` — the token appears nowhere in it, and
the schema rejects unknown keys. **`0.4.0_DS_ClientPlatform~L` and `0.7.0_AE_CloudOps~Y` BOTH filed
this as an OBSERVATION/INERT against my reporting block tonight** (`TO-2-DS` instance `:104`,
`TO-3-AE` instance `:23`) **and both worked around it correctly by putting the block in the `.md` and
saying so in `deploy_evidence`.** ⭐ **That is now the instruction rather than a workaround: 27 of 31
`cell_status` occurrences estate-wide are in `.md` records.**
⚠ **I wrote the unsatisfiable requirement into four TOs and did not pick up either surprise item.
Naming the destination here so this TO is not the fifth.**
⛔ **NEVER bare `terraform apply` — use `safe-apply`.** No `aws lambda update-function-code`.
</reporting>

<standing>
⛔ **ANDREW-DIRECT ~21:3xZ, VERBATIM:** *"all of these should be based on if there is data to populate
and theyre invisible otherwise. this is something that agents need to be better about which is making
sure that when there are forked routes like this, that they are structured following the same pattern,
versus 2 of the 3 doing one thing and the other one having a unique pattern, that kind of architecture
is not acceptable."*
**INVISIBLE — not `$0`, not a placeholder.** And **whatever shape this path takes for Cottonwood, it
takes the same shape for any firm added later.**
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer, **and KEEP WORKING.**
· **No new alert/alarm/monitor** (`PT-inv-5`). **No shadow or build-alongside pipeline** — Andrew veto.
· ⚠ **`PT-b-2` UNCERTIFIED — NO SUBSTRATE SHAPE IS SELECTED.** If this design forces a substrate
  answer, **surface it; do not pick one.**
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="T4AE-AC1" cell_refs="PT-a-1"/>
  <criterion id="T4AE-AC2" cell_refs="PT-a-1,PT-inv-4"/>
  <criterion id="T4AE-AC3" cell_refs="PT-c-2"/>
  <criterion id="T4AE-AC4" cell_refs="PT-a-3"/>
  <criterion id="T4AE-AC5" cell_refs="PT-inv-2"/>
  <criterion id="T4AE-AC6" cell_refs="PT-inv-1,PT-a-3"/>
  <expected_criteria>T4AE-AC1,T4AE-AC2,T4AE-AC3,T4AE-AC4,T4AE-AC5,T4AE-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~Y/deliverables/POSN_TENANCY.TO-4-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 6 (PT-a-1, PT-a-3, PT-c-2, PT-inv-1, PT-inv-2, PT-inv-4); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 6 of 6 declared cells reachable from >=1 criterion (PT-a-1 from AC1+AC2, PT-a-3 from AC4+AC6, PT-c-2 from AC3, PT-inv-1 from AC6, PT-inv-2 from AC5, PT-inv-4 from AC2). Unmapped 0; untraceable 0. *(PT-inv-3 is DECLARED IN &lt;undischarged_carried&gt; and deliberately carries NO criterion — it is UNEXERCISABLE under this grant, and a criterion nobody can discharge is a criterion that gets closed on a substitute. Disclosed rather than dropped. PT-b-2/PT-b-4/R-pt1/PT-inv-7 remain UNCERTIFIED; PT-d-* are TO-1-DE's; PT-b-3 and PT-c-2's consumer half were discharged by TO-2-DS.)*</alignment_denominators>
  <criterion_status_note>⛔ AC1 and AC3 are the two that can be falsely passed. AC1 fails silently on a SINGLE ARM. AC3 fails silently on a BARE 404/403 — which satisfies "the firm has no Satellites" while landing the user in a branch indistinguishable from a refusal, and it is the cheapest thing to build. Both failure modes produce a green-looking result, which is why each names its refutation rather than its expectation.</criterion_status_note>
</proof_of_spec>
</task_order>
