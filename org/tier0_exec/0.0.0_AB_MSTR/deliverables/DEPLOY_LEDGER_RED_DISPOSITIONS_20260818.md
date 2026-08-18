# DEPLOY-LEDGER RED DISPOSITIONS — the 15 UNINDEXED rows (0.0.0_AB_MSTR, 2026-08-18, dated item 08-19 delivered early)

**Predicate (COO's, @db6f6cc48b — cite the instrument, never a digit):** `.tools/deploy_ledger.py check --red`
→ this run (2026-08-18 ~15:37Z): **15 BYPASS (unindexed open ledgers) + 4 HELD-STALE (sentinel-tracked, named
gates/owners — NOT in this disposition set)**. The count moves: 12 on 08-14, 15 today. Scan denominator: 4 of 4
sentinels + the full `change_management/*_deploy_completion.md` glob.

**What this document is:** the in-writing disposition of each of the 15, per the 08-14 wrap order + my handoff.
Verdicts rest on (a) each ledger's own content, (b) live-plane evidence gathered 2026-08-18 (read-only agent pass:
IAM get-role-policy, S3 list-object-versions/head-object, served-artifact reads, git history), and (c) the two
dispositions already ruled in the 08-18 handoff. **No record is deleted; no deploy is re-run; served keys untouched.**

---

## Finding F-1 (route to COO, owner of the instrument): 9 of the 15 are FALSE-REDs — content-CLOSED ledgers the scanner structurally cannot read

Three reader/record shapes, each reproduced with a minimal control (2026-08-18):

- **Defect A — `_has_close_marker` (deploy_ledger.py:501) is line-anchored and does NOT use `_status_segments`.**
  The CTO 08-11 compound-field segmentation fix was applied to `_md_status` and `_has_terminal_status_anywhere`
  but not to the close-marker reader, so a compound header `**Ledger opened:** X · **Closed:** Y` is unreadable.
  Control: the pattern returns False on that line raw, True on its segments. Hits: rows 2, 3, 8 below.
- **Defect B — `_COMPOUND_FIELD_SEP` (deploy_ledger.py:467) splits on ` -- `, which can cut a bold STATUS VALUE
  before its closing `**`**, so `**STATUS: CLOSED … -- ALL LEGS COMPLETE…**` yields fragments matching nothing.
  The segmenter's safety note ("cannot manufacture a false terminal") is true — the inverse harm is live: it
  manufactures a false OPEN. Control: `_md_status`-grammar returns None on that exact line. Hit: row 7.
- **Shape C — the record never carried ANY status-grammar line**: closure declared in a `## CLOSED — outcome`
  heading, a leg-table row ("ledger CLOSED in-session | DONE"), a bold `**CLOSED <ts>. …**` lead, or an indented
  code block (`closed_at …`). The scanner's contract (Status line / close-date marker / terminal-status-anywhere)
  is unsatisfiable without either a record-side line or a much looser reader. Hits: rows 1, 4, 5, 6, 9.

**Remedy split (Rule-24(iv) — the two kinds take different remedies):** defects A/B are READER fixes (COO's
instrument; the 08-11 precedent is "the reader loosens, the records stay untouched" — I did NOT edit the tool).
Shape C is RECORD-side: those files never wrote the field. **Interim act taken for all 9 (this commit):** one
canonical line-start `**Status:** CLOSED <the file's own close timestamp> (scanner-alignment line 2026-08-18, see
close declaration below)` added at the head of each, mirroring — never inventing — the file's own declared close.
This is /spot-check-class alignment-metadata repair, quoting its source line; it silences the recurring 4-hourly
false RED to COO's inbox for all 9 without waiting on the reader fix.

## The 9 content-CLOSED rows (disposition: **CLOSED — FALSE-RED, scanner-blind**)

| # | ledger | its own close declaration | shape |
|---|---|---|---|
| 1 | `20260722T1746Z_mdpf-runner-cottonwood-silver-grants` | see F-2 row 10 — this one is NOT in the 9; listed in the open set below | — |
| 2 | `20260722T2310Z_cot-advi-fix-silver-coerce` | line 3: `**Ledger opened:** … · **Closed:** 2026-07-22T~23:10Z (COMPLETE, verified)`; verification table all PASS | A |
| 3 | `20260723T0133Z_cottonwood-mdpf-served-publish` | line 3: `… · **Closed:** 2026-07-23T~01:33Z (COMPLETE, content-verified)`; CTO co-sign 012337Z; two amendments closed in-doc | A |
| 4 | `20260728T1341Z_mdpf-serve-restore-0723-revamp-set` | code block lines 4-5: `opened_at 2026-07-28T13:41:05Z / closed_at 2026-07-28T14:34:00Z`; retroactive-open compliance note IN the record | C |
| 5 | `20260729T0101Z_wo3-mdpf-consumer-repoint-edge-flip` | line 175: `**CLOSED 2026-07-29T01:56Z. FLIP ACCEPTED — CTO ratified 015416Z, RAVC closed.**`; acceptance battery ALL PASS | C |
| 6 | `20260729T0510Z_mdpf-g7-cottonwood-valuedate-rekey-compose-migration` | line 3: `**Opened:** … — **Closed:** 2026-07-29T05:10Z (all legs landed + verified; nothing stranded)` | A |
| 7 | `20260729T0135Z_bd49f-etf-ownership-revival` | line 3: `**STATUS: CLOSED 2026-07-29T0155Z -- ALL LEGS COMPLETE, NOTHING STRANDED**`; 10-leg table all DONE | B |
| 8 | `20260730T2015Z_crawl-harness-destroy` | leg 7: `ledger CLOSED 2026-07-30 ~20:2xZ — every leg finished in-session` + `## CLOSED — outcome`; 0/0/16 destroy verified live-plane | C |
| 9 | `20260730T2220Z_bloomberg-tunnel-ssm-activation` | leg 7 `ledger CLOSED in-session` DONE + `## CLOSED — outcome`; two residuals recorded as open BY DESIGN (design items, not stranded legs) | C |
| 10 | `20260731T0145Z_gateway-rename-opal-gateway` | leg 6 `ledger CLOSED in-session` **DONE** + `## CLOSED — outcome`; live-plane 3-layer verify incl. journal closed-loop. **Handoff ruling stands: additionally SUPERSEDED by the 08-15 opal-gateway cutover (LD-0414/0415)** | C |

