"""C6-KERNEL -- EXERCISED proof of the two inexpressibility claims (CTO arch-gate bar item 1).

CTO's ruling, and it is correct: "inexpressible" is a claim about what the API REFUSES, and
absence-of-a-method in a source file is exactly the shape that reads clean while a
__getattr__, a base class, a mixin, or a dataclass-generated ordering quietly provides it.
A source read cannot settle it. So this ATTEMPTS each forbidden operation and shows the
failure, with a POSITIVE CONTROL in the same transcript -- because an all-TypeError
transcript is equally consistent with a broken object.

Run:  python exercise_inexpressibility.py
Exit: 0 iff every forbidden op REFUSED *and* every supported op SUCCEEDED.
"""

from __future__ import annotations

import dataclasses
import inspect
import sys

from transition_kernel import CumulativeResidueLedger, InadmissibleRow, ResidueVector

ROWS: list[tuple[str, str, bool, str]] = []


def attempt(claim: str, op: str, fn, want_exc: tuple[type, ...]) -> None:
    """Run a FORBIDDEN op. It must raise one of want_exc."""
    try:
        result = fn()
    except want_exc as exc:
        ROWS.append((claim, op, True, f"{type(exc).__name__}: {str(exc)[:70]}"))
        return
    except Exception as exc:  # noqa: BLE001
        ROWS.append((claim, op, False,
                     f"raised the WRONG type {type(exc).__name__}: {str(exc)[:60]}"))
        return
    ROWS.append((claim, op, False, f"*** SUCCEEDED, returning {result!r} -- NOT inexpressible ***"))


def supported(claim: str, op: str, fn) -> None:
    """POSITIVE CONTROL. A supported op must SUCCEED, or the object is merely broken."""
    try:
        result = fn()
    except Exception as exc:  # noqa: BLE001
        ROWS.append((claim, op, False,
                     f"*** POSITIVE CONTROL FAILED: {type(exc).__name__}: {str(exc)[:60]} ***"))
        return
    ROWS.append((claim, op, True, f"succeeded -> {str(result)[:70]}"))


