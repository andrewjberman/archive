"""AMGT_RESAPP round-95 PREP -- the shape of a READ-ONLY cause reading (row C-S82, CTO round-94 analysis item 3).

  python r95_reading_check.py <reading.md>

A reading names a cause from evidence and says what it did NOT see. This check grades the SHAPE only (the cause itself is the CVO's judgment criterion). The file must hold
these sections, each non-empty, in this order, with these exact level-2 headings:

    ## Sources       one bullet per source read, each with the command or API call, the window (UTC), and a DENOMINATOR line `n=<integer>` (log lines scanned,
                     datapoints returned, requests listed); a source that returned nothing says `n=0` and why
    ## Requests      the two failing requests (ROG on the Model tab, BA on the Posture tab; path `/api/scoped/amgt/security/<ticker>/compare`) as the sources show them:
                     time (UTC), layer that logged them, request id where one exists
    ## Metrics       the function's `Throttles` and `ConcurrentExecutions` over the walk window (15:30Z to 15:50Z, 2026-10-11) as `max=<number>` and `n=<datapoints>` per metric
    ## Concurrency   the function's reserved concurrency as read (`reserved=<integer>` or `reserved=none`) and the account's concurrency limit if it was readable
    ## Layers        for each layer the request crosses (dev-server proxy, CloudFront, API Gateway, Lambda): what was read there and what it shows, or `not readable: <why>`
    ## Cause         ONE line `CAUSE: <TOKEN>` with TOKEN one of THROTTLED, GATEWAY-INTEGRATION, DEV-PROXY, CLOUDFRONT, FUNCTION, UNDETERMINED, then the reasoning; for
                     UNDETERMINED a line `MISSING: <the source that would decide it>`
    ## Not changed  one line stating that nothing was written or changed in any system (`WRITES: none`)

    S1 the file exists and every heading above is present, in order, non-empty.
    S2 `## Sources` has at least three bullets and every bullet carries an `n=<integer>` denominator.
    S3 `## Metrics` carries `Throttles` and `ConcurrentExecutions`, each with `max=` and `n=`.
    S4 `## Concurrency` carries `reserved=`.
    S5 `## Cause` carries exactly one `CAUSE:` line with an allowed token (and `MISSING:` when UNDETERMINED).
    S6 `## Not changed` carries `WRITES: none`.
Verdict: R95 READING SHAPE: YES|NO (exit 0|1). At the base: NO (no reading exists).
"""
import re
import sys

HEADINGS = ("Sources", "Requests", "Metrics", "Concurrency", "Layers", "Cause", "Not changed")
TOKENS = ("THROTTLED", "GATEWAY-INTEGRATION", "DEV-PROXY", "CLOUDFRONT", "FUNCTION", "UNDETERMINED")


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def sections(text):
    found = {}
    order = []
    cur = None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            order.append(cur)
            found[cur] = []
        elif cur is not None:
            found[cur].append(line)
    return found, order


def main():
    if len(sys.argv) != 2:
        print("usage: r95_reading_check.py <reading.md>")
        return 2
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        say(False, "S1 the reading exists", "%s: %s" % (type(exc).__name__, exc))
        print("R95 READING SHAPE: NO")
        return 1
    found, order = sections(text)
    res = []
    present = [h for h in order if h in HEADINGS]
    body = {h: "\n".join(found.get(h, [])).strip() for h in HEADINGS}
    res.append(say(present == list(HEADINGS) and all(body[h] for h in HEADINGS), "S1 every heading is present, in order, non-empty",
                   "headings %s, empty %s" % (present, [h for h in HEADINGS if not body.get(h)])))
    bullets = [ln for ln in body["Sources"].splitlines() if ln.lstrip().startswith(("-", "*"))]
    nodenom = [b for b in bullets if not re.search(r"\bn=\d+\b", b)]
    res.append(say(len(bullets) >= 3 and not nodenom, "S2 at least three sources, each with an n=<integer> denominator",
                   "%d bullets, %d without a denominator" % (len(bullets), len(nodenom))))
    m = body["Metrics"]
    metrics_ok = all(re.search(r"%s[^\n]*max=[0-9.]+[^\n]*n=\d+|%s[^\n]*n=\d+[^\n]*max=[0-9.]+" % (k, k), m) for k in ("Throttles", "ConcurrentExecutions"))
    res.append(say(metrics_ok, "S3 Throttles and ConcurrentExecutions each carry max= and n="))
    res.append(say(bool(re.search(r"reserved=(\d+|none)\b", body["Concurrency"])), "S4 the reserved concurrency is stated"))
    causes = re.findall(r"^CAUSE:\s*([A-Z-]+)\s*$", body["Cause"], re.M)
    cause_ok = len(causes) == 1 and causes[0] in TOKENS and (causes[0] != "UNDETERMINED" or bool(re.search(r"^MISSING:\s*\S", body["Cause"], re.M)))
    res.append(say(cause_ok, "S5 exactly one allowed CAUSE line (and MISSING for UNDETERMINED)", "causes %s" % causes))
    res.append(say("WRITES: none" in body["Not changed"], "S6 nothing was written or changed"))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R95 READING SHAPE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