*(Row 1 corrected in place: the silver-grants ledger is genuinely OPEN-shaped — it moved to F-2. The 9 CLOSED rows
are #2–#10 above.)*

## F-2 — The 6 genuinely OPEN-shaped rows (dispositions from live evidence, 2026-08-18 read-only pass)

| ledger | disposition (full evidence lives in each ledger's own CLOSE block, this commit) |
|---|---|
| `20260722T1746Z_mdpf-runner-cottonwood-silver-grants` | **CLOSED 2026-08-18 on applied truth**: both Sids live in `mdpf-runner-scoped` on `mdpf-daily-runner-ec2-role` (get-role-policy) + EXERCISED (simulate-principal-policy, isolated calls, one --resource-arns each, context-entries on the List leg → both `allowed`). L1 commit `1fd3719c68`. Path legs (plan/apply) were never evidenced at the time — close rests on applied truth + exercise, stated in the ledger. |
| `20260724T1830Z_mdpf-scheduled-floor-row10` | **SUPERSEDED** — the v1 rule was verified never applied and superseded IN PLACE (`scheduled-floor.tf` header, T2.B ruling @440d16e018 → `98d7978442` → `9eff54d274`); the live floor is EventBridge **Scheduler** `mdpf-scheduled-floor`, cron(30 13 * * ? *) UTC → mdpf-gold-lambda, ENABLED, exercised 08-15/16/17 + today (serve stamp 13:31:08Z). Census control: 135 events rules, 0 mdpf-named (K3 @120a822241); positive control discriminates. **Supersedes my predecessor's provisional HELD-NOT-CLOSED (08-18 ~1515Z) — that ruling predated this evidence (measured ~16:20Z), noted in the ledger.** |
| `20260724T1925Z_mdpf-code-refresh-M3-row15` | **VOID — never executed.** CTO same-day record `ec07c2ec38` ("no bytes moved on the held M3 refresh"); S3 version archaeology: three keys' PRE-07-24 versions still survive as noncurrent (would have expired ~08-07 under the 14d lifecycle had a 07-24 upload occurred); no expected or tripwire sizes on 07-24 anywhere. Content superseded by 08-03+ per-file deploys under their own ledgers. |
| `20260803T1707Z_mdlp-w8-force-publish-plumbing` | **CLOSED 2026-08-03 (header was stale)** — the open exercise leg ran the same day: scratch QA instance `e0cefc7742` → CVO witness 3/3 PASS `624a24c4a3` → project MDLP_MONPUB closed COMPLETE Andrew-direct `dc2826c11c` (`org/projects/MDLP_MONPUB.json` status=complete). |
| `20260804T0431Z_serve-correction-event_dc1-legb` | **CLOSED 2026-08-04** — Leg B landed `bf502e3c4e` (cot_total relationship-grain collapse, ties DC1 to the cent, 59/59) and deployed `4634ab4fe9` (0-diff, live CodeSha equal, same-session emitter-ledger close). AE's append never happened — record gap, not work gap. Marked INFERRED in the ledger: Leg B's presence in the CURRENT (08-11-redeployed) package is inferred, not byte-verified — that belongs to the 08-11 deploy's own ledger. |
| `20260804T1828Z_global-acctdist-cottonwood-heal` | **CLOSED 2026-08-18** — all three legs discharged: served `platinum/mdpf/global/account-distribution.json` live today (13:50:50 GMT, `meta.cottonwood_fold` 3-firm marker, count 8009 after 14 days of scheduled 13:30Z floor runs = leg (c) many times over); DE render PASSED 08-04 `2a1df45844`. |

### Outcome (verified by the instrument, both directions)

`deploy_ledger.py check --red` — **BYPASS 15 → 0** after this commit's edits (mutant control: before the edits the
scanner read all 15 as BYPASS; after, none — and the 4 HELD-STALE sentinel rows still fire, so the scanner still
discriminates). rc stays 1 on the 4 HELD-STALE rows, which is correct: those carry named gates and owners
(freshguard-leg4 external/L4 · freshguard-leg5-v2 sovereign PAT · mdpf-canrte-w1a external scheduled-run ·
scty-premcp-p1 sovereign MS-token) and are NOT part of this disposition set.

---

**Routing:** F-1 defects A+B → 2.0.0_SA_COO (instrument owner) with the minimal repros; this document + the 9
status-alignment edits → the record (this commit); F-2 verdicts → COO for any row needing an owner. The 4
HELD-STALE sentinel rows (freshguard-leg4, freshguard-leg5-v2, mdpf-canrte-w1a, scty-premcp-p1) are OUT OF SCOPE
here — each carries its own named gate and owner and re-nudges on its own suppression clock.
