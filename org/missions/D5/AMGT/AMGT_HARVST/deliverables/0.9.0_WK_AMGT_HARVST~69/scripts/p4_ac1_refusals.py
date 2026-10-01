"""HVST-p-4 AC1: the recorded refusals of ft and barrons beside bbg's and wsj's responses, the session envelopes'
presence/age/source (no content), and the request differences by file:line. LOCAL READS ONLY."""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p4_common as C  # noqa: E402

restore = C.block_sockets()  # AC1 needs no network either; prove it
print("SOCKETS: creation blocked and asserted for the duration of this script")
print("NOW_UTC:", dt.datetime.now(dt.timezone.utc).isoformat())

ev = C.events()
jobs = C.job_files()
print("events.jsonl rows read:", len(ev), "| o-5 run records:", ", ".join(C.O5_RUNS), "| jobs in them:", len(jobs))

http_counts = {}
for pub in C.PUBS:
    pjobs = [(r, j) for r, j in jobs if j["publisher"] == pub]
    print("\n" + "=" * 100)
    print("PUBLISHER %s -- jobs in the o-5 runs: %d" % (pub.upper(), len(pjobs)))
    total_http = 0
    for run_id, job in pjobs:
        window = C.job_events(job, ev)
        https = [e for e in window if e["event"] == "http"]
        total_http += len(https)
        print("-" * 100)
        print("JOB %s (run %s)" % (job["job_id"], run_id))
        print("  runs/%s.json: status=%s detail=%r auth_refreshes=%s verification_repairs=%s accepted=%d retry_at=%s" % (
            job["job_id"], job["status"], job.get("detail"), job["auth_refreshes"], job["verification_repairs"],
            len(job["accepted"]), job.get("retry_at")))
        print("  window %s .. %s ; events in window for %s: %d (of which http: %d)" % (
            job["started_at"], job["finished_at"], pub, len(window), len(https)))
        for i, e in enumerate(window, start=1):
            if e["event"] == "http":
                print("   %2d %s http   %-18s %-70s status=%s bytes=%s" % (
                    i, e["at"][11:26], e["host"], e["path"][:70], e["status"], e["bytes"]))
            else:
                extra = e.get("detail") or e.get("status") or ""
                print("   %2d %s %-22s %s" % (i, e["at"][11:26], e["event"], str(extra)[:110]))
        by_status = {}
        for e in https:
            by_status[e["status"]] = by_status.get(e["status"], 0) + 1
        print("  http responses by status: %s" % (by_status or "0 (no request made)"))
        kinds = {}
        for e in window:
            kinds[e["event"]] = kinds.get(e["event"], 0) + 1
        for name in ("reauth_started", "reauth_succeeded", "retry_after_reauth", "verification_started",
                     "verification_succeeded", "retry_after_verification"):
            print("  %-26s %d" % (name, kinds.get(name, 0)))
    http_counts[pub] = total_http
    print("PUBLISHER %s TOTAL http events across its o-5 jobs: %d" % (pub, total_http))

# Counts the criterion asks to be printed (0 named as 0) and hard-asserted so a drift in the ledger fails the script.
print("\n" + "=" * 100)
print("COUNTS (http request/response events over the o-5 jobs):", http_counts)
assert http_counts["barrons"] == 4, http_counts
assert http_counts["ft"] == 1, http_counts  # the second ft job (cooldown) made 0
assert http_counts["bbg"] > 5 and http_counts["wsj"] > 5, http_counts
ftjobs = [j for _, j in jobs if j["publisher"] == "ft"]
assert [j["status"] for j in ftjobs] == ["request_rejected", "cooldown"], [j["status"] for j in ftjobs]
print("ASSERTED: barrons 4 http (client, client, search, client); ft 1 http (search 403) + 0 in the cooldown job; bbg/wsj > 5 each")

# Same-run contrast for barrons: its run holds no other publisher.
b_run = [r for r, j in jobs if j["publisher"] == "barrons"][0]
others = [j["publisher"] for r, j in jobs if r == b_run and j["publisher"] != "barrons"]
print("barrons run %s holds other publishers' jobs: %d %s -> its bbg/wsj comparison is the SAME-DAY four-publisher run "
      "20260930T044003Z-run-b75f9299 (wsj went through the same logged-out -> reauth -> /search path and was 200)" % (
          b_run, len(others), others))

