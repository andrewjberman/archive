# comp-similar — T12 s.4 audit

**TO:** `NFRA_COMPEFFICACY.TO-CE-T-12` · **Cell:** `CE-t-12` · **PRD:** v0.5 `5bbdab5ec7` · **Read vintage:** `6e5d443ad3` · **Assignee:** `0.8.0_AE_CloudComp~F` · **Audit date:** 2026-09-03

```json
{
  "tool": {
    "grade": "PRESENT",
    "value": "comp-similar"
  },
  "shim_path": {
    "grade": "PRESENT",
    "value": ".tools/comp-similar (29 lines)",
    "sha256_before": "5449e4879455b593e1b2229ffab30fec72dd2fdf8101acf08d046336a782626f",
    "sha256_after": "7cb1eff9510ff8ba7f70e6562d4170da7b1f7442afc4bac510bb70e7e3d0ee80"
  },
  "engine_path": {
    "grade": "PRESENT",
    "value": "org/modules/graph/debtscan/comp_similar.py (943 lines)",
    "sha256_before": "414616009644f7a5d7c8d2fbe774190a0be46f8712ae7b3f58624e4ffb9413c7",
    "sha256_after": "ca2624fb03c095faa1a88235dae3eada1652ba11a9c00ae6793d17f1c09aabff",
    "deployed_dependency": {
      "image": "opal-globgrph-derive-runner:latest",
      "image_digest": "sha256:3a4e078d2c65c0243f2aac3c2ad033ac7a154c12cc46d7b9998cf37601188486",
      "image_tag": "20260903-143221",
      "pushed_at": "2026-09-03T14:32:35Z",
      "member": "/app/org/modules/graph/debtscan/summary_corpus.py",
      "member_bytes": 92840,
      "member_sha256": "2c56cd7d50e8b3115d283ea95c5a29f8485ff0ec16f36a4e961ac60add7c6c85",
      "repo_sha256": "2c56cd7d50e8b3115d283ea95c5a29f8485ff0ec16f36a4e961ac60add7c6c85",
      "build_input_member_sha256": "2c56cd7d50e8b3115d283ea95c5a29f8485ff0ec16f36a4e961ac60add7c6c85",
      "state": "CURRENT_DEPLOYED_EQUALS_BUILD_INPUT_EQUALS_COMMITTED after an independent post-cut rebuild; the historical PRE-fix mismatch is preserved in NFRA_COMPEFFICACY-S23 and was not fixed by this cell",
      "historical_owner": "0.7.0_AE_CloudOps"
    }
  },
  "engine_vintage": {
    "grade": "PRESENT",
    "value": "6412cb26f7 before this order; remediation commit pending this local commit"
  },
  "aliases": {
    "grade": "PRESENT",
    "value": []
  },
  "purpose_1line": {
    "grade": "PRESENT",
    "value": "BM25 summary similarity over what resources do, plus an advisory superseded-twin scan that requires heat divergence and suppresses designed parallels and held resources."
  },
  "self_identifies": {
    "grade": "PRESENT",
    "value": "Public shim --help delegates to the import-inert engine and prints org/modules/graph/debtscan/comp_similar.py, NFRA_COMPSIMILAR PH2, and the Rule T carrier."
  },
  "subject": {
    "grade": "PRESENT",
    "value": "Default-budget quoted run: cluster population node_type=NO_SUCH_TYPE; budget-cut quoted run: supersede over the full ARN summary corpus."
  },
  "corpus_or_backend": {
    "grade": "PRESENT",
    "value": "derive-at-scan summary corpus from comp-kuzu, DB kuzu_nessie_db; live-heat mode additionally consumes comp-debris and comp-heat freshness."
  },
  "vintage": {
    "grade": "PRESENT",
    "value": "corpus built: 2026-09-03T13:52:09.642788+00:00 (age: 1.3h), DB kuzu_nessie_db"
  },
  "denominator": {
    "grade": "PRESENT",
    "value": "1871 ARN resources; 1514 summarized; 357 UNKNOWN-thin; budget status separately reports 1871/1871 complete or 1/1871 prefix."
  },
  "resolved_unresolved": {
    "grade": "PRESENT",
    "value": "1514 with purpose summary / 357 UNKNOWN-thin; unresolved query subjects now print SUBJECT_ABSENT_FROM_CORPUS rather than sharing the zero-result shape."
  },
  "blind_spots": {
    "grade": "PRESENT",
    "value": "UNKNOWN-thin rows never form twin claims; absent/partial heat never becomes cold; live heat declares S3 coverage partial; a budget prefix prints PARTIAL_OR_BLIND with scanned n/N and corpus vintage."
  },
  "pagination": {
    "grade": "PRESENT-BUT-WRONG",
    "value": "Rule T work pagination is resumable by deterministic ARN --cursor. Row-output pagination is absent: --top caps candidates without PAGE i of N or the true pre-cap total."
  },
  "timeout": {
    "grade": "PRESENT",
    "value": "Corpus scans accept --budget > COMP_BUDGET_S > 90-second default; 0 is unbounded. Expiry and completion are explicit. The shared summary_corpus retrieval pre-step retains its own 180-second timeout outside this order's engine edit."
  },
  "answer_state": {
    "SUBJECT_ABSENT_FROM_CORPUS": {
      "plant": "offline synthetic corpus lookup for arn:missing",
      "rc": 0,
      "text": "PLANTED absent-subject: ANSWER-STATE: SUBJECT_ABSENT_FROM_CORPUS -- 'arn:missing' did not resolve to a corpus resource"
    },
    "PRESENT_WITH_ZERO_RESULTS": {
      "plant": "arn:fill0 exists in the 24-resource offline corpus and has zero neighbours above SIM_FLOOR 0.15",
      "rc": 0,
      "text": "PLANTED present-zero: ANSWER-STATE: PRESENT_WITH_ZERO_RESULTS -- arn:fill0 is present; zero results cleared the threshold"
    },
    "PARTIAL_OR_BLIND": {
      "plant": "spent-clock scan reads 1 of 24 deterministic ARN units against a stale-vintage fixture",
      "rc": 0,
      "text": "PLANTED stale-corpus: ANSWER-STATE: PARTIAL_OR_BLIND -- scanned 1 of 24 ARN resources; corpus built: 2025-01-01T00:00:00Z (age: STALE)"
    },
    "NOT_APPLICABLE": {
      "plant": "cluster node_type=NO_SUCH_TYPE has zero applicable resources",
      "rc": 0,
      "text": "PLANTED not-applicable: ANSWER-STATE: NOT_APPLICABLE -- node_type=NO_SUCH_TYPE has no applicable population"
    }
  },
  "subprocess_timeouts": {
    "grade": "PRESENT",
    "value": "_run_json has a 180-second library fallback. load_heat_live has a 280-second library cap, but the CLI derives each comp-debris and comp-heat freshness timeout as min(280, Clock.remaining()); unbounded passes timeout=None; exhausted calls are named in the DEFERRED bucket. Shared summary_corpus._kuzu_json has a separate 180-second retrieval timeout."
  },
  "ceiling_behaviour": {
    "grade": "PRESENT",
    "value": "Before metrics, expiry prints BUDGET REACHED, scanned n of N, PREFIX-not-answer, and a real last-ARN cursor; completion prints WITHIN BUDGET N of N and used seconds. Non-verdict report rc remains 0."
  },
  "page_contract": {
    "grade": "ABSENT",
    "value": "No --page/--limit/--all and no PAGE i of N output contract. Rule T cursor pages work, not the capped output rows."
  },
  "size_invariance": {
    "grade": "PRESENT-BUT-WRONG",
    "value": "Wall-clock scan work is size-invariant through budget plus deterministic cursor; live-heat subprocess ceilings derive from remaining budget. Candidate output remains a fixed --top cap without a true-total page contract."
  },
  "moves_1_to_8": {
    "grade": "PRESENT",
    "value": [
      "1 DONE: read the 29-line shim and 943-line engine",
      "2 DONE: write surfaces are wrapper telemetry and the opt-in live-heat temporary JSON, which is removed in finally",
      "3 DONE: no result cache; oracle is derive-at-scan corpus plus injected offline fixtures, with vintage carried",
      "4 DONE: source and independent live run both establish the ARN unit; live denominator 1871",
      "5 DONE: absent ARN, existing isolated summary, budget-cut corpus, empty node-type population, known twin and false twin",
      "6 N-A: no persistent production mutation; battery mutants are sibling temp files removed after execution",
      "7 DONE: independent Kuzu provenance plus served ECR layer byte extraction; semantics falsifier uses known twin/non-twin fixtures",
      "8 DONE: guard-asymmetry archetype; hunted false-twin, blind-row, stale-vintage, zero-vs-absent, and clean-vs-prefix shapes"
    ]
  },
  "archetype": {
    "grade": "PRESENT",
    "value": "guard-asymmetry advisory measurement/report; lead probes guard-asymmetry, success-token-bound-to-wrong-step, and aging-oracle"
  },
  "findings": {
    "grade": "PRESENT",
    "value": [
      "NFRA_COMPEFFICACY-S23: aging-oracle/spec-vs-world — historical DEPLOYED != COMMITTED was true at cut, but current served bytes match after an independent rebuild",
      "terminal-honest/artifact-lies: --top caps output without the true total; recorded as page_contract ABSENT and not widened under this order",
      "guard-asymmetry controls pass: name-same/purpose-different=0.0, name-different/purpose-same=1.0, and similarity without heat yields no supersession"
    ]
  },
  "runs_30d": {
    "grade": "PRESENT",
    "value": "Final pre-commit census: runs.jsonl has 33 exact comp-similar rows in the 30-day window (49 ever), including three T-12 public-wrapper exercises after the 30-run cut baseline; the rail has 363 comp-similar routing references in-window (677 ever)."
  },
  "hook_driven": {
    "grade": "PRESENT",
    "value": "0 known hook calls; the run sink has no caller field. Public wrapper invocations append telemetry after propagating the engine rc."
  },
  "battery": {
    "grade": "PRESENT",
    "value": ".tools/tests/test_comp_similar_battery.py: direct 12/12 PASS; pytest file grain 1/1 PASS; each of four state literals, Rule T expiry, and vintage capture has a red mutant. Directory collect sees this test among 52, then pre-existing test_fabric_check_classify.py raises module-scope SystemExit. Commit-gate clean 3/3 touched code files."
  },
  "overlap": {
    "grade": "PRESENT",
    "value": "comp-dups is not subsumed: it compares name/body while comp-similar compares purpose summaries. load_heat_live() consumes comp-debris and .tools/comp-heat freshness; exact code census found no reverse import of comp_similar by comp-heat and no rc-only gate consumer. OPAL_LCLRPO is the documented human-reviewed candidate-feed destination."
  },
  "proposed": {
    "grade": "PRESENT",
    "value": "CLEARED-candidate for the T12 identity, disclosure, answer-state and Rule T audit scope. Output-row pagination remains explicitly ABSENT for reviewer disposition; no retirement or image action is proposed."
  }
}
```

