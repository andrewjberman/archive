# Finding — secret rotation triage (76 never-rotated secrets)

**Author:** 3.0.0_SA_CVO · **Date:** 2026-06-26 · **Sev:** LOW (hygiene; COO-flagged, folds into the future node_health rotation-staleness dimension) · **Tool:** comp-secrets rotation/list
**Question (COO):** of the 76 never-auto-rotated secrets, is ANY one NOT a by-design app/relay token = a real rotation gap?

**Answer: YES — a handful, all hygiene-tier (none urgent / no active vuln).** Three classes:

1. **BY-DESIGN never-rotate (NOT gaps) — the majority (~48):**
   - Ephemeral / re-minted by their own flows: all `*/otp-*`, `*/otp-relay`, `*/session`, `*/credentials`, `*/jwt/current`, `eclipse_jwt`, `orion/jwt/current`, the `opal/mcp/m365-*` + `ms-ingest` tokens (re-minted by the login/relay/gateway flows; "rotation=off" is correct — they cycle out-of-band, not via SM rotation).
   - Consistency-keys that MUST NOT rotate: `opal/pseudonym/*` + `schwab/anonymization-key` (rotating breaks pseudonym/anonymization stability by design).

2. **Third-party VENDOR API keys (manual-rotation hygiene, not auto-rotation gaps) — ~20:**
   `openai-api-key` + `opal/openai/*` (5) + `anthropic-api-key` + `ai/claude-api-key` + `github-token` + `FredApiKey` + `brightdata`/`massive`/`lusha`/`seeking-alpha`/`find-insure/job-board/*` keys. SM cannot auto-rotate a vendor-issued key, so "rotation=off" is expected. SIGNAL: the OLD ones (185d: `openai-api-key`, `github-token`, `FredApiKey`, `opal/openai/*`; 171d `ai/claude-api-key`) are a manual-rotation-hygiene flag — a 6-month-old key has had 6 months of exposure-if-leaked. Recommend a periodic manual vendor-key rotation pass; not urgent.

3. **GENUINE self-controlled rotation candidates (the real answer to COO's Q) — 3:**
   | secret | age | why it's a candidate |
   |---|---|---|
   | `opal/auth/jwt-private-key` | 81d | JWT SIGNING private key, self-minted — the highest-value rotate candidate (a leak = forge any token); 81d is okay but it should be on a rotation cadence |
   | `opalinvest/jwt-secret` | 179d | JWT secret, self-controlled, 179d-old |
   | `opalinvest/admin-seed` | 179d | admin seed, sensitive, 179d-old |
   These 3 are self-controlled (we mint them), long-lived, and rotating them is feasible + reduces exposure. Still LOW-sev (no evidence of compromise; just hygiene).

**Disposition:** no urgent action. Folds into the node_health rotation-staleness DIMENSION (COND-B) when COO stands it up post-combined-ship — these 3 + the aging vendor keys are the first real burn-down targets. The by-design set (class 1) should be SUPPRESSED in that dimension (a structural predicate: ephemeral/consistency-key names) so it doesn't false-flag, same pattern as the comp-dups suppression classes.

— 3.0.0_SA_CVO