# The challenge marker: the ledger keeps no bodies; the marker is proven by the exception class in the job detail.
print("\n" + "=" * 100)
print("CHALLENGE MARKER (what the record can and cannot show)")
tp = C.LIB / "transport.py"
c_status, _ = C.cite(tp, "if response.status_code in (401, 403):")
c_marks, mn = C.cite(tp, '"captcha-delivery.com"')
c_raise_v, _ = C.cite(tp, 'raise VerificationRequired(f"Publisher verification challenge')
c_raise_r, _ = C.cite(tp, 'raise RequestRejected(f"HTTP')
print("  %s status in (401,403) -> marker test over response.text.lower(); markers at %s: %s" % (
    c_status, c_marks, C.line_text(tp, mn) + " " + C.line_text(tp, mn + 1)))
print("  marker matched  -> %s raises VerificationRequired 'Publisher verification challenge from <host>'" % c_raise_v)
print("  marker absent   -> %s raises RequestRejected 'HTTP <status> from <host><path>'" % c_raise_r)
bj = [j for _, j in jobs if j["publisher"] == "barrons"][0]
fj = ftjobs[0]
print("  barrons detail=%r  => a marker MATCHED (which of the five is not recorded: bodies are not kept)" % bj["detail"])
print("  ft      detail=%r  => NO marker matched; 403 with %s bytes (see ft history below)" % (
    fj["detail"], [e["bytes"] for e in C.job_events(fj, ev) if e["event"] == "http"]))
print("  runtime evidence of the challenge vendor on barrons: nopecha-barrons-compatibility.json (non-secret, 2026-09-15): ", end="")
import json  # noqa: E402
nc = json.loads((C.RUNTIME / "nopecha-barrons-compatibility.json").read_text(encoding="utf-8"))
print("challenge_host=%s provider=%s" % (nc["challenge_host"], nc["provider"]))

# History of the same routes across the ledger (the whole ledger, denominator printed).
print("\n" + "=" * 100)
print("LEDGER HISTORY of the refused routes (whole events.jsonl, %d rows)" % len(ev))
for pub, route in (("ft", "/search"), ("barrons", "/search")):
    rows = [e for e in ev if e["event"] == "http" and e["publisher"] == pub and e["path"] == route]
    print("  %s %s: %d responses" % (pub, route, len(rows)))
    for e in rows:
        print("     %s status=%s bytes=%s" % (e["at"][:19], e["status"], e["bytes"]))
for pub in ("barrons",):
    rows = [e for e in ev if e["event"] == "http" and e["publisher"] == pub and e["path"] == "/client"]
    print("  %s /client: %d responses; bytes distribution: %s" % (
        pub, len(rows), sorted({(e["bytes"]) for e in rows})))
print("  (a 112-byte or 104-byte /client is the logged-out answer: DowJones.check() found no isLoggedIn; the 3.2KB one is logged in)")

