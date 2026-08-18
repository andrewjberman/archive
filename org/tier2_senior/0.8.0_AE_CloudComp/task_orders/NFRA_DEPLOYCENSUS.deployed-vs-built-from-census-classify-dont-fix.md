# TO NFRA_DEPLOYCENSUS — deployed-vs-built-from CENSUS: Lambda packages + EC2-staged code, CLASSIFY don't fix (one bounded read)

<task_order id="NFRA_DEPLOYCENSUS" project="NFRA_COMPRAIL">
<issued_to>0.8.0_AE_CloudComp (alongside NFRA_COMPTOOLS.PREFIX-READS; comp-tool / AWS-compiler lane)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T15:04Z</issued>
<dated>NOW — Andrew-direct 08-18 ~1500Z pulled the census forward ("All recs approved"; CTO relay 150051Z item (iv)). Spawn = MSTR on CTO's 49F push plan (this seat is named for it). One bounded read; NOT a fix pass.</dated>
<status>complete -- census delivered 2026-08-18 (CENSUS_REPORT_20260818.md + proof-of-spec rc=0 VALID; immediate-report clause exercised once: bd merge-daily two-homes, COO-ACKed 161035Z, remedy routed to CTO)</status>
<priority>P2 — a bounded read that answers "how blind have we been"; classify only</priority>
<authority>Andrew-direct 08-18 ~1500Z at the CTO terminal (record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260818_ALL_RECS_APPROVED_49F_END_TO_END_PUSH_AND_MDPF_UNUSED_DELETE.md; item (iv) census pull-forward YES). Method = CLAUDE.md Rule 22a CODE layer + its gate candidate ("an apply-time assertion for code-carrying deploys — and it must CLASSIFY (stale-by-neglect / deliberately-held / two-homes-diverged), because a detector that cannot tell a hold from neglect manufactures the wrong reflex, and the reflex a drift alert invites is 'deploy'"). This TO is the AUTHORIZED census that gate candidate was sequenced behind. MSTR 145245Z: three live two-homes instances in five days (mdpf json/mdpf-vs-platinum; bd legacy-rps-vs-08335338; inf packaged-vs-canonical builder) — the census answers "how many more".</authority>
</task_order>

## THE READ (Rule 22a, exactly)
For every code-carrying deploy in the estate:
- **Lambdas** (`infra/aws/lambda/ci/lambda-source-map.json` is the pairing; it does NOT compare bytes —
  Rule 4's own caveat): download the DEPLOYED package (`get-function` Code.Location), hash each member,
  and diff against THE SOURCE THAT ARTIFACT IS BUILT FROM — resolved through the BUILD INPUT (the
  source-map entry / package manifest), NEVER by filename (Rule 22a: "does deployed match REPO?" is
  malformed when the repo holds two copies of the file — the second is the real defect).
- **EC2-staged code** (`EC2_MANIFEST.json` services): the S3-staged object vs its repo source, AND —
  because staged is DESIRED, executing is APPLIED — the on-instance bytes via SSM where the box is up
  (Rule 22a: `user-data.sh` first-boot-only pulls make a staged object INERT; reading an artifact
  proves what is THERE, never what RUNS). Where SSM is down, say UNREAD, never assume.
- **The bundled-copy axis** (the third two-homes instance's shape): for every Lambda whose package
  carries a member that ALSO exists as a canonical script elsewhere in the repo (`data/*/scripts/**`
  builders bundled into `infra/aws/lambda/**`), diff bundled vs canonical — that is the "one logical
  producer, two independently-editable homes" read.

## CLASSIFY, per finding, exactly one of (Rule 22a's three + two the week added)
`CURRENT` · `STALE-BY-NEGLECT` (deployed older than built-from, no held reason) · `DELIBERATELY-HELD`
(a stated reason exists — cite it; e.g. the smartx-rest-pull docstring-only case 135226Z) ·
`TWO-HOMES-DIVERGED` (bundled vs canonical differ) · `STAGED-INERT` (EC2: staged object cannot reach
the box) · `UNREAD` (SSM down / package unreachable — never silently CURRENT). **A detector that cannot
tell a hold from neglect manufactures the wrong reflex — the reflex is "deploy". This TO FIXES NOTHING.**
Every finding = a row; findings route to owners as dated items AFTER the census, by COO/CTO.

## Acceptance
- DC-1: DENOMINATORS printed: N Lambdas in the source-map / M read / K unreadable (named); N EC2
  services in the manifest / M staged-read / K on-box-read / K UNREAD (named, with why).
- DC-2: every Lambda classified (one of the six), with member-level sha diffs cited for anything not
  CURRENT; bundled-vs-canonical rows for every bundled member (the inf-silver-chain 7 builders as the
  known-positive control — the census must FIND the build_billing_dim divergence or it is broken).
- DC-3: every EC2 service classified staged-vs-repo AND on-box-vs-staged (or UNREAD, named).
- DC-4: NEGATIVE CONTROL: a Lambda known-CURRENT (e.g. smartx-jwt-refresher, three-way CURRENT
  135226Z) reads CURRENT; POSITIVE CONTROL: inf-silver-chain reads TWO-HOMES-DIVERGED on
  build_billing_dim. Both printed. An instrument that has not been seen to discriminate is a
  passing assertion.
- DC-5: the summary table (counts per class) + the finding rows, committed as a deliverable; ZERO
  deploys, ZERO fixes in this TO (classify only). Findings routed by COO/CTO afterwards.
- DC-6: method note: what the census COULD NOT see (its own domain boundary) — e.g. code fetched at
  runtime from S3, containers not in the source-map — stated, so the next reader knows the frame.

<proof_of_spec>
  <expected_criteria>DC-1,DC-2,DC-3,DC-4,DC-5,DC-6</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_DEPLOYCENSUS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc.

## Discipline
Read-only on the estate (downloads + hashes + describes; SSM reads only). Materialise every `list-*`
client-side (never `--query length`, never `--no-paginate`). No alarm/monitor built (moratorium) — the
census IS the read; a gate candidate follows only on Andrew's word. Rail: `comp-pipescript deployed`
for the gold-script sweep (it already exists — reuse, do not rebuild that half); raw `aws` reads
rail-checked with the marker.

## reporting
COO (cc CTO, MSTR) at completion with the table; IMMEDIATELY if a finding is a LIVE served harm
(client-facing, stale-by-neglect on a scheduled producer) — that jumps the routing queue.
