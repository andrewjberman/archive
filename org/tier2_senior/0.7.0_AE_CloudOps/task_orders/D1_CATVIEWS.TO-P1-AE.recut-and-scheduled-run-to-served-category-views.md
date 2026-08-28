<task_order>
<id>D1_CATVIEWS.TO-P1-AE.recut-and-scheduled-run-to-served-category-views</id>
<title>PIPE THE ASSET CATEGORIES DATA: cited-literal re-cut at a valid pin, then a SCHEDULED run that actually emits category_views to the served plane</title>
<project>D1_CATVIEWS</project>
<directive>D1</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_at>2026-08-27T22:4xZ</issued_at>
<status>ACTIVE -- **WAITING ON THE ~13:30Z SCHEDULED FIRE. NO BUILD WORK IS OUTSTANDING AND NO SEAT IS
BLOCKED.** Face written 2026-08-28 ~05:1xZ by `2.0.0_SA_COO~Z` (issuer); it previously read a bare
`ACTIVE`, which told a reader nothing about what remains or how to finish it.

**MEASURED AT THE COMMITS, not taken from a report** -- `0.7.0_AE_CloudOps~Z` did this work before its
session ended:
```
  19:13Z  b3bb7e760c  the mdpf-gold-lambda RE-CUT deployed at pin 14b077f559
  21:13Z  ecd8bf438b  MDPF_GOLD_COMMIT corrected to the pin actually deployed  (ledger CLOSED 1c212ec471)
  21:21Z  e43f37395c  AC5: ViewPlaneError's five-peer refusal EXERCISED on the DEPLOYED bytes
  22:43Z  29bbc39950  AC4: the PRE-FIRE BASELINE captured -- "because AC4's 'before' is PERISHABLE"
  22:48Z  c4bb5d628b  AC4: the SCORER for that baseline, SELF-TEST-GATED and exercised
  00:08Z  89c6409419  AC1: the 13:30Z trigger measured WIRED + ENABLED + PERMITTED, BOTH EventBridge planes
```
*** THAT LANE ALREADY SOLVED THE HARD HALF WITHOUT BEING ASKED.*** `AC4` compares BEFORE against AFTER,
and the "before" **stops existing the moment the fire runs.** It captured the baseline and built a
scorer to read it. **A successor does not need that seat's context -- it needs to RUN the scorer.**

**WHAT REMAINS: all six criteria score AGAINST THE SERVED ARTIFACT, which does not exist until the
~13:30Z fire** -- `cron(30 13 * * ? *)` UTC -> `mdpf-gold-lambda`, measured live and ENABLED. **No proof
instance is filed yet and that is CORRECT, not an omission.**

⛔ **THE STANDING PROHIBITION, RESTATED BECAUSE IT IS THE ONE THING THAT CANNOT BE UNDONE: NO AD-HOC
`mdpf` GOLD RUN BEFORE 13:30Z.** It writes a REAL artifact at the REAL key and **DESTROYS the
time-of-day discriminator `AC1` exists to produce.** `AC1` scores on the SCHEDULED fire ONLY.

⚠ **OWNER STATE: `0.7.0_AE_CloudOps~Z` is DEAF (absent from `liveness.json`).** ⛔ **This is NOT a
respawn ask** -- the fire is hours out and a lane seated now to idle until 13:30Z is the same exposure
at higher cost. **Whoever holds this after the fire runs the scorer and files; the baseline and the
scorer are committed and outlive the session that made them.** ⚠ **DISARMED != REMEDIATED: if nobody is
seated after 13:30Z the fire is unobserved until someone returns.**</status>

## ⛔⛔ {OBSERVATION, ARMED} -> DISARMED SAME-TURN. THE SERVED PLANE STILL CARRIES `Alternatives`, WHICH ANDREW REMOVED FROM L0 ON 08-27.

**Raised by `1.0.0_SA_CTO~Z` (msg 13168) while verifying the 13:50:50Z write. DISARMING OWNER:
`2.0.0_SA_COO~Z` (issuer). This block IS the disarm. ⛔ DISARMED != REMEDIATED.**

**INDEPENDENTLY VERIFIED on the served cottonwood artifact by `2.0.0_SA_COO~Z`:**
```
view_plane.peers     ['Models', 'SMA', 'Alternatives', 'Client']    <- Alternatives IS declared
view_plane.excluded  ['Insurance']  ONLY
nodes.Alternatives   {aum 0.0, display_label 'Alternatives', members []}
CONTROL: Insurance IS in excluded -- the exclusion mechanism WORKS and is in use two keys away.
```
`CategoryViewTree.tsx:348` renders `block.view_plane.peers`, and `:45` states a node is deliberately
**"never silently dropped by a display constant"**. **So the page renders an EMPTY $0 `Alternatives`
card on all four scopes** -- against that component's own *true-zero -> no card, never an empty one*.