# Session envelopes: os.stat only.
print("\n" + "=" * 100)
print("SESSION ENVELOPES (secrets/<pub>.dpapi: os.stat ONLY, never opened; cookies/contents never read)")
first_ledger = ev[0]["at"]
print("  first row of events.jsonl: %s" % first_ledger)
for pub in C.PUBS:
    s = C.session_stat(pub)
    print("  %-8s present=%s bytes=%s mtime_utc=%s  age_now=%s d" % (
        pub, s["present"], s.get("bytes"), s.get("mtime_utc"), s.get("age_now_days")))
    reauth = [e for e in ev if e["event"] == "reauth_started" and e["publisher"] == pub]
    af = C.auth_folders(pub)
    vf = C.verification_folders(pub)
    print("           SessionManager.refresh() runs recorded (reauth_started): %d ; auth/ folders: %d ; verification/ folders: %d" % (
        len(reauth), len(af), len(vf)))
    for n, m in af:
        print("             auth/%s (mtime %s)" % (n, m[:19]))
    if pub == "ft":
        gap = (C.ts(first_ledger) - C.ts(s["mtime_utc"])).total_seconds()
        job0 = [j for _, j in jobs if j["publisher"] == "ft"][0]
        print("           => AGE at the refused o-5 ft job (%s): %.2f days" % (job0["started_at"][:19],
              (C.ts(job0["started_at"]) - C.ts(s["mtime_utc"])).total_seconds() / 86400))
        print("           => SOURCE: the ft envelope has NO auth/ folder and NO reauth event, so SessionManager.refresh (auth.py) did not mint it; "
              "it was written %.0f s BEFORE the first row of the ledger (import-session or a hand-run harvester; which of the two is not recorded)." % gap)
        print("              the ledger's last ft /search 200 is %s; ft.dpapi has not been rewritten since %s" % (
            [e["at"][:19] for e in ev if e["event"] == "http" and e["publisher"] == "ft" and e["path"] == "/search"
             and e["status"] == 200][-1], s["mtime_utc"][:19]))
    if pub == "barrons":
        job0 = [j for _, j in jobs if j["publisher"] == "barrons"][0]
        first_client = [e for e in C.job_events(job0, ev) if e["event"] == "http"][0]
        search = [e for e in C.job_events(job0, ev) if e["event"] == "http" and e["path"] == "/search"][0]
        prior = C.auth_folders("barrons")[-2]
        print("           => BEFORE the attempt: the envelope in use was the one written by the 09-23 reauth (auth/%s, mtime %s), "
              "%.2f days before the attempt's first /client (%s bytes = logged out)." % (
                  prior[0], prior[1][:19], (C.ts(first_client["at"]) - C.ts(prior[1])).total_seconds() / 86400, first_client["bytes"]))
        print("           => SOURCE of the envelope in use at the refusal: the attempt's own SessionManager.refresh -> auth.py (dowjones_harvest_session.py), "
              "mtime %s = reauth_succeeded; the /search 401 came %.1f s after it." % (
                  s["mtime_utc"][11:23], (C.ts(search["at"]) - C.ts(s["mtime_utc"])).total_seconds()))
    if pub == "wsj":
        print("           => wsj: same script (dowjones_harvest_session.py), own reauth at 04:45:47Z, then rewritten at each job end by persist_http_cookies.")
    if pub == "bbg":
        print("           => bbg: envelope rewritten at each job end (persist_http_cookies) and by repair_verification (auth.py:45-52 saves the repaired envelope).")

# Request differences by file:line.
print("\n" + "=" * 100)
print("REQUEST DIFFERENCES ft/barrons vs bbg/wsj, by file:line")
P = C.LIB / "publishers.py"
W = C.LIB / "worker.py"
A = C.LIB / "auth.py"
V = C.LIB / "verification.py"
FT = C.SCRIPTS / "ft_rest_fetch.py"
BB = C.SCRIPTS / "bloomberg_rest_fetch.py"
rows = []


def row(label, path, pattern, after=0):
    ref, n = C.cite(path, pattern, after)
    rows.append((label, ref, C.line_text(path, n)))
    print("  %-46s %s\n        %s" % (label, ref, C.line_text(path, n)[:150]))
    return n


