"""RIV-nm-1 AC3 (RFW-D05, RFW-D11, control): `display_name` leaves a good name alone and never invents one.

Pure, offline. Interface: `rivalfunds.names.display_name(candidates: list[str | None]) -> str | None` (rules in
nm-1 AC2).
  - a single good (mixed-case) name passes through unchanged, including a COMPLETE name of exactly 30 characters
    ('BB Seguridade Participacoes SA': with no other candidate it is returned as is);
  - a good name beside blanks passes through unchanged;
  - no candidate at all -> None: [None, None], [] and ['', '   '];
  - no real name, only a raw ticker -> that ticker (the fallback: a holding is never left nameless)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

GOOD = ["Kimberly-Clark de Mexico SAB de CV", "Alimentation Couche-Tard Inc", "Siemens AG",
        "BB Seguridade Participacoes SA"]


def run(v):
    c.setup_path()
    from rivalfunds.names import display_name as dn

    print("len('BB Seguridade Participacoes SA') =", len(GOOD[-1]))
    for n in GOOD:
        a, b = dn([n]), dn([None, n, "  "])
        print(f"  {n!r}: alone {a!r}, with blanks {b!r}")
        v.check(a == n and b == n, f"a single good name passes through unchanged: {n!r}")
    empty = {"[None, None]": dn([None, None]), "[]": dn([]), "['', '   ']": dn(["", "   "])}
    print(empty)
    v.check(all(x is None for x in empty.values()), "no candidate -> None ([None, None], [], blanks)")
    t = dn([None, "8306 JP Equity"])
    print("ticker only:", repr(t))
    v.check(t == "8306 JP Equity", "with no real name the raw ticker is the fallback, never None")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
