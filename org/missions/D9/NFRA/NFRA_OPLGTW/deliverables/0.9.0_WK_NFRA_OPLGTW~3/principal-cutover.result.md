# NFRA_OPLGTW.TO-OG-a-2: principal cutover result (third run, order as amended @1efed70736)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3c` (worktree `/c/tmp/wk-oplgtw-1-3c`, cut from
`CLOUD` at `3f94e0a024`) | **Commits (LOCAL, this run):**
- `7183f7a3d3`: the three re-targets and the AC14 probe;
- `5c2f6d8ed1`: the probe's line-check fix;
- `189e70f340`: row W3-S15;
- the commit that carries this file, the rebuilt proof instance and the `<status>` flip.

Earlier runs: `d02e73c272` code, `5f47166b4b` rows, `fed567f54e` first proof, `318e119c4f` fixtures, `840de8bd66`
rows, `f8feaf081e` second proof. Nothing was pushed, merged or deployed.

## Read this first: 14 of 14 criteria pass by output; `<status>` is `complete`

The ruling in msg 97141 re-targets exactly three assertions. With them re-targeted, the three granted modules read
`31 passed` (OGA2-AC12). The assert counts per module are unchanged at 123/123, 6/6 and 63/63 (OGA2-AC13). The diff
against `3f94e0a024` changes exactly 3 assertion lines, the three named ones, and each still compares the email
claim to its original email (OGA2-AC14).

## What changed this run

| file | line | before (@`f8feaf081e`) | after (@`7183f7a3d3`) |
|---|---|---|---|
| `tests/test_oauth_durable.py` | 710 | `...["sub"] == email` | `...["sub"] == LocalIssuer.TID + "/" + LocalIssuer.oid_for(email) and claims["email"] == email` |
| `tests/test_jwt_cve_lock.py` | 117 | `...["sub"] == "attacker@opalinvest.com"` | `...["sub"] == _TENANT + "/" + str(uuid.uuid5(uuid.NAMESPACE_URL, "cve-lock/attacker@opalinvest.com")) and claims["email"] == "attacker@opalinvest.com"` |
| `tests/test_schwab_audit.py` | 342 -> 343 | `claims["sub"] == "colleague@opalinvest.com" and claims["typ"] == "access"` | `claims["sub"] == _TENANT + "/" + str(uuid.uuid5(uuid.NAMESPACE_URL, "ogo1-ac06/colleague@opalinvest.com")) and claims["email"] == "colleague@opalinvest.com" and claims["typ"] == "access"` |

- **How each assertion was written:** each stays one physical line. The first two bind the validated claims once
  with `:=`. Each `<tid>/<oid>` expression is the one that test's own fixture mints its principal from.
- **The one extra line:** `test_schwab_audit.py` gains `import uuid` at module scope (line 15), because that test's
  oid can only be written with it. It is the only non-assertion line changed since `f8feaf081e`, and it is row
  W3-S15.
- **The probe:** `probes/og_a2.py` gains AC14. It reads each module two ways:
  - the assert statements, matched structurally between base and HEAD;
  - the `-U0` diff hunks that fall inside an assertion.

  Each must read 1 per module. The changed base line must be the named line @`f8feaf081e`. The HEAD line must compare
  `["email"]` to the original `["sub"]` comparand and carry it as written.
- **Unchanged:** the app modules and `tests/test_principal_cutover.py` are byte-identical to `d02e73c272`.

## Criteria (each invocation run verbatim; AC1..AC12 at `7183f7a3d3`, AC13 and AC14 at `189e70f340`)

| id | verdict | deciding output |
|---|---|---|
| OGA2-AC1 .. AC11 | PASS-by-output, 11 of 11 | `1 passed` each, rc 0. The denominator lines are byte-identical to the previous runs' (11 of 11) |
| OGA2-AC12 | PASS-by-output | `31 passed in 18.37s`, rc 0 (31 of 31) |
| OGA2-AC13 | PASS-by-output | `VERDICT: PASS-OGA2-AC13`. HEAD == base: 123/123, 6/6, 63/63 (58 assert + 5 pytest.raises); modules equal 3 of 3 |
| OGA2-AC14 | PASS-by-output | `VERDICT: PASS-OGA2-AC14`. Assertion statements changed 3, assertion lines changed 3; named line matched 3 of 3; email half kept 3 of 3 |

**The probe's own defect, fixed in this run:** AC14's first run at `7183f7a3d3` read `VERDICT: FAIL-OGA2-AC14` on
the jwt and schwab modules. The fault was in the probe. It compared `ast.unparse`'s single-quoted form of the
original email with a source line that writes the literal double-quoted. The structural half had passed 3 of 3.
The control had missed the fault because it used only a variable.

`5c2f6d8ed1` fixes both:
- the line check now reads the original's source segment;
- the control now has 6 arms (a variable and a double-quoted literal, each with the email half kept, dropped or
  swapped).

The PASS above is the verbatim run after that fix.

## Controls

- **Mutant:** AC14's own verdict path runs in-process with the HEAD copy of `test_jwt_cve_lock.py` minus its email
  half. Result: `VERDICT: FAIL-OGA2-AC14 test_jwt_cve_lock.py: the HEAD assertion does not compare ["email"] to the
  original ...`, rc 1. FIRED-AS-EXPECTED. The earlier AC13 mutant and code mutant stand on unchanged code.
- **Determinism:**
  - AC14: 2 runs, with identical per-module lines.
  - AC13: 2 runs, with identical module lines.
  - AC12: `31 passed` in 2 of 2 runs.
  - AC1..AC11: 11 of 11 denominator lines are identical to the previous runs'.
  - STABLE.

## Checker

`py -3.12 .tools/proof-of-spec-check.py <instance> OGA2-AC1,...,OGA2-AC14` -> `VALID (rc=0)`, violations 0.

- **Artifacts:** 11 of 11 are content-resolved at their pins.
- **Surprises:** 9 of 9 entries resolve to a channel row.
- **Invocations:** 14 of 14 match the criterion text.

The first check read `INVALID (rc=1)` on 5 `introduces` lists. They named tokens that earlier commits had made,
not the pinned ones. Each now names a token its own pin introduced, and nothing else changed.

## Rows

| id | class | hazard | subject |
|---|---|---|---|
| NFRA_OPLGTW-W3-S15 (new, `189e70f340`) | OBSERVATION | INERT | The ruled schwab re-target needs `uuid` at module scope, so one non-assertion `import uuid` line sits beside the three ruled lines |

- W3-S7 and W3-S13 were filed BLOCKING, ARMED. The two amendments disarm them in substance: AC12 now reads
  31 passed. The rows themselves are unedited.
- W3-S8 .. W3-S12 and W3-S14 stand as filed.

## Side effects outside the grant

- The untracked `audit.jsonl` at the worktree root is not committed. The tracked
  `infra/aws/ec2/opal-gateway/audit.jsonl` is unmodified.
- `.venv-og/` and `.scratch/` are not committed.
