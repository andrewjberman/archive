# AMGT-az-4 -- the cold chatter read on the deployed function, and what was cut

Deployed function `opal-amgt-scoped-api`, CodeSha256 `D29LJCXhOStZ51JD4TTt2Jk0QUVDUbXDouXRTUS1ULI=`.
Run: `leadpanel_cold_warm.py --label az4` at 2026-10-06T17:55:49Z (this worker's shell); phase lines read from CloudWatch Logs
`/aws/lambda/opal-amgt-scoped-api`, `AMGT_PHASE route=chatter` joined to each invoke's REPORT line.
Denominator: 27 chatter invokes since 17:55:00Z: 6 cold (REPORT carries Init Duration; all from the days=30 burst, so days 90 and 365
produced no cold sample), 21 warm.

## 1. Deployed phase table (milliseconds)

| phase | cold min | cold max (n=6) | warm min | warm max (n=21) |
|---|---|---|---|---|
| generation read | 1501 | **1632** | 63 | 103 |
| mentions decode | 175 | 257 | 18 | 41 |
| compute (counts) | 209 | 214 | 181 | 203 |
| names | 0 | 0 | 0 | 0 |
| classification | 6 | 10 | 6 | 14 |
| compute (rows, ranking, tone, vintage) | 299 | 349 | 167 | 237 |
| serialize | 2 | 2 | 2 | 2 |
| sum of the chatter phases | 2226 | 2380 | - | - |

| | min | max |
|---|---|---|
| Init Duration (cold, n=6) | 633 | 683 |
| Duration (cold, n=6) | 2987 | 3177 |
| Init + Duration (cold, the script's figure) | 3631 | 3857 |
| Duration (warm, n=21) | 466 | 587 |

Outside every chatter phase line: Duration minus the phase sum is 761-808 ms on each of the 6 cold invokes and 3-7 ms on the 21 warm
ones. These ~0.78 s are paid once per container before the first phase starts or after the last one ends. The phase lines do not show where.

Only one phase was above 1,000 ms: **generation read, 1,501-1,632 ms cold**.

## 2. What was cut (all in the three owned files)

Generation read was the covered-name listing, then the daily snapshot (a listing, a footer read, three connection-opening reads, column
ranges, `to_pylist`) one after the other, with `pq.read_table`'s one-time dataset load inside the read. Measured locally, fresh process:

| piece | before (ms) | now (ms) |
|---|---|---|
| `pq.read_table` first call (3 columns, 59,148 rows) | 285-390 | 4 (`ParquetFile.read`) |
| daily snapshot read, 371 KB object | 640-720 (footer + warm + ranges) | 165 (one request, listing gave Size) |
| `pc.strftime` over 33,665 mention dates | 250-300 | 2 (cast to text, first 7 characters) |
| pyarrow's first Python-to-column conversion | 380 (imports pandas, installed on this device) | 0 (counts walk the columns in Python) |

Changes: `pool_reader` keeps the listed Size and reads a part of 1 MiB or less as one object, a larger part by byte range as before;
`ParquetFile.read` in place of `read_table` for the column reads. `monthly_chatter` starts the daily read, the mention read, then the
covered-name listing, with the names chain after it (no read waits for another), and reads the ranking, the window table and the two
vintage listings together; `_publisher_counts` makes the month text without `strftime` and walks the four text columns once.
`names_read.start` takes any call. Order, keys and values of every served field are unchanged (AC2: EQUAL 3 of 3).

## 3. Local phases (fresh process, `r76_served.py --cell c65 --where local`, bar 1,000 ms)

| phase | base (one run) | now (12 runs) |
|---|---|---|
| generation read | 1964 | 548-675 |
| mentions decode | 423 | 97-203 |
| compute (counts) | 549 | 171-424 |
| names | 0 | 259-469 |
| classification | 117 | 5-10 |
| compute (rows, ...) | 978 | 572-750 |
| sum | 4031 | about 1,900 |

12 of 12 under the bar in that series. Across the series before it (this worker's trials, other layouts) 4 of about 50 fresh runs stalled
8-21 s in a TLS handshake (a names read, the ranking read) (row S1); a stall is a network event on this device, not a phase.

## 4. What remains on the deployed function (inferred, not measured: no deploy was allowed)

The local ratio on generation read is 1964 to about 620. Applied to the deployed 1,501-1,632 ms, generation read would be about 500 ms,
and the other phases overlap their reads, so the chatter phases would sum to about 1.1-1.3 s in place of 2.2-2.4 s. The rest of a cold
request is not reachable from the three files: Init 633-683 ms plus the ~780 ms outside every phase line. Estimated cold total after
the cut: about 2.4-2.7 s against 3.6-3.9 s now. If the deploy of this commit still reads above about 2 s cold, that remainder (Init
plus ~0.78 s before or after the phases) is the evidence ruling 5 asks for as the case for provisioned concurrency; the issuer's
deployed read decides it.