## Quoted exercised output

The public wrapper's default-budget clean control returned rc 0:

> WITHIN BUDGET: scanned 1871 of 1871 ARN resource; budget: 90 s (default), used 20.61 s  
> DEFERRED: 0 of 0 heat subprocess(s) did not return -- each names its reason below  
> ANSWER-STATE: NOT_APPLICABLE -- node_type=NO_SUCH_TYPE has no applicable population  
> corpus built: 2026-09-03T13:52:09.642788+00:00 (age: 1.3h), DB kuzu_nessie_db  
> scanned 1871 ARN resources; 1514 with purpose summary; 357 UNKNOWN-thin; 29 hold-marked

The public wrapper's tiny-budget control also returned rc 0 because this is a non-verdict measurement:

> BUDGET REACHED: 1e-06 s (flag); scanned 1 of 1871 ARN resource; results are a PREFIX, not the answer; resume: comp-similar supersede --top 3 --budget 0.000001 --cursor arn:aws:apigateway:us-east-1::/apis/7k3ed8px20  
> DEFERRED: 0 of 0 heat subprocess(s) did not return -- each names its reason below  
> ANSWER-STATE: PARTIAL_OR_BLIND -- scanned 1 of 1871 ARN resources; corpus built: 2026-09-03T13:52:09.642788+00:00 (age: 1.3h), DB kuzu_nessie_db

