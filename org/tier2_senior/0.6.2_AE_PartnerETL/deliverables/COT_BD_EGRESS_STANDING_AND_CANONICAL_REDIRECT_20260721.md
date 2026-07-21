# Andrew-direct: STANDING cot-BD egress + canonical-BD-Lambda redirection

**Recorded by:** 0.6.2_AE_PartnerETL · **Channel:** Andrew-direct, this session (Claude Code terminal)
**Time:** 2026-07-21T213504Z (~17:35 ET / EDT)
**XXX.md compliance:** durable record + broadcast (COO/CTO/MSTR), same turn. VERBATIM below.

## VERBATIM (Andrew, sovereign)

> "You have my word for egress. THis is not going to be a manual pull though. The entire point of this is to
> do it programmatically. What that means is that you need to look at the structure of the existing daily
> cottonwood REST API pull, there are BD API docs in /data/assets/docs and elsehwere that qualify EXACTLY how
> we design Lambdas for BD. We need one of those set up for this exact purpose in the same canonical format."

## What this establishes (surfaced, not adjudicated)

1. **STANDING egress GRANTED** for the programmatic cot-BD Rebalancer daily pull -- this is the standing word
   the scheduled producer was gated on (supersedes the per-use grants @b5af1e929 / @3e563306c which were
   discovery/scoped-read). The daily scheduled pull is now egress-authorized.
2. **DESIGN REDIRECTION (a correction to my mirror choice).** I built the WS-1 producer mirroring
   `opal-assets-bd49f-daily-pull` (a DataMining->xlsx pull). Andrew directs me to instead follow:
   (a) the STRUCTURE of the EXISTING daily Cottonwood REST API pull, and
   (b) the BD API docs in `data/assets/docs` (BD_API_DESIGN.md et al.) that "qualify EXACTLY how we design
       Lambdas for BD",
   and to build this producer "in the same canonical format." -> the canonical BD-REST-Lambda pattern, not
   the bd49f/xlsx mirror.

## Boundaries that still bind

- cot READ-ONLY on the wire; firm-clean (never blackdiamond/49f); cookie/bearer in-memory only.
- Standing egress covers the cot-BD Rebalancer daily pull for THIS producer's purpose. Other vendors/firms
  still need their own word.

## Disposition

Reworking the WS-1 producer to the canonical BD-REST-Lambda format per BD_API_DESIGN.md + the existing cot
REST pull structure. Findings + the reworked producer -> CTO (WS-E PRD owner) + WS-5 (0.7.0) + Andrew.
