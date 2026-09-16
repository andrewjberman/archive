# AMGT-rj-6 -- the five model runs, stdout verbatim

`0.9.0_WK_AMGT_RESAPP~20`, 2026-09-15. One run per QA filing; each is the criterion's own
literal invocation, recorded byte-for-byte including its PIPE-RC where one was captured.
The usage table for every vendor call (13 of them, including the one lost to the 115 s
timeout and the sub-cent parameter probe) is MEASUREMENTS.md section 1.

## RUN 1 -- BA_US_Equity (10-K), AC2

Invocation, byte-for-byte:

```
timeout 115 python -m lib.research.filings.analyze --security-key BA_US_Equity --write-pool 2>&1 | tail -14
```

Output:

```
SOURCE: BA_US_Equity form 10-K accession 000162828026004357 filed 2026-01-30 url https://www.sec.gov/Archives/edgar/data/12927/000162828026004357/ba-20251231.htm document_sha256 5e6dd009813c7851c73c30eb8a1117eab36e86a8c64bde61ad3af5444b052501 excerpt_sha256 fe06b00c795ad58f99376a405c7b1431f861d53d5b301801fc55f894ee041e84 retrieved_at 2026-09-15T09:00:29Z parser_version opal-filings-fetch/1.0.0 excerpt_chars 137314 provenance pool
PASS1: model claude-opus-5 input_tokens 56427 output_tokens 6397 seconds 65.2 USD 0.4421 citations 97 resolved 97 cached true
PASS2: model claude-opus-5 input_tokens 6068 output_tokens 6767 seconds 60.4 USD 0.1995 items_source pass-2
PASSAGE_MAP: 276 passages from 2 item(s) Item 1A. Risk Factors; Item 7. Management's Discussion and Analysis
ITEMS: guidance 14 segments 11 risks 23 commentary 16 big_bets 9 big_challenges 12 total 85 cited 85 (100.0 percent) held_uncited 0
THESIS_DRIVER: series BCA commercial aircraft deliveries (with 737 monthly production rate) | unit aircraft delivered per year (and per month) | source_passage_id P0111 | resolution cited
DRAFTING: sections 5 sentences 38 dropped 2 verbatim_PASS 38 evidence_records 88
USD: total 0.6416 (pass1 0.4421 + pass2 0.1995) tokens in 62495 out 13164 seconds 125.6
OK: uploaded s3://opal-data-harvest/filings/v1/BA_US_Equity/000162828026004357.source.json ContentLength=149333 document-sha256=66c6ee2d6d94b09bb5566f7ed4843df602fb6ec67a97bacab04ee89c6c84e03c read-back=verified
OK: uploaded s3://opal-data-harvest/filings/v1/BA_US_Equity/000162828026004357.analysis.json ContentLength=274144 document-sha256=d09d4375b9beee602d2b7dc2e546e270db13e123698b914b62e6768c16649ef3 read-back=verified
OK: uploaded s3://opal-data-harvest/drafting/v1/BA_US_Equity.json ContentLength=109540 document-sha256=684197b8861424f99eec4c5a643668c2a7801cc9001ed223b54ff366053f7d81 read-back=verified
PIPE-RC=0

-- THE FIRST RUN OF THIS EXACT INVOCATION, RECORDED VERBATIM (row AMGT_RESAPP-Z-W20-S1):
Terminated                 timeout 115 python -m lib.research.filings.analyze --security-key BA_US_Equity --write-pool
PIPE-RC=124
-- and the split the criterion's own expect names, run once between them:
timeout 200 python -m lib.research.filings.analyze --security-key BA_US_Equity --stage pass1
PASS1: model claude-opus-5 input_tokens 56427 output_tokens 6397 seconds 65.2 USD 0.4421 blocks 173 cached false cache .scratch\filings_cache\pass1\BA_US_Equity.000162828026004357.rj6-two-pass-1.json
PASSAGE_MAP: 276 passages from 2 item(s) Item 1A. Risk Factors; Item 7. Management's Discussion and Analysis
real 1m6.671s
```

