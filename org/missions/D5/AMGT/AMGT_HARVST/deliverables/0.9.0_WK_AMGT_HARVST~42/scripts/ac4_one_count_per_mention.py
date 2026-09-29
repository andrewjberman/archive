"""HVST-e-2 AC4 (JUDGMENT -- presented, NOT graded): does each served count equal one per actual mention of that
company? For the AMZN 09-06 crash report (bbg:TKYJAAVTTCZL00) and EVERY row whose tier moved between the previous
served mention part and the newest one, print the served mention_count and match_forms beside every matched span in
the stored silver text (block, offset, the words around it). Reads S3 and silver only; writes nothing. No verdict."""
import re
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402
import _e2 as E  # noqa: E402

NEW = C.NEW
CRASH = ("bbg:TKYJAAVTTCZL00", "AMZN_US_Equity")
CONTEXT = 45


def spans(text, aliases):
    pattern = NEW._span_pattern(aliases)
    if pattern is None or not text:
        return []
    out = []
    for m in pattern.finditer(text):
        lo, hi = max(0, m.start() - CONTEXT), min(len(text), m.end() + CONTEXT)
        out.append((m.start(), m.group(0), text[lo:m.start()], text[m.end():hi]))
    return out


def one_line(s):
    return re.sub(r"\s+", " ", C.a(s))


def main():
    client = C.store._default_client()
    mparts = C.parts(NEW.GOLD_TABLE, client)
    newest, previous = mparts[-1], mparts[-2]
    print("served newest mention part   : %s ETag=%s" % (C.short(newest[0]), newest[1]))
    print("previous served mention part : %s ETag=%s (the round-15 counts, read for the tier comparison)" % (C.short(previous[0]), previous[1]))
    now = {(r["article_key"], r["security_key"]): r for r in E.rows_of(newest[0], client)}
    prev = {(r["article_key"], r["security_key"]): r for r in E.rows_of(previous[0], client)}
    moved_tier = sorted(k for k in now if k in prev and now[k]["signal_tier"] != prev[k]["signal_tier"])
    keys = sorted(set(moved_tier) | {CRASH})
    print("rows whose tier moved (previous -> newest part): %d of %d ; plus the AMZN crash report row => %d rows presented" % (
        len(moved_tier), len(now), len(keys)))
    articles = {a["article_key"]: a for a in NEW._iter_latest_articles(client=client)}
    securities = {s["security_key"]: s for s in C.load_securities()}
    for art_key, sec_key in keys:
        row, was = now[(art_key, sec_key)], prev.get((art_key, sec_key))
        art = articles[art_key]
        aliases = NEW._security_aliases(securities[sec_key])
        title = art.get("title") or ""
        blocks = art.get("text_blocks") or []
        print("\n" + "=" * 100)
        print("%s | %s | published %s | %s" % (sec_key, art_key, row["published_utc"], one_line(title)))
        print("aliases of the security (as the matcher takes them): %s" % aliases)
        print("SERVED: mention_count=%d match_forms=%s signal_tier=%s (was %s in the previous part: mention_count=%s match_forms=%s tier=%s)" % (
            row["mention_count"], row["match_forms"], row["signal_tier"], "-" if not was else was["signal_tier"],
            "-" if not was else was["mention_count"], "-" if not was else was["match_forms"],
            "-" if not was else was["signal_tier"]))
        total = 0
        places = [("title", title)] + [("block %d" % i, b) for i, b in enumerate(blocks)]
        for where, text in places:
            for off, hit, before, after in spans(text, aliases):
                total += 1
                print("  span %2d  %-9s offset %5d  matched %-28r ...%s[[%s]]%s..." % (
                    total, where, off, hit, one_line(before), one_line(hit), one_line(after)))
        print("matched spans listed above: %d (title %d chars, %d blocks) ; served mention_count: %d" % (
            total, len(title), len(blocks), row["mention_count"]))
    print("\nPRESENTED FOR 3.0.0_SA_CVO~Z AT L9. No verdict is recorded here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
