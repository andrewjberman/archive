# NFRA_COMPEFFICACY -- CE-q-1, Andrew's seven questions answered in writing (draft v1, round 6 tranche 1)

**Author:** `3.0.0_SA_CVO` (the CVO authors, the CTO lands the section in the PRD -- decomp CE-q-1, FWD-5). **Written:**
2026-09-03 18:0xZ. **Bar (FWD-5 ACCEPT):** for each question in his message there is an answer in plain English that says what
the thing actually does, and where he asked "is this just X?" the answer says yes or no and why; each answer points at the
row that answers it and is disputable by him. **State:** five of seven answered from completed orders; two wait for tranche 2
(T-21 comp-system, T-24 comp-platinum). Every fact below is the named deliverable's measurement, read by this seat; nothing
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
- **system** (T-21, 0.8.0_AE_CloudComp~N): *pending tranche 2.*

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

*Pending tranche 2 (T-24, 0.8.0_AE_CloudComp~L).* The answer will say what population platinum enumerates (pages, routes,
gold scripts), from which artifacts, with what denominator, and what it cannot see -- the s.4.3 four-state bar applied to a
coverage tool.

---

**Pointers per question (the row that answers it):** 1 -> T-4, T-15 · 2 -> T-11 · 3 -> T-12, T-13 (HELD), T-14 · 4 -> T-18,
T-20, T-21 (pending) · 5 -> T-19, T-6, T-7 · 6 -> T-23 · 7 -> T-24 (pending).
