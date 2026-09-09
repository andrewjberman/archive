# DEPRECATION DETERMINATION — the consumer walk to a CLIENT-FACING TERMINUS (cell RP-s-7, outcome FWD-6)

Authority: `NFRA_REPORT_PRD.md` manifest row S7 (`FWD-6`), `C-DEPRECATED-TERMINUS`, and
`ANDREW_DIRECT_20260909_1458Z_INFRA_REPORT_FIVE_RULINGS.md` batch 3 (rulings 6, 8, 9 and the CRO's own
"ONE REFINEMENT RULING 9 STILL NEEDS" grain correction). Renders through `STATE_MODEL.md`
(`CHECKED`/`UNCHECKED`/etc.) where a candidate's status resolves cleanly; declares `UNCHECKED` honestly
where the available instrument cannot resolve it.

## 0. THE LAW: age raises the question, the terminus settles it

**`C-DEPRECATED-TERMINUS`: deprecated = ZERO CONSUMERS AT THE CLIENT-FACING TERMINUS**, established by
walking the chain to a served artifact AND a rendered component. **NEVER the first `scripts:` field,
NEVER age.**

This is a superseded-heuristic story, and both halves matter:

- **Ruling 6** (Andrew, first pass): *"If any artifact is over 1 week old it is almost certainly
  deprecated."* An AGE heuristic, offered in good faith on the evidence available at the time.
- **Ruling 9** (Andrew, after this seat's own additional review falsified ruling 6's hypothesis):
  *"the deprecation criterion is ZERO DECLARED CONSUMERS, NOT AGE... The age heuristic of ruling 6 is
  superseded by Andrew's own word here."*
- **The CRO's own follow-on correction, same session:** a ONE-HOP consumer check ("artifact -> the
  `scripts:` field") said all ten candidate artifacts HAVE consumers; Andrew's actual claim was about
  the TERMINUS — whether a *client-facing surface* consumes them, hop N, after following the chain to a
  served artifact and a rendered component. **"Zero declared consumers" at hop 1 says none of the ten
  is deprecated; at the terminus it may say all ten are.** A criterion that inverts on grain is not yet
  a criterion (rule 24(ii), SAME GRAIN).

**So: AGE is a prompt to look, never a verdict.** Being old raises the question and never settles it.
"Old" is never quietly treated as "dead." This document's determination law is the TERMINUS walk, full
stop — and the rest of this document is that walk actually performed, not merely asserted.

## 1. THE GRAIN-INVERSION TRAP, DEMONSTRATED LIVE (not just cited)

Ruling 9's refinement was a worked HYPOTHETICAL when it was written. This cell re-ran it against a real
candidate and got the exact inversion predicted:

- **Hop 1** (`comp-pipescript consumers B_01.holdings_lots.py --pipeline bd-gold`): *"B_01: no
  downstream pipeline consumers (terminal or portal-only)."* Read alone, this LOOKS deprecated.
- **Hop 2**, walked rather than stopped at: `comp-pipescript io D_04.client_portal_summary.py
  --pipeline bd-gold` shows `D_04` READS `HOLDINGS_LOTS_PREFIX <- IMPLICIT: B_01 (via FUNC-key)` — an
  implicit cross-reference the WRITE-side tool missed but the READ-side tool caught. `D_04` then WRITES
  `platinum/firm/dashboard.json` and five more platinum keys, which `comp-pipescript`'s own embedded
  portal-route resolver confirms are served to REAL, NAMED components: `ClientsTab`, `DistributionTab`,
  `AdvisorPublicProfile`, `AdvisorAnalytics`, `PartnerAnalytics`.

