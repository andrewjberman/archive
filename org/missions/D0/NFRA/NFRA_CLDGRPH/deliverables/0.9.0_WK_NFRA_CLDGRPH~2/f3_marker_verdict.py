#!/usr/bin/env python3
"""The stitch marker's VINTAGE reader -- one function, three inputs.

TO-CG-F-3 deliverable step 5: "a night that DID NOT RUN reads differently from
one that did". The discrimination is by VINTAGE, never by whether the object
parses: a marker left over from three nights ago is a perfectly plausible JSON
object, and a reader that only checks shape returns the same answer for it as
for tonight's. So this reader returns THREE distinct verdicts:

    FRESH   -- the key exists and built_at is younger than the age bar
    STALE   -- the key exists and built_at is older than the age bar
    NO-RUN  -- the key does not exist at all

The bar is DEFAULT_AGE_WARN_HOURS = 26.0 h, imported from the estate's own
reader library infra/aws/globgrph/_provenance.py:41 (`> one nightly cycle ==
missed-nightly signal`) rather than re-typed here -- a re-typed constant is a
second carrier of one quantity and drifts.

The consumer this stands in for is comp_debt.py:128-160 / `comp-graph status`,
which reads a LOCAL manifest today; repointing it at this marker is CG-s-25
(TO-CG-F-5), not this order. This order proves the DISCRIMINATION exists on the
marker itself.
"""
import datetime
import json
import os
import sys


def _find_ws(start):
    """Walk UP until the directory that actually carries the reader library.

    Counting parent hops from a deliverables path is how an off-by-one lands a
    sys.path entry on org/ and turns a live import into a silent ImportError,
    which this reader would then report as UNREADABLE-BAR. Locate by EXISTENCE
    of the file being imported instead.
    """
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(12):
        if os.path.isfile(os.path.join(d, "infra", "aws", "globgrph", "_provenance.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


_WS = _find_ws(__file__)
if _WS:
    for _p in (_WS, os.path.join(_WS, "infra", "aws", "globgrph")):
        if _p not in sys.path:
            sys.path.insert(0, _p)

try:
    from _provenance import DEFAULT_AGE_WARN_HOURS as AGE_BAR
    BAR_SOURCE = "infra/aws/globgrph/_provenance.py DEFAULT_AGE_WARN_HOURS (imported)"
except Exception as exc:                                    # pragma: no cover
    AGE_BAR = None
    BAR_SOURCE = "IMPORT FAILED: %s -- the bar is NOT re-typed here, so no verdict" % exc


def age_hours(built_at, now=None):
    """Hours between a marker's built_at (ISO Z) and now. None if unparseable."""
    if not built_at:
        return None
    try:
        t = datetime.datetime.strptime(built_at, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
    except ValueError:
        return None
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return (now - t).total_seconds() / 3600.0


def verdict(marker, present=True, now=None):
    """(verdict, age_h) for a marker dict, or for an ABSENT key (present=False)."""
    if not present or marker is None:
        return "NO-RUN", None
    if AGE_BAR is None:
        return "UNREADABLE-BAR", None
    a = age_hours(marker.get("built_at"), now=now)
    if a is None:
        return "NO-RUN", None
    return ("FRESH" if a < AGE_BAR else "STALE"), a


def render(label, marker, present=True, now=None):
    v, a = verdict(marker, present=present, now=now)
    return "%s=%s age_h=%s" % (label, v, "-" if a is None else "%.2f" % a)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    m = json.load(open(src, encoding="utf-8")) if src != "-" else json.load(sys.stdin)
    print(render("VERDICT", m))
