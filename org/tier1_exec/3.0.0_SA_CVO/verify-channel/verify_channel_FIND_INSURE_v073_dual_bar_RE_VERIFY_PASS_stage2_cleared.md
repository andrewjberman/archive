# /verify-channel Mode A — v0.7.3 dual-bar RE-VERIFY: PASS → Stage 2 CLEARED

**Mode:** A surface-level empirical-smoke-class (the Stage-2 release gate per CVO `2570068ce` ADDITIVE-2)
**Trigger:** DS~B DUAL-BAR RE-VERIFY REQUEST `20260528T051221Z` — v0.7.3 W1 classifier shipped `0e53822a4`
**Verifier:** 3.0.0_SA_CVO — independent read of actual re-grade output (`.runtmp/find-insure-stage1/regrade_v073_result.json`), NOT DS~B self-report (verifier-≠-fixer rule 2)
**Verdict:** **PASS — Stage 2 universe-burn CLEARED to unblock.**

---

## §1 — Independent empirical confirmation (read the artifact, not the report)

Read `regrade_v073_result.json` directly. The 4 SCORED IMOs (am_prominence v0.7.3 classifier, real Stage 1 silver):

| IMO | exp | am_prominence | high_signal≈ | annuity_baseline | wm | bar |
|---|---|---|---|---|---|---|
| lincoln-investment | TP | **0.9415** | ~95 | 5.9 | present | TP-preserved ✓ |
| allianz-life | TN | **0.0117** | ~8.9 | 748.5 | adjacent | TN-suppressed ✓ |
| american-equity | TN | **0.0000** | ~0 | 436.9 | adjacent | TN-suppressed ✓ (F-2 fixed) |
| midland-national | TN | **0.0482** | ~23 | 468.4 | adjacent | TN-suppressed ✓ |

Top-level flags (independently read, not self-reported): `dual_bar_pass: True`; `tn_false_positives: []`; `tp_false_negatives: []`; `taxonomy_version: v3`; `scoring_weights_version: v0.3`. DS~A `.035 discrimination-eval --label v0.7.3`: `discrimination_pass: true`, `fn_rate: 0.0` (+ DS~B-reported TP=1 FP=0 TN=3 FN=0 precision=1.0 fp_rate=0.0, vs v0.7.1 fp_rate=1.0/precision=0.25).

**Values match DS~B's table exactly.** The am_prominence figures are far below my earlier ≈0.27 estimate (`2570068ce`) — CORRECTLY so: v0.7.3 uses high_signal_AM-only numerator (regulatory markers: RIA self-ref / Form-ADV / Series-65-advisor / IAR / advisory-AUM), NOT the generic-AM-inclusive ratio I estimated. Allianz fires massive annuity vocab (ann_base 748.5) with near-zero genuine regulatory markers → 0.0117. The high-signal-term gate is SHARPER than my estimate predicted.

## §2 — Dual-bar (ADDITIVE-2) both PASS

- **Bar 1 TN-suppression: PASS** — allianz (0.0117) + american-equity (0.0) + midland (0.0482) all → adjacent. ZERO present-FP (`tn_false_positives: []`). The v0.7.1 F-1 (class_diversity gate false-presenting TN carriers firing 7 incidental classes) is empirically fixed.
- **Bar 2 TP-preservation: PASS** — lincoln-investment (0.9415) → present (`tp_false_negatives: []`). No genuine target regressed to absent. The FN-guard holds.
- **Margins robust, not knife-edge:** TN carriers at 0.0/0.01/0.05 vs T_present=0.50 (enormous margin); lincoln at 0.94 vs 0.50 (huge margin). Math internally consistent (lincoln hi_sig~95/ann 5.9 vs allianz hi_sig~8.9/ann 748.5 — genuine separation, not a tuned-to-pass artifact).

## §3 — F-2 regression confirmed fixed

american-equity v1=20 (correct absent) → v0.7.1=91 (FP regression from annuity-vocab-as-positive-rollup) → v0.7.3 am_prominence=0.0 → adjacent. The annuity-vocab removal from positive rollup (now denominator-only) reverts the regression. Confirmed.

## §4 — Cambridge IR null-routing judgment: CORROBORATE

DS~B flagged the one judgment call beyond the bare ratio: Cambridge IR (no-JS SPA shell, HTTP 200, "your browser does not support JavaScript") routed via new `is_spa_render_shell()` detector → BLOCKED_UPSTREAM → wm null (per PRD §281 SPA-render-fail), NOT absent.

**CORROBORATE.** Rationale:
- It's an acquisition-failure (no public scoreable content via direct fetch), NOT a true-negative (no AM signal). The distinction is load-bearing: absent = "we read it, no AM signal"; null = "we couldn't acquire signal."
- Aligns with PRD §281 + my `.030` §G1 score_class doctrine (BLOCKED ≠ true-negative) + my AC-T2 Mode A auth-gated/SPA-render-tail finding (`3ced0c99e` §3).
- Classifying Cambridge absent would be a FN on a genuine target (labeled TP); excluding it from the discrimination denominator (not counting as FN) is correct — it's no-data awaiting the AC-T2 v0.3.1 escape-valve re-crawl (the recovery path).
- **Keep the W1-side detector (do NOT revert to upstream-only):** it's defense-in-depth — even before the escape-valve re-crawls, the SPA-shell direct-fetch is correctly routed to null not mis-scored absent. When the escape-valve re-crawls (v0.3.1), the re-crawled content re-scores. W1-side detector (interim correct handling) + AC-T2 escape-valve (recovery) are complementary, not redundant.

## §5 — Verdict + Stage 2 release

**PASS.** v0.7.3 empirically discriminates correctly on the Stage-1 subset — both dual-bars confirmed against actual output, discrimination_pass true, F-1 + F-2 both fixed, Cambridge null-routing sound. **Stage 2 universe-burn is CLEARED to unblock.**

The closing leg of the Stage-1-first-empirical high-leverage moment: my Mode B `810211e17` (b)(i) → v0.7 close → v0.7.1 attempted close → DS~B `5f73af749` 2nd-empirical refutation → CVO `b47f3c37b` REPAIR-AMENDMENT + `2570068ce` CORROBORATE → ws CTO v0.7.3 `8d08c7564` → DS~B impl `0e53822a4` → **this re-verify PASS**. (b)(i) inadequate-solution-coverage is now empirically CLOSED at v0.7.3.

## §6 — Routing + forward

- **ws COO:** Stage 2 release CLEARED — your ratify-GREEN consumes this re-verify-PASS + DS~A discrimination_pass. AE 0.7~A Stage 2 universe-burn unblocked.
- **AE 0.7~A:** Stage 2 unblocked; proceed with universe-burn.
- **DS~B:** re-verify PASS independently confirmed; v0.7.3 discrimination is sound.
- **ws CTO:** LD-0022 joint-decide closes — v0.7.3 empirically validated.

**Forward to universe scale (NOT a blocker; the calibration-drift watch):** T_present=0.50 calibrated on the 5-IMO subset with enormous margins; the Stage-2 distribution monitor (remapped axis `(am_prominence, wm_classification)` per AE 0.7~A coordination) watches whether the conservative threshold generalizes at 99-IMO scale — the subset cannot reveal a universe-scale clustering band. Monitor fires at universe-burn (post-Stage-2-unblock). Unrecoverable acquisition tails (auth-gated/cert-fail/parked/SPA-shell-pre-re-crawl) map to null — fold into the completion-matrix cell-state logic + likely Andrew-sign-off carve-out for the 297/297 off-ramp.

— 3.0.0_SA_CVO 2026-05-28T05:22Z
