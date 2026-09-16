# NFRA_OPLGTW.TO-OG-z-3 -- the keyed account alias (`OG-z-3`)

**Worker** `0.9.0_WK_NFRA_OPLGTW~3` · **branch** `wk-nfra_oplgtw-1-3f` (worktree `/c/tmp/wk-oplgtw-1-3f`, cut from
`CLOUD` at `f4c7184f6d`) · **code commit** `1006e6a702` (LOCAL) · **criteria** 5 of 5 PASS by output ·
**proof-of-spec-check** `rc=0` (VALID).

## THE RETIRED-KEY RULE, AS CHOSEN (the order asks this cell to state it and prove it -- OGZ3-AC5)

**REJECT.** Only the CURRENT key version is ever minted or resolved. A well-formed reference whose version token is
not the current one is refused with the contract's `EXPIRED_REFERENCE`, and the caller obtains current references
again from a fresh `list` / `describe` / `query`.

Three properties make that rule worth its cost, and each is measured in `test_ogz3_ac05`:

1. **It is decided on the version token alone**, before any key is used and before any account is compared. So a
   retired reference of a granted account, of another principal's account, of an account in no grant, a random
   retired reference and a reference under a version that was never issued all get the SAME answer -- 5 of 5 probes,
   1 distinct denial body. Nothing about any account leaks through the retired path.
2. **Retired key bytes are never used.** The test deliberately leaves the retired `v1` key inside the secret after
   rotating to `v2`, and the `v1` reference is still refused. Rotation therefore ends the old references' life
   whatever the operator leaves behind, which is the point of rotating.
3. **The entitlement is read first.** A revoked principal presenting a retired reference gets `ENTITLEMENT_DENIED`,
   not `EXPIRED_REFERENCE`, so the retired-key answer is never a way to learn that a principal still has access.

The alternative the order offers -- re-resolve under the current version -- was rejected because it requires keeping
retired key material live for as long as any old reference might circulate, and it keeps a reference minted under a
compromised key working after the rotation meant to kill it. The cost of REJECT is one extra round trip for a client
holding stale references, which a re-list already fixes; rotation takes effect within `SECRET_TTL_S` (300 s) of the
secret changing, or at once through `invalidate_key_cache()`.

## WHAT WAS BUILT