**ANDREW-DIRECT 2026-08-27 ~21:1xZ, VERBATIM (his phrasing is the ruling):**
> *"We can just get rid of Alternatives at L0, they are differnet things but if its confusing easier
> to just get rid of it"*
Record: `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ANDREW_DIRECT_20260827_REMOVE_ALTERNATIVES_FROM_L0.md`

### ⛔ THE OWNER WAS NAMED IN THE RECORD ITSELF, AND THE ACT WAS NEVER CUT -- THAT IS MINE
That record's own table reads:
```
registry / VIEW_TREE  Alternatives leaves the declared L0 node set
                      DS-class -- data/mdpf/scripts/gold/mdpf_category_registry.py. NOT this lane.
smoke fixture         node + peer entry removed        this lane, this commit
```
`0.4.0_DE_ClientPlatform~Z` did its half (`77d1bbce`, the fixture) **and correctly flagged the other
half as DS-class and not its own.** ⛔ **THE DS-CLASS TO WAS NEVER CUT, AND CUTTING IT IS THE ISSUER'S
JOB. THAT IS `2.0.0_SA_COO~Z`.** This is not a seam inside nobody's scope -- the scope was named in
writing and the issuer did not act on it.
⚠ **AND IT SURVIVED A SMOKE TEST BECAUSE THE SMOKE TEST RAN ON THE FIXTURE, WHICH HAD THE RULING.**
The half that was fixed is the half the test reads.

### ⛔ THE REMEDY -- CORRECTED. IT IS **NOT** THE INSURANCE PATTERN, AND I SPECIFIED IT WRONG.
**I first wrote "moves `peers` -> `excluded`, exactly as `Insurance`, display-only, node UNCHANGED".
That is the WRONG MECHANISM, caught by `1.0.0_SA_CTO~Z` (13174 s.3).** ⚠ **I QUOTED THE CORRECT
TREATMENT AND THEN SPECIFIED A DIFFERENT ONE, ONE PARAGRAPH LATER, FROM THE SAME TABLE I HAD JUST
PASTED.** The 08-27 record says:
```
registry / VIEW_TREE  "Alternatives LEAVES THE DECLARED L0 NODE SET"
                      DS-class -- data/mdpf/scripts/gold/mdpf_category_registry.py
emitted block         view_plane.peers stops carrying it        FOLLOWS the registry
renderer              NO CHANGE
smoke fixture         NODE + peer entry removed                 (DE lane, done @77d1bbce)
```
>> **TWO EXCLUSIONS, TWO MECHANISMS, BOTH ANDREW'S. DO NOT COLLAPSE THEM.**
```
Insurance      STAYS in the node set; DISPLAY-ONLY exclusion; node, members and gold
               partition share explicitly UNCHANGED.
Alternatives   LEAVES the declared L0 node set at the REGISTRY. peers stops carrying it as a
               CONSEQUENCE, not as the act. The node goes too -- the fixture removed node + peer.
```
⛔ Still **PRODUCER-SIDE, NOT PORTAL-SIDE** -- a portal filter is precisely the hardcoded display
constant `CategoryViewTree.tsx:45` forbids. That half of my line was right; the mechanism was not.
⚠ **DATA COST IS NIL EITHER WAY TODAY** (`Alternatives` is `aum 0.0, members 0` on all four served
scopes) -- **which is exactly why getting the mechanism right matters here rather than later: nothing
in the numbers would have caught it.**

### ⭐ SOVEREIGN CONFIRMATION FROM HIS OWN EYE, ~14:0xZ (relayed verbatim by `1.0.0_SA_CTO~Z`, 13174)
> *"Just checked the dashboard, we actually dont even need Alternatives either. It's really just Models
> SMAs and Client."*

**L0 = `Models` / `SMA` / `Client`.** ⚠ **He reached this from the RENDERED PAGE, independently, ~7
minutes after the item was filed and WITHOUT having seen it** -- *"just checked the dashboard"*.
**The empty $0 card was visible enough to draw sovereign comment on first look: that is the cost of the
seam, measured. It reached his eye before it reached a fix.**
⛔ **HIS NEW SENTENCE CONFIRMS THE DECISION, NOT THE TREATMENT.** It must not be read as re-specifying
the mechanism, nor as widening or narrowing the 08-27 scope. Verbatim relay, not adjudication.
⛔ **NOT IMPLEMENTED HERE:** DS-class file, no live DS lane, and **NO AD-HOC PRODUCER RUN** -- the
next scheduled write is 13:50:50Z tomorrow. Surfaced, owner named, remedy specified, sovereign told.

## ⭐⭐ `TP1AE-AC1` DISCHARGES. MEASURED 2026-08-28T13:52:37Z by `2.0.0_SA_COO~Z`.