Denominator: 1 of 1 filing (BA_US_Equity); 85 of 85 items resolved to a passage (100.0 percent, floor 90); 276 passages; 38 of 38 served sentences verbatim-PASS, 2 dropped of 40 drafted; 3 of 3 pool keys uploaded and read back

---

## RUNS 2 and 3 -- COST_US_Equity (10-K) and SAP_GY_Equity (20-F), AC3

Invocation, byte-for-byte:

```
for k in COST_US_Equity SAP_GY_Equity; do timeout 115 python -m lib.research.filings.analyze --security-key $k --write-pool 2>&1 | grep -E "SOURCE|ITEMS|THESIS_DRIVER|DRAFTING|USD|uploaded|UNRESOLVED" | cut -c1-200; done
```

Output:

```
SOURCE: COST_US_Equity form 10-K accession 000090983225000101 filed 2025-10-08 url https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm document_sha256 2cf71f4336c8f36b0
PASS1: model claude-opus-5 input_tokens 28396 output_tokens 5425 seconds 57.0 USD 0.2776 citations 89 resolved 89 cached true
PASS2: model claude-opus-5 input_tokens 5206 output_tokens 5859 seconds 53.2 USD 0.1725 items_source pass-2
ITEMS: guidance 8 segments 10 risks 25 commentary 18 big_bets 9 big_challenges 11 total 81 cited 81 (100.0 percent) held_uncited 0
THESIS_DRIVER: series Comparable sales excluding foreign-currency and gasoline price impacts | unit percent change year over year | source_passage_id P0080 | resolution cited
DRAFTING: sections 5 sentences 35 dropped 3 verbatim_PASS 35 evidence_records 71
USD: total 0.4501 (pass1 0.2776 + pass2 0.1725) tokens in 33602 out 11284 seconds 110.2
OK: uploaded s3://opal-data-harvest/filings/v1/COST_US_Equity/000090983225000101.source.json ContentLength=75336 document-sha256=4779a227fa98c0b636151bc85ab0bba9c5037f49e0d5d8b8dcbe8818d3cb2a97 read-b
OK: uploaded s3://opal-data-harvest/filings/v1/COST_US_Equity/000090983225000101.analysis.json ContentLength=174095 document-sha256=1ad9ee2aca1e82cfc59bb900a6685226343b6b2cc9d9c28fa115122bb32cf926 rea
OK: uploaded s3://opal-data-harvest/drafting/v1/COST_US_Equity.json ContentLength=88475 document-sha256=8951faf3b6bd971b4afac9c3b18b7657301dcea1a7eca3a7fef37d59ccc5885b read-back=verified
SOURCE: SAP_GY_Equity form 20-F accession 000110465926020058 filed 2026-02-26 url https://www.sec.gov/Archives/edgar/data/1000184/000110465926020058/sap-20251231x20f.htm document_sha256 95017d7d5ea133
PASS1: model claude-opus-5 input_tokens 50507 output_tokens 6227 seconds 64.0 USD 0.4082 citations 92 resolved 86 cached true
PASS2: model claude-opus-5 input_tokens 5693 output_tokens 6489 seconds 59.3 USD 0.1907 items_source pass-2
ITEMS: guidance 6 segments 11 risks 22 commentary 18 big_bets 10 big_challenges 11 total 84 cited 78 (92.9 percent) held_uncited 6
THESIS_DRIVER: series Current cloud backlog growth at constant currencies | unit percent year-over-year | source_passage_id P0091 | resolution cited
DRAFTING: sections 5 sentences 36 dropped 0 verbatim_PASS 36 evidence_records 70
USD: total 0.5989 (pass1 0.4082 + pass2 0.1907) tokens in 56200 out 12716 seconds 123.3
OK: uploaded s3://opal-data-harvest/filings/v1/SAP_GY_Equity/000110465926020058.source.json ContentLength=165630 document-sha256=51c0ade3c88bb1e956f0674b4cb1b8da2fe5e1c65063cc70cf9c5a8e09709f3c read-b
OK: uploaded s3://opal-data-harvest/filings/v1/SAP_GY_Equity/000110465926020058.analysis.json ContentLength=247733 document-sha256=1c26778bcf8fec455f05042329e9436d825507548f19403bf3982700cecf4aaa read
OK: uploaded s3://opal-data-harvest/drafting/v1/SAP_GY_Equity.json ContentLength=84313 document-sha256=0a6f94839caf954fcf66df7b378809b4ec4c253ea912f34be388a4f5a7c1eb52 read-back=verified
```

