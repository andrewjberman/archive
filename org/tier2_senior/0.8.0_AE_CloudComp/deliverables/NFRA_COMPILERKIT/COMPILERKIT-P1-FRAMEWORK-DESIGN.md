# NFRA_COMPILERKIT-P1 -- Recognizer-SDK FRAMEWORK DESIGN (RAVC COO + CTO)

**Author:** 0.8.0_AE_CloudComp~D (framework-lead, MSTR-assigned). **2026-07-07.**
**Pair:** 0.4.0_DS_ClientPlatform~A (recognizers; author-DS / commit-AE, org/modules/graph is exec-lane).
**Reconcile-not-build:** `comp_ladder.py` (proto Recognizer/Rule SDK + fidelity gate) + `cse_schema.py`
(the CSE IR: enums + fail-closed validator + CloudNode/CloudEdge mapping + parity/coverage) are the
CONTRACT. P1 = reconcile the 2 EXISTING production compilers onto it as a parity-oracle PAIR.
**CTO #3 ruling (binds the whole SDK):** COMPILERKIT = PURE-LEXICAL provenance ONLY ({source,locus,evidence}
= file:line). The boto3/live-AWS recognizers (compiler #1's #11 LIVE-AWS + extract_event_invoke) RE-HOME to
FEDOBS -- NOT this framework (a mutable runtime api-response is non-lexical/non-deterministic -> erodes
fidelity, LAW 1).

---

## 1. What the framework is (the keystone)

ONE shared Recognizer SDK both production compilers realize, so a new recognizer is a modular, orthogonal,
additive, deterministic unit that composes with no ordering deps and passes the SAME fidelity + parity gates.
The two compilers become a PARITY-ORACLE PAIR: refactored onto the SDK, each must REPRODUCE its current C1
graph (AC2) -- the parity oracle is the refactor's safety net.

Pipeline (PRD 4.1, both compilers already realize this shape):
```
  source artifact --[front-end adapter]--> EnrichedTree --[recognizers]--> CSE(C0 Entity + C1 Relationship,
                                                                            each w/ file:line provenance)
                 --[materializer]--> CloudNode/CloudEdge   --[fidelity_check@build + parity-oracle]--> gate
```

## 2. The interface DS~A builds against (a-d she asked for)

### (a) The Recognizer base
```python
class FrontEndCapability(IntEnum):        # ordered tiers; a recognizer declares the MINIMUM it needs
    RAW_TEXT          = 0                  # line/regex over source text (TF jsonencode, heredoc dispatch)
    LEXICAL_AST       = 1                  # python `ast` -- coarse, single-file, no cross-file resolution
    RESOLVED_SEMANTIC = 2                  # ts-morph TypeChecker.getSymbol -- cross-file RESOLVED edges

@dataclass
class Site:                               # one candidate lexical locus a recognizer found
    source: str                           # repo-relative file
    locus: str                            # "L{n}" or "L{a}-{b}"
    evidence: str                         # the LITERAL bytes at that locus (comp_ladder C0 style)
    payload: dict = field(default_factory=dict)   # recognizer-local extracted data

class Recognizer(ABC):
    artifact_class: str                   # "python" | "terraform" | "tsx"
    concept: str                          # "s3-key-const" | "flows-to" | "tf-iam-policy" | ...
    requires: FrontEndCapability          # the tier this recognizer needs to be HONEST

    @abstractmethod
    def iter_sites(self, tree: "EnrichedTree") -> Iterable[Site]: ...
    @abstractmethod
    def emit(self, site: Site, tree: "EnrichedTree") -> list[CSE]: ...

    def recognize(self, tree) -> list[CSE]:          # SDK-provided; capability-gated (see (b))
        if tree.capability < self.requires:
            return [self.degrade(site) for site in self.iter_sites(tree)]   # LAW-1 honest-degrade
        return [cse for site in self.iter_sites(tree) for cse in self.emit(site, tree)]
```
DS~A writes `iter_sites` + `emit` per recognizer; the SDK owns `recognize()` (capability-gating + degrade).

### (b) The capability-tiered enriched-tree (hard-part #1 resolution)
`EnrichedTree` = a normalized tree from a front-end adapter carrying per-node provenance + its capability
tier. A recognizer DECLARES `requires`; the registry only dispatches it to a tree whose front-end supplies
`capability >= requires`. A front-end that CANNOT supply the needed tier -> `degrade()` emits
`Concept(untyped)+confidence<=0.34` (LAW 1) -- NEVER a downgraded guess. This is the AST-vs-regex impedance
answer: #2's recognizers (RESOLVED_SEMANTIC) simply don't run -- honestly -- on a LEXICAL_AST tree.
```python
class FrontEnd(ABC):
    capability: FrontEndCapability
    lifecycle: str                        # "per-artifact" (#1) | "whole-project" (#2)  (hard-part #2)
    @abstractmethod
    def build_trees(self, scope) -> Iterable["EnrichedTree"]: ...
```
Two lifecycles, one interface (hard-part #2): `PerArtifactFrontEnd` (compiler #1: parse each file/TF ->
authoritative-map assembly) and `WholeProjectFrontEnd` (compiler #2: persistent ts-morph Project +
incremental 1-level dependent closure). The registry iterates `front_end.build_trees(scope)` and runs the
capability-matched recognizers over each tree -- incrementality is the front-end's concern, not the recognizer's.

### (c) The CSE-emit contract (provenance binding)
The SDK provides `emit_cse(...)` -- a recognizer CANNOT emit an invalid CSE (it `validate_or_raise`s):
```python
def emit_cse(*, verb, subject: EntityRef, edges: list[RelationshipDelta], provenance: Provenance,
             confidence: float, marker_head: str, producer_kind, compiler_id, artifact_class) -> CSE:
    cse = CSE(event_id=..., schema_version=SCHEMA_VERSION, producer={"kind":producer_kind,...},
              compiler={"id":compiler_id,"artifact_class":artifact_class,"version":...},
              transformation={"verb":verb,"subject":subject,"edges":edges},
              provenance=provenance, execution_meta=..., head={"marker_head":marker_head},
              qualifiers={"confidence": confidence})
    validate_or_raise(cse)          # fail-closed: off-enum/provenance-less/non-decompressible -> raise
    return cse
```
Provenance binding: `provenance = Provenance(source=file, locus="L{n}", recognizer=self.concept,
evidence=<literal bytes>)`. Entity/Relationship come from `cse_schema` enums (subject etype in Entity,
edge rtype in Relationship). `to_ladder_node(cse)` -> `fidelity_check` guarantees decompression (AC6).

### (d) The hot-reloadable registry (+ the PROMOTE-seam)
```python
class RecognizerRegistry:
    def register(self, r: Recognizer) -> None       # keyed (artifact_class, concept); dup = error
    def hot_reload(self, recognizers_dir: str)       # load new/changed recognizers w/o restart (CVO gap#8)
    def recognizers_for(self, artifact_class, capability) -> list[Recognizer]   # capability-matched
```
**"Name the hot-registration SEAM with PROMOTE" (my interpretation -- CONFIRM):** the registry's hot-register
entrypoint is a NAMED SEAM registered as a critical surface (comp-surface-check) + exercised by `/seams`
(mechanical: a registered recognizer actually dispatches; declarative: the registry manifest matches the
loaded set; semantic: its CSEs pass parity). I read "with PROMOTE" as: a newly hot-registered recognizer is
surfaced (PROMOTE-class event) so a silent no-op registration can't hide. Flagging for CTO/COO confirm --
alt reading = wire it to the COMPROUTE PROMOTE mechanism (TH-C), which I can do if that's the intent.

## 3. The parity-oracle + fidelity gates (AC2 + AC6)
- **fidelity@build (AC6):** every emitted CSE -> `to_ladder_node` -> `fidelity_check`; a non-decompressible
  (latent) CSE = build FAIL = NOT DONE. Already enforced in `cse_schema.validate` S3.6.
- **parity-oracle (AC2):** per compiler, run ALL its recognizers over a fixed source scope -> materialize
  the CSEs to CloudNode/CloudEdge -> structurally diff vs the CURRENT graph -> assert reproduction. The
  `cse_schema.parity_check` scaffold proves MAPPING totality (the precondition); the full round-trip diff
  needs a live-graph EXPORT -- I own the export+diff harness (cse_schema flags "consult 0.8.0"). This is the
  framework's build-gate; every recognizer refactor must hold parity before it lands.

## 4. Open decisions for CTO (BEFORE DS~A builds against the affected parts)
1. **FLOWS_TO KIND + condition (hard-part #4, LOAD-BEARING):** compiler #2's most valuable recognizer is
   FLOWS_TO with a KIND discriminator (passthrough/rename/recompute-guarded) + condition -- the spread-bug
   the regex can't see. The current `RelationshipDelta = {rtype, target, verb}` has NO place for edge-KIND
   or condition. Generalizing without it REGRESSES the capability that justified TSGRAPH. cse_schema is
   CTO-arch-gated (a governed version-bump). PROPOSAL: bump the CSE algebra to add
   `RelationshipDelta.kind: str` + `RelationshipDelta.condition: str` (optional; empty for edges without a
   discriminator). NEEDS CTO ratification (schema version-bump 0.1 -> 0.2) before compiler #2's FLOWS_TO
   recognizer is built. This is the #1 blocking design decision.
2. **PROMOTE-seam meaning (see 2d)** -- named-critical-surface seam vs COMPROUTE-PROMOTE wire. CONFIRM.
3. **Uniform coverage/no-silent-Unknown parity (hard-part #5):** compiler #2's coverage model
   (coverage{attempted,resolved} + unresolved[] + collapse-detector) is far richer than #1's. PROPOSAL:
   the SDK MANDATES a uniform coverage contract (every `recognize()` returns a `Coverage{attempted,
   resolved, unresolved[]}` alongside its CSEs) so a weak recognizer can't silently under-report while
   parity passes. Adopt #2's model as the SDK reference. CTO confirm it's mandatory (AC3).
4. **CSE store/materializer** (AC-emission): P1 emits CSEs; the CSE->CloudNode/CloudEdge materializer +
   store is NFRA_CSE P2 (cse_schema S6). P1's parity-oracle needs only the in-memory materialize+diff.
   Confirm P1 scope excludes the persistent writer.

## 5. Sequencing (unblocks DS~A now)
- **DS~A starts NOW** on the parity-critical PURE-LEXICAL recognizers that DON'T depend on the open items:
  compiler #1's #1-3 (S3-key-const [ast], dispatch-catalog [regex, the D1-class she owns], read/write-
  classifier) + her 3 in-flight DEBTSCAN lexical dispatch/read recognizers (same family). Interface = the
  Recognizer base + emit_cse above (provisional; stable for these).
- **HELD for CTO ruling #1:** compiler #2's FLOWS_TO recognizer (needs the KIND/condition schema-bump).
- **I build the SDK skeleton** (`comp_recognizer_sdk.py`: Recognizer/FrontEnd/Site/EnrichedTree bases +
  emit_cse + RecognizerRegistry + the parity-oracle harness + a runnable self-test) on RAVC-ACK -- the
  concrete interface DS~A imports; commit into org/modules/graph (exec-lane, AE-committed per the pattern).
- **Each recognizer = AC2 parity-oracle + AC6 fidelity.** DS~A authors -> I commit+wire+run parity ->
  confirm reproduction. CTO arch-gates the SDK shape + the schema-bump.

## 7. Survey corroboration -- material sharpenings (fold into the build)

An independent structural survey of both compilers corroborated the recognizer-map and sharpened four
load-bearing points:

1. **FEDOBS carve-out is NARROWER than the pre-stage said -- ONLY Pass 8 leaves.** In `build_graph`, the
   ONLY live-boto pass is **Pass 8 `extract_event_invoke`** (list_event_source_mappings / list_subscriptions
   / get_bucket_notification_configuration; edges tagged `provenance:"live-derived"`). **Pass 7 `extract_sfn`
   is a FALSE ALARM -> it STAYS in COMPILERKIT:** it imports `comp_aws_cli` only to reuse the PURE-PYTHON
   ASL-string walker (`_sfn_task_invokes`); boto3 is lazy and NEVER called ("zero API calls",
   extract_sfn.py:15-16,90). So the FEDOBS re-home set = Pass 8 + the standalone live satellites
   (`comp_aws_cli`, `extract_iam`'s `boto3.client('iam')` leg) -- NOT Pass 7. The COMPILERKIT pure-lexical
   set for #1 = Passes 2,1,4,4b,5,6,7 (S3/api/eventbridge/lambda-ec2/lambda-routes/pipeline-DAG/SFN-ASL).
2. **The biggest reconcile = PROVENANCE-GRAIN UPLIFT on compiler #1.** #1's `TraceGraph.Node` carries
   `file_path + function_name + source_sha` -- **NO line number** (freshness is SHA-drift, not locus). The
   CSE contract (LAW 2) requires `provenance.locus` = file:line evidence. So #1's pure-lexical passes must be
   UPLIFTED to line-grain: capture the match line at recognition. TEMPLATE EXISTS -- #1's own satellites
   `extract_iam`/`extract_transforms` already compute `line = content[:pos].count('\n')+1`. This is a
   concrete refactor line-item per recognizer (not a redesign): each `iter_sites` records the Site.locus.
   #2 (ts-morph) already emits file:line everywhere (`getStartLineNumber()`), so it satisfies the contract
   as-is. => the parity-oracle for #1 must tolerate the ADDED locus (a strict superset of today's node attrs;
   parity is on the node/edge SET, locus is additive provenance -- confirm the oracle keys on id+type, not
   the full attr blob).
3. **C0/C1 (extract/detect) split -- #2 has it, #1 fuses it.** #2 cleanly separates structural extraction
   (`extractor_full.ts`) from query-time detection (`tsgraph_detectors.yaml` over Kuzu) -> maps directly to
   CSE C0 (structural sites) + C1 (derived claims). #1 FUSES recognition + edge-emit in each pass. The SDK's
   Recognizer(C0)/Rule(C1) split (comp_ladder already models it) is the reconcile direction -- #1's passes
   decompose into a C0 recognizer (emit the site) + a C1 rule (the edge). Low-risk: the edge is already there;
   we're just naming the C0 site under it (which the fidelity gate REQUIRES anyway).
4. **Coverage/no-silent-Unknown -- mandate #2's model (open-decision #3).** #2 records every unresolved in
   `unresolved[]` + coverage{attempted,resolved} + a collapse-detector; #1 silently defaults unknowns to
   READS (documented `BLAST_EDGE_CAVEAT` over-report). The SDK MUST make the coverage channel first-class so
   #1 can't silently under-report while parity passes. Adopt #2's coverage model as the SDK reference (AC3).
Plus: node-id schemes diverge (#1 `lambda:/s3:/gold:` vs #2 `rc:*#name/type:/field/endpoint:/rqk:`) -> the
materializer maps BOTH onto `cse_schema.CLOUDNODE_PREFIX_TO_ENTITY`'s canonical scheme (already defined).
And #2 has `--changed` incrementality (changed files + 1-level dependents); the `iter_sites` contract carries
the changed-set (hard-part #2 front-end lifecycle).

## 6. Acceptance (TH-C-style, per the TO)
- Every recognizer's C0/C1 PASSES `comp_ladder.fidelity_check` (non-decompressible = NOT DONE).
- The 2-compiler parity-oracle reproduces the current graph (AC2).
- Pure-lexical only (live-AWS dropped to FEDOBS); coverage contract uniform (AC3).
- CTO arch-gates; CVO exercises (fidelity + parity, blind).
