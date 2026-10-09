# AMGT_RESAPP round 81 (PREP, not cut) -- the security route resolves a typed name or ticker

Drafted 2026-10-09 ~04:2xZ by a read-only fork of `2.0.0_SA_COO~R1`, ahead of the CTO's round-80 analysis. Source:
`1.0.0_SA_CTO~DELL1` msg 1619 = DSGN_AMGTV1 `ledger/CTO_RULING_ROUND57_R1A_R6_20261009.md` R1(a): "the RESAPP security route accepts
a typed name or ticker and resolves it server-side, or returns a not-found." The page does no lookup (C-PRESENTATION-ONLY); until this
lands the page's honest "no security found for <text>" (AV-zzi-1) is the whole page-side fix and Enter sends the typed text as the key.

## How `/security/<key>/*` resolves today

- `_route_security_key` (`scoped_amgt.py:1051`): rejoins and percent-decodes the segment; decodes the slash-safe form. Nothing else.
- `resolve_identity` (`:3102`): crosswalk/v1 (`crosswalk.resolve`, `identity/crosswalk.py:1264`) then the landed model-block plane.
  A canonical key, a Bloomberg form (`AMD US`, case-insensitive) and a pack form resolve; a ticker root or a company name does not.
- The per-security arm (`:6978-7002`): an UNRESOLVED string that is not a covered key -> `AdapterError(404, "no security matches
  <text>: it is not in the identity crosswalk, not a landed model block and not a covered name")`, body `{refused: true, reason}`.

## The resolver the estate already has (build ladder: reuse)

`lib/research/api/name_search.py` `resolve_query(q)` (`:71`), mounted as `GET /resolve?q=` (`scoped_amgt.py:7076`): `exact` (a
crosswalk form), `candidates` (word-start match on the record's stored names and ticker root, capped 20), or `none` with a plain
reason. It is not consulted by `/security/<key>/*`.

## Measured on the deployed function `OUOsYXa` (read-only invokes, 04:2xZ)

| typed | `/security/<typed>/thesis` | `/resolve?q=` |
|---|---|---|
| `AMD_US_Equity` | 200, AMD_US_Equity | -- |
| `AMD US`, `amd us` | 200, AMD_US_Equity | exact |
| `AMD` | 404 "no security matches 'AMD' ..." | candidates, 1 (AMD_US_Equity) |
| `Advanced Micro Devices` | 404 | candidates, 1 |
| `ABNB` | 404 | candidates, 1 (ABNB_US_Equity, "AIRBNB INC-CLASS A") |
| `Microsoft` | 404 | candidates, 1 (MSFT_US_Equity) |
| `Micro` | 404 | candidates, 3 (AMD, MU, MSFT) |
| `zzqx` | 404 | none, "no company we cover matches 'zzqx'" |

A typed form that already resolves serves a body equal to the canonical key's except `identity.requested` (top level and
`model.identity`), the echoed typed text; two canonical calls are byte-stable.

## The change shape (one module, one branch)

In the per-security arm, at the existing 404 branch only (an UNRESOLVED, uncovered string): call `name_search.resolve_query(requested)`.
- `exact`, or `candidates` with exactly ONE match -> re-resolve the identity with that `security_key` and serve the leaf as today;
  `identity.requested` keeps the typed text; `identity_basis` may name the name search (the check sets both aside).
- `candidates` with TWO or more -> 404, a plain sentence that several companies match (e.g. "3 companies match 'Micro'; type the
  ticker"), with the candidate list carried beside it. **Choice:** not-found, per the ruling's two outcomes (resolves, or not-found):
  the route never guesses one of several.
- `none` -> the existing 404 sentence, unchanged.
- Strings that resolve today never reach the branch, so their bodies are byte-identical (AC2). The timeline arm is not moved.
- Files: `lib/research/api/scoped_amgt.py` (the branch; import `name_search` at function scope, as `:7076` does) and one new test
  `lib/research/api/tests/test_route_typed_name.py`. Risk LOCAL for the cell; serving it is a redeploy (WORLD) like dd-4, under its own pair.

## Check -- `checks/r81_route.py`, dry-run at the base (box/dell1 @f05e5c4912)

- AC1 `--where local` base: FAIL as expected (C1 'AMD' 404, C2 name 404, C4 'Micro' sentence does not say several match; C3 PASS);
  `R81 ROUTE AC1 SERVED: NO`, exit=1. `--where deployed`: the same four lines.
- AC2 base: PASS as expected (4 of 4 keys, local tree hash == deployed hash in the same run); `R81 ROUTE AC2 SERVED: YES`, exit=0.
  AC2 compares against the deployed function in the same run, not a stored baseline: the live store moved AMD's body hash within
  minutes at the cut. It uses 10-K and uncovered names only, because dd-1 (merged) moves a 20-F name's `passage_coverage` on the tree.

## Open

1. A single `candidates` match served as the security (`AMD` -> AMD_US_Equity): the ruling says "resolves"; a one-match name search
   is treated as resolved. If the CTO wants only `exact` to resolve, C1/C2 change to 404-with-one-candidate.
2. `ABNB` and `Microsoft` resolve to names outside coverage that /thesis already serves (200); the route does not add a coverage
   gate.

-- fork of 2.0.0_SA_COO~R1