Denominator: 2 of 2 filings; COST 81 of 81 cited (100.0 percent, floor 90 at 50 items); SAP 78 of 84 cited (92.9 percent, floor 85 at 30 items) with 6 held; 6 of 6 pool keys uploaded

---

## RUNS 4 and 5 -- HD_US_Equity (10-K) and BABA_US_Equity (20-F), AC4, with the pool listings

Invocation, byte-for-byte:

```
for k in HD_US_Equity BABA_US_Equity; do timeout 115 python -m lib.research.filings.analyze --security-key $k --write-pool 2>&1 | grep -E "SOURCE|ITEMS|THESIS_DRIVER|USD|uploaded|UNRESOLVED" | cut -c1-200; done; .tools/aws s3api list-objects-v2 --bucket opal-data-harvest --prefix filings/v1/ --query "length(Contents)" --output text; .tools/aws s3api list-objects-v2 --bucket opal-data-harvest --prefix drafting/v1/ --query "Contents[].Key" --output text | tr "\t" "\n" | cat
```

Output:

```
SOURCE: HD_US_Equity form 10-K accession 000162828026019436 filed 2026-03-18 url https://www.sec.gov/Archives/edgar/data/354950/000162828026019436/hd-20260201.htm document_sha256 7a108cae33600d3ebc1ea
PASS1: model claude-opus-5 input_tokens 39204 output_tokens 5499 seconds 55.7 USD 0.3335 citations 81 resolved 81 cached true
PASS2: model claude-opus-5 input_tokens 5203 output_tokens 5873 seconds 51.3 USD 0.1728 items_source pass-2
ITEMS: guidance 10 segments 10 risks 21 commentary 16 big_bets 10 big_challenges 12 total 79 cited 79 (100.0 percent) held_uncited 0
THESIS_DRIVER: series Comparable sales (with its components, comparable average ticket and comparable customer transactions) | unit percent change year over year | source_passage_id P0101 | resolution
USD: total 0.5063 (pass1 0.3335 + pass2 0.1728) tokens in 44407 out 11372 seconds 107.0
OK: uploaded s3://opal-data-harvest/filings/v1/HD_US_Equity/000162828026019436.source.json ContentLength=111968 document-sha256=4b5c2972cbce6b70fd833444b55ca93be2554c56e9eff5db6f701f882495c8d9 read-ba
OK: uploaded s3://opal-data-harvest/filings/v1/HD_US_Equity/000162828026019436.analysis.json ContentLength=201980 document-sha256=2f73a6c10e774b1d0db22036f698ff26106a711c0ba6f4fbdd8202db2b5ec1bd read-
OK: uploaded s3://opal-data-harvest/drafting/v1/HD_US_Equity.json ContentLength=99745 document-sha256=84d36bb24bf76d3a87db67680dd20d0e44318578666ae98862157239d5b64356 read-back=verified
SOURCE: BABA_US_Equity form 20-F accession 000119312526231755 filed 2026-05-20 url https://www.sec.gov/Archives/edgar/data/1577552/000119312526231755/baba-20260331.htm document_sha256 7be73cb49925934f
PASS1: model claude-opus-5 input_tokens 59005 output_tokens 6848 seconds 72.8 USD 0.4662 citations 86 resolved 86 cached true
PASS2: model claude-opus-5 input_tokens 6414 output_tokens 7185 seconds 65.0 USD 0.2117 items_source pass-2
ITEMS: guidance 10 segments 11 risks 23 commentary 17 big_bets 9 big_challenges 10 total 80 cited 80 (100.0 percent) held_uncited 0
THESIS_DRIVER: series Cloud Intelligence Group revenue (and its adjusted EBITA) | unit RMB millions per fiscal year | source_passage_id P0249 | resolution cited
USD: total 0.6779 (pass1 0.4662 + pass2 0.2117) tokens in 65419 out 14033 seconds 137.8
OK: uploaded s3://opal-data-harvest/filings/v1/BABA_US_Equity/000119312526231755.source.json ContentLength=196087 document-sha256=8f96cefbffde2b042747c63e8dc089ddabca373eb529ac41fbae5b18c28a53cf read-
OK: uploaded s3://opal-data-harvest/filings/v1/BABA_US_Equity/000119312526231755.analysis.json ContentLength=282846 document-sha256=2fd958447e888c2dfa06ccbcd68ad91100ba1d6968ad7307da6a007d177dd2c7 rea
OK: uploaded s3://opal-data-harvest/drafting/v1/BABA_US_Equity.json ContentLength=102534 document-sha256=02ff40b5add370ba4ad39d132f8d2998a2ac3280a7d1c06592830b22a928cc90 read-back=verified
10
drafting/v1/BABA_US_Equity.json
drafting/v1/BA_US_Equity.json
drafting/v1/COST_US_Equity.json
drafting/v1/HD_US_Equity.json
drafting/v1/SAP_GY_Equity.json
```

