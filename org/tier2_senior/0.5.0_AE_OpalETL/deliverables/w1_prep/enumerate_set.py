"""enumerate_set -- make an enumeration an ARTIFACT, so a denominator cannot be a summary of it.

WHY THIS EXISTS. Three measurement defects in three consecutive pages, all mine, all the same shape:

  CERT-5  /valuations   a footer count stated from a list ending in `head -10` (the 4th was line 11)
  CERT-6  /correlations a page count carried in my HEAD across six runs instead of derived
  CERT-7  /macro        a time SPAN read off `uniq -c | sort -rn | head -5` -- a FREQUENCY RANKING,
                        whose least-populated rows were the boundary values, and `head -5` cut them

After the first two I wrote constraint K10 ("never state a count from a truncated list -- nor from
memory"). Then I produced CERT-7 **in the same run whose constraint list contains K10**.

So the rule was never the missing piece. A rule I can recite did not survive being in a hurry --
which is exactly the regression CVO~Z diagnosed against themselves: a discipline you demonstrably
hold does not survive pace unless something MECHANICAL carries it.

THE MECHANICAL PIECE: you never read a denominator off a pipeline. You capture the FULL set once,
to a file, and every figure is DERIVED from that file by this module. The file is the artifact; the
numbers are functions of it. `head`, `sort -rn` and top-N summaries cannot sit between the set and
the claim, because the claim is computed from the set.

    from enumerate_set import Enumeration
    e = Enumeration.from_lines(lines, name="macro-timeseries-family")
    e.save("evidence/family.txt")     # the artifact
    e.count()                         # 79   -- of the FULL set, always
    e.span(key=lambda s: s.split()[1])# ('05:26:01', '05:26:10')  -- min/max, never a top-N
    e.denominator()                   # a printable string carrying count + how it was obtained

Read-only, stdlib-only. Not a comp-tool; a personal guard on my own lane.
"""
from __future__ import annotations

import io
import os


class Enumeration:
    """A captured full set. Every statistic is derived from the whole thing, by construction."""

    def __init__(self, items: list[str], name: str, source: str) -> None:
        self.items = list(items)
        self.name = name
        self.source = source
        self._path: str | None = None

    @classmethod
    def from_lines(cls, lines, name: str, source: str = "unspecified") -> "Enumeration":
        if isinstance(lines, str):
            lines = lines.splitlines()
        return cls([x for x in (s.strip() for s in lines) if x], name, source)

    def save(self, path: str) -> str:
        """Persist the FULL set. This file is the artifact a denominator cites."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with io.open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.items) + "\n")
        self._path = path
        return path

    def count(self) -> int:
        return len(self.items)

    def span(self, key=None):
        """min/max over the WHOLE set. The defect this replaces read a span off a frequency
        ranking, where the boundary values were the rarest rows and were the ones truncated."""
        if not self.items:
            return (None, None)
        vals = sorted(key(x) if key else x for x in self.items)
        return (vals[0], vals[-1])

    def distribution(self, key=None) -> dict[str, int]:
        """Full distribution -- every bucket, never a top-N. Sorted by KEY, not by frequency,
        so reading a range off it is correct by default rather than by luck."""
        out: dict[str, int] = {}
        for x in self.items:
            k = key(x) if key else x
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))

    def denominator(self, of: str = "items") -> str:
        """The printable denominator, carrying its own provenance. A count that cannot say where
        it came from is the thing this module exists to prevent."""
        where = f"; full set persisted at {self._path}" if self._path else "; NOT PERSISTED"
        return f"{self.count()} of {self.count()} {of} enumerated in full from {self.source}{where}"


def selftest() -> int:
    """Exercise the failure the module was built for: a top-N summary hides the boundary values."""
    # 12 items whose rarest buckets are the extremes -- the CERT-7 shape exactly.
    items = ["a 01"] + ["a 03"] * 5 + ["a 04"] * 5 + ["a 10"]
    e = Enumeration.from_lines(items, "selftest", "synthetic")
    lo, hi = e.span(key=lambda s: s.split()[1])
    assert (lo, hi) == ("01", "10"), (lo, hi)
    # what the defective approach would have produced: top-2 buckets by FREQUENCY
    top2 = sorted(e.distribution(key=lambda s: s.split()[1]).items(), key=lambda kv: -kv[1])[:2]
    naive = sorted(k for k, _ in top2)
    assert (naive[0], naive[-1]) == ("03", "04"), naive
    assert e.count() == 12
    print("selftest PASS: span over the full set = ('01','10'); "
          "a top-2-by-frequency read would have said ('03','04') -- both boundaries lost, "
          "which is CERT-7 reproduced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