The answer-state grain is one `--self-test` invocation, not four unrelated subcommands. It returned rc 0 and printed all four `PLANTED ... ANSWER-STATE:` lines recorded in the JSON block. The independent battery then altered each literal separately; all four mutants were detected.

## Deployment identity and change boundary

The order's historical statement is preserved, not silently rewritten: its earlier measurement found the image's `summary_corpus.py` PRE-fix. Before this cell ran, NFRA_CLDGRPH independently rebuilt and pushed `latest`. I read the served ECR artifact itself: Docker layer `sha256:515c90b2a5b2a706939459cb0959dff4de573e312a06a2282f4b833ae4ef152f` contains the 92,840-byte member with SHA-256 `2c56cd7d...add7c6c85`, equal to the build-input ZIP member and current repo bytes. Image digest, tag and push time are in the schema. `NFRA_COMPEFFICACY-S23@c8a2ebbe1d5` records that temporal divergence and keeps the historical owner `0.7.0_AE_CloudOps`; the shared-row commit's override preserves this seat as `surfaced_by`. This cell performed no image build, tag, deployment, or summary-corpus edit.

Similarity thresholds, BM25 scores, suppressors, heat-divergence requirement and rank formula are unchanged. The established controls remain name-same/purpose-different `0.0`, name-different/purpose-same `1.0`, the same cold candidate/replacement pair, and no supersession without heat. The implementation change is scheduling/disclosure: exact answer-state dispatch, shared `_compbudget.py`, deterministic ARN boundaries, remaining-derived live-heat timeouts, and public help delegation.

