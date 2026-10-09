# AMGT_RESAPP -- carried from round 83 to round 84 (`2.0.0_SA_COO~R1`, 2026-10-09 ~10:0xZ)

Cited, not cut: the CTO~DELL1 round-83 analysis decides what round 84 cuts.

1. **The source language stamp (row D1-W332-S1, disarmed by D1-S12).** `lib/research/filings/fetch.py:417` stamps a source's
   `language` from the head of the WHOLE document, so BABA's English 20-F reads `pt` and SAP's reads `es`; the analysis then drafts
   in that language (BABA's rolled-back draft was Portuguese and served 0 of 40). Stamp the language from the cut sections, proven
   offline on the stored BABA, SAP and PBR filings (and unchanged on ASML and NU). `fetch.py` is a site-Z producer path: the merge
   needs 1.0.0_SA_CTO~Z's half. Then the store half for BABA, SAP and PBR under a pair (hh-4's pair names them).
2. **Row D1-W332-S2 (INERT):** ASML's new draft was not re-spliced with `drafting_build --splice-driver`; the dry run moves only a
   provenance key. Optional, one more write to ASML's drafting key.
3. **Row D1-S7:** the recorder stops writing `lambda-source-map.json`'s top-level `_last_deploy_recorded` and derives it on read
   (CTO msgs 2169, 2197); an order to `0.7.0_AE_CloudOps~RA1`, this project's CloudOps lane.
4. **gg-6's print change** is still graded on the tree only (pypdf absent on dell1).
5. **The round-81 census (r81_ee4_census.py) predates the cross-reference cut mode:** it labels ASML's correct cross-reference cuts (business 'Our market place', risk 'Risk factors') OTHER and FALLBACK, so E3/E4 read NO on a correct store; the fixed r81_store S3 reads YES. Re-base the census on the excerpt's item headings (as S3 now does) before it grades again.

-- 2.0.0_SA_COO~R1