print("-- transport per publisher")
row("bbg: session builder call", P, 'inner = self._module.build_session(bundle=bundle)')
row("bbg: curl_cffi chrome impersonation", BB, 'creq.Session(impersonate="chrome"')
row("bbg: User-Agent taken from the bundle", BB, '"User-Agent": bundle.get("user_agent")')
row("ft:  session builder call (native, no proxy)", P, 'inner = self._module.build_session(use_proxy=False, bundle=bundle)')
row("ft:  curl_cffi chrome, verify=False", FT, 'kwargs = {"impersonate": "chrome", "timeout": 70, "verify": False}')
row("ft:  HARD-CODED User-Agent Chrome/126 (not the bundle's)", FT, '"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
row("ft:  bundle cookies set on .ft.com", FT, 's.cookies.set(name, value, domain=".ft.com", path="/")')
row("wsj: UA from the bundle (wsj only)", P, 'headers = {"User-Agent": bundle["user_agent"]} if pub == "wsj" else {}')
row("wsj/barrons: curl_cffi chrome session", P, 'inner = requests.Session(impersonate="chrome", timeout=45, headers=headers)')
print("   => barrons gets NO User-Agent override (headers={} at the line above): curl_cffi's own Chrome default UA; "
      "contracts.json requires exactly that for barrons.")
row("barrons contract: curl default UA", C.LIB / "contracts.json", 'curl Chrome default User-Agent consistent with its impersonation')
print("-- the request itself")
row("ft:  GET https://www.ft.com/search?q=<company>", P, 'response = self.session.get("https://www.ft.com/search"')
row("wsj/barrons: GET /client?legacy=false (auth oracle)", P, 'response = self.session.get(self.base + "/client?legacy=false"')
row("wsj/barrons: logged-out test (isLoggedIn)", P, 'if not isinstance(value, dict) or value.get("isLoggedIn") is not True:')
row("wsj/barrons: GET /search?query=<company>", P, 'response = self.session.get(self.base + "/search", params=params,')
print("   => the wsj and barrons request lines are the SAME code (DowJones class); they differ only in host and in the UA line above.")
print("-- what happens after a refusal")
row("worker: two-attempt loop", W, 'for attempt in range(2):')
row("worker: AuthExpired -> reauth, uses attempt 0", W, 'except AuthExpired:')
row("worker: reauth call", W, 'envelope = self.sessions.refresh(publisher)')
row("worker: VerificationRequired branch", W, 'except VerificationRequired as exc:')
row("worker: repair ONLY on attempt 0 and ONLY bbg/barrons", W, 'if attempt or publisher not in {"bbg", "barrons"}:')
row("worker: RequestRejected -> request_rejected + 900s", W, 'except RequestRejected as exc:')
row("auth: reauth path for wsj/barrons (Dow Jones SSO)", A, 'if publisher in {"wsj", "barrons"}:')
row("auth: reauth path for every other publisher (ft: ft_harvest_session)", A, 'module = importlib.util.module_from_spec(spec)')
row("publishers: check_auth (ft: nothing to check)", P, 'def check_auth(self):')
row("publishers: FT comment 'an isolated 403 does not log in'", P, "# FT's observed login redirect")
row("verification: repair() refuses every publisher but bbg/barrons", V, 'if publisher not in {"bbg", "barrons"}:')
row("contracts: barrons automatic verification ENABLED", C.LIB / "contracts.json", '"automatic_verification_enabled": true')
row("contracts: ft refresh_signal = 403 alone is NOT a re-auth", C.LIB / "contracts.json",
    '"refresh_signal": "Verified publisher logout or login redirect; 401/403 alone is request_rejected, not reauthentication"',
    after=C.find_line(C.LIB / "contracts.json", '"Financial Times"'))
row("cli: import-session (how a session is placed by hand)", C.LIB / "__main__.py", 'if args.command == "import-session":')

# Where ft and barrons differ from bbg and wsj -- stated from the rows above and the recorded sequences.
print("\nDIFFERENCE SUMMARY (measured rows above; no inference in this block)")
print("  bbg  : attempt 0 got 403 + challenge marker -> worker.py branch 'except VerificationRequired' RAN (attempt 0, bbg in set) -> "
      "verification_started/succeeded -> retry -> 200. (events in the bbg job above)")
print("  wsj  : attempt 0 got a logged-out /client -> AuthExpired -> reauth -> retry -> /client 200, /search 200. No challenge.")
print("  barrons: attempt 0 got a logged-out /client -> AuthExpired -> reauth (spends attempt 0) -> retry at attempt 1 -> /search 401 + challenge marker "
      "-> VerificationRequired at attempt 1 -> the guard 'if attempt or ...: raise' re-raises -> request_rejected. verification_repairs=0, "
      "verification_started events=0.")
print("  ft   : ONE GET /search -> 403, 270955 bytes, no marker -> RequestRejected -> check_auth is a no-op for ft -> re-raised -> request_rejected. "
      "ft is outside the worker's verification set and has no repair() in verification.py; nothing else in the path can act on a bare 403.")
restore()
print("\nAC1 DONE rows_cited=%d" % len(rows))
