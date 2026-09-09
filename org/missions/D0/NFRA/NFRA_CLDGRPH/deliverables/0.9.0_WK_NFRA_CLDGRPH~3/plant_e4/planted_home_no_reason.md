# E4-AC1 NEGATIVE CONTROL -- a home record with a label where its reason should be

Fed through the SAME parser as the real record. The home is a legal value, the
owner is a real serial, the producer block is complete and the cells are well
formed -- everything a careless parser checks -- and the `reason` is four words.
A cell whose verb is *decide* is exactly the place where a passing parser with
no reason floor certifies a coin toss.

```json
{
  "cell": "CG-s-20-CONTROL",
  "home": "JOIN_PROJECTION",
  "owner": "0.8.0_AE_CloudComp",
  "reason": "it seems better this way",
  "producer": {
    "tf_resource": "control tf resource",
    "schedule": "control schedule",
    "s3_key": "control key",
    "vintage_now": "control vintage"
  },
  "consumer": {"file": "control.py", "lines": "1-2"},
  "later_round_cells": [
    {"surface": "control surface", "lane": "0.8.0_AE_CloudComp", "verb": "extend",
     "accept": "a control accept"}
  ],
  "rebuild_path_to_projection": 0
}
```
