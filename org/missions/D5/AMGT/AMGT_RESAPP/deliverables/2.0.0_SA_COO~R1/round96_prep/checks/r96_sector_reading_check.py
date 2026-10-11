"""AMGT_RESAPP round-96 PREP -- the SHAPE of the listing-sector reading (CTO round-95 analysis item 1).

  python r96_sector_reading_check.py <reading.md>

Question the reading answers: does the STORED Bloomberg-fed data for the LISTING of `SAN_FP_Equity` (SAN FP) and `CSL_AU_Equity` (CSL AU) already carry a sector or industry
field (a GICS or BICS sector, industry group, industry), so that a classification could be served from an exchange-qualified source rather than from the classifications table's
bare-ticker row? No Bloomberg call is made: the reading is of already-landed objects only. This check grades the SHAPE (the outcome itself is the CVO's judgment). The file holds
these level-2 headings, each non-empty, in this order:

    ## Sources      one bullet per source read: the object or table, its key or path, its vintage, and a denominator `n=<integer>` (rows, fields or objects read)
    ## Listings     for EACH of SAN_FP_Equity and CSL_AU_Equity: the Bloomberg ticker, then a line `FIELDS: none` or `FIELDS: <name>=<value>; <name>=<value>` of every field whose
                    name matches sector, industry, GICS, BICS or SIC, and a line `SOURCE: <object and field path>` (or `SOURCE: none`)
    ## Census       `fields scanned n=<integer>` and `matched n=<integer>` (the denominator of the field-name sweep, over every object named in Sources)
    ## Control      `CONTROL: <security_key> FIELDS: <name>=<value>; ...` for ONE listing known to be served with a sector today, read by the SAME sweep: the proof that the
                    sweep can see a sector field (an absence is not read without it)
    ## Surfaces     lines `READ: <surface>` (at least two) and `NOT READ: <surface>` (at least one: the surface next door that this reading did not reach)
    ## Outcome      ONE line `OUTCOME: SECTOR-SERVED`, `OUTCOME: SECTOR-ABSENT` or `OUTCOME: PARTIAL`; for SECTOR-SERVED or PARTIAL a line `SERVE-FROM: <source and field>`
    ## Not changed  `WRITES: none` and `BLOOMBERG CALLS: none`

    S1 every heading present, in order, non-empty.
    S2 `## Sources` has at least three bullets, each with an `n=<integer>`.
    S3 `## Listings` names both keys and each carries a `FIELDS:` line and a `SOURCE:` line.
    S4 `## Census` carries `fields scanned n=<integer>` and `matched n=<integer>`.
    S5 `## Control` carries a `CONTROL:` line whose FIELDS is not `none`.
    S6 `## Surfaces` carries at least two `READ:` lines and at least one `NOT READ:` line.
    S7 `## Outcome` carries exactly one allowed `OUTCOME:` line (and `SERVE-FROM:` unless SECTOR-ABSENT).
    S8 `## Not changed` carries `WRITES: none` and `BLOOMBERG CALLS: none`.
Verdict: R96 SECTOR READING SHAPE: YES|NO (exit 0|1). At the base: NO (no reading exists).
"""
import re
import sys

HEADINGS = ("Sources", "Listings", "Census", "Control", "Surfaces", "Outcome", "Not changed")
OUTCOMES = ("SECTOR-SERVED", "SECTOR-ABSENT", "PARTIAL")
KEYS = ("SAN_FP_Equity", "CSL_AU_Equity")


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


def main():
    if len(sys.argv) != 2:
        print("usage: r96_sector_reading_check.py <reading.md>")
        return 2
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        say(False, "S1 the reading exists", "%s: %s" % (type(exc).__name__, exc))
        print("R96 SECTOR READING SHAPE: NO")
        return 1
    found, order = sections(text)
    body = {h: "\n".join(found.get(h, [])).strip() for h in HEADINGS}
    present = [h for h in order if h in HEADINGS]
    res = [say(present == list(HEADINGS) and all(body[h] for h in HEADINGS), "S1 every heading is present, in order, non-empty",
               "headings %s, empty %s" % (present, [h for h in HEADINGS if not body.get(h)]))]
    bullets = [ln for ln in body["Sources"].splitlines() if ln.lstrip().startswith(("-", "*"))]
    nodenom = [b for b in bullets if not re.search(r"\bn=\d+\b", b)]
    res.append(say(len(bullets) >= 3 and not nodenom, "S2 at least three sources, each with an n=<integer> denominator",
                   "%d bullets, %d without a denominator" % (len(bullets), len(nodenom))))
    listings = body["Listings"]
    miss = []
    for k in KEYS:
        i = listings.find(k)
        if i < 0:
            miss.append(k)
            continue
        nxt = min([listings.find(o, i + len(k)) for o in KEYS if o != k and listings.find(o, i + len(k)) >= 0] or [len(listings)])
        chunk = listings[i:nxt]
        if not re.search(r"^\s*[-*]?\s*FIELDS:\s*\S", chunk, re.M) or not re.search(r"^\s*[-*]?\s*SOURCE:\s*\S", chunk, re.M):
            miss.append(k + " (FIELDS or SOURCE line)")
    res.append(say(not miss, "S3 both listings carry a FIELDS line and a SOURCE line", "missing %s" % miss))
    census = body["Census"]
    res.append(say(bool(re.search(r"fields scanned n=\d+", census)) and bool(re.search(r"matched n=\d+", census)),
                   "S4 the field-name sweep states its denominator and its matches"))
    ctl = re.search(r"CONTROL:\s*(\S+)\s+FIELDS:\s*(.+)", body["Control"])
    res.append(say(bool(ctl) and ctl.group(2).strip().lower() not in ("none", ""), "S5 a control listing shows the sweep can see a sector field",
                   "control %s" % (ctl.group(1) if ctl else None)))
    surf = body["Surfaces"]
    n_read = len(re.findall(r"^\s*[-*]?\s*READ:\s*\S", surf, re.M))
    n_not = len(re.findall(r"^\s*[-*]?\s*NOT READ:\s*\S", surf, re.M))
    res.append(say(n_read >= 2 and n_not >= 1, "S6 at least two surfaces read and one named as not read", "read %d, not read %d" % (n_read, n_not)))
    outs = re.findall(r"^\s*[-*]?\s*OUTCOME:\s*([A-Z-]+)\s*$", body["Outcome"], re.M)
    serve = bool(re.search(r"^\s*[-*]?\s*SERVE-FROM:\s*\S", body["Outcome"], re.M))
    res.append(say(len(outs) == 1 and outs[0] in OUTCOMES and (outs[0] == "SECTOR-ABSENT" or serve),
                   "S7 exactly one allowed OUTCOME (and SERVE-FROM unless SECTOR-ABSENT)", "outcomes %s serve-from %s" % (outs, serve)))
    nc = body["Not changed"]
    res.append(say("WRITES: none" in nc and "BLOOMBERG CALLS: none" in nc, "S8 nothing written and no Bloomberg call"))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R96 SECTOR READING SHAPE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
