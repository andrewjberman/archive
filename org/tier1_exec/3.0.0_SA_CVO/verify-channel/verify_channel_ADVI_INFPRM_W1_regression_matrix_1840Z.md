# verify-channel — ADVI_INFPRM.W1 cross-tenant regression matrix (asymmetric-bug bar)

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | **W1 commit:** portal DEV 3d5d05b8
**Bar:** fixing external-Inflection layout resolution must NOT regress internal/49F/demo (asymmetric bug).
**Mode:** data/logic (rendered-pixel = Andrew/CTO; headless fabric-down).

## Verdict: PASS (data/logic) — no cross-tenant regression; the change is asymmetric (external-Inflection only)

### Hook logic (useTenantLayout.ts, post-W1) — strictly additive
Two-param: layoutFirm=LAYOUTS[firmId]||DEFAULT (firmId-scoped: roles/panels/tabs/routes); dataFirm=LAYOUTS[firmOverride??firmId]||DEFAULT (data-path: dataSources/features/includesCash). Fast-path: if dataFirm===layoutFirm return layoutFirm by-reference (every single-param caller + internal-on-own-partner-page). Merge only when scopes diverge.

### Matrix-field literals (independently read; NOT proxy)
| firm | roles.composition.enabled | clientDetailHandler | usesStatic | includesCash |
|---|---|---|---|---|
| DEFAULT (pre-W1 external fallback) | true (L371) | undefined (L336) | false | false (L364) |
| 49financial | true (L101) | 'lambda' (L41) | false | false (L90) |
| demo | true (L86) | 'lambda' (L30) | false | false (L76) |
| inflection | false (L135) | 'static' (L42) | true | true (L122) |

### Regression matrix verification
- **49F external** (pre=DEFAULT, post=49F layout): composition true==true, usesStatic false==false, includesCash false==false -> IDENTICAL. NO REGRESSION.
- **demo external** (pre=DEFAULT, post=demo layout): true/false/false == DEFAULT -> IDENTICAL. NO REGRESSION.
- **inflection external** (pre=DEFAULT, post=INFLECTION): composition true->false (S1 fix: Role Composition now HIDDEN), usesStatic false->true (S3 fix: Book static adapter loads), includesCash false->true (Orion AUM, intended). The intended asymmetric fix.
- **internal admin**: firmOverride=internal?FIRM_ID:undefined (inflection/index.tsx:157) = 'inflection' (defined); firmId = page firm = 'inflection'; firmId==firmOverride -> fast-path -> INFLECTION_LAYOUT == pre-W1 useTenantLayout(firmOverride). IDENTICAL.

### Process note (transparency)
First literal grep false-read the values (pattern 'composition:' substring-matched 'groDecomposition:', inverting the table); caught it because the literals contradicted the code comments + RD~C's claim (sharpest-test/re-check-on-contradiction). Re-grepped excluding Decomposition -> the table above is the corrected, correct read.

### Honest limits
- Rendered-pixel confirmation (the 4 cases ON SCREEN) is Andrew/CTO visual smoke (headless down) — this is the data/logic layer.
- Internal non-regression rests on firmId==firmOverride for internal-on-their-partner-page (confirmed). Any internal flow producing firmId!=firmOverride would hit the merge-branch (roles from firmId-layout) — that is the intended two-scope design, not a working-firm-broke regression; no such divergent flow found in the W1 sites.

RAVC2 PASS to RD~C; CC CTO/COO (INFPRM.W1 closure bar).
— 3.0.0_SA_CVO
