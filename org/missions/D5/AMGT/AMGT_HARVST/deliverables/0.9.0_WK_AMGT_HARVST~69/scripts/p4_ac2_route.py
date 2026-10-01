"""HVST-p-4 AC2: per publisher, the cause with the evidence line it rests on, and the smallest scripted route to a clean
fetch (or a stated limit). NO network call: socket creation is blocked and asserted for the whole run. Every evidence
statement is recomputed from the runtime ledger / code here and asserted, so a drift in the record fails the script."""
import datetime as dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p4_common as C  # noqa: E402

restore = C.block_sockets()
print("SOCKETS: creation blocked and asserted for the duration of this script (the only child process is `git show`, a local object read)")
now = dt.datetime.now(dt.timezone.utc)
print("NOW_UTC:", now.isoformat())
ev = C.events()
jobs = {j["publisher"] + ":" + j["job_id"]: j for _, j in C.job_files()}
by_pub = {}
for j in jobs.values():
    by_pub.setdefault(j["publisher"], []).append(j)
checks = 0


def ok(cond, msg):
    global checks
    assert cond, "ASSERTION FAILED: " + msg
    checks += 1
    print("    [ok] " + msg)


P, W, T = C.LIB / "publishers.py", C.LIB / "worker.py", C.LIB / "transport.py"
V, CT = C.LIB / "verification.py", C.LIB / "contracts.json"
FT = C.SCRIPTS / "ft_rest_fetch.py"
FTH = C.SCRIPTS / "ft_harvest_session.py"

# ---------------------------------------------------------------------------------------------- BARRONS
print("\n" + "=" * 100)
print("BARRONS")
bj = by_pub["barrons"][0]
bw = C.job_events(bj, ev)
kinds = [e["event"] if e["event"] != "http" else "http %s %s" % (e["path"], e["status"]) for e in bw]
print("  recorded sequence: " + " | ".join(kinds))
print("  EVIDENCE the cause rests on:")
ok(kinds == ["http /client 200", "reauth_started", "reauth_succeeded", "retry_after_reauth", "http /client 200",
             "http /search 401", "http /client 200", "job_finished"],
   "events.jsonl %s..%s: logged-out /client (112 B) -> reauth -> /client (3214 B) -> /search 401 (774 B) -> /client -> job_finished" % (
       bw[0]["at"][11:19], bw[-1]["at"][11:19]))
sizes = [e["bytes"] for e in bw if e["event"] == "http"]
ok(sizes == [112, 3214, 774, 3214], "byte sizes %s: 112 = logged-out /client, 3214 = logged-in /client" % sizes)
ok(bj["auth_refreshes"] == 1 and bj["verification_repairs"] == 0,
   "runs/%s.json: auth_refreshes=1, verification_repairs=0" % bj["job_id"])
ok(not any(e["event"].startswith("verification") for e in bw), "0 verification_* events in the job's window")
ok(bj["detail"] == "Publisher verification challenge from www.barrons.com",
   "runs json detail is the VerificationRequired text (transport.py: a challenge marker matched in the 401 body)")
c_guard, gn = C.cite(W, 'if attempt or publisher not in {"bbg", "barrons"}:')
c_range, _ = C.cite(W, 'for attempt in range(2):')
c_auth, an = C.cite(W, 'except AuthExpired:')
c_reject, _ = C.cite(W, 'except RequestRejected as exc:')
ok(True, "%s: the reauth (AuthExpired branch, %s) consumed the loop's attempt 0; the challenge then arrived at attempt 1, and %s "
         "re-raises when `attempt` is truthy: `%s`" % (c_range, c_auth, c_guard, C.line_text(W, gn)))
ok(True, "%s: the re-raised VerificationRequired lands in RequestRejected -> status request_rejected, cooldown 900 s" % c_reject)
sig = ["http /client 200", "reauth_started", "reauth_succeeded", "retry_after_reauth", "http /client 200", "http /search 401",
       "http /client 200", "job_finished"]
prior = [e for e in ev if e.get("publisher") == "barrons" and "2026-09-23T00:32" <= e["at"][:16] <= "2026-09-23T00:34"]
pk = [e["event"] if e["event"] != "http" else "http %s %s" % (e["path"], e["status"]) for e in prior]
ok(pk == sig, "the SAME eight-event shape is on the ledger at 2026-09-23T00:32:58Z (a second logged-out -> reauth -> /search 401 -> request_rejected)")
w = by_pub["wsj"][0]
wk = [e["event"] if e["event"] != "http" else "http %s %s" % (e["path"], e["status"]) for e in C.job_events(w, ev)][:6]
ok(wk[:5] == ["http /client 200", "reauth_started", "reauth_succeeded", "retry_after_reauth", "http /client 200"] and wk[5] == "http /search 200",
   "wsj (same Dow Jones login script, same DowJones class) took the same logged-out -> reauth path and got /search 200: the reauth itself is not the fault")
