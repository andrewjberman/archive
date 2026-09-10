# TO NFRA_SYSPARITY.TO-RB1-SITEZ -- CLOSE THE RULE-BANK VERSION DRIFT: head is v1.8, EIGHT SDK assertion sites across SEVEN files still assert v1.2, and the eighth file's hits are a DELIBERATE NEGATIVE CONTROL that must not be touched

<to_id>NFRA_SYSPARITY.TO-RB1-SITEZ</to_id>
<project>NFRA_SYSPARITY</project>
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_date>2026-09-09</issued_date>
<status>complete</status>

**BLOCKER: NONE. GO immediately.** Bounded, measured, and reversible. Nothing here deploys and nothing here touches AWS.

---

## AUTHORITY

**ANDREW-DIRECT 2026-09-09 ~22:3xZ at the `1.0.0_SA_CTO~Z` terminal, VERBATIM: "Yes agreed with COO~Z."** Given in answer to `/open-calls` CALL 2 of 3, whose REC was, verbatim: *"Hand it to `2.0.0_SA_COO~Z` as one cell in an existing round rather than seating a lane for it."* Relayed by `1.0.0_SA_CTO~Z` at msg 20661, which stated it was relaying and not directing: how it is cut, and where, is this issuer's.

**WHY IT WAS UNOWNED:** lane `0.8.0_AE_CloudComp` is not seated, so there was no agent to route it to, and it drifted all session. **The card's own argument was that waiting for a lane to be seated is how it reached ~20 days.**

## WHY THIS FACE SITS ON `NFRA_SYSPARITY` AND NOT IN AN OPSEC ROUND -- DISCLOSED, NOT GLOSSED

The rec says "one cell in an existing round". **That literal mechanism was not available and the reason is mechanical rather than preference:**
- The only round this issuer owns is `NFRA_OPSEC202609`, which is `EXECUTING` -- and **Rule 27 freezes the decomposition mid-round**, so no cell can be added to it.
- The rule-bank surface is also outside that PRD's ratified territory, so a cell there would be a scope violation even unfrozen.
- `NFRA_COMPEFFICACY` is `ROUND_CLOSE` with **no COO seated**, and seating one is Andrew's act.

**`NFRA_SYSPARITY` is `status: active`, REOPENED 2026-09-01, and NOT pipeline-registered (`dep_stage` absent), and `infra/system/system_parity.py` is literally its surface.** So the INTENT is executed exactly -- folded into an existing active project, handed to an ALREADY-SEATED agent, no lane seated, no frozen decomposition touched -- while the stated mechanism is departed from and said so here. This paragraph is the disclosure; it also rides this issuer's next message to `1.0.0_SA_CTO~Z`.

## THE DRIFT, MEASURED AT THIS SEAT AND NOT INHERITED

`comp-find 'rule-bank v1\.' infra/system` -- **DENOMINATOR: 11 hits across 173 files scanned.** Head is **v1.8**, read at source: `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml:12` `version: "1.8"`. That file states its own rule: *"Version scheme = meta.version, bumped ONLY by explicit promotion with a printed denominator (LAW-2)"* and names itself `canonical_source`.

**THE EIGHT SITES ACROSS SEVEN FILES -- this is the work:**
```
infra/system/sdk/gensdk/scaffold.py:62                                    version: "rule-bank v1.2 (...)"
infra/system/sdk/gensdk/scaffold.py:144                                   ontology_ref: "... rule-bank v1.2 ..."   <- SAME FILE, two sites
infra/system/sdk/00_manifest/examples/fork-attempt.company.yaml:63        version: "rule-bank v1.2 (...)"
infra/system/sdk/00_manifest/examples/sandbox.company.yaml:56             version: "rule-bank v1.2 (...)"
infra/system/sdk/tenants/acme/adapters/acme-canon-patterns.yaml:7         ontology_ref: "... rule-bank v1.2 ..."
infra/system/sdk/tenants/acme/company.yaml:51                             version: "rule-bank v1.2 (...)"
infra/system/sdk/tenants/demo/adapters/demo-canon-patterns.yaml:7         ontology_ref: "... rule-bank v1.2 ..."
infra/system/sdk/tenants/demo/company.yaml:51                             version: "rule-bank v1.2 (...)"
```
Seven files, eight sites -- `scaffold.py` carries two. This count was reached independently here and MATCHES `3.0.0_SA_CVO~Z`'s corrected figure of 7 files / 8 sites.

