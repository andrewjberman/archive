# NFRA_OPLGTW round 2 -- rulings on the six cut questions

By `1.0.0_SA_CTO~O`, 2026-09-28 ~21:1xZ, on `2.0.0_SA_COO~O`'s
`deliverables/2.0.0_SA_COO~O/ROUND2_CUT_QUESTIONS_20260928.md` @d9cc0bbcdc (msg 26212).

| # | Ruling |
|---|---|
| Q1 | ADOPTED, with one addition. Machine and bearer callers (the MS-ingest identity, `token_broker.py:192`) are named OUT of R-3's scope under R-3(f) in t-1's first criterion. t-1 also carries a test that neither path reaches `resolve_tier` as a person, so "they do not pass through it" is a measured claim and not a reading. t-2's 14-day pre-read shows 0 tier deltas for them too. |
| Q2 | ADOPTED. `identity_scope.py` and `query_v0.py` are named out of scope in t-1. W3-S9 stays ARMED on those two, owner `2.0.0_SA_COO~O`, and becomes a round-3 enrichment item. |
| Q3 | AMENDED ~21:2xZ by this seat, superseding the first text: NO kind row. `name()` refuses `eip` correctly. `aws_eip` has no name argument, so its identity is AWS-issued (allocation id, public IP), and `org/standards/NAMING_SCHEMA.json` v1.12 `not_covered` lists both "AWS-issued identifiers" and "tag keys and values". `aws_eip` also sits in neither `tf_type_map` nor `tf_unmapped_own_name`, so the naming gate never grades it. Rule 30 therefore has no name to build: n-1 declares the EIP and its association with NO hand-typed Name tag, and no builder call (build ladder rung 1). n-1 applies TARGETED to the EIP and its association through `safe-apply`, so no unapplied NFRA_MCPORTAL resource rides along. It is cut after MP-a-1's build. |
| Q4 | ADOPTED. E4 is the seal plus the offline grade. FWD-2's live exercise is the COO's one real run at close (rule 22), through the E1 walkthrough identity. It is not a worker criterion. |
| Q5 | ADOPTED. 09-11..09-17 stays as R-OG-23A's baseline, plus one post-release window of equal length ending at the cut. Both are printed with their request counts. |
| Q6 | HELD on Andrew. A fresh venv built from the gateway's requirements file is a PyPI download, which is egress off Opal infrastructure. His G-MOTO yes (~20:4xZ, @f8d1103a38) names NFRA_OPALAI's one pinned `moto` install and does not stretch to this. Recommendation to Andrew: yes, one venv from the pinned requirements file, into a scratch path, for E10's suite only. Until his word, E10 is cut with its suite criterion HELD on that gate. |
