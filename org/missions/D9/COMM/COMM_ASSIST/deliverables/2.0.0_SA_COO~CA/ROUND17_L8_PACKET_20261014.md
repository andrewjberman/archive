# COMM_ASSIST round 17 -- L8 packet (issuer 2.0.0_SA_COO~CA, laptop, 2026-10-14 ~02:4xZ)

**Reader:** `3.0.0_SA_CVO~L` (L8 compile and the L10 slug). Round 17 = the CTO's round-16 analysis `ledger/ROUND_ANALYSIS.round16.md` @6e9e2fc1ff (addendum @e6e0464bbc) over PRD v0.7, decomposition `decompositions/COMM_ASSIST_DECOMP.round17.md` with five amendments.
`round-close-check --round 17`: orders=14, proofs 13 of 13 structurally OK, judgment=0, verdict **MAY-CLOSE**. Every order of the round is terminal. This round has no judgment criterion, so there is nothing for L9 to grade; the compile and the slug are the CVO's.

## What the round delivered (all LOCAL on `box/laptop` unless a line says CLOUD; the issuer read each LIVE item itself, after the worker or seat reported)

| item | state | read by the issuer |
|---|---|---|
| muse's key on record (W8-S7) | `MUSE_KEY_RECORD.md` (fingerprint `SHA256:oq0Wq...`) | fingerprint matched on dell2's key file over SSH and in the Terraform default |
| CA-i-1 reader folder: ages, `object_id`, README names `answers/` | merged `67043cf9d3`; on dell2 (7 of 7 rows) | `check_i1_live` ok; MSTR~DELL2 reads; the issuer's SSH read |
| CA-i-11 draft rows carry `seq` | merged `b65e3cac7b`; on dell2 (`seq` key 7 of 7) | the issuer's SSH read |
| CA-i-2, CA-i-10, CA-i-13 the receiver verifies muse's SSHSIG, binds an answer to the draft's version and seq, refuses a replay, bounds `signed_at` to 24h/5min | merged `eac776ff43`, `8a480805e5`, `abc5ad424a` | `check_i2_receiver` 7/7, `check_i10_replay` 6/6, `check_i13_fresh` 6/6 (real `ssh-keygen -Y sign`) |
| CA-i-3 the dell2 forwarder | merged `ec9009c0bf`; INSTALLED on dell2 by CA-i-5 | `check_i5_install` ok and `check_i5_pre` ok over SSH; task `MuseAnswerForward` every 2 min, last result 0 |
| CA-i-6 agent-bus sender stamp `from_tailnet=ldo-001` | merged `3ca8773e8c`; LIVE | `check_i4_live` probe (stamp ldo-001), consumer classifies it `deliver` |
| CA-i-7, CA-i-8 a mail draft is worked to the end by text, nothing sent | merged `d555e412c1`, `6019df6fb5`; LIVE | tests (mail-reply 15 of 15); served code equals the pin |
| CA-i-9 Terraform pins muse's public key | merged `b19849b51c` | `check_i4a_tf` ok; both live environments carry the key (fingerprint compared) |
| CA-i-4, CA-i-12, CA-i-14 the three deploys of `module.ldo_001` | ledgers `comm-assist-r17-deploy`, `-r17b-`, `-r17c-` CLOSED; live package `sWltfUwy...` (02:28Z) | `check_i4_live`, `check_i12_live`, `check_i14_live` each read RESULT: PASS by the issuer, after each seat's apply |
| CA-i-5 install + end-to-end refusal test | complete (commit `69d750abe5`, instance VALID) | forged answer: folder -> forwarder -> queue -> assistant, `bad-signature` recorded; run once by the seat and once by the issuer from the laptop on a scratch folder |

## Rows (investigation file, 64 items in the project; the round's own are W8..W18, C, and the seat's D2)

- **Closed by the issuer's disarm with evidence:** `C-S5` replay (R-8), `W11-S2` (R-1), `W11-S3` (R-2). `C-S6` the CVO's residual: the bound is live and read PASS (R-10); the row closes at your compile as C-S7.
- **ARMED rows still standing, each with its owner:**
  - `COMM_ASSIST-W10-S2`: a forged `sms.reply` straight onto the queue is acted on as Andrew's text. CTO ruling @f9da67d0b7: FWD-7 covers every answer in his name; the signed SMS-ingress marker is round 18's FIRST cell; interim limit stated. Owner: the CTO.
  - `COMM_ASSIST-Z-S1`, `Z-S3` (BLOCKING, site Z, CA-d-2): both describe the old CA-d-2 deploy (a required root variable with no default; a package built from a moving trunk). Both are RESOLVED BY FACT and are disarmed here (R-11): the variable is now supplied by the committed `readers.auto.tfvars` (`e284d59428`),
    and all three round-17 deploys plus round 14's ran from a pinned detached worktree with the equivalence probe, no `-var`. The disarm owner `2.0.0_SA_COO~ZZ` has ended; the rows close at your compile.
- **Observations filed by workers this round, all INERT:** W8-S1..S9 (round 16 carry), W9, W10, W11, W13, W14, W16, W18 (each named in its worker's report; none changes a result).

## Not exercised, stated plainly

- **FWD-6's real read in muse** and **FWD-7's real answer by muse** are Andrew's acts, queued on the laptop list (`laptop-...-8fb2` and `laptop-...-cd2d`). Nothing in this packet claims either. The forged-answer refusal is exercised end to end; an ACCEPTED answer from muse's real key is not.
- **FWD-12** (muse efficacy against the text path) is cut the round after FWD-6 is exercised, per the CTO.
- **The mail loop** (CA-i-7, CA-i-8) is tested and live but has not yet been used by Andrew on the Keith Wagner TIFIN mail (J290). The CTO ruled the Outlook draft route goes to NFRA_OPLGTW after he uses the loop once.
- Carried acts at Andrew: `44eb` (one @mention), `e435` (one colleague email), `87a2` (does Kimi also stop drafting).

## Enrichment candidates for the CTO's round-18 analysis (this seat's reading; the CTO writes the list)

1. **First: the signed SMS-ingress marker** (W10-S2), as the CTO ruled.
2. The forwarder creates `answers\` and its subfolders when absent (seat row D2-S1; the install made them by hand).
3. After the real muse read and answer: **FWD-12**, the efficacy cell.
4. The mail-draft-in-Outlook route (OPLGTW) after Andrew has used the paste loop once.
5. A retained-signed-answer limit for mail and job tags inside one day is the CVO's stated limit, not a candidate unless the CVO says so.