**`B_01` is not deprecated.** A reader who stopped at hop 1 — or who trusted "no downstream pipeline
consumers" as the verdict — would have filed it as a decommissioning candidate. This is `C-DEPRECATED-
TERMINUS`'s whole point, shown rather than argued.

## 2. THE WALK, PERFORMED, ON ANDREW'S OWN TEN CANDIDATES

The ten artifacts ruling 6/9 discuss by id (`B_01`, `B_02`, `A_03`, `INF_D_00`, `INF_D_04`, `INF_D_07`,
`INF_D_03`, `INF_D_02b`, `INF_C_01`, `INF_D_00c`), resolved to files and walked with
`comp-pipescript io`/`consumers` (pipeline-internal chain) and `comp-platinum reverse` (S3 key -> route
-> component, per build-ladder rung 2 — query the existing graph, never rebuild):

| Candidate | Resolved file | Terminus finding | Basis |
|---|---|---|---|
| `B_01` | `data/black_diamond/scripts/gold/B_01.holdings_lots.py` | **ALIVE** (2-hop) | feeds `D_04` (implicit, read-side); `D_04` reaches `ClientsTab`/`DistributionTab`/etc., CONFIRMED not speculative |
| `B_02` | `.../B_02.canonical_lots.py` | **ALIVE** (2-hop) | writes `canonical_holdings_key` -> `B_00, B_03, D_04`; same `D_04` terminus as above |
| `A_03` | `.../A_03.positions_cube.py` | **ALIVE** (2-hop) | writes `silver/allocations/*` -> `B_00, B_01, C_02, C_04, D_04`; same `D_04` terminus |
| `INF_D_00` | `data/inf/scripts/gold/INF_D_00.portal_aggregates.py` | **AMBIGUOUS** | writes `platinum/firm/clients_tab.json` (no confirmed route; `comp-platinum` returns only `[SPECULATIVE]` catch-all matches) and `platinum/firm/filters/dimensions.json` (`"no components found -- check Lambda@Edge handlers for this key"`, the tool's own honest non-answer) |
| `INF_D_04` | `.../INF_D_04.client_portal_summary.py` | **ALIVE, CONFIRMED** | `getPlatinumAdvisorNnaClients` -> `DistributionTab`; `getPlatinumFirmDashboard` -> `ClientsTab`; `getHeaderMetrics` -> `PartnerAnalytics`, `ClientsTab` — none marked `[SPECULATIVE]` |
| `INF_D_07` | `.../INF_D_07.concentration_risk.py` | **UNRESOLVED-BY-THIS-WALK** | `comp-pipescript` reports `WRITES: (none detected)` — a PARSER MISS (`OUTPUT_PREFIX + 'firm/concentration_risk.json'`, a concatenated key); `comp-platinum reverse` on the reconstructed key returns a blank `PRODUCER` (off this tool's index entirely) and only `[SPECULATIVE]` consumers |
| `INF_D_03` | `.../INF_D_03.composition_artifacts.py` | **AMBIGUOUS** | writes 2 platinum keys (`firm_composition.json`, per-advisor `composition.json`); `comp-platinum` returns only `[SPECULATIVE]` catch-all matches for both |
| `INF_D_02b` | `.../INF_D_02b.top_holdings.py` | **AMBIGUOUS** | writes `platinum/firm/top_holdings.json`; `[SPECULATIVE]` catch-all only |
| `INF_C_01` | `.../INF_C_01.canonical_nna.py` | **UNRESOLVED-BY-THIS-WALK, LIKELY ALIVE** | `comp-pipescript` reports `WRITES: (none detected)` — a PARSER MISS (write routed through a `_write_s3(df, key)` helper with a computed key); the file's OWN governance comments describe it as an "ATOMIC SET" chokepoint, "NEVER#2 co-signed by CTO + COO", under a SERVE-RELEASE-ACK discipline — textual evidence of active production status this walk could not independently confirm reaches a rendered component |
| `INF_D_00c` | `.../INF_D_00c.portal_leaderboard.py` | **ALIVE, CONFIRMED** | `getFirmLeaderboard` -> `AdvisorsTab`, `ClientsTab`, `index` — not marked `[SPECULATIVE]` |

**Tally: 5 of 10 ALIVE (3 by chain, 2 confirmed direct); 3 of 10 AMBIGUOUS (a platinum key exists, no
confirmed route); 2 of 10 UNRESOLVED-BY-THIS-WALK (the write itself is invisible to the static tool).
ZERO of 10 are shown DEAD by this walk.** Ruling 6's "these look deprecated" and the un-walked "zero
declared consumers at hop 1" reading are both falsified for at least half the set, and none of the
other half is affirmatively dead either — every one of them is honestly `UNCHECKED` or `COARSE`
(looked at the wrong grain), never rendered as a confirmed deprecation.

## 3. DECLARED BLINDNESSES — named rather than hidden

The coordinator's own instruction on this cell: *"if the walk cannot be completed for some candidate...
that is a real limit and belongs in the deliverable as a declared blindness, not as a silent
omission."* Three, filed as surprise-channel rows `NFRA_REPORT-Z-W1-S1` and `-S2` because they are
ESTATE-WIDE tool-capability gaps and not specific to this cell's ten candidates, and carried here in
summary because they bound what this document can honestly claim:

1. **`comp-blast`'s served graph models NO edge between `GOLD_SCRIPT` and Lambda/portal nodes at all**,
   confirmed by a positive control: `arn:aws:lambda:...:inf-api-positions`, a lambda independently known
   to be live, shows ZERO `gold:` ancestors upstream in the same graph. A bare `comp-blast` zero-count on
   a gold script is therefore NOT evidence toward or against deprecation for ANY gold artifact in the
   estate — this document does not use `comp-blast` downstream/upstream counts as a terminus signal for
   that reason, and instead uses `comp-pipescript`'s embedded portal-route resolver and `comp-platinum
   reverse`, which DO model the `platinum/` key convention.
2. **`comp-pipescript`'s static WRITES parser misses a dynamically-constructed S3 key** (prefix-variable
   concatenation, or a write routed through a key-building helper function), producing a false `WRITES:
   (none detected)` for `INF_D_07` and `INF_C_01`. This is why those two render `UNRESOLVED-BY-THIS-WALK`
   rather than `CHECKED`/anything — the instrument cannot see the write at all, so it certainly cannot
   confirm or deny a terminus.
3. **Pipeline-identity ambiguity on the three bare-named candidates.** `B_01`, `B_02` and `A_03` exist,
   byte-identically named, in BOTH `data/black_diamond/scripts/gold/` and `data/cot/scripts/gold/`.
   Ruling 6/9's text does not say which firm tree it means. This walk resolved them against
   `black_diamond` (`bd-gold`) only. If the ruling in fact meant Cottonwood's copies, the METHOD above
   still applies unchanged but the specific verdicts in §2 would need re-running against `cot-gold` —
   declared, not assumed away.

**The `[SPECULATIVE]`-vs-confirmed distinction in §2 is the tool's own, not this cell's invention**:
`comp-platinum reverse` marks a match `[SPECULATIVE]` when it falls back to a catch-all route pattern
without a directly traced key, and prints plain component names with no tag when it traced a real
`endpoint -> route -> component` chain. This document treats only the untagged form as `CHECKED`.

## 4. What this document does NOT do

- **Issues no decommissioning action and no retirement-register entry.** Ruling 8 makes
  decommissioning/cleaning "a function of this work" at the PROGRAM level, but the retirement register
  with owner/reason/date is `S8` (`RP-s-8`), downstream of this cell, and `S8`'s own bound says
  "never-widen sign-off (CTO+COO) still governs RETIRING SERVED OUTPUT — this project CLASSIFIES, it
  does not delete." This document classifies; it deletes nothing and recommends deleting nothing.
- **Does not treat AMBIGUOUS or UNRESOLVED-BY-THIS-WALK as DEAD.** Per §0, "old is never quietly
  treated as dead," and this document extends that discipline to "unresolved is never quietly treated
  as dead" either — five candidates could not be walked to a confirmed terminus, and all five are
  reported as exactly that, not as deprecation candidates.
- **Does not re-run the walk against `comp-blast`** as if its zero-count were meaningful for gold
  scripts, per the declared blindness in §3.1.
