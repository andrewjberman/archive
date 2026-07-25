"""CLEAN-control fixture (env sensor): synthetic SOURCE reading exactly the six
live keys of inf-gold-trigger -- covered=6, member=0, orphan=0 -> CLEAN rc=0.
Proves the sensor can return CLEAN (a detector only ever seen to fire is
untested)."""
import os

A = os.environ.get("GOLD_INSTANCE_ID")
B = os.environ.get("INF_AOR_FOLD_ACTIVE")
C = os.environ.get("INF_GOLD_DISPATCH_HOLD")
D = os.environ.get("INF_GOLD_DISPATCH_RELEASE")
E = os.environ.get("INF_GOLD_RELEASE_PROVENANCE")
F = os.environ["PERF_SILVER_STALENESS_CEILING_DAYS"]