## THE EXCLUSION -- THE ONE THING THIS FACE CAN GET WRONG CHEAPLY

⛔ **`infra/system/system_parity.py` IS NOT IN SCOPE AND ITS THREE HITS MUST NOT BE "FIXED".** They are the tool's OWN TEST FIXTURES and are self-excluded by design:
```
:574  "doc_ok.md":   "carries rule-bank v1.2 here"
:675  "rb_req.md":   "carries rule-bank v1.2 here"
:676  "rb_stale.yaml": "adapter pinned at rule-bank v1.1"      <- THE NEGATIVE CONTROL
:692  chk("23 COVERAGE MUTANT (rulebank shape): required doc current but v1.1 site stale -> FAIL"
```
⭐ **THE `v1.1` AT :676 IS A DELIBERATE NEGATIVE CONTROL AND :692 IS THE MUTANT THAT CONSUMES IT.** "Fixing" it would make the mutant pass on a stale site and **destroy the discrimination the check exists to provide** -- a silent, permanent loss of a control, which is worse than the drift this face closes. Verified at this seat with `comp-read --enumerate`: all four hits band as CODE, none in a docstring or comment.

## THE WORK

Move the eight sites to the head version. **Reuse the existing string shape at each site rather than inventing a new one** -- some read `version: "rule-bank v1.X (...)"` and some `ontology_ref: "NFRA_ONTOLOGY rule-bank v1.X, vocabulary-bound (...)"`.

⚠ **READ THE PARENTHETICAL BEFORE BUMPING THE NUMBER.** Every site carries a ratification pin alongside the version -- `LD-0311 @086238604`, some also `LD-0315`. **A bump that moves `v1.2` to `v1.8` and leaves a v1.2-era ratification pin behind is a HALF-FIX that reads as complete.** Whether those citations move too is `RB1-AC4` and is a judgment, not this face's to decide alone.

<expected_criteria>RB1-AC1, RB1-AC2, RB1-AC3, RB1-AC4</expected_criteria>

<criterion id="RB1-AC1"><invocation>comp-find 'rule-bank v1\.' infra/system --limit 40</invocation><expect>The denominator RE-ESTABLISHED at the worker's own vintage before any edit, with the hit count and files-scanned stated. If the set is no longer 11 hits / 8 in-scope sites / 3 fixture hits, STOP and report -- another seat has moved it and this face's premise is falsified. A census taken after the edit is not a baseline.</expect></criterion>

<criterion id="RB1-AC2"><invocation>comp-find 'rule-bank v1\.2' infra/system --limit 40</invocation><expect>ZERO in-scope hits remain after the edit, with the fixture hits in system_parity.py explicitly enumerated as the only survivors and named as such. State the denominator, not just the zero -- a zero over an unstated scope is not evidence.</expect></criterion>

<criterion id="RB1-AC3"><invocation>python infra/system/system_parity.py --self-test</invocation><expect>The NEGATIVE CONTROL SURVIVES: system_parity.py unmodified (git diff shows zero changes to it) AND its self-test still passes, including the "23 COVERAGE MUTANT (rulebank shape)" arm that consumes the v1.1 stale site. If the tool has no --self-test flag, state the actual invocation used and its result. A mutant that no longer discriminates is a FAIL even if every other criterion passes.</expect></criterion>

<criterion id="RB1-AC4" judgment="true"/>

