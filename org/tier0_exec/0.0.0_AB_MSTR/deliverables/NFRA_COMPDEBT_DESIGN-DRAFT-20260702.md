# comp-debt — DESIGN (MSTR-authored DRAFT -> CTO arch-gate)

**Charter:** Andrew-direct 2026-07-02 (routed via CTO). Design + build `comp-debt`, a
generalizable comp-tool that identifies estate DEBT with GROUNDED verdicts.
**First consumer:** `NFRA_PIPELINE` (PRD §5) — find deprecated/floating resources to
decommission across 49F/INF/COT. **Then:** powers the cloud-wide `NFRA_DEBTSCAN` expansion.
**Arch-gate:** CTO gates the signal-fusion + verdict schema + the dormant-guard before build.
**Author:** 0.0.0_AB_MSTR. **Status:** DRAFT for CTO arch-gate. **Grounding:** 5-way read-only
fan-out 2026-07-02 (3 direct: graph / dormant-keystone / comp-dups+DEBTSCAN; 2 from those
findings + direct tooling checks: git-heat/usage, cloudtrail/tf-drift — builder confirms
CloudTrail-Lake availability at build).

---

## 1. Thesis — comp-debt is a FUSION + a GUARD, not a new scanner

Two load-bearing findings reshape the build from "a new 6-signal engine" to "a fusion layer + one new guard":

1. **Most signals already have substrate.** comp-dups exists and is the finished DUPLICATES
   signal (with a Rule-22-honest dual-evidence dead-confirm). The graph reachability signal
   already ran (D1 sweep) — including its precision lesson. NFRA_DEBTSCAN is the estate-wide
   sweep+ledger orchestration. So comp-debt REUSES: it *calls* comp-dups (never reimplements),
   *adopts* pipescript's debt-flag vocabulary, and *feeds* DEBTSCAN (which becomes comp-debt's
   estate-wide consumer, not a peer). Only **three signals are genuinely new-build**: CLOUDTRAIL,
   GIT-HEAT, and a unified TF-DRIFT.

2. **The guard is the real product.** Mechanical signals CANNOT discriminate keep-from-kill:
   a deliberate belt and a corpse look identical on every signal — both `state="DISABLED"`,
   both zero-invocation, both zero graph-consumers. Only the **intent annotation** (the comment
   explaining *why* it is idle) separates them, and **no structured keep-dormant registry exists
   today**. comp-debt's core value is the dormant-vs-dead guard + the registry it must build.

Proof the signals don't discriminate (both literally say "dormant"):
- KEEP: `infra/aws/terraform/inf-pipeline/eventbridge.tf:218` — `state="DISABLED"`, *"WIRED-NOT-ARMED ... arm via state=ENABLED."*
- DEAD: `infra/aws/terraform/bd-pipeline/lambdas.tf:241` — *"DECOMMISSIONED ... superseded by D_02."*

---

## 2. Architecture

```
comp-debt/
  grounding_lib.py     # SHARED: dual-evidence dead-confirm (lifted out of dup_scan.py)
                       #   verdict = graph-zero-consumer AND metric-zero-over-N-day-window
                       #   verdict STRING carries the window; either-leg-alone => INFERRED
  signals/
    graph.py           # REUSE: comp-kuzu/blast/xref/pipescript + FP-suppression overlay
    duplicates.py      # CALL comp-dups (dup_scan.run_scan) — thin adapter, no fork
    tf_drift.py        # NEW: comp-iam reconcile (DESIRED-TF vs LIVE) + live-aws for fresh
    cloudtrail.py      # NEW: CW invocation-metrics (15mo) primary + CloudTrail cross-confirm
    git_heat.py        # NEW: last-commit-touch + last-repo-reference over N days
    usage.py           # REUSE: agent_telemetry/ + comp-which-rail.log + comproute-routing
  dormant_guard.py     # KEYSTONE: intent-annotation discriminator + keep-dormant registry read
  fuse.py              # per-resource 3-way verdict + per-signal grounding cite + firm-scope
keep-dormant.yaml      # NEW registry (org/modules/graph/) — the guard's lookup source
```

**comp-debt = the per-signal engine library + grounded-verdict fusion + the guard.**
**NFRA_DEBTSCAN = the estate-wide orchestration that runs comp-debt nightly** and files graded
findings into its existing ledger (`org/modules/graph/debtscan/`, dated + `*_latest`), under its
CVO >=0.80 precision gate + verify-before-delete doctrine. comp-debt emits into the DEBTSCAN
ledger schema so each signal is just a new family in the existing burn-down.

---

## 3. The six signals (source · detects · grounding · maturity)

