# AMGT_HARVST round 36 -- drain-end packet (L8 input) -- `2.0.0_SA_COO~H`, 2026-10-02 ~06:3xZ

Round-35 analysis @89539ccbc2 -> issuance @fa2be63ade (decomposition section 49), plus three mid-round amendments:
- 49.1 ai-4, CTO 28084;
- 49.2 ai-5, CTO 28222;
- 49.3 ai-6, CTO tick-2 ruling @bb3c328367, a DIRECT ACT with no L8-L10.

5 of 5 L8-bearing orders are terminal. The box rebooted between 04:15Z and 04:55Z, and this seat relaunched at 04:59Z.

## 1. Cells

| cell | result | merged | check at the base |
|---|---|---|---|
| `HVST-ai-1` `~90` | Limb-2a grader per minute with a +/-1 min guard band, 1,440 clean minutes required | @623176e469 | `ai-1.AC2.output.txt` PASS. It reads FAIL by supersession once ai-6 merges. |
| `HVST-ai-2` `~92` | **CANCELLED** (CTO 28235). AC1 PASS 16/16. AC2 FAIL: 3 jobs, 72 of 120 min. The ft session died 74m45s after a sign-in whose hCaptcha Andrew solved by hand (0 vendor calls). No keep-alive page load appears in the run records. The cookie-seed fix (W92-S16) is merged. | records @7463a1fcd4 | -- |
| `HVST-ai-3` `~91` | Capture at load armed on all five publishers, plus the vendor-equivalence test and a status CLI | @f084adea63 | `ai-3.AC2.output.txt` PASS |
| `HVST-ai-4` `~91` | bbg HTML branch in `silver_from_bronze`: the stranded in-tab bbg bodies parse | @3319bb1c60 | `ai-4.AC2.issuer_grade.txt` PASS |
| `HVST-ai-5` `~90` | One `silver_append` per source per upload pass, with bad rows isolated locally (Z-C-S57 amendment @58748baf51) | @6a0a2ebc79 | `ai-5.AC2.issuer_grade.txt` PASS |
| `HVST-ai-6` `~90` | Limb-2a grader per CHALLENGE with a +/-2 min guard band (direct act). A band minute that is unmonitored also voids. Presentations are paired oldest-first with their pass or fail. | @3df5ba2128 | `ai-6.AC2.issuer_grade.txt` PASS |

**ONE REAL RUN of the drain (ai-4 + ai-5).** The per-row upload ran at about 90 s per row, because each row re-read
576 bbg silver parts (69 MB). It was stopped at 05:57:34Z. The batched pass ran from 05:58 to 06:00Z and took 244 due
rows to 0, uploading 243 in one part. 1 row was held on a cross-row conflict; it builds alone and was uploaded alone at
06:01Z. bbg outbox: 830 rows, 829 uploaded, 1 pending (W91-S19).

## 2. Served gold -- rebuild #4 (the last under the signed pair), @65eeb43b35

The act ran at 06:03Z with universe round33 (212 securities). Its gate held; VERIFY read the written parts: mention
gone 0, changed 0, added 4,854; daily gone 0, other 0.

Independent read of served gold after the act:

| table | before | after | by publisher (after) |
|---|---|---|---|
| article_security_mention | 9,521 | **14,375** | sa 10,802, bbg 2,298, wsj 785, ft 449, barrons 41 |
| chatter_daily | 58,088 | **58,300** | +212 rows as of 2026-10-02 |

Rebuilds used: **4 of 4.** Silver keeps growing (the sa and wsj drivers run), and no further gold refresh is
authorised. See section 5, item 1.

## 3. FWD-11 per publisher

| pub | (1) robust auth | (2a) under the ai-1 per-minute grader | (2b) planted fixture |
|---|---|---|---|
| bbg | r33 | INSUFFICIENT on 1,440 min (348 clean); 25 presented, **15 in clean minutes, 15 passed** | **PASS-FIXTURE** (7 captures) |
| wsj | MET (r34) | INSUFFICIENT (431 clean); 0 presented | OPEN (no sample) |
| barrons | MET (r34) | INSUFFICIENT (0 clean); 0 presented | OPEN (no sample) |
| ft | **not met**: ai-2 cancelled | INSUFFICIENT (136 clean); 0 presented | OPEN (no sample) |
| sa | not graded | INSUFFICIENT (53 clean); 0 presented | OPEN (no sample) |

The CTO's tick-2 ruling replaces the 1,440-minute count with a per-challenge +/-2 min band. ai-6 implements it, merged
@3df5ba2128. Its AC2 at the base over the real windows (`ai-6.AC2.issuer_grade.txt`, 06:29Z) reads:

| pub | presented | void | non-void | non-void passed | grader verdict |
|---|---|---|---|---|---|
| bbg | 25 | 16 | 9 | 9 | MET |
| wsj | 0 | 0 | 0 | 0 | MET-BY-ABSENCE |
| barrons | 0 | 0 | 0 | 0 | MET-BY-ABSENCE |
| ft | 0 | 0 | 0 | 0 | MET-BY-ABSENCE |
| sa | 0 | 0 | 0 | 0 | MET-BY-ABSENCE |

These are the GRADER's verdicts. `3.0.0_SA_CVO~Z` grades limb 2a on them; this seat does not. ft's 2a absence sits
beside its limb (1), which is NOT met. ai-1's AC2 now reads FAIL by supersession, as expected.

## 4. Depth (FWD-14) and drivers

| pub | pairs | stored | driver |
|---|---|---|---|
| sa | 35 of 89 | 4,331 | running (relaunched 05:1xZ, pid 31676) |
| wsj | 84 of 89 | 371 | running (pid 26928) |
| bbg | 61 of 89 | 830 (829 in silver) | stopped (STOP_BBG) while the drain ran; restart owed |
| ft | 3 of 89 | 62 | OFF (STOP_FT): ai-2 cancelled |

## 5. Proposed for round 37 (the CTO decides)

1. **Gold refresh after 4 of 4.** Either a new signed pair for further ad-hoc rebuilds, or gold made a scheduled
   producer. CLAUDE.md requires production pipelines to be scheduled; an ad-hoc run is QA.
2. **FWD-11 ft limb (CTO 28235):** one 2 h run started from a hand-solved sign-in while Andrew is present, proving
   the keep-alive fires once per page load.
3. **W91-S19:** one bbg body (`TD7VMGKGCTIZ00`) whose nested `duration` mixes int and str. Options are a coercion
   cell or accepting 1 stranded article of 830.
4. **(2b) for wsj, barrons, ft and sa:** no challenge has been presented at load, so no sample exists.
5. **Restart the bbg driver** (it stayed stopped through the drain) and run a barrons driver.

## 6. Rows this round

- New: Z-S58 (O(n^2) drain); Z-W90-S11; Z-W92-S15, S16, S17; disarm rows Z-S59 to Z-S62.
- CVO rows: Z-C-S57 (ADJUDICATION_v46).
- Disarmed by Z-S59 to Z-S62: Z-S57, Z-S58, Z-W91-S19 and Z-C-S57.
- Carried: Z-S56 (ft hold) is closed out by the ai-2 cancel.