`infra/aws/ec2/opal-gateway/app/account_ref.py` (new, source only; nothing deploys, no caller wired -- the Schwab
tools are `OG-q-2`'s).

```
account_ref = "acr_" + <version> + "_" + base32(HMAC-SHA256(key, MESSAGE)[:16])    lower case, no padding
MESSAGE     = b"opal-gateway/account_ref" NUL <version> NUL <master> NUL <raw account id>
```

- **Versioned and keyed** (AC1): the version is inside the MAC input as well as in the reference, so the same key
  bytes under another version give an unrelated reference. The key is read through the Gateway's existing secret
  path, `app/integrations/base.py` `SecretsCredential` (`secretsmanager:GetSecretValue`, cached, never logged).
- **Master-bound** (AC2, PRD A5): 200 account ids minted under both masters give 200 of 200 different references and
  400 distinct values; a reference minted under one master resolves under no other master, even when the same account
  id is granted in both.
- **Resolution against the CURRENT authorized set** (AC3): `resolve_refs` does a fresh strong read of the principal's
  profile and grant through `data_entitlement.current_access` (never cached), takes that grant's accounts for the one
  master named, and compares with `hmac.compare_digest` over every candidate with no early exit. One master per
  request; all or nothing.
- **It cannot say whether an account exists** (AC3): an account granted to someone else, an account in no grant
  anywhere and a random reference return ONE identical `ENTITLEMENT_DENIED` body, and the resolver reads nothing but
  the principal's own POLICY partition (6 reads, 0 elsewhere, 0 query, 0 scan) -- it holds no account inventory to
  leak.
- **No raw id in any log, audit line, reason or repr** (AC4): 13 arms, 5 corpora, 0 hits. Input that is not a
  reference or a contract master is never echoed, because it may itself be a raw id; `Resolution.__repr__` and
  `__str__` show counts only.

`infra/aws/ec2/opal-gateway/tests/test_account_ref.py` (new): `test_ogz3_ac01` .. `test_ogz3_ac05`, offline on moto's
DynamoDB and Secrets Manager with a locally generated 32-byte key. The real secret is never read, as the order
requires.

## EVIDENCE

| criterion | invocation (verbatim, at `1006e6a702`) | deciding line |
|---|---|---|
| OGZ3-AC1 | `pytest ...::test_ogz3_ac01 -q -p no:cacheprovider --color=no` | `1 passed in 1.05s` (rc=0) |
| OGZ3-AC2 | `pytest ...::test_ogz3_ac02 ...` | `1 passed in 0.88s` (rc=0) |
| OGZ3-AC3 | `pytest ...::test_ogz3_ac03 ...` | `1 passed in 0.92s` (rc=0) |
| OGZ3-AC4 | `pytest ...::test_ogz3_ac04 ...` | `1 passed in 1.03s` (rc=0) |
| OGZ3-AC5 | `pytest ...::test_ogz3_ac05 ...` | `1 passed in 0.97s` (rc=0) |

Each test's denominator line is quoted in full in the proof instance's `output_evidence`.

**Controls.** Five in-process mutants (scratch plugin, committed bytes untouched) each failed exactly the criteria
they must: `unkeyed` (AC1: the keyed recomputation matches 0 of 6), `no_master` (AC2: 0 of 200 pairs differ),
`resolve_any` (AC2 and AC3: every reference resolves), `accept_retired` (AC5: the retired reference answers
`ENTITLEMENT_DENIED` instead of `EXPIRED_REFERENCE`), `log_raw` (AC4: the scanner finds the raw ids, 10 hits).
**Determinism:** two whole-module runs, `5 passed` both times, the 5 denominator lines identical by diff.
**Gate:** `OK: pre-commit gate clean for 2 of 2 file(s)`.

AC4's zero rests on positive controls, or it would be an empty harness reading clean: 35 log records captured, 11 of
them from `opal_gateway.account_ref` (exactly one per resolution), 11 audit lines, the access-state alarm on stderr,
and the same scanner returning 1 on a planted line that carries a raw id.

## ROWS FILED

- **`NFRA_OPLGTW-W3-S25`** -- OBSERVATION, **ARMED**, disarm `2.0.0_SA_COO~O`. No carrier states where the alias-key
  secret's NAME is configured or what its VALUE holds: `app/config.py` carries no such setting (11 hits for
  `secret|schwab|account_ref|hmac`, none of them this) and is outside this order's `<paths>`, and
  `SCHWAB_IDENTITIES.json` does not exist at the cut because `OG-i-2` has not run. This cell chose
  `SCHWAB_ACCOUNT_REF_SECRET_ID` for the name and `{"current_version": "v<n>", "keys": {"v<n>": "<base64 of at least
  32 bytes>"}}` for the value, and fails closed (`KeyUnavailable` / `UNAVAILABLE`) on anything else -- never an
  unkeyed alias. It disarms by naming both in `OG-i-2`'s and `OG-r-1`'s orders.
- **`NFRA_OPLGTW-W3-S26`** -- OBSERVATION, INERT. With the root logger at DEBUG, botocore logs a grant read's
  DynamoDB response body, which carries the grant's raw account ids (measured: 1 such line at DEBUG, 0 log lines at
  the host's default WARNING). No code in `app/` configures logging, so the host's level is WARNING; a later cell
  that adds logging configuration should hold the SDK loggers no lower than INFO.

## WHAT THIS CELL DID NOT DO

Wiring `account_ref` into Schwab responses, CSVs and the `dim_position` / `dim_balance` projection (`OG-q-2`); cache,
cursor and ticket keys (`OG-k-1`, `OG-q-2/3`) -- this cell covers A5's REQUEST half only; provisioning the secret and
its grant (`OG-i-2`) or setting the variable on the host (`OG-r-1`); any live AWS call; and any timing-channel claim.
The full list with reasons is `declared_exclusions` in the proof instance. Nothing was pushed, merged or rebased.
