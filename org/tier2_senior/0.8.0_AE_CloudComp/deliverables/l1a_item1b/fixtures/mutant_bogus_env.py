"""Mutant fixture (env sensor): synthetic SOURCE reading one known-live key
(positive control -> covered) and one nonexistent key (-> orphan). Never an
infra mutation; the live function is only ever read."""
import os

LIVE_KEY = os.environ.get("INF_GOLD_DISPATCH_RELEASE")          # known-live -> covered
BOGUS = os.environ.get("ZZZ_NO_SUCH_ENV_KEY_9999")              # nonexistent -> orphan
