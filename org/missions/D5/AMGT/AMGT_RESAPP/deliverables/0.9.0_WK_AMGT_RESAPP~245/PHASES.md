# AMGT-aw-1 -- the cold first request, by phase (local plane, fresh process per run)

Source: `profile_phases.py <before|after> <route> 3`, one NEW python process per run, one request each, the AMGT_PHASE lines the code now logs. Values are the MEDIAN of 3 runs, in ms. `before` is the same code with the stored-name read turned off (every unnamed row reads its model block, exactly the earlier path); `after` is the code as committed. Phases are as logged: `names` = the three name sources and the display name; `classification` = the classification join (chatter: the classification table read); `generation read` = pointer and rows (chatter: the daily gold read); `mentions decode` = the mention gold read and decode (chatter only); `compute` = the rest of the build (chatter logs two compute spans, summed); `serialize` = the JSON body. `init` = import time before the request, not a request phase. Reading the stored objects uses the live store from this device, so absolute times are this device's and one run's; the before/after difference in `names` is the finding.


## route `trending`

| phase | before ms | after ms |
|---|---|---|
| names | 2540 | 740 |
| classification | 1151 | 760 |
| generation read | 407 | 419 |
| compute | 309 | 303 |
| serialize | 1 | 1 |
| **request total** | 4750 | 2452 |
| init (imports, not a phase) | 519 | 521 |
| GetObject of a model block | 24 | 0 |
| GetObject of a stored refdata object | 0 | 24 |

Runs (total ms): before [4750, 4588, 5183], after [2646, 2411, 2452].

## route `breakout`

| phase | before ms | after ms |
|---|---|---|
| names | 2654 | 706 |
| classification | 936 | 753 |
| generation read | 416 | 438 |
| compute | 304 | 315 |
| serialize | 1 | 1 |
| **request total** | 4555 | 2478 |
| init (imports, not a phase) | 485 | 579 |
| GetObject of a model block | 24 | 0 |
| GetObject of a stored refdata object | 0 | 24 |

Runs (total ms): before [4555, 4406, 4893], after [2510, 2448, 2478].

## route `chatter`

| phase | before ms | after ms |
|---|---|---|
| names | 3441 | 1540 |
| classification | 45 | 46 |
| generation read | 1380 | 1336 |
| mentions decode | 1194 | 1136 |
| compute | 1508 | 1444 |
| serialize | 1 | 1 |
| **request total** | 6981 | 5145 |
| init (imports, not a phase) | 529 | 556 |
| GetObject of a model block | 25 | 0 |
| GetObject of a stored refdata object | 0 | 25 |

Runs (total ms): before [6981, 7060, 6946], after [5176, 5145, 5001].
