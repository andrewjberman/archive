"""AMGT_RESAPP round-98 PREP -- the SHAPE of the payload-key reading (CTO round-97 analysis item 2; AMGT_CORPUS round-47 ADDENDUM 1).

  python r98_payload_key_reading_check.py <reading.md>

Question the reading answers: the Thesis payload (`/security/<key>/thesis`) serves `fiscal_year_figures` TWICE (top level and `model.fiscal_year_figures`, 32.3 percent of the
response each) and `check_face` (24.9 percent). Which of the three keys does each portal BUILD read: DEV (`origin/DEV`) and the PROD-built page (`origin/PROD`)? A key no build
reads may be dropped by a later cell under its own redeploy pair; this reading drops nothing and writes nothing. This check grades the SHAPE (the outcomes are the CVO's
judgment). The file holds these level-2 headings, each non-empty, in this order:

    ## Sources      one bullet per source read: the ref, the tree and file set, the tool, and a denominator `n=<integer>`
    ## Keys         for EACH of `fiscal_year_figures` (top level), `model.fiscal_year_figures` and `check_face`: one line
                    `KEY: <key> | DEV: <n> site(s) <file:line, ...> | PROD: <n> site(s) <file:line, ...>` (`0 site(s) none` when unread), each site classified in words as a
                    top-level read or a model read where the key name alone is ambiguous
    ## Census       `DEV files scanned n=<integer>`, `PROD files scanned n=<integer>` and `matched n=<integer>` (the sweep's denominator over the portal's `src/`)
    ## Control      `CONTROL: <key> | DEV: <n> | PROD: <n>` for ONE key the builds are known to read differently or at all (for example `team_sheet`: round 46's reading is 0 files
                    on PROD), run by the SAME sweep: the proof that the sweep sees a read and distinguishes the two builds
    ## Surfaces     lines `READ: <surface>` (at least two) and `NOT READ: <surface>` (at least one: for example the built bundle's minified code, a consumer outside
                    `src/pages/SecurityAnalysis`, the print or PDF route, another client of the API)
    ## Outcome      exactly three lines `OUTCOME <key>: READ-BY-BOTH|READ-BY-DEV-ONLY|READ-BY-PROD-ONLY|READ-BY-NEITHER`, one per key
    ## Not changed  `WRITES: none`

    S1 every heading present, in order, non-empty.
    S2 `## Sources` has at least three bullets, each with an `n=<integer>`.
    S3 `## Keys` carries one `KEY:` line for each of the three keys, each with a DEV and a PROD count.
    S4 `## Census` carries `DEV files scanned n=`, `PROD files scanned n=` and `matched n=`.
    S5 `## Control` carries a `CONTROL:` line with a DEV and a PROD count, at least one of them above 0.
    S6 `## Surfaces` carries at least two `READ:` lines and at least one `NOT READ:` line.
    S7 `## Outcome` carries exactly one allowed `OUTCOME <key>:` line for each of the three keys.
    S8 `## Not changed` carries `WRITES: none`.
Verdict: R98 PAYLOAD KEY READING SHAPE: YES|NO (exit 0|1). At the base: NO (no reading exists).
"""
import re
import sys

HEADINGS = ("Sources", "Keys", "Census", "Control", "Surfaces", "Outcome", "Not changed")
KEYS = ("fiscal_year_figures", "model.fiscal_year_figures", "check_face")
OUTCOMES = ("READ-BY-BOTH", "READ-BY-DEV-ONLY", "READ-BY-PROD-ONLY", "READ-BY-NEITHER")


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
        print("usage: r98_payload_key_reading_check.py <reading.md>")
        return 2
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        say(False, "S1 the reading exists", "%s: %s" % (type(exc).__name__, exc))
        print("R98 PAYLOAD KEY READING SHAPE: NO")
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
    miss = []
    for k in KEYS:
        pat = r"^\s*[-*]?\s*KEY:\s*%s\s*\|\s*DEV:\s*\d+.*\|\s*PROD:\s*\d+" % re.escape(k)
        if not re.search(pat, body["Keys"], re.M):
            miss.append(k)
    res.append(say(not miss, "S3 each of the three keys has a KEY line with a DEV and a PROD count", "missing %s" % miss))
    cen = body["Census"]
    res.append(say(all(re.search(p, cen) for p in (r"DEV files scanned n=\d+", r"PROD files scanned n=\d+", r"matched n=\d+")),
                   "S4 the sweep states its denominators and its matches"))
    ctl = re.search(r"CONTROL:\s*(\S+)\s*\|\s*DEV:\s*(\d+)\s*\|\s*PROD:\s*(\d+)", body["Control"])
    res.append(say(bool(ctl) and (int(ctl.group(2)) > 0 or int(ctl.group(3)) > 0), "S5 a control key shows the sweep sees a read",
                   "control %s" % (str(ctl.groups()) if ctl else "None")))
    surf = body["Surfaces"]
    n_read = len(re.findall(r"^\s*[-*]?\s*READ:\s*\S", surf, re.M))
    n_not = len(re.findall(r"^\s*[-*]?\s*NOT READ:\s*\S", surf, re.M))
    res.append(say(n_read >= 2 and n_not >= 1, "S6 at least two surfaces read and one named as not read", "read %d, not read %d" % (n_read, n_not)))
    outs = re.findall(r"^\s*[-*]?\s*OUTCOME\s+(\S+?):\s*([A-Z-]+)\s*$", body["Outcome"], re.M)
    got = {k: v for k, v in outs}
    res.append(say(sorted(got) == sorted(KEYS) and len(outs) == 3 and all(v in OUTCOMES for v in got.values()),
                   "S7 exactly one allowed OUTCOME line for each of the three keys", "outcomes %s" % outs))
    res.append(say("WRITES: none" in body["Not changed"], "S8 nothing was written"))
    print("   arms passed %d of %d" % (sum(1 for r in res if r), len(res)))
    ok = all(res)
    print("R98 PAYLOAD KEY READING SHAPE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
