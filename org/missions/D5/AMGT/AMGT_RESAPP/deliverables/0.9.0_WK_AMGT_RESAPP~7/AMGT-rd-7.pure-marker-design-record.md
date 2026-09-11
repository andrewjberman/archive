# AMGT-rd-7 -- THE STARRED WATCHLIST: design record

`0.9.0_WK_AMGT_RESAPP~7`, round 5/v5, cell AMGT-rd-7 (row S16, FWD-15). Code:
`lib/research/watchlist/store.py` + `lib/research/watchlist/__init__.py`. Tests:
`lib/research/watchlist/tests/test_watchlist.py`.

## Where it lives

No new table, no new Terraform. `infra/aws/terraform/amgt-resapp/security-metrics-table.tf`
(AMGT-rd-2, landed) names this cell explicitly as an allowed occupant of its own table:
*"AMGT-rd-7 (starred watchlist, PER-FIRM) may persist here or in a sibling keyspace; this
schema does not preclude either."* This cell takes the first option: `opal-amgt-security-
metrics`, base table key `(axis_date HASH, ticker RANGE)`.

The writer axes (AMGT-rd-5 chatter, AMGT-rd-6 price) use `axis_date = "<AXIS>#<as_of_date>"`
with `AXIS` one of a small closed set of ranking-axis names (`CHATTER` / `PRICE` /
`TRENDING` / `BREAKOUT`). This cell uses `axis_date = "WATCHLIST#<firm_id>"` -- a
namespace prefix a four-letter axis name can never collide with, on the SAME base table,
with no schema change and no new index. `ticker` is the existing range key; the marker
row's only other attribute is `starred: true`.

## AC1 -- per-firm, not per-user, and the tenancy boundary is structural

`star(firm_id, ticker)` / `unstar(firm_id, ticker)` / `list_starred(firm_id)` take a
`firm_id` and NEVER a user identity -- there is no parameter, column, or code path in
this module that could partition by user. Sharing across a firm's PMs is therefore not
an observed behavior of two calls landing on the same row by convention; it is the
absence of anything that could make them diverge.

The cross-firm boundary is the partition key itself. `list_starred(firm_id)` issues one
`Query` keyed on `_partition_key(firm_id)` (`WATCHLIST#<firm_id>`) against the base
table's hash key -- DynamoDB's Query semantics return ONLY items whose partition key
equals the given value. There is no scan, no client-side filter, and no code path that
ever receives another firm's rows and discards them; a firm's data is unreachable from
another firm's read, not merely unreturned by convention. `lib/research/watchlist/tests/
test_watchlist.py::test_starred_watchlist_tenancy_boundary_across_firms` proves both the
RESULT (each firm's view excludes the other's ticker) and the MECHANISM (each firm's own
Query call is recorded against that firm's own partition value, never the other's).

## Reversibility to per-user (Andrew reserved this; not built)

`_partition_key()` is the one function that encodes the per-firm decision. Reversing to
per-user is adding a second parameter to that one function (and threading it through the
three public calls that already pass `firm_id`) -- a key change, not a rewrite of this
module, the table, or the tests' shape. Not built here: Andrew has not given that word.

## AC2/AC3 -- the pure-marker / non-wiring proof

`star()` and `unstar()` each make exactly one call against the persistence seam
(`_dynamodb()`) and return. Structurally, there is nothing else in `store.py` capable of
computing a ranking, calling a vendor, or placing work on a queue for something else to
pick up later -- `comp-find "harvest|refresh|enqueue|trigger" lib/research` (AC3) finds
zero hits in this module; its 12 hits across the tree are pre-existing, unrelated code
(`lib/research/freshness/build_view.py`'s `last_refreshed` field name, `lib/research/
social/measure.py`'s vendor-spend guard) that this module never imports or calls.

The test suite proves the ABSENCE, not merely the intent: `test_star_is_a_pure_marker_
no_network_call` and its `unstar` counterpart patch the persistence seam with an
in-memory fake table AND block the raw network socket (`socket.socket.connect` and
`socket.create_connection`) for the duration of the call. This is deliberately broader
than spying on one hand-picked hook -- it does not matter what WOULD have made a network
call (a different AWS client, a raw HTTP request, some future transitive import); any of
them raises `_VendorCallDetected` and fails the test loudly. A third test
(`test_star_has_no_side_effect_beyond_the_marker_row`) asserts the fake table recorded
EXACTLY one call and that only one `Table()` was ever requested -- proving no SECOND
table (a queue-shaped table, a collection-request table) was reached for either. The
transitive path the cell names as the real risk -- "a star row that some other job later
treats as a work queue" -- has no job in this codebase that reads the `WATCHLIST#`
namespace at all today; nothing exists yet to wire it to. That is a fact about the
estate's current state, not a structural guarantee for all time, and is exactly what AC4
asks a human reader to weigh (see the task order's own AC4 text) rather than a mechanical
suite closing off.