| Signal | Source (reuse/new) | Detects | Grounding cite | Retention | Maturity |
|---|---|---|---|---|---|
| **GRAPH** | comp-kuzu/blast/xref/pipescript (reuse) | no-consumer / orphaned-output / producer-nothing-reads | node-id + snapshot-id + file_path | graph vintage (carry BEHIND/age) | ran @ **0.70** precision — needs the overlay below |
| **DUPLICATES** | comp-dups (call) | TF-label-collision / content-dup / multi-homed | resource-id + module-path + BM25 + `dead_status` window | nightly | **DONE** — call it |
| **TF-DRIFT** | comp-iam reconcile + live-aws (new fusion) | live-absent-from-TF, or TF-declared-not-applied | role/resource-id + TF path + live `get-*` | live | new-build (reconcile is census; fresh => live) |
| **CLOUDTRAIL** | CW metrics + CloudTrail (new) | 0 invocations/events over N days | resource-arn + CW metric + window | CW 15mo / CT 90d(+Lake) | new-build |
| **GIT-HEAT** | git (new) | file untouched + unreferenced N days | file:line + last-commit SHA/date | full history | new-build (trivial) |
| **USAGE** | agent_telemetry/ + rail-log + comproute (reuse) | tool/artifact un-invoked over N days | log line + timestamp | ~10-30d (bounded — carry it) | partial (rail-tools only today) |

**Note (served-artifact query-log gap):** served JSON is read by the portal from S3 via
CloudFront; there is no Trino/Athena query-log over it. The only "cold served artifact" signal is
S3/CloudFront access logging (confirm enabled at build); absent that, USAGE covers tools, not
served artifacts — state the gap, never a false-clean.

---

## 4. Verdict schema (per NFRA_PIPELINE §5 / §4.2 / §7.2-AC2)

```json
{
  "resource_id": "<type>:<id>", "firm": "bd|cot|inf|shared",
  "verdict": "LIVE-KEEP | KEEP-DORMANT | DEBT-DECOMMISSION",
  "debt_subtype": "no-consumer|cold|dead|duplicate|un-managed|null",
  "signals": [ {"signal":"graph","state":"orphan","grounding":"node 7978..@snap; file:line",
                "level":"INFERRED|CONFIRMED"} , ... ],
  "keep_dormant": {"ruled": true, "tier":"A|B|C", "evidence":"file:line intent-annotation"},
  "confidence": "advisory|grounded",            // grounded only when >=1 CONFIRMED signal + no contra live-use
  "action": "none (emit-only)"                  // comp-debt NEVER acts
}
```

**AC2 bar (machine-checkable):** a `DEBT-DECOMMISSION` verdict requires **>=1 CONFIRMED signal
AND no contradicting live-use AND the keep-dormant guard ruled-out**. Anything short = KEEP-DORMANT
or advisory-only.

---

## 5. THE KEYSTONE — the dormant-by-design vs dead guard

**Default fail-safe:** a resource that trips only the mechanical debt-signals (Tier-C below)
defaults to **KEEP-DORMANT, never DEBT.** Flip to DEBT only when a Tier-A/B keep-signal is
affirmatively *ruled out* AND a positive dead-marker is present ("superseded by X", "not consumed",
"cleanup tracked"). Rationale (Andrew/§5): a false-negative (miss a corpse) is recoverable; a
false-positive (decommission a deliberate belt) is THE named failure mode.

**Discriminators, ranked:**
- **Tier A (any ~sufficient => KEEP-DORMANT):** an explicit `keep-dormant.yaml` / `opal:lifecycle=keep-dormant` tag [**to build**]; an adjacent intent-annotation with a re-arm verb ("arm via ENABLED", "wired-not-armed", "DEPLOYED DORMANT", "go-live gated on X"); a documented rollback path / `lifecycle.ignore_changes` protecting an operationally-flipped value (the mdpf `custody_source` pattern); named in a CLAUDE.md NEVER/rollback rule or a change-management LEVER/rollback ledger; wired-as-fallback-in-code (a live env-gate branch even if defaulted off).
- **Tier B (corroborating):** referenced in a runbook/SOP as the manual/emergency path; a QA keep-warm node whose alarm *acknowledges* the idle as by-design; a `DISABLED` rule whose target function is live via another path.
- **Tier C (NEVER sufficient alone — these ARE the debt signals):** bare `DISABLED`, 0 CloudTrail, no graph consumer, git-cold, un-queried.

**The registry to build (the gap):** no keep-dormant tag/registry exists today (grep-confirmed);
intent lives only as unstructured prose. comp-debt builds `org/modules/graph/keep-dormant.yaml`
(resource-id + reason + rearm-condition + owning-annotation-cite), seeded from the Tier-A
annotation parse. Then the guard becomes a lookup, not a comment-parse. Real KEEP examples the
registry must capture (all file:line-grounded): inf `wired-not-armed` rule, ycharts deployed-dormant
lambda, mdpf `custody_source` rollback lever (`lifecycle.ignore_changes`), the LEVER-2 manual-SSM
dispatch in the custody-flip ledger, bd-gold-qa-runner manual-dispatch belt, deliberately-un-managed
`secret_version`s (a TF-DRIFT false-positive trap — must NOT read as drift-debt).

---

## 6. Grounding discipline (Rule 22 — non-negotiable, every signal)

