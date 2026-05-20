<task_order>
  <metadata>
    <id>YALP_MDSRC.004</id>
    <slug>ae-ws4-ycharts-operational-pattern-declaration</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <completed>2026-05-20 -- WS-4 YCharts operational-pattern design doc shipped: docs/briefs/mdsrc-ws4-ycharts-operational-pattern-20260520.md. Orion JWT + Eclipse dual-track baseline documented (AC1); YCharts-adapted pattern declared for capture / SM cookie-bundle shape / freshness gate (Q2 = active authenticated probe) / refresh Lambda / CW namespace YCharts/SessionResilience / daily cron (AC2); jwt-vs-cookie credential difference addressed -- three structural reasons jwt_freshness.py decode-exp does not port (AC3); both capture branches designed (headless Branch A / attended Branch B) AND the shared WS-1 Q3 auth/WAF finding cited (AC4); committed design doc + session log w/ Compiler Tools section + RAVC2 (AC5). Single-concurrent-session constraint (WS-1 Finding 2) folded in as the load-bearing design driver. Design-only -- no code/TF per v0.2. RAVC2 to COO + CC CTO.</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-20 — Andrew GO received; COO dispatched. Original gate: STAGED — Phase 0 audit, unblocked on Andrew GO (PRD v0.2 §9/§11: the four Phase-0 audits dispatch in parallel on Andrew GO). No inter-TO dependency — TO-1..4 are fully parallel. On GO: COO flips status->pending + dispatch_held=false + fires the GO message.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct (CEO interview 2026-05-20). WS-4 declares the YCharts-adapted operational pattern that v0.3 implementation builds on. 0.7.0_AE_CloudOps provided the JWT architecture consult on ADVI_JWTRES — the right lane for the Orion/Eclipse baseline.</priority>
    <sla>~2-4 effort-days (PRD §9). Investigation/design TO; parallel with TO-1/2/3.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2 (1.0.0_SA_CTO). This TO = WS-4 / §8 TO-4 (v0.1 WS-C, renumbered WS-4 unchanged by the v0.2 amendment). Read §2.3 (the Orion operational pattern) + §3.1 (YCharts is cookie-session + CSRF + WAF, NOT JWT) before scoping.</prd>
    <orion_baseline>ADVI_JWTRES (complete) — the Orion pattern: `infra/aws/lambda/inf-pipeline/*/jwt_freshness.py` (decode-exp freshness gate, assert_fresh_or_exit / recover_or_exit), the `inf-jwt-trigger` Lambda (Playwright capture), Secrets Manager `orion/jwt/current` + S3 fallback `s3://opal-data-inf/orion/jwt/current.json`, CW namespace `Inflection/JwtResilience`, daily refresh cron.</orion_baseline>
    <eclipse_baseline>ADVI_ECLDAT (complete) — the Eclipse dual-track JWT variant of the same pattern.</eclipse_baseline>
  </references>

  <context>
    YALP_MDSRC evaluates moving portal market-data surfaces to a daily automated YCharts pull. WS-4 declares the OPERATIONAL PATTERN for that pull. Andrew's framing was "manual jwt refresh and lib/secrets storage like how we do it for Orion" — but PRD §3.1 establishes a key correction: YCharts has NO JWT. It is a Django session-cookie web app (ycsessionid + csrftoken) behind an AWS WAF challenge token. The Orion OPERATIONAL pattern (capture -> Secrets Manager -> freshness gate -> refresh Lambda -> CW alarms -> daily cron) transfers cleanly; the CREDENTIAL is a cookie bundle, not a JWT — so the `jwt_freshness.py` decode-the-exp mechanism does NOT port directly, and the WAF bot-detection layer must be solved by the capture mechanism. WS-4's output is a DESIGN DOC, not code. v0.2 authorizes NO code/Terraform/Lambda change.
  </context>

  <scope>
    <in_scope>
      - Extract and document the Orion JWT pattern (`jwt_freshness.py`, `inf-jwt-trigger`, Secrets Manager `orion/jwt/current`, CW `Inflection/JwtResilience`, daily cron) and the Eclipse dual-track variant as the BASELINE — capture / SM storage / freshness gate / refresh / CW / cron.
      - DECLARE the YCharts-adapted operational pattern given PRD §3.1 (cookie-session + CSRF + WAF, no JWT). Cover ALL of:
        * Credential-capture mechanism — a real-browser / Playwright-style capture that solves the AWS WAF JS challenge.
        * Secrets Manager storage shape for the cookie BUNDLE (ycsessionid + csrftoken + aws-waf-token + any required headers) — contrast with the single-JWT shape.
        * The FRESHNESS GATE (Q2) — there is no `exp` claim to decode; design a lightweight authenticated probe OR use the `Set-Cookie` max-age. State the chosen signal + its failure/recovery behavior (the cookie-world analogue of assert_fresh_or_exit / recover_or_exit).
        * Refresh Lambda mechanism, CloudWatch namespace + alarms, daily cron cadence.
      - Explicitly address the JWT-vs-cookie credential difference (PRD §3.1) — do not gloss it.
      - Output is a committed DESIGN DOC.
    </in_scope>
    <out_of_scope>
      - NO Lambda, Terraform, Secrets Manager resource, or code authored — v0.2 is design-only. (NOTE for v0.3: when this design is implemented, the implementing TO carries `comp-iam service` + `comp-iam gaps` mandates for the new Secrets Manager + Lambda boto3 calls.)
      - The official-API-vs-scrape decision (Q1) — design the scrape-path capture mechanism AND note what changes if the official API is chosen; v0.3 decides.
      - YCharts endpoint capability + portal surfaces — the three DS domain audits (TO-1/2/3).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the design work">
      <step>
        <run>(none) — read-only review of shipped Orion/Eclipse Lambda source. `comp-iam service &lt;lambda&gt;` is NOT yet applicable — no Lambda is authored in this WS.</run>
        <expect>Documented-none: WS-4 produces a design doc, not code. The IAM/route compiler mandates attach to the v0.3 IMPLEMENTATION TO, not this audit.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — design doc, no code.</run>
        <expect>No py_compile / ruff / ds-precommit gate applies.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — design completeness is checked by the acceptance criteria, not a compiler tool.</run>
        <expect>Documented-none. Carry-forward note for v0.3: the implementing TO MUST run `comp-iam service` (Phase 1) + `comp-iam gaps` (Phase 2 if iam.tf changes).</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Consumes the shared YCharts auth/WAF finding (Q3 — does the WAF challenge defeat headless capture) from whichever DS domain audit (WS-1/2/3) reached the auth layer first — per PRD §4/§7 the auth probe is recorded once + shared, not triplicated. Sequence the WS-4 capture-mechanism section AFTER that finding is available, OR design BOTH branches (headless WAF-solvable vs attended capture) and let WS-5 (TO-5) pick. ADVI_JWTRES / ADVI_ECLDAT Lambda source is read-only — no coordination needed. No shared files.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The Orion + Eclipse JWT patterns are documented as the baseline — capture, Secrets Manager storage, freshness gate, refresh mechanism, CloudWatch observability, cron cadence.</ac>
    <ac id="AC2">The YCharts-adapted operational pattern is declared for ALL of: credential capture (WAF-challenge-solving), Secrets Manager storage shape for the cookie bundle, the freshness gate (Q2 resolved — the chosen non-JWT freshness signal named, with failure/recovery behavior), the refresh mechanism, CloudWatch observability, the cron cadence.</ac>
    <ac id="AC3">The JWT-vs-cookie credential difference (PRD §3.1) is addressed explicitly — why `jwt_freshness.py`'s decode-exp does not port, and what replaces it.</ac>
    <ac id="AC4">If WS-4's capture section is reached before the shared Q3 auth/WAF finding is available, BOTH capture branches are designed (headless WAF-solvable vs attended) for WS-5 to pick — OR the section cites the finding.</ac>
    <ac id="AC5">Deliverable is a committed design doc. Session log under `org/tier2_senior/0.7.0_AE_CloudOps/logs/` (run date) with a Compiler Tools section stating the documented-none rationale + the v0.3 `comp-iam` carry-forward note. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The YCharts integration operational-pattern design doc (committed under `docs/` — `docs/briefs/` or `docs/architecture/` per AE judgment; cite the path in the RAVC2).
    - Session log with a Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT author any Lambda, Terraform, Secrets Manager resource, or code — v0.2 is design-only. The implementation is a v0.3 TO.</rule>
    <rule>Do NOT assume YCharts has a JWT — PRD §3.1: it is a cookie bundle. The freshness gate must be designed around that.</rule>
    <rule>Do NOT pre-decide official-API vs scrape (Q1) — design the scrape-path capture mechanism and note the official-API delta.</rule>
    <rule>No emojis in the design doc, the session log, or CLI transcripts (CLAUDE.md ASCII-only).</rule>
  </do_not>
</task_order>