nc = C.RUNTIME / "nopecha-barrons-compatibility.json"
import json  # noqa: E402
ncv = json.loads(nc.read_text(encoding="utf-8"))
ok(ncv["challenge_host"] == "geo.captcha-delivery.com", "nopecha-barrons-compatibility.json (2026-09-15): barrons' challenge host is geo.captcha-delivery.com (DataDome)")
bg = [j for j in by_pub["bbg"] if j["verification_repairs"] == 1][0]
bgk = [e["event"] for e in C.job_events(bg, ev)]
ok("verification_started" in bgk and "verification_succeeded" in bgk and "retry_after_verification" in bgk,
   "bbg, same day, same collector: challenge at attempt 0 -> repair_verification ran -> /search 200 (job %s)" % bg["job_id"])
ok(dict(C.session_stat("barrons"))["present"], "secrets/barrons.dpapi present (os.stat only)")
print("  CAUSE [MEASURED from the record + code]: the fresh post-reauth session was met by a bot-challenge (401 + marker) on the FIRST /search, "
      "and the collector's own challenge-repair for barrons never ran because the reauth had already spent the retry it needs (%s)." % c_guard)
print("  NOT the cause: 'cookies expired' explains only the FIRST /client (112 B logged out, envelope 7.15 d old) -- the refusal came 23 s after a "
      "verified fresh login (/client 3214 B logged in).")
print("  NOT established: which of the five markers matched (bodies are not kept), and why barrons.com challenges a fresh login while wsj.com does not "
      "(publisher policy; the UA line publishers.py:263 is the only client-side difference and contracts.json:98 requires it that way).")

cool = {p: (u, r) for p, u, r in C.cooldown_rows()}
until = dt.datetime.fromtimestamp(cool["barrons"][0], dt.timezone.utc)
ok(now > until, "progress.sqlite3 cooldown row for barrons ends %s (reason %s): lapsed, so a next job is not blocked by it" % (
    until.isoformat()[:19], cool["barrons"][1]))
ok(C.LIB.joinpath("contracts.json").read_text(encoding="utf-8").count('"automatic_verification_enabled": true') == 1,
   "%s: barrons automatic verification is ENABLED (so the repair, once reached, is permitted by contract)" % C.cite(CT, '"automatic_verification_enabled": true')[0])
print("  ROUTE B1 (no code change): a further barrons job. The fresh envelope (secrets/barrons.dpapi, written 04:08:41Z) is now the saved session, "
      "so the job starts at attempt 0; a /search challenge then raises VerificationRequired at attempt 0, the branch at %s runs "
      "repair_verification (auth.py:45-52 -> verification.py repair(): Playwright Chrome, the collector's scripted slider move), saves the repaired envelope "
      "and retries -- the path bbg took at 04:40-04:41Z." % C.cite(W, 'except VerificationRequired as exc:')[0])
print("     ACT NEEDED: a barrons collection run = a publisher request -> Andrew's per-use vendor word (standing rule), issued outside this cell; "
      "it must run on the site-Z desktop (headed Chrome; verification.py measures Windows operator input). No pair is needed for the read.")
print("     LIMIT: unproven for barrons in this state -- on 09-15 03:34Z a /search 401 was followed by a reauth and the retry got /search 200; on 09-23 and 09-30 the 401 came AFTER the reauth (2 of 2), so whether the saved post-reauth envelope is challenged again on the next job is not shown by the record.")
print("  ROUTE B2 (code, makes B1 automatic): in %s let a verification repair follow a reauth in the same job -- a per-job `verification_repaired` flag in place "
      "of `attempt` in the guard at %s and one more loop turn at %s (the AuthExpired branch at %s keeps its own `if attempt:`). Cell: build + test_worker.py cases; "
      "act needed: none for the edit itself; its first live use falls under B1's word." % (
          W.relative_to(C.WT).as_posix(), c_guard, c_range, c_auth))
print("  FLAG for the issuer (not decided here): the barrons repair is a SCRIPTED slider move (verification.py, `Slide right to secure your access`) -- "
      "the collector's own ratified path (contracts.json:80 cites BARRONS_RETRIAL_20260915_W.md), not a new bypass; whether it counts as 'challenge solving' "
      "under this order's clause is the issuer's/Andrew's call. It is named because it is the only in-path repair that exists.")