def main() -> int:
    v1 = ResidueVector(axes={"objects_written": 2.0})
    v2 = ResidueVector(axes={"objects_written": 5.0})

    print("=" * 88)
    print("CLAIM 1 -- A SCALAR RESIDUE IS INEXPRESSIBLE (ResidueVector)")
    print("=" * 88)

    # THE DECORATOR LINE, shown because @dataclass(order=True) would generate __lt__ silently.
    src = inspect.getsource(ResidueVector)
    deco = src.splitlines()[0] if src else "<unavailable>"
    fields = dataclasses.fields(ResidueVector)
    print(f"  decorator line      : {deco.strip()}")
    print(f"  dataclasses.fields  : {[f.name for f in fields]}")
    print(f"  __lt__ is object's? : {ResidueVector.__lt__ is object.__lt__ if hasattr(ResidueVector, '__lt__') else 'ABSENT'}")
    print(f"  MRO                 : {[c.__name__ for c in ResidueVector.__mro__]}")
    print(f"  has __getattr__     : {'__getattr__' in ResidueVector.__dict__}")
    print()

    attempt("scalar-inexpressible", "v1 < v2", lambda: v1 < v2, (TypeError,))
    attempt("scalar-inexpressible", "v1 > v2", lambda: v1 > v2, (TypeError,))
    attempt("scalar-inexpressible", "sorted([v1, v2])", lambda: sorted([v1, v2]), (TypeError,))
    attempt("scalar-inexpressible", "float(v1)", lambda: float(v1), (TypeError,))
    attempt("scalar-inexpressible", "int(v1)", lambda: int(v1), (TypeError,))
    attempt("scalar-inexpressible", "sum([v1, v2])", lambda: sum([v1, v2]), (TypeError,))
    attempt("scalar-inexpressible", "v1.total()", lambda: v1.total(), (AttributeError,))
    attempt("scalar-inexpressible", "v1 + v2", lambda: v1 + v2, (TypeError,))
    attempt("scalar-inexpressible", "ResidueVector(axes={})",
            lambda: ResidueVector(axes={}), (ValueError,))
    attempt("scalar-inexpressible", "ResidueVector(axes={'a': 'not-a-number'})",
            lambda: ResidueVector(axes={"a": "not-a-number"}), (ValueError,))

    # POSITIVE CONTROLS -- the object is not merely broken.
    supported("scalar-inexpressible POSITIVE",
              "v1.within(envelope) -> per-axis verdict",
              lambda: v1.within(ResidueVector(axes={"objects_written": 3.0})))
    supported("scalar-inexpressible POSITIVE",
              "v2.breached_axes(envelope) -> the breached list",
              lambda: v2.breached_axes(ResidueVector(axes={"objects_written": 3.0})))
    supported("scalar-inexpressible POSITIVE", "v1 == v1 (equality IS supported)",
              lambda: v1 == ResidueVector(axes={"objects_written": 2.0}))

    print("\n" + "=" * 88)
    print("CLAIM 2 -- AN AGENT-SELF-REPORTED LEDGER ROW IS INEXPRESSIBLE")
    print("=" * 88)
    ledger = CumulativeResidueLedger()

    public = [n for n in dir(ledger) if not n.startswith("_")]
    print(f"  public API surface  : {public}")
    print(f"  has __getattr__     : {'__getattr__' in CumulativeResidueLedger.__dict__}")
    print(f"  MRO                 : {[c.__name__ for c in CumulativeResidueLedger.__mro__]}")
    print()

    for name in ("append", "add_row", "submit", "append_row", "add", "insert", "record_row"):
        attempt("selfreport-inexpressible", f"ledger.{name}(row)",
                (lambda n=name: getattr(ledger, n)(("leg1", "axis", 7.0))), (AttributeError,))

    attempt("selfreport-inexpressible",
            "record_measurement(..., 7.0, ...)  # a VALUE where a measurement is required",
            lambda: ledger.record_measurement("leg1", "objects_written", 7.0, "I counted it myself"),
            (InadmissibleRow,))
    attempt("selfreport-inexpressible",
            "record_measurement(..., lambda: 'seven', ...)  # non-numeric measurement",
            lambda: ledger.record_measurement("leg1", "objects_written", lambda: "seven", "prose"),
            (InadmissibleRow,))

    # POSITIVE CONTROL -- a REAL measurement records.
    supported("selfreport-inexpressible POSITIVE",
              "record_measurement(..., lambda: 3.0, ...) records a real value",
              lambda: ledger.record_measurement("leg1", "objects_written", lambda: 3.0, "fixture count"))
    supported("selfreport-inexpressible POSITIVE",
              "ledger.cumulative() after that measurement",
              lambda: dict(ledger.cumulative().axes))

    print("\n" + "=" * 88)
    print("TRANSCRIPT")
    print("=" * 88)
    ok = 0
    for claim, op, passed, detail in ROWS:
        flag = "OK  " if passed else "FAIL"
        ok += 1 if passed else 0
        print(f"  [{flag}] {op:<62} {detail}")

    total = len(ROWS)
    forbidden = [r for r in ROWS if "POSITIVE" not in r[0]]
    positives = [r for r in ROWS if "POSITIVE" in r[0]]
    print("\n" + "=" * 88)
    print(f"  forbidden ops REFUSED : {sum(1 for r in forbidden if r[2])}/{len(forbidden)}")
    print(f"  supported ops SUCCEEDED: {sum(1 for r in positives if r[2])}/{len(positives)}  "
          f"<- without these, an all-TypeError transcript would be consistent with a broken object")
    print(f"  TOTAL                 : {ok}/{total}")
    print("=" * 88)
    if ok != total:
        print("RESULT: FAIL -- at least one claim is NOT exercised-true.")
        return 1
    print("RESULT: PASS -- both inexpressibility claims EXERCISED, with positive controls.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