AC1 requires `category_views` on the SERVED PLANE for **at least one firm**, from a **SCHEDULED** run,
with **key, bucket, byte size and LastModified recorded**. All four, for **FOUR firms**:
```
BUCKET  opal-data-portal-v2   (PLATINUM_BUCKET, mdpf-daily-trigger:172 -- read, not guessed)
  2026-08-28T13:50:50Z   4339 B   platinum/mdpf/49financial/category-views.json
  2026-08-28T13:50:50Z   5116 B   platinum/mdpf/cottonwood/category-views.json
  2026-08-28T13:50:51Z   4442 B   platinum/mdpf/global/category-views.json
  2026-08-28T13:50:52Z   4331 B   platinum/mdpf/inflection/category-views.json
```
**PROVENANCE = SCHEDULED, and it is not inferred from the clock.** ⭐ **THE ARTIFACT NAMES ITS OWN
WRITER:**
```
_provenance.written_by  'opal-assets-mdpf-portal-publisher'      <- the writer, IN the artifact
_provenance.written_at  '2026-08-28T13:50:49Z'
as_of                   '2026-08-27'      source_vintages  cottonwood/category-views: '2026-08-27'
```
**13:50:50Z matches the six-day scheduled cadence to the second; ad-hoc writes on this prefix land at
arbitrary times (16:28, 15:42, 19:46).** The timestamp IS the scheduled-vs-adhoc discriminator this TO
exists to protect, and the `written_by` field makes it a stated claim rather than an inference.

**CONTENT IS REAL, not an empty shell at a plausible size** -- 5 nodes carrying Andrew's own rulings:
```
Client  aum 294,905,777.43 · display_l1_axis 'fee_taking'
Models  aum 186,785,080.61 · 2 children
SMA     aum 0.0  members_present False, with absent_reason: a TRUE ZERO (Andrew-direct 2026-08-25)
Insurance  view_plane_excluded True, quoting Andrew-direct 2026-08-24 verbatim
Alternatives  aum 0.0
```
⛔ **THIS DISCHARGES `TP1AE-AC1` ONLY.** AC2-AC6 are separate criteria and no claim is made about
them here.

## ⛔⛔⛔ CORRECTION TO THE SECTION BELOW, BY ITS OWN AUTHOR (`2.0.0_SA_COO~Z`, 13:3xZ)

**I wrote below that "`TP1AE-AC1` LIVES HERE" at the 13:30Z gold floor and that AC1 "scores the GOLD
floor". READ AC1'S OWN TEXT (`:262`): *"`category_views` EXISTS ON THE SERVED PLANE for at least one
firm, emitted by a SCHEDULED producer run."*** ⛔ **AC1 SCORES THE SERVED PLANE, NOT GOLD.**
```
so AC1 discharges when platinum/mdpf/{firm}/category-views.json EXISTS
   -> written by the 13:50:50Z PUBLISHER
   -> THE SAME CLOCK AS ANDREW'S CARDS, not twenty minutes earlier
13:30Z mdpf-scheduled-floor is NECESSARY (it produces the input) and NOT SUFFICIENT (it is not
   the served plane AC1 names).
```
⚠ **I HAVE NOW MIS-STATED THIS CLOCK TWICE, IN OPPOSITE DIRECTIONS** -- first conflating 13:30Z with
Andrew's cards, then separating AC1 from the cards when AC1 rides the SAME write. **Both errors came
from reasoning about the SCHEDULE instead of reading the CRITERION.** The criterion names an artifact;
the artifact names its writer; the writer has the clock. That order is the fix.

**MEASURED 13:33:56Z, the AC1 probe itself:**
```
platinum/mdpf/**/category-views.json          0 objects     <- correct and EXPECTED at 13:33Z
POSITIVE CONTROL, same prefix, same probe:    platinum/mdpf/cottonwood/{account-distribution,
  account-units,aggregate-aua-timeseries,aum-metrics}.json  4 objects
>> THE PROBE WORKS AND THE ABSENCE IS REAL, not a broken read. Bucket opal-data-portal-v2
   (PLATINUM_BUCKET, mdpf-daily-trigger:172).
```
⭐ **RE-RUN THAT EXACT PROBE AFTER ~13:51Z.** AC1 also requires key, bucket, byte size and
`LastModified` RECORDED, and that the run be SCHEDULED rather than ad-hoc.

## ⛔⛔ 13:30Z IS `TP1AE-AC1`'s GATE. IT IS **NOT** WHEN ANDREW'S CARDS APPEAR.

**Found by `1.0.0_SA_CTO~Z` (msg 13141) 2026-08-28 12:3xZ. Recorded here by `2.0.0_SA_COO~Z`, the
ISSUER OF THIS TO AND THE SEAT THAT MADE THE SAME CONFLATION IN WRITING TO ANDREW.** The mdpf chain is
**FOUR staged schedules**, not one fire -- all on EventBridge **Scheduler**, all `TZ=UTC` explicitly
read (a local-time reading here is hours wrong):
```
12:52Z  mdpf-feeder-backstop-daily              -> mdpf-feeder-trigger
13:30Z  mdpf-scheduled-floor                    -> mdpf-gold-lambda            <- TP1AE-AC1 LIVES HERE
13:40Z  mdpf-accrual-bridge-daily               -> mdpf-accrual-trigger
13:50Z  opal-assets-mdpf-portal-publisher-daily -> opal-assets-mdpf-portal-publisher   <- THE SERVED WRITE
```
**MEASURED, not inferred from the names** -- version history of `platinum/mdpf/cottonwood/aum-metrics.json`
with a same-prefix control on `global/`: **`13:50:50Z`, TO THE SECOND, SIX CONSECUTIVE DAYS**
(08-22 through 08-27).

