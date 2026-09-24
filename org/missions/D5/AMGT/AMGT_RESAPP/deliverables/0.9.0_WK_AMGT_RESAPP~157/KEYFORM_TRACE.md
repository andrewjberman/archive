# AMGT-ro-6 -- The Deere key-form trace: why Peers prices Deere and Posture calls it UNRESOLVED

Measured only, no source edited. All reads: (a) `lib.research.identity.crosswalk` built IN MEMORY from
its default coverage/registration sources, (b) one S3 GET attempt for `universe/v1/2026-09-24.json`
(fell back to the local `UNIVERSE_FALLBACK`, as designed -- no write). No Bloomberg call, no server
started.

## 1. PEERS

The Peers engine's candidate database is `lib.research.peers.universe.load_candidate_universe()`
(`lib/research/peers/universe.py:678-724`), an independent scanner store built by
`build_candidate_universe()` and keyed **by bare ticker root, not by canonical security_key form**:

```
lib/research/peers/universe.py:497   root, exchange = ticker_root(security_key)
lib/research/peers/universe.py:506   ticker = root if (root and root not in rows) else security_key
```

`peers()` (`lib/research/peers/engine.py:637-961`) grades every row in that scanner database and, for
each retained candidate, emits a member object whose PRICED fields (`ticker`, `name`, `price`, `ev`,
`ey`, `market_cap_musd`, factor block) are copied straight off the scanner `row` -- **unconditionally**,
with no gate on identity resolution (`lib/research/peers/engine.py:886-899`). Identity is then attached
as one extra field:

```
lib/research/peers/engine.py:900   member["identity"] = resolve_identity(row.get("ticker"), widened_identity_index)
```

Note the input: `row.get("ticker")` -- the **bare root form** (`"DE"`), never `"DE_US_Equity"`. So
Deere renders as a fully priced member (its scanner row carries price/ev/ey/market cap data
independently of any crosswalk join) and separately carries whatever `resolve_identity("DE", ...)`
returns on the `identity` sub-object -- the priced fields do not depend on that call succeeding.

## 2. POSTURE

Posture's route boundary is `resolve_identity(requested)` in `lib/research/api/scoped_amgt.py:1784-1886`,
called ONCE per `/security/{key}/*` request on the raw path segment (`requested`), with an explicit
"NO THIRD BRANCH" doctrine (`scoped_amgt.py:1793-1810`):

1. `crosswalk.resolve(requested_text)` (`scoped_amgt.py:1826`) -- MEASURED only if the crosswalk record's
   `resolution == RESOLUTION_MEASURED`.
2. Failing that, a **landed-artifact** fallback: `model_block_<requested_text>.json` read verbatim off
   disk (`scoped_amgt.py:1841-1859`) -- the filename is the string as received, "nothing appended,
   rewritten, split or stripped."
3. Failing both, `IDENTITY_UNRESOLVED` is returned with `reason` taken **verbatim** from the crosswalk's
   own miss reason (`scoped_amgt.py:1873-1886`, `miss = reason or (record or {}).get("reason") or ...`).

