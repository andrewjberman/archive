# RESULT -- IRPT_BCKEND.TO-IB-rtf-11 (the directory entry reads the payload-2.0 event shape)

Worker `0.9.0_WK_IRPT_BCKEND~1`. Full verbatim run: `IB-rtf-11_R68-AC1_battery_output.txt` (this
commit), rc=0, token `IBR68-DIRECTORY-ENTRY-READS-PAYLOAD-2-0` printed. Every count below is
re-derived by the battery on each run.

## Arm (a) -- the event shape, measured

`api/integrations.tf:57` declares `payload_format_version = "2.0"` for every function this
project routes through `local.route_functions` (one `for_each`, one shared shape). `routes.json`
enumerates **2 of 2** DECLARED routes whose `handler` is `irpt-directory-search`:
`GET .../directory/search` (`directory-search`) and `POST .../directory/resolve`
(`resolve-scope`) -- both behind the SAME `aws_apigatewayv2_integration.handler["directory"]`, so
both carry payload format 2.0. `_authz/served.py` itself reads a 2.0 event's query string from
`event["queryStringParameters"]` and its body from `event["body"]` (a JSON string,
base64-encoded when `isBase64Encoded`) -- see `claimed_firm()` and the FIRM_BINDING check at
`served.py:614-616`, which reads exactly those two carriers before anything is resolved. The
fixture (`directory/tests/fixtures/payload_v2_event.json`, committed) carries ONE realistic 2.0
event per route in that shape, sha256 `68ca0e6c28598b8510d25df0a6299a1cff8eecce7a0e10f4132d2e224a022c49`,
no token and no real e-mail (every identifier is a placeholder matching the existing acceptance
fixtures' `firm_fixture49`/`acc_S1`).

## Arm (b) -- the fix, minimal, one helper, both call sites

`directory/entry.py` gains ONE helper, `_event_params(event)`, that returns
`queryStringParameters` merged with the parsed `body` (base64-decoded when `isBase64Encoded`); a
malformed body raises a plain `ValueError`, which `_authz/errors.reason_for` (unedited) already
classifies as the declared `INVALID_INPUT` policy reason, never the residual `UNEXPECTED` -- so
the refusal-shape requirement is met with zero change to `_authz/`. `search()` reads `q`/`limit`
from it; `resolve()` reads `selection` from it; `limit` is bounded exactly as `handler.py`
already bounds it (`max(1, min(int(limit or DEFAULT_LIMIT), MAX_LIMIT))`) -- unedited.
`handler.py`, `_authz/served.py`, `_authz/enforce.py`, `_authz/errors.py` and
`_authz/loaders.py` are verified BYTE-IDENTICAL (sha256 of the committed blob) to this order's
cut commit `4ceb7f8361` -- no change to any of them.

## Arm (c) -- the suite, the fixture honoured, the false behaviour demonstrated

`directory/tests` (new file `test_entry.py` added; `test_handler.py`/refresh/expiry unchanged):
**67 of 67** pass (was 59 of 59 before this cell -- no `directory/` test previously called
`entry.search()`/`entry.resolve()` at all; see the surprise row below). On the REAL, fixed
`entry` module against the committed fixture: `q="Desmond Achebe"` -> **1** document (the exact
match); `q="" limit="2"` -> **2** documents, `q=""` unlimited -> **6** (`DEFAULT_LIMIT` honoured,
wider than the `limit=2` case); `resolve(selection={"account_ids":["acc_S1"]})` (from the
fixture's JSON `body`) -> `ok=True, account_ids=["acc_S1"]`. THE NEGATIVE CONTROL: `entry.py` as
it stood at `9f72f4d6a4` (byte-identical to this order's cut, confirmed in arm (b)), loaded from
that commit's blob and run IN MEMORY (`__file__` faked to the real path so its sibling imports
resolve against the real, unedited `served`/`loaders`/`handler`/`ids`) against the SAME fixture:
`search(q="Desmond Achebe")` -> **6** documents (the unfiltered, `DEFAULT_LIMIT`-bounded
projection -- `q` silently ignored, exactly S92's prediction) and `resolve(...)` ->
`ok=False, partial_reason="selection matches nothing in the viewer's projection"` (the selection
never reaches the compute). False behaviour DEMONSTRATED on the identical fixture, same
directory/scope, only the entry module's vintage differing.

## Arm (d) -- the staging contract, `m of m`

`lambda-source-map.json`'s `irpt-directory-search` entry: `entry.py` is a declared `files`
member (its sha MOVES with this edit -- confirmed: pre-fix `9f72f4d6a4` blob vs the worktree now
differ -- that is the point; this manifest field is NOT hand-edited, nothing in this order
touches it). Its 7 `staged_from` members (`served.py`, `enforce.py`, `errors.py`, `resolve.py`,
`keys.py`, `ids.py`, `loaders.py`) each still resolve their declared `pin`/`sha256` at HEAD after
the edit: **7 of 7**.

## Surprise filed this cell

`IRPT_BCKEND-W1-S33` (OBSERVATION, INERT): bound (b)'s premise -- "every `directory/` test that
passed a top-level `q`/`selection` is REWRITTEN to the 2.0 shape" -- has no `directory/` member
to rewrite. No test under `directory/tests/` ever called `entry.search()`/`entry.resolve()` at
all before this cell (`test_handler.py` exercises `handler.py` directly, which has its own,
unrelated event contract). The ONE test that constructs the top-level-`q`/`selection` event S92
describes is `_authz/tests/test_guarded_entries.py`'s `base_event()`, outside this order's
`<paths>`. Measured before and after this order's fix: that file's 96 tests pass unchanged both
times (`96 passed`, rc=0) because none of its assertions inspect the served `data` payload's
content -- so it neither breaks from the fix nor exercises the 2.0 shape either side of it,
which is exactly the gap `R68-AC2` asks this seat to name. Not this seat's to fix (`_authz/tests/`
is outside `<paths>`); this order's own new `directory/tests/test_entry.py` supplies the
coverage the premise assumed already existed.

## R68-AC2 (judgment, recorded for `3.0.0_SA_CVO`, no verdict)

A suite that passed 100 percent (`_authz/tests/test_guarded_entries.py`, 96 of 96, both before
and after this fix) never exercised the deployed event shape because its `base_event()`
(`:129-151 @9f72f4d6a4`) hand-builds an event carrying top-level `q`/`limit`/`selection` and
never a `queryStringParameters`/`body` pair -- the harness constructed its own event rather than
one derived from the integration's own contract. `api/integrations.tf:57` is the one place that
states the wire format (`payload_format_version = "2.0"`); nothing in the test file reads it, so
the harness's event shape can drift arbitrarily far from what API Gateway actually delivers
without any assertion noticing, because the assertions test refusal codes and byte-leak absence,
never whether the caller's own parameters (`q`, `limit`, `selection`) reached the compute at all.
A route's acceptance instrument must therefore carry ONE FIXTURE PER ROUTE captured from the
integration's own contract (`payload_format_version` + the route's method, per
`docs/contracts/investor-reporting/v1/routes.json`) -- never hand-built to a guess -- and at
least one assertion that a value placed in THAT fixture's caller-supplied field (not a top-level
key invented by the test) reaches the compute's output, the way this cell's
`directory/tests/test_entry.py` and `battery_ib_rtf_11.py` arm (c) now do for this one function.
The same gap plausibly holds for `irpt-performance-adapter`, `irpt-status`, `irpt-narrative`,
`irpt-export-render` and `irpt-holdings` (all six IN_LANE functions share `test_guarded_entries.py`
as their in-process suite and its one `base_event()` shape) -- not measured here, since arm (b)'s
BOUNDS name `directory/entry.py` alone; that generalisation, if wanted, is a future cell's.