>> ⛔ **`TP1AE-AC1` DISCHARGING AT 13:30Z DOES NOT MEAN THE CARDS ARE VISIBLE.** AC1 scores the GOLD
   floor. The artifact the page fetches -- `/api/general/mdpf/{firm}/category-views.json` ->
   `platinum/mdpf/{firm}/category-views.json` -- is written **twenty minutes later, by a DIFFERENT
   Lambda on a DIFFERENT schedule.**
>> ⛔ **A LOOK AT 13:35Z SEES NOTHING, AND NOTHING IS WRONG.** That is a wasted sovereign look
   manufactured by a stage nobody had opened.

⚠ **INSTRUMENT TRAP ON THAT MEASUREMENT, worth more than the number:** `head-object` alone returns the
LATEST version, which on this key is an **AD-HOC write at 16:28Z** -- it would have said "the prefix is
written at 16:28." **The version LIST exposes the cadence; the head is ONE SAMPLE of it, and here the
newest sample is the least representative.** Ad-hoc writes are ROUTINE on this prefix, which is exactly
why the scheduled-vs-adhoc discriminator this TO protects matters.

⚠ **THE BOUND, STATED BY ITS AUTHOR:** `category-views.json` **does not exist yet**, so its own
history cannot be read -- only its four siblings at the same prefix, which are unanimous. The claim is
**the PREFIX is written by the 13:50Z publisher**: a strong same-writer inference, NOT a direct
measurement of the new key. ⭐ **If the key appears between 13:30 and 13:50 that FALSIFIES this and is
good news, not a problem.**


<decomp_ref>
workflows/atom_decomposition/runs/d1-catviews/20260824T195537Z/DECOMP.md — stage-3 decomp for
D1_CATVIEWS, round 1 CERTIFIED. **Cells this TO discharges: D1-inv-2, D1-inv-3, D1-inv-4.**
</decomp_ref>

<basis>
**ANDREW-DIRECT ~22:4xZ:** *"we still havent gotten data flowing to the Asset Categories panel,
theyre just using mock numbers from DE, which is fine because theyre only on DEV Branch, but we need
to figure that out, what agent is tasked with piping that data?"*

⛔ **THE MEASURED ANSWER WAS: NOBODY. THIS TO IS THAT ANSWER BEING FIXED.**
```
category_views SERVED         opal-data-portal-v2  0 keys containing 'category'
                              opal-data-cot        0 keys containing 'category'
PRODUCER CODE                 EXISTS AND IS BUILT --
                              mdpf_category_registry.py:844  build_category_views(...)
                              mdpf_gold_consolidator.py:537  _shape_category_views(...)
OPEN D1_CATVIEWS TOs          ONE -- TO-I1-DS (channel enumeration, NOT production),
                              held by 0.4.0_DS_ClientPlatform~T, not a live seat
```
**The code is built. The artifact has never existed. No TO covered producing it.**

⚠ **WHY THE GAP PERSISTED, stated plainly because it is this office's miss:** the COO NO-SHIP ruling
`@0d08954d4c` (~19:3xZ) named exactly this work and said *"the path runs through an AE-class re-cut,
and **there is no AE seat**."* **That was true when written and stopped being true at ~21:0xZ when
AE seats came online. Nobody re-cut it.** This TO is ~90 minutes late.
</basis>

<the_interlock>
⛔ **THIS IS NOT A DEADLOCK AND MUST NOT BE READ AS ONE.** The build refuses at the **default pin**
because PACKAGE names `mdpf_category_registry`, which **does not exist at `bf74d031c1` (2026-08-10)** —
that pin **predates the module's birth at `be05d938af` (2026-08-19)**. **That refusal is the interlock
working, not a breakage.**
**The sanctioned shape is a CITED-LITERAL RE-CUT** — `build_package.py` names the **`4e0410825e`
precedent**. **AE-class, which is why it is yours.**

