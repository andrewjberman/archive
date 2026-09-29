"""HVST-e-2 AC1: THE ACT (the ONLY writer in this cell) and its proof against the pair.

Sequence: (a) BEFORE from S3, refusing to go on if it differs from the COO half s.3; a pre-put in-memory
prediction set against the pair (a move outside it stops the run BEFORE the first put); (b) `build-mention`,
then -- only if it exits 0 -- `build-daily`, each ONCE, output verbatim; (c) AFTER re-read through
`publication_gold._latest_gold_snapshot_rows`; (d) moved rows set against the pair; (e) every prior part still
exists with its ETag unchanged. NO delete anywhere. NO event put. Re-running after a put stops at (a)."""
import datetime
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402
import _e2 as E  # noqa: E402

NEW = C.NEW
T_M, T_D, T_E = NEW.GOLD_TABLE, NEW.GOLD_DAILY_TABLE, NEW.GOLD_EVENT_TABLE


def say(s=""):
    print(s)
    sys.stdout.flush()


def run_producer(command, as_of):
    cmd = [sys.executable, "-m", "lib.research.harvest.publication_gold", command,
           "--securities-json", C.SECURITIES, "--as-of", as_of.isoformat()]
    say("$ python -m lib.research.harvest.publication_gold %s --securities-json <%s> --as-of %s" % (
        command, C.SECURITIES.split("deliverables" + C.os.sep)[-1].replace("\\", "/"), as_of))
    p = subprocess.run(cmd, cwd=C.REPO, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    say("rc=%d" % p.returncode)
    say("stdout: %s" % C.a(out).strip())
    if err.strip():
        say("stderr: %s" % C.a(err).strip())
    return p.returncode, out


def new_part(before_parts, after_parts):
    b = {p[0] for p in before_parts}
    return [p for p in after_parts if p[0] not in b]


def main():
    client = C.store._default_client()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    say("== (a) BEFORE, from S3 (as-of for both producers = today UTC = %s; the halves allow %s) ==" % (
        as_of, " or ".join(str(d) for d in E.AS_OF_ALLOWED)))
    before = E.snapshot(client)
    stop = []
    for t in C.TABLES:
        parts = before[t]
        key, etag, _size = parts[-1]
        rows = NEW._latest_gold_snapshot_rows(t, client=client)
        want = E.BEFORE_EXPECT[t]
        got = (len(parts), C.short(key), etag, len(rows))
        say("%-26s parts=%d newest=%s ETag=%s rows=%d   as at the cut: %s -> %s" % (
            t, got[0], got[1], got[2], got[3], want, "SAME" if got == want else "DIFFERENT"))
        if got != want:
            stop.append("BEFORE state of %s differs from the COO half s.3" % t)
    if as_of not in E.AS_OF_ALLOWED:
        stop.append("as-of %s is outside both halves" % as_of)
    before_rows = {t: NEW._latest_gold_snapshot_rows(t, client=client) for t in (T_M, T_D)}

    securities = C.load_securities()
    articles, title_of, hits = C.read_inputs(client)
    say("inputs: securities=%d silver articles=%d listing hits=%d" % (len(securities), len(articles), len(hits)))
    pred = C.memory(NEW, securities, articles, title_of, hits, as_of)
    o_m, l_m = E.check_mention(before_rows[T_M], pred[T_M], title_of)
    o_d, l_d = E.check_daily(before_rows[T_D], pred[T_D], as_of)
    say("PRE-PUT prediction (in memory, same functions the producers call) against the pair: mention outside=%d daily outside=%d" % (len(o_m), len(o_d)))
    stop += ["PRE-PUT %s" % s for s in o_m + o_d]
    if stop:
        for s in stop:
            say("STOP BEFORE THE FIRST PUT: %s" % s)
        say("AC1 FAIL (nothing written)")
        return 1

    say("\n== (b) THE PRODUCERS, once each, mention then daily ==")
    rc, out = run_producer("build-mention", as_of)
    if rc != 0:
        say("STOP: build-mention failed; daily is NOT built; nothing is deleted. The object, if written, stays.")
        say("AC1 FAIL")
        return 1
    mid = E.snapshot(client)
    nm = new_part(before[T_M], mid[T_M])
    for k, etag, size in nm:
        say("WRITTEN %s ETag=%s ContentLength=%d (HEAD read-back)" % (k, etag, size))
    if len(nm) != 1:
        say("STOP: expected exactly one new mention part, found %d; daily is NOT built" % len(nm))
        say("AC1 FAIL")
        return 1
    rc, out = run_producer("build-daily", as_of)
    if rc != 0:
        say("STOP: build-daily failed; nothing is deleted. The object, if written, stays.")
        say("AC1 FAIL")
        return 1

    say("\n== (c) AFTER, re-read through publication_gold._latest_gold_snapshot_rows ==")
    after = E.snapshot(client)
    fails = []
    written = {}
    for t in C.TABLES:
        fresh = new_part(before[t], after[t])
        written[t] = fresh
        key, etag, _size = after[t][-1]
        rows = NEW._latest_gold_snapshot_rows(t, client=client)
        say("%-26s parts before=%d after=%d  new parts=%d %s  newest=%s ETag=%s rows=%d" % (
            t, len(before[t]), len(after[t]), len(fresh), [C.short(p[0]) + " ETag=" + p[1] + " size=%d" % p[2] for p in fresh],
            C.short(key), etag, len(rows)))
    for t in (T_M, T_D):
        if len(written[t]) != 1 or after[t][-1][0] != written[t][0][0]:
            fails.append("newest %s part is not the one just written" % t)
    if written[T_E] or after[T_E][-1] != before[T_E][-1]:
        fails.append("chatter_event changed")
    say("newest mention and daily = the parts just written: %s ; newest event part unchanged (key, ETag, size): %s" % (
        not [f for f in fails if "newest" in f], after[T_E][-1] == before[T_E][-1]))

    say("\n== (d) MOVED ROWS against the pair ==")
    after_rows = {t: NEW._latest_gold_snapshot_rows(t, client=client) for t in (T_M, T_D)}
    o_m, l_m = E.check_mention(before_rows[T_M], after_rows[T_M], title_of)
    o_d, l_d = E.check_daily(before_rows[T_D], after_rows[T_D], as_of)
    say("-- article_security_mention (COO half s.4.1) --")
    for s in l_m:
        say(s)
    say("-- chatter_daily (COO half s.4.2) --")
    for s in l_d:
        say(s)
    say("-- chatter_event: not written; newest part unchanged: %s --" % (after[T_E][-1] == before[T_E][-1]))
    for s in o_m + o_d:
        say("OUTSIDE THE PAIR: %s" % s)
    say("OUTSIDE THE PAIR rows/counts: %d" % (len(o_m) + len(o_d)))
    fails += o_m + o_d

    say("\n== (e) every prior part still exists with its ETag unchanged ==")
    for t in C.TABLES:
        now = {p[0]: p[1] for p in after[t]}
        missing = [p[0] for p in before[t] if p[0] not in now]
        changed = [p[0] for p in before[t] if p[0] in now and now[p[0]] != p[1]]
        say("%-26s prior parts=%d present=%d ETag unchanged=%d missing=%d changed=%d" % (
            t, len(before[t]), len(before[t]) - len(missing), len(before[t]) - len(missing) - len(changed), len(missing), len(changed)))
        for k in missing:
            fails.append("prior part MISSING: %s" % k)
        for k in changed:
            fails.append("prior part ETag CHANGED: %s" % k)

    say("\nS3 KEYS WRITTEN BY THIS RUN:")
    for t in (T_M, T_D):
        for k, etag, size in written[t]:
            say("  %s ETag=%s size=%d" % (k, etag, size))
    for f in fails:
        say("FAIL: %s" % f)
    say("AC1 %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