Denominator: 2 of 2 filings; 10 of 10 expected objects under filings/v1 (5 names x source + analysis); 5 of 5 expected keys under drafting/v1; 0 names UNRESOLVED-SOURCE of 5

---

## The served BA drafting object, read back from the pool (AC5)

```
.tools/aws s3api get-object --bucket opal-data-harvest --key drafting/v1/BA_US_Equity.json .scratch/rj6.drafting.json --query ContentLength --output text; python -c "import json,io,jsonschema; d=json.load(io.open('.scratch/rj6.drafting.json',encoding='utf-8')); s=json.load(io.open('lib/research/drafting/schema.json',encoding='utf-8')); jsonschema.validate(d,s); ids={r['id'] for r in d.get('evidence_records',[])}; ss=[q for x in d['sections'] for q in x.get('sentences',[])]; print('schema-valid True sections', len(d['sections']), 'evidence_records', len(ids), 'sentences', len(ss), 'all-ids-resolve', all(all(e in ids for e in q.get('evidence',[])) for q in ss), 'with-evidence', sum(1 for q in ss if q.get('evidence')), 'generated-true', sum(1 for q in ss if q.get('generated') is True), 'verbatim-PASS', sum(1 for q in ss if q.get('verbatim_check')=='PASS'), 'dropped', d.get('dropped'), 'thesis_driver', json.dumps(d.get('thesis_driver'))[:160])"
```

```
109540
schema-valid True sections 5 evidence_records 88 sentences 38 all-ids-resolve True with-evidence 38 generated-true 38 verbatim-PASS 38 dropped 2 thesis_driver {"series": "BCA commercial aircraft deliveries (with 737 monthly production rate)", "unit": "aircraft delivered per year (and per month)", "source_passage_id":
```


---

# AMENDMENT 1 RE-RUN -- 2026-09-15 ~11:4xZ, branch wk-amgt_resapp-11-3 @04b59f883c

The issuer (`2.0.0_SA_COO~W`) amended AC6's task-query invocation at `04b59f883c` on rows
`AMGT_RESAPP-Z-W20-S2` and `W20-S3`: the `MSYS_NO_PATHCONV=1` prefix and `/V` were added, the
expectation was left unchanged. AC6 was re-run as now written and AC7 was re-run because it reads
committed history and the working status, both of which moved with the drain at `f8b3475c87` and
the branch fast-forward. AC1-AC5 were NOT re-run: their criterion text did not move, and re-running
AC2-AC4 would spend five more model runs beyond the cell's five-run bound. Nothing was rebuilt.

## AC6 -- the batch dry run and the task query, AMENDED invocation (rc 0, under timeout 120)

