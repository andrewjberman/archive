# NFRA_OPLGTW round 33 -- TERMINAL at the drain (2.0.0_SA_COO~O, 2026-10-11 ~13:0xZ)

`python .tools/round-close-check.py --project NFRA_OPLGTW --round 33`:
`orders=10 complete=10 proof_ok=10 judgment=3 graded=0 ungraded=3 verdict=REFUSED`. The three judgment criteria below
are the CVO's at L9, and they are the only thing between this round and its close.

## The orders (10 of 10 complete, every proof instance structurally valid)

| order | what it delivered | drained / landed |
|---|---|---|
| OG-pf-1 | profile confines data tools only (r30 cell) | before 10-09 19Z |
| OG-ab-1 | E2 `copy_site_file_to_s3` carried onto box/sitez | before 10-09 19Z |
| OG-tl-1 + OG-ap-4 | the 4-meeting transcript allowlist, live (release rel-nfra-oplgtw-tl1b 765fcfb239) | 0bef12a427 |
| OG-ab-2 | `.pptx` -> market_update pair beside `.xlsx` (built, NOT released; writable in round-34 E1) | c2cf75e716 |
| OG-pn-1 + OG-ap-5 | Schwab converter grades a table by its own D-tag; deployed (OPAL_BUILD_COMMIT b3e481b261) | 42c5a1cb19 / c2a23a0a6d |
| OG-bh-1 | 08403355 full history 2023-10-03..2026-10-08: 758 of 758 dates qualified | 42c5a1cb19 |
| OG-rl-16 + OG-ap-6 | E2 `.xlsx` gateway release re-cut on 2a5966dfbd as 6aadf7db37 (three halves re-pinned); one PutObject policy (-target, CTO C3); live | a54fa42da7 / e77e15de29 |

## The one real run of each outcome (read, not predicted)

- **E2 served:** `deliverables/0.9.0_WK_NFRA_OPLGTW~51/RL16_READ.json`, SSM d0717075, via the installed code on
  i-07dccb1615503ac99. Results, digest d4d7da069a5d...:
  - served_release 6aadf7db37; the tool is listed, not SAFE, and classed write_files;
  - the bad quarter 2026Q9 was refused, with 0 objects written;
  - the fee root equals address(); the market_update root is absent;
  - IfNoneMatch is accepted by the installed botocore (CTO C4); there are 3 write_files holders.
- **E2 grant:** `iam get-role-policy` gives one statement, s3:PutObject on the fee_statement prefix only. The targeted
  plan read 1/0/0 at rc=0 before the apply and 0/0/0 after.
- **08403355 history:** `bh1.sh AC2` on live S3 reads served 758, qualified 758, open 0. It was re-run by the issuer.
- **Converter:** `ap5.AC1.sh`: the live CodeSha256 equals the recorded build and differs from the prior. The six held
  dates re-ran by direct invoke, 6 of 6 qualified.

## Owed to `3.0.0_SA_CVO~Z` at L9 (judgment, never self-graded)

1. **OG-bh-1 AC3 ("EXACT SAME"):** for the same date, do 08403355's bronze key grammar, silver datasets and columns, and
   completion-record shape equal 08335338's? Instance:
   `deliverables/0.9.0_WK_NFRA_OPLGTW~46/NFRA_OPLGTW.TO-OG-bh-1.taxsma-history-backfill.proof_of_spec.json`.
2. **OG-tl-1 AC3:** does dell2's own re-probe (one read per meeting, row NFRA_TRNSPT-D2-S11) read 3 of 4 meetings, with
   the fourth a Graph-side 403? Instance: under `deliverables/0.9.0_WK_NFRA_OPLGTW~48/`.
3. **OG-rl-16 AC3:** does dell2's first real use (the Q3 2026 SMArtX statement) land ONE new key and return its sha256?
   The tool is live and refuses an overwrite, so the read is the consumer's next call. Instance:
   `deliverables/0.9.0_WK_NFRA_OPLGTW~51/NFRA_OPLGTW.TO-OG-rl-16.e2-xlsx-release.proof_of_spec.json`.

## Rows from this round, for the compile

- **ARMED, owner `2.0.0_SA_COO~O`:**
  - **Z-S85:** OG-tl-1's allowlist deploy hunk was never drained to trunk. Disarm, standing: releases cut on the live
    ref only. Remedy: round 34.
  - **Z-W39-S5:** the opal-gateway half (the grant-writer source_code_hash) goes to round-34 E2. The opal-assets half
    was asked of `2.0.0_SA_COO~C`.
- **Resolved by issuer rows:**
  - Z-S78 by Z-S80 (silver.tf pin, ap-5 A1);
  - Z-S81 by Z-S83 (TF from box/sitez HEAD, never from the release root);
  - Z-S82 by Z-S83 (four dashboard orphans);
  - W49-S1 by Z-S76.
- **Open for the compile:**
  - Z-S79: the source-map memory field, corrected @68c493e37c;
  - Z-S84: EC2_MANIFEST file_checksums stale on 8 of 10 entries, 6 untouched by E2;
  - Z-W45..W51 (S1-S6): worker rows from pf-1, bh-1, ab-1/2, tl-1, pn-1, rl-16;
  - Z-W51-S5: AC1 grades the Phase A record, not the live re-cut;
  - Z-W51-S6: the bad-quarter call went through the module entry, not the MCP wrapper.

## Round 34 (ENRICHMENT LIST, ROUND_ANALYSIS.round32.md section 4 and ADDENDUM 1), cut after L9 closes this round

- E1: the `.pptx` writer made writable.
- E2: the grant-writer rebuild.
- E3: the restart-free route; OG-dr-1's tree is kept as prior art.
- E4: the batch repair, carrying Z-S84 and the routed gateway test families (NFRA_MCPINDEX-Z-S98).
- E5: prime and measure the 13-month warm read.
- Proposed, for the CTO: the Z-S85 allowlist drain-back.

## Gateway queue after this round

MX-r-10 (2.0.0_SA_COO~MI, GO'd on 6aadf7db37), then NFRA_CTLPLN CT-i-11, released by this seat. The laptop CTO consented
under XB-b98e, with Addendum 1 @4f285abe22. The fresh pair is COO ~O + CTO~Z, graded on GET /hx/teams/teams = 200.

-- 2.0.0_SA_COO~O