⛔⛔ **PIN TEST CORRECTED 22:5xZ — "CONTAINS THE MODULE" IS NOT SUFFICIENT AND MY ORIGINAL WORDING WAS
WRONG. Measured by `0.7.0_AE_CloudOps~Z` AT THE DEPLOYED BYTES, before building anything.**
```
DEPLOYED mdpf-gold-lambda  CodeSha256 57V6D/ZNiAGSKBe2UkJ33aevjHDCLj0HNRphN//+iKg=
  mdpf_category_registry.py   12,602 B   build_category_views   ABSENT   ViewPlaneError ABSENT
  mdpf_gold_consolidator.py   55,629 B   _shape_category_views  ABSENT   import registry ABSENT
CONTENT-RESOLVED: both members EXACT match at be05d938af
  NEG CONTROLS bf74d031c1 / 4e0410825e / HEAD all DIFFER -> the match DISCRIMINATES
```
>> ⛔ **`be05d938af` CONTAINS THE MODULE, IS WHAT IS DEPLOYED, AND EMITS NOTHING. A re-cut there passes
   `build_package.py:181`, produces a clean zip, deploys GREEN — and changes nothing: a SILENT NO-OP
   WEARING A SUCCESSFUL BUILD**, which `AC2`/`AC3`/`AC4` would then be measured against on an artifact
   that never appeared. <<
⭐ **THE CORRECT TEST IS THE EMIT PATH, NOT THE MODULE FILE:** does the pin carry
`_shape_category_views` **and** `"category-views"` in the consolidator's A4 loop. **Resolve it by
CONTENT (`git show <pin>:<file>`, normalised, with a negative control) — never by date, filename, or
`is-ancestor`.**
⭐ **AND IT ANSWERS ANDREW'S QUESTION AT THE ROOT: `category_views` has never existed because THE
RUNNING CODE CANNOT PRODUCE IT.** Not a bug, not a config gap — **an old build.** Corroborated on the
data plane: `portal/gold/mdpf/` in `opal-data-assets` holds **0 category keys of 292**, across 4
scopes and 5 artifact types that DO exist.

⛔⛔ **PIN RE-RULED 23:0xZ — `14b077f559`. THE EARLIER `4e0410825e` RULING IS WITHDRAWN: I RULED OVER
A THREE-OPTION SET AND THE SET WAS INCOMPLETE.**
`0.7.0_AE_CloudOps~Z` swept **every commit touching either module in `be05d938af..HEAD` —
DENOMINATOR 19** (18 from the log + the deployed pin as a control) — and **exactly ONE satisfies all
three criteria.** ⚠ **`4e0410825e` was not even in that population; the three pins I chose among were
the three already NAMED in the interlock and the TO. A named set is not a measured set.**
```
be05d938af   IMPORT NO   EMIT NO   BUCKETS NO    the deployed pin
14b077f559   IMPORT YES  EMIT YES  BUCKETS YES   *** SATISFIES ALL THREE -- USE THIS ***
407e1e057b   IMPORT YES  EMIT YES  BUCKETS NO
3e88e10511..ba2a91d980 (12 more)   YES YES NO
bd6f0bbccd / efec3ca8b5 / ecf55a119e / a0643a35fc  NO NO NO
```
**VERIFIED INDEPENDENTLY AT THE ISSUER'S SEAT, BY CONTENT, WITH A NEGATIVE CONTROL:**
`_shape_category_views` consolidator **2** · `category-views` consolidator **13** / registry **2** ·
`SMA_BUCKETS` consolidator **1** / registry **2** · `import mdpf_category_registry` **1**.
**NEG CTL at `be05d938af`: `_shape_category_views` = 0 — the check discriminates.**

⭐ **THIS DISSOLVES THE TRADE-OFF THE EARLIER RULING RESTED ON.** I wrote *"getting data flowing and
getting the new tree are TWO acts"* **because I believed every emit-capable pin lacked
`SMA_BUCKETS`.** `14b077f559` carries **both**. ⛔ **It is ONE act, and the two-acts sentence above is
withdrawn.**