## Consumer and rc census

The executable census found one public code caller: `.tools/comp-similar`, which invokes the engine, appends telemetry, and propagates its rc. No hook, gate, `&&`, or reverse `.tools/comp-heat` import consumes the report rc as a verdict. Inside this engine, `load_heat_live()` is the library orchestration that invokes `.tools/comp-debris --json` and `.tools/comp-heat freshness --json`; this is the comp-heat library-use relationship named by the order. Humans/agents and the documented OPAL_LCLRPO review path consume the advisory candidate text. Therefore prefix and semantic answer states retain rc 0; rc 1/2 is reserved for unreadable input or execution/retrieval failure.

## Acceptance evidence

| Criterion | Evidence |
|---|---|
| `T12-AC1` | The single JSON block contains all 31 semantic s.4 fields; it names shim, engine, before/after SHA, and current served-image member identity. |
| `T12-AC2` | One self-test invocation prints four distinct ratified tokens; rc 0 for each planted state; partial carries `corpus built ... age: STALE`. |
| `T12-AC3` | Historical mismatch is preserved in S23 with owner; current image, build-input member and repo SHA are equal after a foreign post-cut rebuild; this cell made zero image/summary-corpus change and retained similarity controls. |
| `T12-AC4` | Public help exposes Rule T; real 1/1871 prefix and 1871/1871 completion are quoted; cursor names a fully processed ARN; rc census establishes non-verdict behavior and the comp-heat relationship. |
| `T12-AC5` | New battery direct 12/12, pytest 1/1, six red mutants, D1-D3 C3b/C3c regression, and commit-gate 3/3 clean. Directory collection interference is stated. |
| `T12-AC6` | The proof instance resolves its sole surprise to `S23@c8a2ebbe1d5`; the shared-file override preserved authorship. This lane's implementation commit and push state are LOCAL, and this seat never pushes per ruling 93726. |