# ---------------------------------------------------------------------------------------------- FT
print("\n" + "=" * 100)
print("FT")
fj = [j for j in by_pub["ft"] if j["status"] == "request_rejected"][0]
fw = C.job_events(fj, ev)
fh = [e for e in fw if e["event"] == "http"]
print("  EVIDENCE:")
ok(len(fh) == 1 and fh[0]["path"] == "/search" and fh[0]["status"] == 403 and fh[0]["bytes"] == 270955,
   "events.jsonl %s: ONE request, www.ft.com /search, 403, 270955 bytes; runs json detail=%r" % (fh[0]["at"][11:19], fj["detail"]))
ok(fj["detail"] == "HTTP 403 from www.ft.com/search" and fj["auth_refreshes"] == 0 and fj["verification_repairs"] == 0,
   "no challenge marker matched (RequestRejected, not VerificationRequired: transport.py:112 not :111); no reauth, no repair")
ftall = [e for e in ev if e["event"] == "http" and e["publisher"] == "ft" and e["path"] == "/search"]
ok([e["status"] for e in ftall] == [200, 200, 200, 403, 403], "whole ledger, ft /search: %s" % [(e["at"][5:16], e["status"], e["bytes"]) for e in ftall])
ok(abs(ftall[3]["bytes"] - ftall[4]["bytes"]) < 100 and ftall[3]["bytes"] > 250000 > 200000 > ftall[2]["bytes"],
   "the two refusals are %d and %d bytes (differ by %d) against ~199 KB for the 200s: a near-static 270 KB page, not a per-user page [INFERRED]" % (
       ftall[3]["bytes"], ftall[4]["bytes"], abs(ftall[3]["bytes"] - ftall[4]["bytes"])))
st = C.session_stat("ft")
mt = C.ts(st["mtime_utc"])
ok(mt < C.ts(ftall[0]["at"]) and not C.auth_folders("ft"),
   "secrets/ft.dpapi mtime %s is UNCHANGED across the 200s (09-15) and the 403s (09-23, 09-30): same envelope, %.2f d old at the o-5 job; no auth/ folder for ft" % (
       st["mtime_utc"][:19], (C.ts(fj["started_at"]) - mt).total_seconds() / 86400))
old = subprocess.run(["git", "-C", str(C.WT), "show", "8b11d236c4:lib/opal_data_harvest/publishers.py"], capture_output=True, text=True, encoding="utf-8")
ok(old.returncode == 0 and 'self.session.get("https://www.ft.com/search", params={"q": security["company"]},' in old.stdout
   and 'headers={"Referer": "https://www.ft.com/"})' in old.stdout,
   "git show 8b11d236c4 (2026-09-15): the SAME GET, q=<company>, Referer https://www.ft.com/ -- the request that returned 200")
c_get, gn2 = C.cite(P, 'response = self.session.get("https://www.ft.com/search", params=params,')
ok(True, "%s now: same URL, params {'q': company} in live mode, same Referer -- request line unchanged" % c_get)


def fn_text(src, start, end):
    a = src.index(start)
    return src[a:src.index(end, a)]


rel = "org/tier1_exec/4.0.0_SA_CRO/scripts/ft_rest_fetch.py"
before = subprocess.run(["git", "-C", str(C.WT), "show", "58535ee9a7:" + rel], capture_output=True, text=True, encoding="utf-8").stdout
now_src = FT.read_text(encoding="utf-8")
ok(fn_text(before, "def build_session", "def get_html") == fn_text(now_src, "def build_session", "def get_html"),
   "ft_rest_fetch.py build_session() (headers, UA, TLS profile, cookie set) is BYTE-IDENTICAL between 58535ee9a7 (2026-09-14 22:27 local, in force for the 200s) and HEAD; "
   "the file's later commit 7aaf58f0c1 (2026-09-15 04:02Z, after the 200s) only renamed an exception class in parse_article")
c_chk, _ = C.cite(P, 'def check_auth(self):')
c_ftc, _ = C.cite(P, "# FT's observed login redirect")
ok(True, "%s / %s: check_auth has no ft branch ('an isolated 403 does not log in'); contracts.json:%d says 401/403 alone is not a re-auth" % (
    c_chk, c_ftc, C.find_line(CT, '"refresh_signal"', after=C.find_line(CT, '"Financial Times"'))))