⚠ **WHAT `14b077f559` IS:** `0.4.0_DS_ClientPlatform~Z`'s `TL2DS-AC2/AC4/AC5` — *"the SMA L1/L2
restructure + scope-B emit as ONE act."* **Its TO is COMPLETE, accepted 7/7, instance `rc=0 VALID`.**
⚠ **CITATION CORRECTED 23:1xZ — `AC2`/`AC4`/`AC5` are CVO-certified, and the DURABLE CARRIER IS
`org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoZ_D1_CATVIEWS_TL2DS_CERTIFICATIONS_20260827.md`
@`b57d6d0d1f` (97 lines, verified at this seat).** ⛔ **When I first cited those certifications as
support for this pin, THEY HAD NO ARTIFACT — they existed only as broker message ids.**
`3.0.0_SA_CVO~Z` found that themselves and wrote the record; **it re-states the verdicts at their
ISSUING vintages and does NOT re-certify.** ⭐ **A citation without an artifact is not a citation, and
I made one on a production pin.**
⛔ **AND `TL2DS-AC3` IS *NOT* CERTIFIED BY THAT SEAT** — it was delivered before the criteria they
took, and no verdict was ever issued on it. **So the disjointness support `@98b4475edc` is
`0.4.0_DS_ClientPlatform~Z`'s OWN ADDENDUM, uncertified.** ⚠ **It is a strong argument on its face and
I verified it independently — but do NOT cite it as certified.**
⛔⛔ **THE JUSTIFICATION ABOVE WAS CORRECTED 23:0xZ BY `0.4.0_DS_ClientPlatform~Z` — AUTHOR OF BOTH
THE COMMIT AND THE CRITERION. THE PIN STANDS; MY CITED SUPPORT WAS THE WRONG HALF.**
~~`TL2DS-AC3` verified `D1-inv-2` byte-unchanged, so this commit is MEASURED not to move the
five-peer served total.~~
**`TL2DS-AC3` HAS TWO LEGS AND ONLY ONE REACHES THIS PIN:**
```
STRUCTURAL  git diff 407e1e057b^ 407e1e057b + a grep proving sma_member_aum was NEVER READ.
            ⛔ EXPIRES AT 14b077f559 -- the restructure's whole point is that sma_member_aum IS
            now read, consumed into the SMA bucket keys at :641-643. The non-interference proof
            was true of the EARLIER commit and DOES NOT EXTEND TO THE PIN.
EXERCISED   five-peer sum 1000.00 == 1000.00 ON THE RESTRUCTURED CODE. THIS leg covers the pin.
            ⚠ BOUND: it ran on a FIXED/SYNTHETIC node_aum. It proves THE CODE PATH PRESERVES THE
            IDENTITY. It does NOT prove production values are unchanged.
```
>> ⛔ **"MEASURED NOT TO MOVE THE SERVED TOTAL" WAS TOO STRONG BY ONE WORD.** The measured claim is:
   **the identity holds under exercise on a fixture.** <<
⭐ **AND THE PIN IS SAFE FOR A DIFFERENT REASON THAN I GAVE: on a plane that has NEVER SERVED, there
is no served total to move.** Nobody has compared a real run against a real prior artifact **because
the artifact has never existed** — which is this TO's entire subject. ⛔ **`AC2`/`AC3` ARE WHERE THE
REAL ARTIFACT IS FIRST READ. Do not treat the fixture exercise as having pre-discharged them.**
⚠ **THE CONCLUSION WAS RIGHT AND THE EVIDENCE WAS NOT. A right answer from invalid evidence is not
knowledge, and an executor inheriting my sentence would have believed production values were already
proven unchanged.**

⭐⭐ **REPLACEMENT SUPPORT RECORDED `@98b4475edc` BEFORE THE PIN IS ACTIONED — AND IT IS STRONGER THAN
WHAT IT REPLACES, BECAUSE IT IS A PROOF BY CONSTRUCTION RATHER THAN BY EXERCISE.**
**KEY-SPACE DISJOINTNESS, exhaustive, denominator = the whole file: `node_aum` occurs EXACTLY 4 TIMES
in the consolidator.**
```
:625  node_aum = {Models, SMA, Alternatives, Insurance, Client}   CONSTRUCT -- five peers, ONCE
:629  node_aum[f"Models > {label}"] = sum(...)                    ADD
:641  node_aum[f"SMA > {bucket}"]   = sum(...)                    ADD
:646  build_category_views(..., node_aum=node_aum)                PASS
```
1. **the five peer keys are written EXACTLY ONCE, at `:625`, before either loop**
2. **`TOP_LEVEL_PEERS` (registry `:94`) are all BARE TOKENS carrying no `" > "`**
3. **both later writes use f-strings that ALWAYS contain `" > "`** — so no loop write can EVER equal
   a peer key. **They ADD; they cannot REASSIGN.**
∴ **`sum(TOP_LEVEL_PEERS)` is fixed by `:625` alone and is STRUCTURALLY UNREACHABLE from the
restructure's writes — for ALL INPUTS, including production data.** ⭐ **This is what my retracted
sentence purported to establish and could not: it holds without a fixture.**

⛔ **AND IT DOES NOT PRE-DISCHARGE `AC2`/`AC3`.** Disjointness proves the restructure **cannot move**
the five-peer sum. **It says NOTHING about what the emitted values ARE.** `AC2`/`AC3` remain **the
first reading of a real artifact.**
⭐ **`0.4.0_DS_ClientPlatform~Z` recorded it as an ADDENDUM and left the accepted instance
`@44955a2721` UNTOUCHED** — *"amending an accepted, CVO-certified instance to retro-fit a
justification it was never asked to carry would have been the worse act; `AC3` remains a PASS for what
it was written to prove."* **Correct, and the same principle this office applied to `D1F3DS-AC3`.**
⚠ **STILL TRUE: `D1-inv-4` is TRUE BUT UNENFORCED at this commit** — `AC3` verifies a value nothing
guards, and must say so.
⛔ **HEAD REMAINS FORBIDDEN.** `14b077f559` is a **specific cited pin**, which is the sanctioned
cited-literal shape; **HEAD is not, until the NO-SHIP is lifted BY NAME.**

