# NFRA_TRUNCLASS.SWEEP -- the truncation-class census across every comp-tool parser

**Seat:** 0.8.0_AE_CloudComp - **Date:** 2026-08-20 ~1450Z - **TO:** NFRA_TRUNCLASS.SWEEP (COO, P1
ANDREW-NAMED CLASS; authority: Andrew-direct 2026-08-20 ~005xZ, *"truncated outputs is a very risky
error type and one we've seen crop up many times"*) - **Full row data:**
`NFRA_TRUNCLASS_SWEEP_CENSUS_20260820.json` (every hit with final class + why + what a wrong answer
would look like)

## TRC-1 -- The census, with its denominator

**Corpus (a PREDICATE, not a roster):** every `.tools/comp-*` executable (99) UNION the engine home
`org/modules/graph/*.py` (125) UNION every `.py` a wrapper directly invokes outside that home (20),
DEDUPED (7 overlap: a `.tools/*.py` can be both a glob match and wrapper-invoked).

**Scanned: 237 of 237 corpus files, 93,913 lines. Hits: 398.**

| shape | detector family | hits |
|---|---|---|
| S1 first-delimiter split | `split('.')[0]` / `partition` / `cut -d` / `${v%%.*}` | 54 |
| S2 fixed-width cut | `[:N]` / `%.Ns` / `cut -c` | 289 |
| S3 head-N on variable output | `head -N` / `LIMIT N` / `--max-items` / `grep -m` | 15 |
| S4 single-page read | boto3 `.list_*(` w/o local token walk / `--no-paginate` | 39 |
| S5 wrong-grain count (FIFTH SHAPE, named per the TO's invitation) | `grep -c` / `wc -l` line-grain read as occurrence-grain | 1 |

## TRC-2 -- Every hit classified, none omitted (398/398, 0 residual)

| final class | rows | meaning |
|---|---|---|
| **CONFIRMED-LATENT** | **11** | the shape is real and the input CAN exceed the page/width; below threshold at today's estate scale (margins measured) |
| **CONFIRMED-MEDIUM** | **1** | can produce a wrong answer today on a plausible input |
| RETIRED-DEAD | 1 | real shape inside the retired comp-surface-check engine (dead code; NOT a deletion warrant) |
| SAFE-BY-GRAMMAR | 52 | delimiter cannot legitimately occur inside the extracted segment (ARN/s3-URI/module-root/key:value) |
| SAFE-BY-QUOTA | 4 | AWS service quota bounds the set below one page (e.g. managed policies/role <= 20 < 100/page) |
| SAFE-BY-DESIGN | 8 | the cut IS the question's grain (latest-event `--max-items 1`, declared caps, header sniff, full-set `list_buckets`) |
| SAFE-BY-CONSTRUCTION | 1 | input domain is the function's own glob grammar |
| SAFE-WITH-GUARD | 1 | cross-match possible but a uniqueness guard collapses ambiguity to refusal |
| EXAMINED-AND-SAFE | 21 | token walk verified within +/-10 lines of the `list_*` call |
| DISPLAY-SAFE | 297 | rendering/summary/short-id/date-grammar cuts; verdict tokens computed BEFORE the cut (sampled reads) |
| DOC-STRING | 1 | catalog prose describing the anti-pattern (it is the warning, not an instance) |

## TRC-3 -- Severity by what the output AUTHORIZES (the confirmed twelve)

**Tier 1 -- feeds a security/integrity VERDICT (a truncation here manufactures a clean pass):**
1. `.tools/comp-firmsep-sweep.py:73` -- `iam list-roles --max-items 1000`, token dropped. The sweep
   UNIVERSE is one page. **Measured this hour: 212 roles live (auto-paginated, materialised), margin
   788.** Wrong answer: at >1000 roles, "firm separation holds" over a truncated universe -- an
   unswept role's cross-firm grant escapes as a clean pass.
2. `.tools/comp-deadgrant.py:206` -- `list-secrets --max-items 500`, one call per region. Its own
   docstring documents the universe at 78 (2026-07-09), margin 422. Wrong answer: secret #501+ never
   enters the dead-grant sweep -> false "no dead grants".
3. `org/modules/graph/clobber_scan.py:182` -- `list_object_versions` unpaginated (1000/page). Wrong
   answer: a clobber older than the newest 1000 versions reads as no-clobber.

**Tier 2 -- feeds the ESTATE CENSUS/graph (an absent edge = the deletion-warrant shape):**
4-11. `org/modules/graph/comp_aws_cli.py:460,472,482,531,839,1405,1454,1632` -- SNS topics/subs,
   SQS queues, CloudFront distributions, ECS clusters, Lambda event-source-mappings: single-page
   `list_*` with no local token walk (pages ~100). Latent at estate scale. Wrong answer: resource
   #101+ never enters the census -- a REAL resource reads as nonexistent to every graph consumer.

**Tier 3 -- wrong ARTIFACT resolution (well-formed answer about the wrong thing):**
12. `org/modules/graph/vectorize_audit_cli.py:23` (CONFIRMED-MEDIUM) -- dotted `script_id` stem-glob
   fallback (`split('.')[0]` + glob) runs BEFORE the full-id glob and takes `matches[0]`
   first-match-wins: `INF_D_06.cash_drag` can resolve to sibling `INF_D_06_other.py` when the exact
   file is absent -> an audit verdict about a sibling script.

Plus the nullified: `org/modules/graph/surface_check_cli.py:846` (sns subs single-page) sits in the
RETIRED comp-surface-check engine -- dead code, severity nullified, classified not omitted.

**Per the TO: NOTHING WAS FIXED. Each fix rides its own tool's row** (owners: comp-firmsep-sweep +
comp-deadgrant + clobber_scan + comp_aws_cli census legs + vectorize_audit resolver -- this seat
authors several of them; routing is COO's cut, input = this census).

## TRC-4 -- Prior specimens re-tested as fixtures (the method flags what it must)

- **Dot-split specimen:** (a) the SHIPPED regression battery
  `.tools/tests/test_comp_adversary_path_truncation.py` re-run this session: **4/4 PASS**
  (CENSUS-100PCT 17,344/17,344; MUTANT-OLD-TRUNCATES: the pre-fix pattern still fails 4/4);
  (b) the census scanner's own `--fixture-check`: a synthetic `serial.split('.')[0]` on a dotted
  serial path **is flagged S1: PASS**.
- **Single-line-JSON `grep -c` specimen:** (a) `--fixture-check`: a synthetic `grep -c` call site
  **is flagged S5: PASS**; (b) live grain demonstration this session:
  `printf '{"offer":1,"offer2":2,"offer3":3}' | grep -c offer` -> **1** while the occurrence grain
  (`grep -o | wc -l`) -> **3**.

## Method findings -- the census's own instruments failed twice and both were caught by controls

- **M1 corpus double-count:** run 1 scanned 7 files twice (wrappers-glob ∩ wrapper-invoked),
  inflating the denominator 244->237 and hits 431->398. Caught on duplicated rows; deduped by
  normalized path. *The census briefly committed the class it censuses.*
- **M2 file-scoped auto-safe failed OPEN 19/38:** the S4 "paginator present in file" rule laundered
  unpaginated calls behind a paginated sibling. Caught by a line-local (+/-10 lines) re-check of all
  38 rows; the line-local rule replaced it. 19 rows re-entered review; 8 became Tier-2 confirmed.
- **M3 (adjacent, same session, disclosed):** my carry-forward exercise harness truncated evidence
  strings for display BEFORE checking them and manufactured a false FAIL -- the display limit acted
  as the oracle. Fixed to check full strings. The class does not spare the instruments built to
  hunt it.

## TRC-5 -- proof instance

`org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS.SWEEP_PROOF_OF_SPEC.json`,
validated by `.tools/proof-of-spec-check.py <instance> TRC-1,TRC-2,TRC-3,TRC-4,TRC-5` -- TRUE rc
cited in the RAVC (measured without a pipe).

## Interim-discipline status

The TO's standing interim ("a GONE verdict on any dot-bearing path is UNVERIFIED") RETIRED this
morning: its own condition ("until the dot-fix lands") met at @b9cab628ce, re-verified live, COO
concurred (Msg 63092), independently corroborated by MSTR's overnight supersede.