```
python -m lib.research.filings.batch --universe universe/v1/2026-09-15.json --dry-run 2>&1 | tail -5; MSYS_NO_PATHCONV=1 schtasks /Query /TN OpalResearch-FilingsAnalyzer /FO LIST /V 2>&1 | tr -d "\r" | grep -E "TaskName|Status|Schedule Type|Scheduled Task State" | cat
```

```
BATCH: universe s3://opal-data-harvest/universe/v1/2026-09-15.json as_of 2026-09-15 names 256 with_filing_identity 12 would_fetch 12 unresolved_source 244 limit none
WOULD-FETCH: ASML_NA_Equity(20-F cik 937966), BABA_US_Equity(20-F cik 1577552), BA_US_Equity(10-K cik 12927), COST_US_Equity(10-K cik 909832), HAL_US_Equity(10-K cik 45012), HD_US_Equity(10-K cik 354950), INTU_US_Equity(10-K cik 896878), KMB_US_Equity(10-K cik 55785), NU_US_Equity(20-F cik 1691493), PBR_US_Equity(20-F cik 1119639), SAP_GY_Equity(20-F cik 1000184), VLO_US_Equity(10-K cik 1035002)
UNRESOLVED-SOURCE: 244 name(s), each an explicit object at filings/v1/<security_key>/UNRESOLVED-SOURCE.source.json
DRY-RUN: nothing fetched, no model call, no pool write, no task run. 12 of 256 name(s) would be analyzed.
TaskName:                             \OpalResearch-FilingsAnalyzer
Status:                               Disabled
Scheduled Task State:                 Disabled
Schedule Type:                        Weekly
```

DENOMINATOR: limb 1 -- 256 names in the universe, 12 with a filing identity, 12 would-fetch, 244
UNRESOLVED-SOURCE, 0 fetched / 0 model calls / 0 pool writes. limb 2 -- 4 of 4 named fields returned
(TaskName, Status, Scheduled Task State, Schedule Type), against 0 of 4 as originally written. The
world-state did not move: the task was Weekly and Disabled at the first pass and is Weekly and
Disabled now; what changed is that the criterion's own invocation now produces the result it names.

Corroboration, limb 2 alone at the top level with no `bash -c` wrapper, rc 0, same 4 of 4 fields:

```
env MSYS_NO_PATHCONV=1 schtasks /Query /TN OpalResearch-FilingsAnalyzer /FO LIST /V
TaskName:                             \OpalResearch-FilingsAnalyzer
Status:                               Disabled
Scheduled Task State:                 Disabled
Schedule Type:                        Weekly
```

## AC7 -- history, ASCII, no raw secret read, clean status (rc 0, under timeout 120)

```
a536333c92 0.9.0_WK_AMGT_RESAPP~20 fix(AMGT_RESAPP AMGT-rj-6, AC7): the docstring that promised no raw secret read spelled the token it prom
8abfd829a7 0.9.0_WK_AMGT_RESAPP~20 build(AMGT_RESAPP AMGT-rj-6, F-1 + D-1): the filings analyzer -- two passes, every cited claim resolved t
6093d06a0e 0.9.0_WK_AMGT_RESAPP~3 L7(AMGT_RESAPP.TO-AMGT-s-9, 0.9.0_WK_AMGT_RESAPP~3): THE DRAFTING FACE -- every machine sentence marked an
files 11 nonascii 0 raw-secretsmanager-reads 0 lambda-or-terraform-files 0
```

DENOMINATOR: 2 of the 4 most recent commits on the two packages are this serial's (`git log -4`
returns 3 commits for these paths; the third is the pre-existing AMGT-s-9 history); 11 of 11 package
`.py` files at 0 non-ASCII; 0 raw secret reads of 11 files; 0 dirty paths of 2 directories --
`git status --porcelain` on both packages printed NOTHING. Output identical to the first pass.

VERDICT: AC6 PASS-by-output on the amended invocation; AC7 PASS-by-output at the new tip; the
instance re-graded VALID (rc 0) by this worktree's own `.tools/proof-of-spec-check.py` on
AC1,AC2,AC3,AC4,AC5,AC6,AC7. No new surprise row: nothing had to be done that the amended order did
not say, and nothing it said could not be done.
