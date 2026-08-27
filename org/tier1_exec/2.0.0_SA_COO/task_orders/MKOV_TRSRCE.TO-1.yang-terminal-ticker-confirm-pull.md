# Task Order: MKOV_TRSRCE TO-1 (v1.1, REPLACES v1.0) -- Yang mechanism question (gates everything else)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-mkov-trsrce-to1-v1.1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MKOV_TRSRCE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <dispatch_state>DISPATCHED 2026-07-07T16:57Z -- REVISED scope per PRD v1.1 (commit 41de08a6b, project JSON 683c092d9). REPLACES the original "confirm ticker symbols + pull 3 tickers' full history" ask -- this is now a QUESTION not an extraction, per DS 0.2.0's new empirical evidence (real ex-date dividend flow, not synthetic smoothing). Likely much faster than v1.0's estimate.</dispatch_state>
    <gate_note>Gates: none (starting point). Effort: Yang-dependent, likely much faster than a full data pull (this is a question, not an extraction).</gate_note>
  </metadata>

  <objective>Answer, don't yet build: how does Yang source/compute the dividend contribution folded into `return` -- gross vs net, from what Bloomberg field or point series? Does his pipeline already have (or can it cleanly add) a net-dividend variant for international indices, or would a net figure require sourcing an entirely different published index?</objective>

  <requirements>
    <requirement id="1">Get a concrete answer routing to one of: (a) apply a net-dividend adjustment to the existing gross figure [cheap, primary path]; (b) source a net-dividend point series Yang already has access to [moderate, primary path]; (c) neither is clean, fall back to sourcing NDDUEAFE directly [heavier, EAFE-only fallback].</requirement>
    <requirement id="2">Confirm as a sanity check on the corrected framing (not a new investigation): does this affect S&amp;P/Russell at all? Expected answer: no, gross==net domestically.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>Concrete path (a/b/c) identified with Yang's confirmation.</criterion>
    <criterion>S&amp;P/Russell domestic-unaffected sanity check confirmed.</criterion>
  </acceptance_criteria>

  <cross_domain_coordination>
    <item>This is the hard gate for MKOV_TRSRCE.TO-2 (implement the dividend-basis fix, EAFE-only, path depends on this TO's answer) -- notify COO on completion so TO-2 can be scoped+GO'd to the right path.</item>
  </cross_domain_coordination>

  <references>
    <ref type="prd">docs/architecture/MKOV_TRSRCE_PRD.md v1.1 SS6 TO-1 (commit 41de08a6b)</ref>
    <ref type="project">org/projects/MKOV_TRSRCE.json</ref>
  </references>
</task_order>
```

<!-- ZOMBIE-RESOLVED 2026-07-13T08:04Z by 2.0.0_SA_COO.
     This TO was <status>pending</status> -- which means DISPATCHED -- while its assignee was
     NOT REGISTERED. Nobody was there. The board read it as ACTIVE work in flight.
     Flipped pending -> staged: `staged` is the TRUE state (scoped, awaiting a GO when a live
     lane exists). NOT flipped to complete -- THE WORK WAS NEVER DONE.
     Detector: .tools/to-liveness-join.py (e8ed4e1d2) -- the join /to-check and fabric-check
     never made. A dispatch into an unverified lane is a hope, not a drive. -->