- **Two-layer per candidate:** the signal is the SYMPTOM = **INFERRED**, non-actionable. Promotion
  to a reserved word ("dead"/"unused"/"provably") REQUIRES a live/source confirm leg — CW
  last-invocation for a lambda, `s3api list-object-versions`/`head-object` for a key,
  `sns list-subscriptions-by-topic` for a topic, dispatcher-catalog source-grep for a gold script.
  Cite `desired`(graph/TF) + `applied/exercised`(live primitive).
- **FP-suppression overlay (graph):** run every graph orphan through the 14 documented classes in
  `suppression_v1.yaml` (`FP_API_LAMBDA`, `FP_ECS_TRIGGER`, `FP_INF_DISPATCHER_CATALOG`,
  `FP_MDPF_UNSTITCHED`, `FP_SECRET_RUNTIME_ACCESS`, ...). The D1 sweep's 0.70 precision was 100%
  one mechanism: **absent-edge-because-unmodeled misread as absent-edge-because-dead.** Disambiguate
  explicitly or the tool false-decommissions live resources.
- **Precision gate:** verdicts stay ADVISORY below the CVO >=0.80 precision bar; reserved words
  illegal until source-confirmed AND above gate.
- **Vintage-carry:** propagate the comp-kuzu provenance header (built-age / BEHIND / UNKNOWN
  VINTAGE) + the resolver's `generated_from` date into every verdict; a stale/behind graph =>
  UNVERIFIABLE, never clean.

---

## 7. Invariants (from §9 / Rule 13 / CLAUDE.md)

- **Firm-separation is a hard param.** `comp-debt --firm {bd|cot|inf}`; bd/cot/inf signals NEVER
  cross (gate + IAM). cot is a completely separate firm from bd.
- **Ground on LIVE, not TF-desired** for TF-DRIFT (comp-iam default = DESIRED/census; use reconcile
  + live `get-*` for a fresh/in-flight change).
- **Emit-only — comp-debt NEVER acts.** Decommission is downstream, `comp-blast`-preceded
  (zero-consumer confirm) and **human-gated for unrecoverable classes** (EC2 stop/terminate,
  S3 delete, IAM-role delete = CTO arch-gate + COO + Andrew confirm-first on specific IDs).
- **Generalizable — no hardcoded pipelines.** The 49F/INF/COT pass is the proving template;
  NFRA_DEBTSCAN cloud-wide reuses the identical tool/schema.

---

## 8. Build plan (sequencing; parallel with NFRA_PIPELINE — design doesn't gate on the pipelines)

1. **`grounding_lib.py`** — lift the dual-evidence dead-confirm out of `dup_scan.py` into a shared
   library every signal uses (this generalizes the one place the Rule-22 discipline already lives).
2. **`dormant_guard.py` + `keep-dormant.yaml`** — the keystone + its seeded registry. CTO arch-gates
   this specifically (§5 FP-guard). Highest governance value; build first alongside (1).
3. **REUSE adapters** — `duplicates.py` (call comp-dups), `graph.py` (comp-kuzu + FP overlay +
   pipescript flags), `usage.py` (telemetry read). Low new-code.
4. **NEW signals** — `git_heat.py` (trivial), `tf_drift.py` (reconcile+live), `cloudtrail.py`
   (CW-metrics + CloudTrail; confirm Lake availability).
5. **`fuse.py` + `--firm`** — 3-way verdict + per-signal grounding + firm-scope.
6. **DEBTSCAN integration** — comp-debt emits the DEBTSCAN family schema; wire the owed comp-dups
   nightly-post-derive hook in the same cadence TO.

**Ownership:** MSTR owns the design + the governance-critical dormant-guard; the heavy signal-code
build delegates to a builder-lane UNDER MSTR ownership + CTO arch-gate (not hand-coded in-session).

---

## 9. Open questions for the CTO arch-gate

1. **keep-dormant registry form** — a repo YAML (`keep-dormant.yaml`, source-of-truth, git-reviewed)
   vs an AWS tag (`opal:lifecycle=keep-dormant`, live but drift-prone) vs both (YAML canonical + tag
   projected). MSTR lean: **YAML canonical** (reviewable, firm-scopable, no live-drift), tag optional.
2. **precision-gate owner per signal** — does each new signal (cloudtrail/git-heat/tf-drift) need its
   own CVO precision adjudication before non-ADVISORY, like D1 did? MSTR lean: **yes** (per-signal
   >=0.80 before it can authorize even a human-gated decommission).
3. **USAGE served-artifact gap** — accept "tools-only" coldness for v1, or block on enabling
   S3/CloudFront access logging for served-artifact coldness? MSTR lean: **v1 tools-only + state the
   gap loudly**, served-artifact coldness a fast-follow.
4. **builder-lane assignment** — which lane builds the signal-code under MSTR+CTO (a DE/AE, or the
   graph-module owner given the heavy comp-kuzu/DEBTSCAN reuse)?
