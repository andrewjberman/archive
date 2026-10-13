"""CA-i-1 AC1: refresh.with_age(items, read_at, keys) stamps every item with its age in whole minutes and the field it came from.

Prints:  I1-AGES ok=<True|False> arms=<n> of 5 failed=<names|none> reason=<text>
Contract: first key in `keys` whose value parses as an ISO UTC time wins; age_minutes = whole minutes from that time to read_at, never negative;
no parsable key -> age_minutes None and age_from None (an item is never silently dropped or aged from the wrong field). Inputs are not mutated.
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
READ_AT = "2026-10-13T22:30:00Z"


def main():
    failed, why = [], ""
    try:
        from data.transcripts.scripts.muse_reader import refresh

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:50]))

        def basic():
            out = refresh.with_age([{"t": "2026-10-13T20:00:00Z", "x": 1}], READ_AT, ("t",))
            return len(out) == 1 and out[0]["age_minutes"] == 150 and out[0]["age_from"] == "t" and out[0]["x"] == 1

        def first_key_wins():
            out = refresh.with_age([{"a": "2026-10-13T22:00:00Z", "b": "2026-10-13T10:00:00Z"}], READ_AT, ("a", "b"))
            return out[0]["age_minutes"] == 30 and out[0]["age_from"] == "a"

        def unparsable_is_none_not_dropped():
            out = refresh.with_age([{"t": "not a time"}, {}, {"t": None}], READ_AT, ("t",))
            return len(out) == 3 and all(o["age_minutes"] is None and o["age_from"] is None for o in out)

        def future_is_zero_and_offset_form():
            out = refresh.with_age([{"t": "2026-10-13T23:30:00Z"}, {"t": "2026-10-13T22:00:00+00:00"}], READ_AT, ("t",))
            return out[0]["age_minutes"] == 0 and out[1]["age_minutes"] == 30

        def not_mutated():
            src = [{"t": "2026-10-13T20:00:00Z"}]
            keep = copy.deepcopy(src)
            refresh.with_age(src, READ_AT, ("t",))
            return src == keep

        for name, fn in (("basic", basic), ("first-key-wins", first_key_wins), ("unparsable-kept-as-none", unparsable_is_none_not_dropped),
                         ("future-zero-and-offset", future_is_zero_and_offset_form), ("inputs-not-mutated", not_mutated)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("import")
    print("I1-AGES ok=%s arms=%d of 5 failed=%s reason=%s" % (not failed, 0 if "import" in failed else 5 - len(failed),
                                                              ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