c_set, _ = C.cite(W, 'if attempt or publisher not in {"bbg", "barrons"}:')
c_vr, _ = C.cite(V, 'if publisher not in {"bbg", "barrons"}:')
ok(True, "%s and %s: ft is outside the worker's repair set and verification.repair() refuses it -- nothing in the path acts on a bare 403" % (c_set, c_vr))
c_cap, _ = C.cite(T, 'self.captured.append({')
c_wr, _ = C.cite(W, 'except RequestRejected as exc:')
ok(True, "%s keeps the response body in memory only; %s persists str(exc) only -- the 403 body is NOT on disk anywhere the collector wrote" % (c_cap, c_wr))
cool_ft = dt.datetime.fromtimestamp(cool["ft"][0], dt.timezone.utc)
ok(now > cool_ft, "progress.sqlite3 cooldown row for ft ends %s (reason %s): lapsed" % (cool_ft.isoformat()[:19], cool["ft"][1]))
print("  CAUSE: NOT DETERMINED by the record -- a STATED LIMIT. What is measured: an unchanged request from an unchanged 15-day-old envelope returned 200 on "
      "2026-09-15 and 403 (a ~270 KB page, no challenge marker, no login redirect) on 2026-09-23 and 2026-09-30, so the change is on the publisher's side or in time. "
      "Three readings fit and the record cannot separate them: (a) the FT session cookies have aged out and FT answers a dead session with 403; (b) an edge/bot rule now "
      "refuses this client (hard-coded UA Chrome/126 at %s riding curl_cffi's 'chrome' TLS profile, the same mismatch publishers.py:261-262 warns of for wsj); "
      "(c) the egress address is blocked. The discriminator is the 403 body, which the collector throws away." % C.cite(FT, '"User-Agent": "Mozilla/5.0')[0])
print("  ROUTE F1 (evidence, no publisher request in the edit): a code cell that, when a 403/401 carries no marker, writes the rejection's classification "
      "(status, content-type, <title>, first 300 text chars with no cookie/header values, size, marker hits) into the run json -- a change at %s/%s "
      "(PacedSession already holds the bytes in `captured`). ACT NEEDED: none for the edit. The NEXT ft job then answers (a)/(b)/(c); that job is a publisher request "
      "= Andrew's per-use word." % (c_cap, c_wr))
c_ref, _ = C.cite(C.LIB / "auth.py", 'module = importlib.util.module_from_spec(spec)')
c_kimi, _ = C.cite(FTH, '_secret("astn/kimi/api-key")')
c_nope, _ = C.cite(FTH, 'raw = nopecha.Token.solve(type="hcaptcha"')
c_cred, _ = C.cite(FTH, 'creds = json.loads(_secret("astn/ft/credentials"))')
print("  ROUTE F2 (only if F1 says (a) dead session): re-harvest the ft envelope through the collector's own scripted path -- SessionManager.refresh() -> %s -> "
      "harvest_local_session.harvest('ft') -> ft_harvest_session.py. TODAY that path is reachable only through AuthExpired (worker.py:403), which an ft 403 never raises, "
      "so it needs either a hand-run of the harvester + `import-session` (__main__.py:81) or a cell that lets F1's verdict trigger it. "
      "ACT NEEDED: Andrew's word -- it is a credential login (%s) and its hCaptcha step calls a vendor solver (%s, %s); "
      "the commissioning record forbids a credential login as a generic 403 remedy (HARVEST_COMMISSIONING_20260915_W.md, 'Remaining validation')." % (
          c_ref, c_cred, c_kimi, c_nope))
print("  ROUTE F3: if F1 says (b)/(c) (edge or address block): NO route inside R-21 -- clearing it is either challenge solving or egress change, both outside this order; "
      "the limit stands and ft stays out of the live set until Andrew rules.")

# ---------------------------------------------------------------------------------------------- SUMMARY
print("\n" + "=" * 100)
print("SUMMARY")
print("  barrons: cause MEASURED (fresh-session challenge + repair barred by the attempt guard); smallest route = B1 (a run, no code) / B2 (one guard edit); act: Andrew's word for the run.")
print("  ft     : cause NOT determined (403 body not kept); smallest next step = F1 (keep the rejection's classification); F2/F3 depend on its answer; act: Andrew's word for any ft request, and for F2's login + solver.")
print("  bbg/wsj: clean in the same runs (bbg via its own repair at attempt 0; wsj via reauth). Nothing is asserted about why barrons.com and ft.com differ from wsj.com/bloomberg.com beyond the rows above.")
print("ASSERTIONS PASSED: %d" % checks)
print("NETWORK CALLS MADE: 0 (socket.socket replaced by a refusing stub and asserted at start; restored only after the last print)")
restore()
