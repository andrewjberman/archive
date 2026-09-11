# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-s-9`

Worktree `/c/tmp/wk-irpt-1-3`, branch `wk-irpt_bckend-1-3`, re-cut by the issuer from `1f795d1f71`
(the commit at which the issuer ADOPTED VERBATIM this worker's `W3-S5` repair from IB-s-7, as
channel row `S13`). Fourth order in slot `~3`, after IB-s-8, IB-s-6 and IB-s-7.

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-1-3`;
   `test -d org && test -d .tools` -> `TREE-OK`. Then the paths this face names, specifically:
   the IB-s-8 ycharts Terraform root (applied, 9 resources), the intake package, `_authz/`,
   `_scope/`, `_keys/`, `_gate/`, the `irpt-common` layer from IB-s-13, and `.tools/terraform.exe`
   provisioned in the worktree by the issuer (a PATH substitute would re-pin remote state).

2. **Read the SUPPLEMENT's packet FIRST, as the supplement instructed -- and could not.**
   The supplement (channel row `IRPT_BCKEND-S14`, PRD v0.10 @`3624e60def`) names
   `docs/research/investor_reporting_ycharts_variants_20260911/` as the reuse source to read
   *before* `cloud_transport.py`. It is ABSENT from this worktree. Measured rather than assumed:
   `git merge-base --is-ancestor 72acd16e66 HEAD` -> NO, `3624e60def` -> NO, with a POSITIVE CONTROL
   on `1f795d1f71` -> YES, so the instrument is not simply answering NO to everything.
   `git ls-tree -r 72acd16e66` shows the 26 files ARE in the local object store. Read them by object
   reference (`git show 72acd16e66:<path>`) -- a read, never a merge or a rebase. Filed as row
   **`IRPT_BCKEND-W3-S7`** and cited as `path@72acd16e66` everywhere the packet is used.

3. **Then the named reuse sources**, in the order v0.9 fixes:
   `docs/research/investor_reporting_ycharts_cloud_20260911/test_cloud_transport.py` first (the
   contract), then `cloud_transport.py` (sha256 `fc571666b1c0...`), then
   `docs/research/investor_reporting_ycharts_auth_20260910/recovery_contract.py` (the v0.5 decision
   table).

4. **Re-grounded the face's premises against live state before building.**
   - The ycharts Terraform root is ALREADY APPLIED by IB-s-8, so `generate.tf` is an ADDITION and
     its first plan must show ONLY this cell's additions. It did: `4 to add, 0 to change, 0 to
     destroy`.
   - `AnalysisReport.schema.json` and `settings.json` are this worker's own IB-s-7 artifacts; one id
     space, no reshaping at the boundary.
   - The `REQ-` id space: `_keys.queue_message` requires an uppercase namespace, so request ids are
     `REQ-` + 24 hex.
   - `gate.destination_for` requires a `gate.BoundRequest`, NOT an `_authz.FirmBinding`. The job
     therefore takes BOTH and REFUSES if they name different firms, rather than silently trusting
     whichever arrived first.

5. **Built `infra/aws/lambda/investor-reporting/ycharts/generate/`** -- four modules, `tests/`,
   `fixtures/har/`:
   - `transport.py` (538 lines) -- the packet's `cloud_transport.py` **MOVED IN**, not imported: a
     Lambda zip cannot import from `docs/`. Three deliberate changes, each named in the header: lazy
     env reads; `ReplayTransport` as a SIBLING class rather than a `live=False` flag on the live one
     (a flag means the live path is one wrong boolean away); and the v0.5 decision table carried in.
     Plus the `waf_action` field and its rule (step 8 below).
   - `recipe.py` (768 lines) -- the seven steps, `VARIANT_BY_COUNT`, `variant_for_comparison_count()`,
     `recipe_for()`, `validate_envelope()` with 17 refusal codes, `generation_body()` (August's 34
     keys, July derived BY SUBTRACTION), `reconcile_owned()` (by opaque deterministic name, NEVER by
     recency), `step_upload()` (RECONCILES expected-vs-echoed rows rather than merely parsing).
   - `job.py` (610 lines) -- Opal's own async job. 8 states, conditional `claim_intent`, duplicate
     re-delivery checked FIRST (before the identity GET), three censuses, `ROUTES = {}`.
   - `templates.json` -- the three templates as CAPTURED CONFIGURATION with their measured outputs,
     the variant selection rules, the comparison catalog and the body shapes.
   - `fixtures/har/` -- 14 files plus `FIXTURE_MANIFEST.json` separating **MEASURED** from
     **EXTENDED**, so the two are distinguishable without trusting any prose.

6. **Built the offline suite** (`tests/run_offline_suite.py`, 793 lines, 11 arms) and `netguard.py`.
   Everything imports with no AWS, no network and no vendor.

7. **Opened the ledger, COMMITTED THE OPEN SENTINEL, uploaded, applied, verified, closed, committed
   the close -- in that order.** The sentinel commit at `9e40afcf4a` exists because of this worker's
   own IB-s-6 finding (row `IRPT_BCKEND-W3-S4`): for a deploy that completes inside one turn, "the
   sentinel is COMMITTED" and "open -> act -> close -> commit -> grade" cannot both be met unless
   there is a commit BETWEEN the open and the close. Now there is, and the sentinel has two commits
   in git (`9e40afcf4a` open, `a0e05b957d` close).

8. **Found a real defect in a NAMED REUSE SOURCE and filed it.** The variants README records a
   measured 202 during calculation polling whose ONLY signal was the `x-amzn-waf-action: challenge`
   RESPONSE HEADER; its body carried the ordinary `calculating` payload. `recovery_contract.decision()`
   classifies a WAF challenge by reading the BODY, so that response classifies `INVALID_RESPONSE` --
   wrong remedy twice over (a challenge treated as a protocol failure, and work discarded that the
   packet's own recovery preserved). This cell's copy adds `Reply.waf_action` and classifies it
   BEFORE the body rules as its own outcome `WAF_REFRESH_REQUIRED`. Filed as row
   **`IRPT_BCKEND-W3-S8`**, INERT here and ARMED for any cell that carries `decision()` verbatim.
   **It surfaced only because the fixture was built from the README rather than from the classifier**
   -- a fixture derived from the code under test would have carried `awswaf` in the body and passed.

9. **Found a stale manifest in my OWN package at report time, and repaired it properly.**
   `FIXTURE_MANIFEST.json` -- the MEASURED-vs-EXTENDED provenance carrier, and a packaged zip
   member -- had gone stale at `88c97c1529`, which changed two of the fixtures it describes
   without regenerating it. Measured by RE-DERIVING every row from disk: 2 of 13 file rows carried
   a wrong sha256 and byte count, and 2 of 4 declared denominators disagreed with the fixtures.
   Filed as **`IRPT_BCKEND-W3-S9`**, repaired by recomputation, and **redeployed** under its own
   change-management entry `irpt-bckend-s9-manifest` -- because a repair that leaves the served
   bytes unequal to the committed source breaks the very equality arm (h) grades. The battery now
   re-derives the manifest on every run, load-bearing in arm (h), with mutant **M4** proving that
   check can fail on a ONE BYTE change.

10. **Graded the criteria under bounds**, recorded verbatim with denominators, then ran the controls
   (four mutants, two determinism runs plus a comparison against the graded run), then wrote the
   proof instance, validated it, and flipped the status.

## Traps hit, and what each cost

- **`safe-commit` `git add -f` force-adds gitignored files under a DIRECTORY pathspec.** A directory
  pathspec staged a 685.5 MB Terraform provider binary out of `.terraform/`; the commit gate caught
  it. Fixed by passing explicit FILE paths. Documented at `.tools/safe-commit.sh:49`.
- **Heredoc backslashes arrive HALVED in the Bash tool.** `src.split("\\n")` became a literal
  newline and a line-continuation backslash was eaten. Every subsequent script was written with the
  Write tool; edits went through the Edit tool.
- **`comp-find --scope all` returned `0 hit(s) across 0 file(s)`** -- which is OUT-OF-CORPUS, not
  absence. The flag is `--corpus all`. A zero that means "I did not look" reads identically to a zero
  that means "it is not there", which is why the denominator line matters more than the count.
- **Adding `WAF_REFRESH_REQUIRED` created a TENTH decision branch** and raised a `KeyError` in the
  v0.8 expectations map -- the map was a forward list. Fixed by adding the branch and moving 9 -> 10.
- **`BROWSER_CHALLENGE` then classified AS `WAF_REFRESH_REQUIRED`**, because its fixture carried BOTH
  signals. Removed `waf_action` from that fixture so the two branches are reached by DIFFERENT
  signals (body interstitial vs response header) and neither rule can pass while the other is dead.

## Surprise rows filed on this order

| id | class | hazard | one line |
|---|---|---|---|
| `IRPT_BCKEND-W3-S7` | OBSERVATION | ARMED | The supplement's variants packet is not in this branch's ancestry; read by object reference at `72acd16e66` and cited that way. |
| `IRPT_BCKEND-W3-S8` | OBSERVATION | ARMED | The carried decision table cannot see a WAF challenge whose only signal is the response header -- and the live run measured exactly that case. |
| `IRPT_BCKEND-W3-S9` | OBSERVATION | ARMED | The fixture manifest -- the MEASURED-vs-EXTENDED carrier, and a deployed zip member -- went stale in my own package; no gate anywhere ties a manifest of hashes to the files it describes. |

Both are ARMED with a `disarm_owner` naming what this cell disarmed SAME TURN and what is the
issuer's / CVO's to route. Neither was worked around silently and neither widened this order.

## Commits on this order (all LOCAL on `wk-irpt_bckend-1-3`)

| hash | subject |
|---|---|
| `5e4a92380b` | IB-s-9: the YCharts generation chain as Opal's own async job -- source |
| `88c97c1529` | IB-s-9: the issuer supplement -- three recipes in one handler |
| `9e40afcf4a` | IB-s-9: commit the OPEN change-management sentinel for irpt-bckend-s9, before the act |
| `a0e05b957d` | IB-s-9: close change-management entry irpt-bckend-s9 -- all five legs proven |
| `a2c335b99e` | IB-s-9: repair the STALE fixture manifest (row W3-S9) and commit the OPEN sentinel, before the act |
| `2146d82bd2` | IB-s-9: close change-management entry irpt-bckend-s9-manifest -- all five legs proven |

Plus the closing commit that carries this log, the result document, the proof instance and the
`<status>` flip.

Two change-management entries, both CLOSED, both with their sentinel committed OPEN before the act
and removed at the close: `20260911T0417Z_irpt-bckend-s9_deploy_completion.md` (the build) and
`20260911T0452Z_irpt-bckend-s9-manifest_deploy_completion.md` (the manifest repair). Six other
seats' entries remain open in this tree and are not mine to close.