<preflight>
comp-schedule: RUN 2026-09-09 ~23:0xZ at the issuer's seat. REACHED-DENOMINATORS C1=23, C2=7, C3=12, C4=20, C5=335; the three DECIDABLE carriers arm **26** gates (C1 23 sentinel lines -> 7, C2 7 open deploy-ledger entries -> 7, C3 12 standing NEVER clauses -> 12); C4 SEMI-DECIDABLE 20 -> 0; C5 NOT-DECIDABLE 335 -> 0, of which 137 are non-null prose and are **a reading list, never gates**. **ZERO gates name NFRA_SYSPARITY.** The two DRIFT CANDIDATES are `G-3` (owner CTO, the never-widen co-sign on inf silver) and `G-7` (owner POD4, the trading-calendar guard); **neither binds this face.** ⛔ **The DEPLOY-LEDGER carrier does NOT bind here** -- this face deploys nothing, writes no AWS resource and opens no ledger; it edits eight version strings in repo files. Orientation at its stated vintage, never a criterion.
comp-iam: DECLARED-NOT-APPLICABLE -- this face creates no role, attaches no policy, and makes no AWS call of any kind. There is no IAM surface to verdict.
comp-adversary: DECLARED-NOT-APPLICABLE -- this face pins no commit-scoped claim at cut. Its one inherited figure (7 files / 8 sites) was RE-DERIVED at the issuer's seat with `comp-find` and its denominator is printed on the face; `RB1-AC1` re-establishes it again at the worker's own vintage rather than carrying it forward on trust.
</preflight>

# pipeline-override: NFRA_SYSPARITY declares no dep_stage and this TO genuinely stands OUTSIDE the pipeline -- it has no PRD, no decomposition, no round and no L5/L6 limb. It is a bounded hygiene correction assigned directly by Andrew (2026-09-09 ~22:3xZ, "Yes agreed with COO~Z") to an already-seated lane. SETTING a dep_stage on that project row would be the WORSE act: it would assert a machine-readable pipeline stage that does not exist, to satisfy a gate rather than to describe the world. The <preflight> limb the same gate asked for is PRESENT above and was not overridden -- only the dep_stage limb is, and only because the honest value is ABSENT rather than unset.

<proof_of_spec>
Criterion ids minted at cut by the issuer: `RB1-AC1`, `RB1-AC2`, `RB1-AC3`, `RB1-AC4`. The ASSIGNEE fills a `PROOF_OF_SPEC.schema.json` instance under its own deliverables home and validates it with `.tools/proof-of-spec-check.py <instance> "RB1-AC1,RB1-AC2,RB1-AC3,RB1-AC4"` BEFORE the complete flip. **`RB1-AC1` is the control that must be able to fail:** a changed census means the premise moved and the correct act is to stop. **`RB1-AC4` is a JUDGMENT criterion and carries no verdict from this lane** -- whether the `LD-0311 @086238604` ratification pins alongside each version string must move with the version, or whether they correctly record the ratification of the SHAPE rather than of the current head, is reserved. Record it `UNVERIFIABLE-BY-INSTRUMENT` with a `status_reason` naming the adjudicating seat. Every `surprises` entry opens with a row id.
</proof_of_spec>

<compiler_tools_mandate>
  <phase id="1" when="before write">Re-ground the census (RB1-AC1) and read the canonical rule bank's own version rule at `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` before assuming what "head" means.</phase>
  <phase id="2" when="before commit">Confirm `git diff` shows ZERO changes to `infra/system/system_parity.py`. That file appearing in the diff at all is the failure this face is most likely to produce.</phase>
</compiler_tools_mandate>

<paths>
infra/system/sdk/
infra/system/system_parity.py
org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml
org/tier2_senior/0.7.0_AE_CloudOps/task_orders/NFRA_SYSPARITY.TO-RB1-SITEZ.rule-bank-version-drift.md
</paths>
