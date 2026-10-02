"""RIV-ic-1 AC2 (the seam against the REAL served gold) -- the census over served G1 and G4 for 2026-09-29, READ-ONLY.

The S3 sink is wrapped so any put raises. Expect:
  - one holdings row per universe fund (the denominator equals `len(universe.entries())`);
  - price and gics rows for the same securities (equal, non-zero counts), and at least one price `arrived` (G4 holds 2026-09-29);
  - control: every status is in {arrived, missing, stale}, and every missing row carries a reason."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-29"


class ReadOnly:
    def __init__(self, inner):
        self._s = inner
        self.kind = getattr(inner, "kind", "s3")

    def __getattr__(self, name):
        if name in ("put", "put_if_absent", "delete", "copy"):
            raise RuntimeError(f"READ-ONLY check: {name} refused")
        return getattr(self._s, name)


def run(v):
    c.setup_path()
    from rivalfunds import gold_input_census as ic
    from rivalfunds import sinks, universe

    ents = universe.entries()
    out = ic.build(DAY, ReadOnly(sinks.get_sink("s3")), ents, readings=[])
    hold, px, gics = (out[out.input_kind == k] for k in ("holdings", "price", "gics"))
    print(f"universe {len(ents)} funds | holdings rows {len(hold)} | price rows {len(px)} (arrived {int((px.status == 'arrived').sum())})"
          f" | gics rows {len(gics)} (arrived {int((gics.status == 'arrived').sum())})")
    print(hold[["subject", "status", "reason"]].to_string(index=False))
    v.check(len(hold) == len(ents), "one holdings row per universe fund")
    v.check(len(px) == len(gics) > 0 and int((px.status == "arrived").sum()) > 0, "price and gics rows match, some prices arrived")
    v.check(set(out["status"]) <= {"arrived", "missing", "stale"}
            and out[out.status == "missing"]["reason"].fillna("").astype(str).str.len().gt(0).all(),
            "control: statuses in the enum, every missing row carries a reason")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