~~PIN RULED BY THE ISSUER: `4e0410825e`. USE IT.~~ **WITHDRAWN — see above.**
```
be05d938af   emit NO    = the DEPLOYED pin. A no-op re-cut. EXCLUDED.
4e0410825e   emit YES   L1 machinery YES (l1_nodes 7, members_present 4, render_state 2,
                        absent_reason 3 -- IDENTICAL counts to HEAD)   SMA_BUCKETS ABSENT (0)
HEAD         emit YES   everything   ⛔ FORBIDDEN -- the interlock bars HEAD until the NO-SHIP is
                        lifted BY NAME, and this TO does not lift it
```
⚠ **STATED SO IT IS NOT DISCOVERED LATER: at `4e0410825e` the data flows on the OLD SMA STRUCTURE.
`SMA_BUCKETS` is absent, so Andrew's ~20:5xZ ETF/ALT tree WILL NOT BE PRESENT in the emitted
artifact.** That is **consistent with deployed reality** — `TO-L2-DS`'s restructure is committed and
**not deployed** — and the new tree needs a later pin advance, which needs the NO-SHIP lifted.
**Getting data flowing and getting the new tree are TWO acts, and this TO is the first.**
⭐ **`0.7.0_AE_CloudOps~Z` hypothesised `4e0410825e` would yield EMPTY L1 sets and fail `AC3`, then
MEASURED IT FALSE before sending — the L1 counts are identical at both pins.** The real delta is
narrow and specific, and the narrow version is what this ruling rests on.

⛔⛔ **THE `D1_CATVIEWS` NO-SHIP STANDS AND THIS TO DOES NOT LIFT IT.** `build_package.py:266` names
**"a COO/Andrew ship ruling"** as what lifts it. **This TO produces the EVIDENCE that would justify a
lift; it does not perform one, and completing it is not an argument that the pin may advance.**
**No pin advance, no promote, no PROD anything.**
</the_interlock>

<cells>

| cell | what this TO owes it |
|---|---|
| `D1-inv-2` | **GOLD-plane: the five top-level peers SUM TO `total_aua`, per firm** — **measured ON THE SERVED ARTIFACT**, not in a test harness, **denominator printed**. |
| `D1-inv-4` | **VIEW-plane: rendered L0 values sum to `total_aua − Insurance`, AND every L1 set sums to its L0 parent** — on the served output. ⛔ **`0.4.0_DS_ClientPlatform~Z` measured this invariant TRUE BUT UNENFORCED** (perturbing an L1 bucket by +5.00 raises nothing, in SMAs *and* Models). **You are verifying a value that NOTHING GUARDS — say so in the deliverable.** |
| `D1-inv-3` | **Legacy `non_model` fields BYTE-UNCHANGED** — the regression direction that announces nothing if it breaks. |

</cells>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `TP1AE-AC1` | **`category_views` EXISTS ON THE SERVED PLANE for at least one firm**, emitted by a **SCHEDULED** producer run. **Key, bucket, byte size and `LastModified` (UTC, `s3api`) recorded.** ⛔ **An ad-hoc run is PERMITTED FOR QA and is NEVER the acceptance** — *"ad-hoc artifacts are never production evidence"*, and *"success-of-upstream as the only trigger is a defect."* **The SCHEDULED fire is the acceptance.** | `D1-inv-2` | |
| `TP1AE-AC2` | **`D1-inv-2` holds ON THE SERVED ARTIFACT** — five gold-plane peers sum to `total_aua`, per firm, **denominator printed, measured on the fetched bytes.** | `D1-inv-2` | |
| `TP1AE-AC3` | **`D1-inv-4` holds on the served output** — L0 values sum to `total_aua − Insurance`, and **every L1 set sums to its L0 parent, with member counts exhibited.** ⚠ **An L1 set that sums because it is EMPTY is not a pass.** ⛔ **Report that the invariant is UNENFORCED** (measured by `0.4.0_DS_ClientPlatform~Z`) — **a passing value behind no guard is a different state from a guarded one.** | `D1-inv-4` | |
| `TP1AE-AC4` | **`D1-inv-3` byte-unchanged** — legacy `non_model` fields identical before/after, **by hash or ETag**, not by inspection. | `D1-inv-3` | |
| `TP1AE-AC5` | ⛔ **The `ViewPlaneError` path EXERCISED at least once AGAINST A REAL MISMATCH** and shown to refuse. **Its FIRST real exercise must not be a client-facing producer run** — that is the specific hazard the NO-SHIP ruling named: a five-peer invariant that raises on mismatch can **abort a client-facing producer**. | `D1-inv-2` | |
| `TP1AE-AC6` | ⛔ **DESIRED ≠ APPLIED ≠ EXERCISED on every claim**, and **the re-cut pin is cited by CONTENT** (`git show <pin>:<file>` + a negative control), **never by `merge-base --is-ancestor`** — a cherry-picked or ephemeral pin resolves only by content. **No `.tf` cited as evidence of force.** | `D1-inv-2` `D1-inv-3` | |

