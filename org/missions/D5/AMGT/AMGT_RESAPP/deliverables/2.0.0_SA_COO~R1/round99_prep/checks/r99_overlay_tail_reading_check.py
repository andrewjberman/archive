"""AMGT_RESAPP round-99 PREP -- the SHAPE of the overlay-tail reading (CTO round-98 analysis item 2; be-1 CTO half ADDENDUM 1).

  python r99_overlay_tail_reading_check.py <reading.md>

Question the reading answers: over the last 24 hours of the live function's own log (`/aws/lambda/opal-amgt-scoped-api`), which invocations ran longer than 20 seconds, which route
and which name each served where its own log lines say, whether each was a cold start, and what ran beside it. The reading drops nothing and changes nothing. This check grades the
SHAPE; the outcomes are the CVO's judgment. The file holds these level-2 headings, each non-empty, in this order:

    ## Window       `WINDOW <start UTC> to <end UTC>` and `FUNCTION CodeSha256 <value> LastModified <value>` as read at the end of the window
    ## Counts       `INVOCATIONS n=<integer>` (the REPORT lines of the window), `OVER 20 s n=<integer>`, `ATTRIBUTED n=<integer>` (a route read from the invocation's own log lines),
                    `UNATTRIBUTED n=<integer>`, `COLD n=<integer>` (an init duration among the over-20 s), `POOL-FULL n=<integer>` (an over-20 s invocation whose own log carries a
                    'Connection pool is full' warning) and `NO POOL-FULL n=<integer>` -- ATTRIBUTED + UNATTRIBUTED equals OVER 20 s, and POOL-FULL + NO POOL-FULL equals OVER 20 s
    ## Routes       one line per route seen among the over-20 s: `ROUTE <route> | n=<integer> | max_ms=<integer>`; or the single line `ROUTE none attributable` with the reason
    ## Names        one line per name seen: `NAME <security key> | n=<integer> | max_ms=<integer>`; or `NAME none attributable` with the reason
    ## Beside       `BESIDE`: per over-20 s invocation or per cluster, what else ran in the same minute (the count of invocations in that minute from the REPORT lines), as lines
                    `MINUTE <UTC minute> | over20=<integer> | invocations=<integer>`; at least one line
    ## Sources      one bullet per query or read, each with `n=<integer>` (a denominator)
    ## Surfaces     lines `READ: <surface>` (at least two) and `NOT READ: <surface>` (at least one: for example the API gateway's own log, the S3 request log, the client side)
    ## Not changed  `WRITES: none`

    S1 every heading present, in order, non-empty.
    S2 `## Window` carries a WINDOW line and a FUNCTION line.
    S3 `## Counts` carries the seven counts; ATTRIBUTED + UNATTRIBUTED = OVER 20 s and POOL-FULL + NO POOL-FULL = OVER 20 s.
    S4 `## Routes` carries at least one ROUTE line; every `n=` is an integer and the ROUTE counts sum to ATTRIBUTED or the line is `ROUTE none attributable`.
    S5 `## Names` carries at least one NAME line (or `NAME none attributable`).
    S6 `## Beside` carries at least one MINUTE line.
    S7 `## Sources` has at least two bullets, each with an `n=<integer>`.
    S8 `## Surfaces` carries at least two READ lines and at least one NOT READ line.
    S9 `## Not changed` carries `WRITES: none`.
Verdict: R99 OVERLAY TAIL READING SHAPE: YES|NO (exit 0|1). At the base: NO (no reading exists).
"""
import re
import sys

HEADINGS = ("Window", "Counts", "Routes", "Names", "Beside", "Sources", "Surfaces", "Not changed")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def sections(text):
    found, order, cur = {}, [], None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            order.append(cur)
            found[cur] = []
        elif cur is not None:
            found[cur].append(line)
    return found, order


def count(body, label):
    m = re.search(r"^\s*[-*]?\s*%s\s+n=(\d+)" % re.escape(label), body, re.M)
    return int(m.group(1)) if m else None


