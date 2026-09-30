# AMGT_HARVST ROUND 14 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~07:4xZ

**Issuance:** `278c53f472` (one order over `ROUND_ANALYSIS.round13.md` @`f1de5ca7ce`; decomp section 26).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Close run:** `c-1` AC1 re-run on the trunk after the drain (same verdict).

## 1. ONE ORDER, TERMINAL, VALID

`HVST-c-1` (`~40`, LOCAL), drained `16011327b7` (audited: landed 10 = branch 10). Read-only; no served move, no vendor.

## 2. WHAT THE HELD-OUT READ FOUND

- **Held-out denominator:** 130 of 263 mention rows over 50 securities are outside the five tuned securities (44 tier-A/B
  rows over 24 securities); the newest capture is 2026-09-15, so nothing postdates the rule.
- **The rule forms 0 held-out events.** So **the held-out pass is NOT a precision grade, and the round-13 pass stays
  IN-SAMPLE** -- stated on every surface the cell wrote, and here.
- **Recall:** under the rule's own grouping, 0 held-out stories with >= 2 tier-A/B articles failed to qualify. A worker
  supplement (the rule never forms a story without a tier-A article) finds **6 tier-B-only clusters** -- AMZN x2 (one is 3
  articles, 09-06..09-10, on the Miami cargo-plane crash), DELL, INTC, MSFT, QCOM (four on Nvidia's PC push, seen from
  other companies). Presented for L9, no verdict.
- **Burst-shape census:** the larger shape (>= 5 articles over >= 2 days, one story) is **UNEXERCISED** at story level
  (53 story-runs; 6 exceed 3 articles or 1 day, all in-sample, none reaches 5-over-2). **No held-out pass stands for that
  shape.** A looser any-tier-A/B-day unit shows 3 runs of the larger shape, none held-out, all chaining unrelated stories
  (an upper bound; the worker names the unit choice in row `Z-W40-S3`).

## 3. THE FIXTURE (MECHANISM TEST, NOT A GRADE) -- and the defect it found

- **Variant 1, the story is a security's ONLY coverage:** the rule forms **0 events** -- its name-detection step reads the
  story's own recurring words ("quantum", "battery", "plant") as the security's NAME and strips them, so the paraphrased
  headlines share no term. **Row `Z-W40-S1` (ARMED, disarm owner this seat): a recall loss on a security's FIRST
  single-story burst.** No security in today's harvest has that shape, so nothing served is wrong today.
- **Variant 2, the same story among other coverage:** one story of six articles; the event spans only the two qualifying
  days (a third day with one tier-A publisher falls outside) -- the rule as written (row `Z-W40-S2`, INERT).

**`Z-W40-S1` DISARMED BY SPECIFICATION (this seat, same turn):** latent until a new security's first burst lands; the
remedy is a round-15 candidate for the CTO -- name detection must not strip a word that appears in only ONE story of the
security (a name recurs ACROSS stories; a story's words recur within it). Until that lands, any cell that onboards a new
security or grades events for one must read `Z-W40-S1` first.

## 4. JUDGMENT FOR L9 (presented, not graded)

`c-1` AC4: (1) held-out events -- none; (2) the 6 near-miss clusters with every headline. **Is any of them a real burst of
coverage about its own company that the rule declined?** (The Nvidia-PC clusters on DELL/INTC/MSFT/QCOM are the same
co-mention shape round 9 removed; the AMZN crash cluster is tier-B only.)

## 5. ROWS -- the gate's own fold: 94 ids, GRADUATED 56, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 13 (26 files)

New: `Z-W40-S1` (ARMED, disarmed by specification above), `Z-W40-S2`, `Z-W40-S3` (INERT). Carried with named owners:
`Z-S37` (the tool's authoring lane), `Z-W37-S4` (the account holder), `Z-W39-S1` (disarmed by condition, round-13
analysis). **Armed rows with an owner this seat could not seat: NONE.**

## 6. FOR THE ROUND-15 CUT (the CTO decides)

1. `Z-W40-S1`'s fix (cross-story name detection), with a fixture as its criterion and a held-out re-read.
2. The held-out read can only become a precision grade when held-out EVENTS exist: that needs new captures (the sa 402
   blocks sa; bbg is unplannable) or new securities with bursts -- so it is bounded by the vendor state, not by a cell.
3. Unchanged: the portal push (Andrew's hold), the Seeking Alpha 402 (the account holder).

## 7. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing, and cuts no round-15 cell.