The docstring is explicit that "This module performs NO conversion between identifier forms
anywhere" (`scoped_amgt.py:1808-1810`) -- whatever form the URL carries (here `"DE_US_Equity"`) is
resolved AS GIVEN. It is not this module that built the `_US_Equity` suffix; it only resolves the
string handed to it at the route boundary, which for a Peers-linked comparable is a form Peers itself
never emits (Peers's own identity call at engine.py:900 uses `"DE"`, not `"DE_US_Equity"`).

`packs.py` (`lib/research/posture/packs.py`) is not itself an identity resolver: `build_pack()`
(`packs.py:85-274`) consumes an already-resolved `security_key` and an already-fetched peer set; its
only ticker-keyed logic is folding `peer_set["members"]` into `"P:<ticker>"` evidence elements
(`packs.py:200-221`), which is downstream of, and blind to, whichever identity resolution failed
upstream. `packs.py` is invoked from `lib/research/posture/judge.py:399-568` (`run()`), not from
`scoped_amgt.py` directly (measured: zero hits for `comparable_key` in `scoped_amgt.py`, and zero
hits for `from lib.research.posture` other than `judge.py:59`'s own `import packs as packs_module`)
-- so the UNRESOLVED verdict served to the portal is produced at the `resolve_identity()` route
boundary (`scoped_amgt.py:1784`) before any pack is ever built.

## 3. CROSSWALK

Built in memory from the default sources (`lib.research.identity.crosswalk.load_crosswalk()`,
`crosswalk.py:994-1015`), reading `COVERAGE_PATH_DEFAULT` = `org/missions/D5/AMGT/AMGT_RESAPP/
deliverables/0.9.0_WK_AMGT_RESAPP~4/universe.json` (89 coverage names) plus
`lib/research/identity/registrations.json` (28 registration rows). Measured directly against both
source files (read-only, no `crosswalk.build_crosswalk()` write):

- Coverage (`universe.json`, 89 `names[]` entries): no `folder` containing `"DEERE"` and no
  `bloomberg_ticker.value` starting `"DE "` -- **zero Deere rows**.
- Registrations (`registrations.json`, `{"registrations": [...]}`, 28 rows): no row with `"DE"` in its
  `bloomberg` field -- **zero Deere rows**.

So no crosswalk record exists for Deere under ANY alias form (`crosswalk.py:966-991 _build_index`
only indexes `bloomberg`, `display_ticker`, `model_key`, `bloomberg + " Equity"` and
`association_keys` off records that exist in the first place -- there is no Deere record to index).
`crosswalk.resolve("DE_US_Equity")` and `crosswalk.resolve("DE")` both return
`RESOLUTION_UNRESOLVED` for the identical reason (`crosswalk.py:1059-1090`, the literal text quoted
in Posture's served reason).

`universe/v1` (AMGT-rk-4's widened identity set, the ONLY other surface `resolve_identity()` in
`engine.py:232-283` can fall through to): a live S3 GET for
`s3://<POOL_BUCKET>/universe/v1/2026-09-24.json` returned `NoSuchKey`, so
`load_union_universe()` (`engine.py:1169-1187`) fell back to `UNIVERSE_FALLBACK`, which **is the
same 89-name `universe.json`** used as crosswalk coverage above -- zero Deere entries there either.
So even the widened positioning-chain fallback (`engine.py:206-229 build_widened_identity_index`,
consulted only inside `engine.py`'s own `resolve_identity`, never inside `scoped_amgt.py`'s) carries
no Deere identity today. Deere has **no persisted or measured canonical identity anywhere in this
estate**, under any form.

Landed-artifact fallback (Posture's surface 2): no `model_block_DE_US_Equity.json` exists anywhere
in the tracked/untracked/gitignored corpus (measured zero, `comp-find --name` over the whole repo).

## 4. THE RULE PROPOSED

Peers renders a fully priced Deere row because its scanner candidate database
(`lib/research/peers/universe.py`) is populated and keyed by bare ticker root independently of the
identity crosswalk -- price/ev/ey/market-cap fields are never gated on `resolve_identity()` succeeding
(`engine.py:886-900`); the identity call is attached as a separate, optional field that a consumer can
ignore. Posture's route boundary (`scoped_amgt.py:1784`), by contrast, is a hard gate: a request that
names a security by a form neither surface (crosswalk, landed artifact) has ever measured returns
UNRESOLVED and nothing downstream (`packs.py`, `judge.py`) ever runs. Both engines already compute an
identity-resolution verdict for the SAME candidate through the SAME crosswalk (`crosswalk.resolve`),
but off DIFFERENT input forms of the SAME candidate (Peers queries the bare root `"DE"` at
`engine.py:900`; Posture is queried with whatever string reaches its route, here `"DE_US_Equity"`) --
and for Deere both forms are UNRESOLVED because no record exists under any alias for Deere at all, so
the form mismatch is not itself what breaks this case. The smallest rule that makes the two surfaces
agree WITHOUT guessing an identity: a Peers member row already carries the crosswalk's own verdict on
itself (`member["identity"]["resolution"]`, `engine.py:900`) computed at ranking time -- Posture's
"Comparable" link for that member should CARRY that already-computed identity object through
(never re-derive or reconstruct a key form for the route boundary to re-resolve), and any Peers
consumer (portal or otherwise) treating a member as posture-linkable should gate on that same
`identity.resolution == "MEASURED"` field Peers already returns, rather than allowing a priced row
with an UNRESOLVED identity to read as a fully resolved comparable. This does not fix Deere's
underlying absence from coverage/registrations/universe -- that is a data question for the CTO's own
ruling, not this cell's to decide.
