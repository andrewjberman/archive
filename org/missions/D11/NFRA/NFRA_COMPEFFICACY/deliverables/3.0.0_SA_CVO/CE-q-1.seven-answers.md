# NFRA_COMPEFFICACY -- CE-q-1, Andrew's seven questions answered in writing (v2, all seven answered; round 6)

**Author:** `3.0.0_SA_CVO` (the CVO authors, the CTO lands the section in the PRD -- decomp CE-q-1, FWD-5). **Written:**
2026-09-03 18:0xZ. **Bar (FWD-5 ACCEPT):** for each question in his message there is an answer in plain English that says what
the thing actually does, and where he asked "is this just X?" the answer says yes or no and why; each answer points at the
row that answers it and is disputable by him. **State (v2, 18:3xZ):** all seven answered from completed orders (T-21 and T-24 landed in round 6's second tranche);
the platinum answer carries the lane's own two uncomputed criteria as part of the answer, not hidden behind it. Every fact below is the named deliverable's measurement, read by this seat; nothing
here is this seat's own measurement unless it says so.

## 1. Is the one he was unsure of a tool or a built-in?

**Answer: neither of the two names that are not tools is a tool.** `comp-hud` is not a tool: it is the rail's hook
(`.tools/hooks/comp-tool-hud.sh`, a PreToolUse gate on Bash), recorded as DOES-NOT-EXIST at row T-4 by this seat at the
enumeration (decomp CE-t-4, DONE). `comp-legacy` is not a tool either: 0 of 106 entrypoints exist under that name (row T-15,
CE-t-15, DONE). Both stay on the list marked as such, per FWD-1, and are never dropped. *If the name he was unsure of is a
third one, the brief's parenthetical names it and this answer is re-pointed at that row in the second pass.*

## 2. Is the deny-tester needed in practice?

**Answer: needed when an IAM change ships, not in daily practice -- and it now works honestly, which it did not.** `comp-denytest`
derives the expected verdict from the change type (deny-add, allow-removal, no-op) and simulates it; before T-11 a plan with
no testable change collapsed into a generic error, and a `MissingContextValues` simulation could print a deny that was
byte-identical to a real one. After T-11 (0.8.0_AE_CloudComp~E, @7c2dbf6611) it separates no-subject, present-zero and
unsupported-change with exact tokens, defers the conditioned-grant false deny as NOT-DECIDABLE rc 2 instead of a verdict,
and bounds its AWS subprocess under Rule T. Usage is the honest part: 8 runs ever and 2 in 30 days at the issuer's pinned
baseline (6 in 30 days re-measured, most of them the audit's own). The lane surfaced RETIRE-candidate on usage and
removed nothing. **So: yes as a deploy-time instrument for IAM changes (it is the only thing in the estate that turns an
IAM diff into an expected verdict and it caught a real false-deny class); no as a tool anyone reaches for otherwise.**
Whether that is "keep on the short list" or "retire" is his FWD-4 call, with the measured numbers above.

## 3. Does the similarity tool supplant the three roll-ups?

**Answer: no.** `comp-similar` (T-12, 0.8.0_AE_CloudComp~F, @3b1ef874ad) is BM25 similarity over what resources *do* --
summary text -- plus an advisory superseded-twin scan that requires heat divergence and suppresses designed parallels and
held resources. It is not `comp-dups` (a separate engine by the CTO's arch-gate ruling 3; T-13 is HELD at the CTO on that
ruling), and it is not `comp-drift` (T-14: propagation across 13 declared topology seams -- whether a change reached the
places it must reach -- not function similarity). Three different questions: "does anything else do this?", "is this a
duplicate?", "did this change propagate?". The lane's own guard controls make the point measurable: same name, different
purpose scores 0.0; different name, same purpose scores 1.0; similarity without heat divergence yields no supersession.

## 4. What do pulse, heat and system actually do, and do they work?

- **pulse** (T-18, 0.8.0_AE_CloudComp~M, @cd5e84ae2f): the danger-map-before-commit reflex -- `comp-pulse diff` checks a
  commit's files against the estate's danger map and prints a measured CLEAN or the hits. It works: 12,778 recorded runs, of
  which 12,763 are the `diff` mode the pre-commit hook fires (the hook is the caller for ~99.9% of them, by mode evidence), and
  the new battery passes 12 of 12 with a mutant per state. No second engine does this; coldness is `comp-debris`'s, not pulse's.
- **heat** (T-20, 0.8.0_AE_CloudComp~I, @4e96cfba07): the resource heat/coldness state library that `comp-similar`'s
  superseded-twin scan consumes. It works at the CLI and JSON grain (four states, four tokens, a mutant each). The one thing it
  does not do yet is return a typed state through its library consumer -- the consumer calls the CLI as a subprocess and gets
  an untyped dict (row S29, the issuer's boundary ruling; the consumer half is CE-t-12 work).
- **system** (T-21, 0.8.0_AE_CloudComp~N, engine @2e1102da89): the compiler of the served state -- it compiles
  repository-local cross-surface evidence into `infra/system/06_current_state` and its `--check` reports one of four
  verdicts: current, stale, error, or not-decidable (the 0/2/1/3 check contract its `--help` names). It works: the engine
  self-test prints all four ratified answer-state tokens in one invocation, 45 of 45 pass; the new battery passes 5 of 5
  direct and under pytest; the task order names `--check` as the auto-refresh verdict surface and no hook was changed.
  It is not comp-blast (T-6 owns the blast universe) and it overlaps nothing else on the list. The lane's own caveat:
  its engine commit was LOCAL at the deliverable and the distinct-seat exercise was requested from another seat.

## 5. Is trace just dataflow?

**Answer: no -- and it is not a subset of blast either, which is what the PRD had recorded.** `comp-trace` (T-19,
0.8.0_AE_CloudComp~B, deliverable @bfbff9dc14) traverses a head-pinned working-tree graph of 2,302 nodes with `gold:`,
`lambda:`, `s3:`, `eventbridge:` ids and declares `--exact`, `--all` and direction spellings. `comp-dataflow` (T-7) is a
producer/consumer gate over file writes, a different plane. `comp-blast` answers over the kuzu graph of 27,134 nodes carrying
none of trace's id prefixes, so blast resolves 38.6% of trace's own ids as spelled and 58.2% under the best mapping. On that
measurement the CTO re-adjudicated R-4's conditional word at L2 (PRD v0.6 @7138c4a176): comp-trace is kept, T-19 closed
NOT-RETIRED, and the three trace-only flags were carried into blast under CE-t-6 (@dad11b5207) so nothing was lost either way.

## 6. Where does cache sit against platinum?

**Answer: on a different plane; neither contains the other.** `comp-cache` (T-23, 0.8.0_AE_CloudComp~J, @895b54ef8d) is
React Query cache-key analysis across `portal/src` -- keys, collisions with generated TSX, the audit made zero portal changes.
`comp-platinum` answers the portal-page-to-gold-script plane: which page reaches which gold script. The cache tool's own
identity line says so. Whether platinum's universe is assembled honestly is question 7.

## 7. How is platinum's coverage universe assembled?

**Answer: from the portal's page components outward, one composite of three tools, over a universe of 22 component
files.** `comp-platinum` (T-24, 0.8.0_AE_CloudComp~L, implementation @f7a6772964, LOCAL at the deliverable) is a full-stack
trace from a portal page to a gold script. Its composite is defined as portal component dataflow, then the routing table,
then the firm gold DAG (the pipescript component), under one shared `--budget` carrier. Its coverage universe is the 22
component files under `portal/src/pages`, named by file stem; four `index` stems collide and the tool discloses that as a
named limitation rather than hiding it. Four subcommands: `page` (one component's full-stack trace), `reverse` (S3 key to
routes to components), `tab-audit` (every ADVI tab), `summary` (one line per component with fetch/transform/S3/API-GW
counts). Exercised by a seat other than the builder: `comp-platinum page FactorTilts --budget 0` returned the trace with
the BD firm and bucket, the fetch, and "WITHIN BUDGET: scanned 3 of 3 component" in about three seconds. **What it cannot
yet say, by its own account:** the four-state bar is met two of four ways -- an absent component and a budget-cut run
print their states, but planted PRESENT_WITH_ZERO_RESULTS and NOT_APPLICABLE modes do not exist for this composite, and the
battery has no red mutant per arm; the lane marked T24-AC2 and T24-AC5 UNCOMPUTABLE-BY-CONSTRUCTION under an
implementation-first pace cut and said so on the face. That is the honest state of the coverage tool's own coverage
claim, and it is graded as such at the close.

---

**Pointers per question (the row that answers it):** 1 -> T-4, T-15 · 2 -> T-11 · 3 -> T-12, T-13 (HELD), T-14 · 4 -> T-18,
T-20, T-21 (pending) · 5 -> T-19, T-6, T-7 · 6 -> T-23 · 7 -> T-24 (pending).
