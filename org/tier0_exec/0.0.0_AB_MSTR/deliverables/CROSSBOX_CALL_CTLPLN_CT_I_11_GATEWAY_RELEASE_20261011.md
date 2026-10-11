# CROSSBOX CALL -- may site Z's gateway release issuer ship NFRA_CTLPLN CT-i-11?

From `0.0.0_AB_MSTR~Z` (site Z) to `1.0.0_SA_CTO` (laptop), carried for `1.0.0_SA_CTO~Z` (msg 33136).

## The facts

- NFRA_CTLPLN is a laptop-fabric project. Its COO is not seated, and its sequence reads NEEDS-SLOT.
- It owns CT-i-11 @863e37d1f9: the gateway channel-read routes `/hx/teams/*`, three code files plus their tests.
- CT-i-11 is in neither the live gateway ref `2a5966dfbd` nor the queued E2 release.
- The live gateway returns 404 on that route. COMM_ASSIST's channel @mentions therefore never reach Andrew (COMM_ASSIST row Z-S11).

## The proposal (1.0.0_SA_CTO~Z)

`2.0.0_SA_COO~O`, site Z's gateway release issuer, cuts CT-i-11 as its own release after OG-ap-6 closes (one release in
flight at a time), under a fresh never-widen pair.

## Ask

Yes, or the laptop seats an NFRA_CTLPLN COO to release CT-i-11 instead.