</acceptance_criteria>

<reporting>
Deliverable + proof instance in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~Z <0.7.0_AE_CloudOps~Z@opal.agent>" -F <msgfile>`,
message file written by a **non-shell writer**, never a heredoc.
**Push state MEASURED** with a control, **or the words "push state UNMEASURED"**.
⛔ **`cell_status` per cell from OBSERVED states only — put the block in the `.md` MEASUREMENT RECORD,
NOT the proof instance:** `PROOF_OF_SPEC.schema.json` is `additionalProperties:false` and has no slot
for it. **Do not synthesize cell states from criterion verdicts.**
⛔ **NEVER bare `terraform apply` — use `safe-apply`.** No `aws lambda update-function-code`.
⚠ **`aws s3 ls` renders LOCAL time; `s3api` renders UTC** — name which produced any timestamp.
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· **No new alert/alarm/monitor** — standing moratorium. **No shadow or build-alongside pipeline,
  no duplicate output path, no standing parity comparator** — Andrew complete veto.
· ⚠ **The panel currently renders MOCK numbers from DE on DEV.** ⛔ **Do NOT treat the mock as a
  contract or reconcile the real output to it** — if served output disagrees with the mock, **the
  mock is wrong**, and that is a finding for `0.4.0_DE_ClientPlatform~Z`, not a defect to fix here.
· ⛔⛔ **AND AGREEMENT WITH THE MOCK IS ALSO WORTHLESS — `0.4.0_DE_ClientPlatform~Z` DISCLOSED THIS
  AGAINST THEIR OWN ARTIFACT, UNPROMPTED.** The smoke fixture (portal `@20373baa`) is **NOT an
  independent description of the expected block: it was DERIVED FROM `mdpf_category_registry.py`.**
  >> **SO IF THE SERVED ARTIFACT MATCHES THE FIXTURE, THAT IS NOT TWO SOURCES AGREEING — IT IS THE
     PRODUCER AGREEING WITH A RESTATEMENT OF ITSELF.** ⛔ **Do NOT cite fixture agreement as
     corroboration in any criterion.** Same author, one rung, counted twice. <<
  ⭐ **WHAT THE FIXTURE IS LEGITIMATELY GOOD FOR — a SHAPE CHECKLIST, and use it only that way:**
  children with **both** buckets emitted for every firm · **ETF 4 members / ALT 2** · `l1_nodes` and
  `un_noded_members` **ABSENT**.
  ⚠ **TWO PLACES THE FIXTURE IS KNOWINGLY AHEAD OF THE PRODUCER — A MISMATCH THERE IS EXPECTED AND IS
  NOT A DEFECT IN THE SERVED ARTIFACT:** (1) **per-member `aum`** — `_members()` does not emit it
  (`registry:900-903`), and the fixture carries **invented** values because Andrew ~22:3xZ asked the
  drilldowns to show amounts; (2) **EVERY MAGNITUDE is invented** — *"the $4.00M is not cottonwood's
  DIVZ AUM."* ⛔ **Do not report either as a producer defect.**
  ⭐ **`0.4.0_DE_ClientPlatform~Z` re-derives the fixture against the served artifact once one exists,
  and reports disagreement as a DE finding. Nothing is owed to that lane by this TO.**
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="TP1AE-AC1" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC2" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC3" cell_refs="D1-inv-4"/>
  <criterion id="TP1AE-AC4" cell_refs="D1-inv-3"/>
  <criterion id="TP1AE-AC5" cell_refs="D1-inv-2"/>
  <criterion id="TP1AE-AC6" cell_refs="D1-inv-2,D1-inv-3"/>
  <expected_criteria>TP1AE-AC1,TP1AE-AC2,TP1AE-AC3,TP1AE-AC4,TP1AE-AC5,TP1AE-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~Z/deliverables/D1_CATVIEWS.TO-P1-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 3 (D1-inv-2, D1-inv-3, D1-inv-4); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 3 of 3 declared cells reachable from >=1 criterion (D1-inv-2 from AC1+AC2+AC5+AC6, D1-inv-4 from AC3, D1-inv-3 from AC4+AC6). Unmapped 0; untraceable 0. *(The decomp's remaining cells are NOT this TO's: the Client-L1 family (D1-k-*), channel enumeration (D1-i-*, carried by TO-I1-DS), the render/consumer cells (D1-c-*) and the SMA-tree family (D1-h-r3, discharged by TO-L2-DS) are untouched by producing the served artifact.)*</alignment_denominators>
  <criterion_status_note>⛔ AC1 is the one that can be falsely passed, and the failure is cheap and invisible: an AD-HOC run produces a real artifact at a real key, and every downstream criterion then measures TRUE against it. The artifact would be genuine and the acceptance would still be wrong, because a pipeline whose only trigger is a human is not a pipeline. AC1 passes on the SCHEDULED fire or it does not pass.</criterion_status_note>
</proof_of_spec>
</task_order>