def main():
    if len(sys.argv) != 2:
        print("usage: r99_overlay_tail_reading_check.py <reading.md>")
        return 2
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        say(False, "S1 the reading exists", "%s: %s" % (type(exc).__name__, exc))
        print("R99 OVERLAY TAIL READING SHAPE: NO")
        return 1
    found, order = sections(text)
    body = {h: "\n".join(found.get(h, [])).strip() for h in HEADINGS}
    present = [h for h in order if h in HEADINGS]
    res = [say(present == list(HEADINGS) and all(body[h] for h in HEADINGS), "S1 every heading is present, in order, non-empty",
               "headings %s, empty %s" % (present, [h for h in HEADINGS if not body.get(h)]))]
    w = body["Window"]
    res.append(say(bool(re.search(r"^\s*[-*]?\s*WINDOW\s+\S+.*\bto\b", w, re.M)) and bool(re.search(r"^\s*[-*]?\s*FUNCTION\s+CodeSha256\s+\S+\s+LastModified\s+\S+", w, re.M)),
                   "S2 the window and the function's hash and time are stated"))
    c = {k: count(body["Counts"], k) for k in ("INVOCATIONS", "OVER 20 s", "ATTRIBUTED", "UNATTRIBUTED", "COLD", "POOL-FULL", "NO POOL-FULL")}
    ok3 = (all(v is not None for v in c.values()) and c["ATTRIBUTED"] + c["UNATTRIBUTED"] == c["OVER 20 s"]
           and c["POOL-FULL"] + c["NO POOL-FULL"] == c["OVER 20 s"])
    res.append(say(ok3, "S3 the seven counts are stated; the two splits each sum to OVER 20 s", str(c)))
    routes = re.findall(r"^\s*[-*]?\s*ROUTE\s+(.+?)\s*\|\s*n=(\d+)\s*\|\s*max_ms=(\d+)", body["Routes"], re.M)
    none_r = bool(re.search(r"^\s*[-*]?\s*ROUTE none attributable", body["Routes"], re.M))
    sum_ok = none_r or (bool(routes) and c["ATTRIBUTED"] is not None and sum(int(n) for _r, n, _m in routes) == c["ATTRIBUTED"])
    res.append(say(sum_ok, "S4 the ROUTE lines sum to ATTRIBUTED (or none attributable, with a reason)", "%d route line(s)" % len(routes)))
    names = re.findall(r"^\s*[-*]?\s*NAME\s+(\S+)\s*\|\s*n=(\d+)\s*\|\s*max_ms=(\d+)", body["Names"], re.M)
    none_n = bool(re.search(r"^\s*[-*]?\s*NAME none attributable", body["Names"], re.M))
    res.append(say(bool(names) or none_n, "S5 the NAME lines (or none attributable)", "%d name line(s)" % len(names)))
    minutes = re.findall(r"^\s*[-*]?\s*MINUTE\s+\S+.*\|\s*over20=(\d+)\s*\|\s*invocations=(\d+)", body["Beside"], re.M)
    res.append(say(bool(minutes), "S6 at least one MINUTE line with its over-20 s and invocation counts", "%d line(s)" % len(minutes)))
    bullets = [ln for ln in body["Sources"].splitlines() if ln.lstrip().startswith(("-", "*"))]
    nodenom = [b for b in bullets if not re.search(r"\bn=\d+\b", b)]
    res.append(say(len(bullets) >= 2 and not nodenom, "S7 at least two sources, each with an n=<integer>", "%d bullets, %d without n=" % (len(bullets), len(nodenom))))
    surf = body["Surfaces"]
    n_read = len(re.findall(r"^\s*[-*]?\s*READ:\s*\S", surf, re.M))
    n_not = len(re.findall(r"^\s*[-*]?\s*NOT READ:\s*\S", surf, re.M))
    res.append(say(n_read >= 2 and n_not >= 1, "S8 at least two surfaces read and one named as not read", "read %d, not read %d" % (n_read, n_not)))
    res.append(say("WRITES: none" in body["Not changed"], "S9 nothing was written"))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R99 OVERLAY TAIL READING SHAPE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
