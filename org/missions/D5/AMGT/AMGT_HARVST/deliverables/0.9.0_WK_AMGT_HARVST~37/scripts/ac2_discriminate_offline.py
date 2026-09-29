#!/usr/bin/env python3
"""HVST-w-5 AC2 -- OFFLINE discrimination of the bbg search/query refusal (row AMGT_HARVST-Z-S32).

No network: HARVEST_REFUSE_NETWORK=1 is set here, and socket connects are additionally made to raise.
Reads (never writes) the MAIN tree's .runtime/opal-data-harvest (events.jsonl, verification/*, the stored
bbg contract probes, the DPAPI session vault -- only captured_at, cookie NAMES/expiries and counts are printed,
never a value) and this cell's own ac1_capture.json. Every statement in the hypothesis table is computed
from those inputs or is a labelled caveat.
"""
import collections
import datetime
import glob
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

os.environ["HARVEST_REFUSE_NETWORK"] = "1"


def _refuse(*a, **k):
    raise RuntimeError("network refused: AC2 is offline")


socket.socket.connect = _refuse
socket.create_connection = _refuse

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
sys.path.insert(0, str(REPO))
common = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                        check=True).stdout.strip()
MAIN = (Path(common) if Path(common).is_absolute() else (REPO / common)).resolve().parent
RT = MAIN / ".runtime" / "opal-data-harvest"
assert RT.is_dir(), RT
from lib.opal_data_harvest.storage import dpapi  # noqa: E402  (local DPAPI decrypt of stored evidence)


class _Tee:
    def __init__(self, a, path):
        self.a, self.f = a, open(path, "w", encoding="utf-8")

    def write(self, x):
        self.a.write(x)
        self.f.write(x)

    def flush(self):
        self.a.flush()
        self.f.flush()


sys.stdout = _Tee(sys.stdout, DELIV / "ac2_output.txt")


def T(s):
    return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00")).astimezone(datetime.timezone.utc)


def load_events():
    out = []
    for line in (RT / "events.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def main():
    print(f"AC2 offline. HARVEST_REFUSE_NETWORK={os.environ['HARVEST_REFUSE_NETWORK']}; main runtime root={RT}")
    cap = json.loads((DELIV / "ac1_capture.json").read_text(encoding="utf-8"))
    live_u, live_s = cap["calls"][0]["classification"], cap["calls"][1]["classification"]
    live_at = T(cap["calls"][1]["at"])

    # ---- 1. stored search/query + article evidence, by day and status --------------------------------
    ev = load_events()
    bbg = [e for e in ev if e.get("publisher") == "bbg"]
    http = [e for e in bbg if e.get("event") == "http"]
    sq = [e for e in http if e["path"] == "/nemo-next/api/search/query"]
    pending = []
    for e in bbg:                                   # security_key = the next job_finished of the same run
        if e.get("event") == "http" and e["path"] == "/nemo-next/api/search/query":
            pending.append(e)
        if e.get("event") == "job_finished":
            for p in pending:
                p["key"] = e.get("security_key")
            pending = []
    print(f"\n[1] STORED bbg events: {len(bbg)} of {len(ev)} events.jsonl rows; http={len(http)}; search/query={len(sq)}")
    by = collections.Counter((e["at"][:10], e["status"]) for e in sq)
    for k in sorted(by):
        print(f"    search/query {k[0]} HTTP {k[1]} x{by[k]}")
    s200 = [e for e in sq if e["status"] == 200]
    s403 = [e for e in sq if e["status"] == 403]
    print(f"    search/query totals: 200={len(s200)} 403={len(s403)} of {len(sq)}; 403 body bytes distinct={sorted({e['bytes'] for e in s403})}")
    last200 = max(T(e["at"]) for e in s200)
    first200 = min(T(e["at"]) for e in s200)
    since = [e for e in sq if T(e["at"]) > last200]
    print(f"    every 200 falls in {first200.isoformat()} .. {last200.isoformat()} ({(last200 - first200).total_seconds() / 60:.0f} min); "
          f"since the last 200: {len(since)} search/query calls, {sum(e['status'] == 200 for e in since)} x 200 (+ the live AC1 call: HTTP {live_s['status']})")
    other = collections.Counter((e["path"].split("/story/id/")[0] + ("/story/id" if "/story/id/" in e["path"] else ""), e["status"])
                                for e in http if e["path"] != "/nemo-next/api/search/query")
    for k in sorted(other):
        print(f"    other path {k[0]} HTTP {k[1]} x{other[k]}")
    art403 = [e for e in http if "/article/api/story/id/" in e["path"] and e["status"] != 200]
    art_total = sum(1 for e in http if "/article/api/story/id/" in e["path"])
    user_total = sum(1 for e in http if e["path"] == "/user-info")
    user200 = sum(1 for e in http if e["path"] == "/user-info" and e["status"] == 200)
    print(f"    article API (www.bloomberg.com): {art_total} calls, non-200={len(art403)} "
          f"{[(e['at'][:19], e['status'], e['bytes']) for e in art403]}")
    print(f"    /user-info (login.bloomberg.com): {user200} of {user_total} HTTP 200 stored; live AC1 call HTTP {live_u['status']} "
          f"-> {user200 + (live_u['status'] == 200)} of {user_total + 1}")

    # ---- 2. per-query table ---------------------------------------------------------------------------
    print("\n[2] search/query per security key (key = job_finished that followed the call)")
    kc = collections.defaultdict(list)
    for e in sq:
        kc[e.get("key")].append((e["at"][5:16], e["status"]))
    for k, v in kc.items():
        print(f"    {k}: {v}")
    post = [e for e in sq if T(e["at"]) > last200]
    post_keys = {e.get("key") for e in post}
    both_arms = [k for k, v in kc.items() if {s for _, s in v} == {200, 403}]
    print(f"    post-09-15: {len(post)} calls over {len(post_keys)} DISTINCT securities, all 403={all(e['status'] == 403 for e in post)}; "
          f"securities seen with BOTH 200 and 403: {both_arms}; live query 'Lenovo' -> {live_s['status']}")

    # ---- 3. gaps (burst hypothesis) ---------------------------------------------------------------------
    ts = sorted(T(e["at"]) for e in sq)
    gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
    post_ts = [t for t in ts if t > last200]
    pg = [(b - a).total_seconds() for a, b in zip(post_ts, post_ts[1:])]
    print(f"\n[3] gaps between consecutive search/query calls: post-09-15 min={min(pg) / 60:.1f} min over {len(pg)} gaps; "
          f"first post-09-15 gap {(post_ts[0] - last200).total_seconds() / 86400:.1f} d; live call was "
          f"{(live_at - post_ts[-1]).total_seconds() / 3600:.1f} h after the last stored 403")
    within_regime = [g for g in gaps if g < 3600]
    print(f"    09-15 window: {len(within_regime)} gaps < 1h among 200/403 interleaved calls")

    # ---- 4. session age at each call ------------------------------------------------------------------------
    print("\n[4] session age at call (captured_at read from the stored DPAPI envelopes; nothing else printed)")
    sa = json.loads(dpapi((RT / "bbg-search-contract" / "session-after.dpapi").read_bytes(), decrypt=True))
    cap_0915 = T(sa["bundle"]["captured_at"])
    vault = json.loads(dpapi((RT / "secrets" / "bbg.dpapi").read_bytes(), decrypt=True))
    cap_vault = T(vault["bundle"]["captured_at"])
    print(f"    09-15 session (bbg-search-contract/session-after.dpapi) captured_at={cap_0915.isoformat()}, cookies={len(sa['bundle']['all_cookies'])}")
    print(f"    live vault (secrets/bbg.dpapi) captured_at={cap_vault.isoformat()}, cookies={len(vault['bundle']['all_cookies'])}, "
          f"http_updated_at={vault.get('http_updated_at')}")
    print(f"    parked session used by AC1: captured_at={cap['session_captured_at']} age at call {cap['session_age_hours']} h, cookies={cap['cookie_count']}")
    age_rows = []
    for e in sq:
        t = T(e["at"])
        base = cap_0915 if t.date() == datetime.date(2026, 9, 15) else (cap_vault if t >= cap_vault else None)
        age = None if base is None else (t - base).total_seconds() / 3600
        age_rows.append((e["at"][5:19], e["status"], None if age is None else round(age, 2)))
    for r in age_rows:
        print(f"    {r[0]} HTTP {r[1]} session_age_h={r[2]}")
    a200 = [r[2] for r in age_rows if r[1] == 200]
    a403_known = [r[2] for r in age_rows if r[1] == 403 and r[2] is not None and r[2] >= 0]
    fresh403 = [r for r in age_rows if r[1] == 403 and r[2] is not None and 0 <= r[2] < max(a200)]
    print(f"    200 session ages: {min(a200):.2f}..{max(a200):.2f} h (n={len(a200)}); 403s on a session YOUNGER than the oldest 200: "
          f"{len(fresh403)} of {len(a403_known)} with a known age -> {fresh403}")
    print(f"    live AC1: 403 on a session {cap['session_age_hours']} h old (parked); its _px3 expiry:")
    for c in cap["px_cookies"]:
        if c["name"] in ("_px3", "_px2"):
            ex = c["expires"]
            print(f"      {c['name']} {c['domain']} expires "
                  f"{datetime.datetime.fromtimestamp(ex, datetime.timezone.utc).isoformat() if ex and ex > 0 else ex} "
                  f"(= {(ex - T(cap['session_captured_at']).timestamp()) / 60:.1f} min after capture)")
    v_px3 = [c for c in vault["bundle"]["all_cookies"] if c["name"] == "_px3"]
    print(f"    live vault _px3 present={bool(v_px3)} expires={[c.get('expires') for c in v_px3]} (name/expiry only)")

    # ---- 5. stored 403 bodies and the fingerprint / client class -------------------------------------------------
    print("\n[5] stored 403 evidence")
    print(f"    producer 403 bodies: events.jsonl carries BYTE COUNTS only; {sum(e['bytes'] == 535 for e in s403)} of {len(s403)} search/query "
          f"403s + {sum(e['bytes'] == 535 for e in art403)} of {len(art403)} article 403s are exactly 535 B; live AC1 403 = {live_s['bytes']} B "
          f"-> {sum(e['bytes'] == 535 for e in s403) + sum(e['bytes'] == 535 for e in art403) + (live_s['bytes'] == 535)} of "
          f"{len(s403) + len(art403) + 1} non-200 www.bloomberg.com responses are 535 B. No stored producer body exists, so byte-identity of "
          f"structure with the live body is NOT MEASURABLE beyond length.")
    live_body = json.loads(live_s["body_text_retained"])
    print(f"    live 403 body: PX JSON keys={sorted(live_body)} appId={live_body['appId']} hostUrl={live_body['hostUrl']} "
          f"markers={live_s['markers_present']} content-type={live_s['content_type']} server={live_s['headers'].get('server')}")
    shas = {}
    for f in sorted(list(RT.glob("bbg-*.dpapi")) + list((RT / "bbg-search-contract").glob("response-*.dpapi"))):
        b = dpapi(f.read_bytes(), decrypt=True)
        t = b.decode("utf-8", "replace")
        if "Are you a robot" in t:
            shas[f.name] = (len(b), hashlib.sha256(b).hexdigest()[:12], re.findall(r"_pxAppId = '([^']+)'", t)[:1])
    print(f"    stored browser-context 403 HTML pages: {len(shas)} files, distinct sha256={len({v[1] for v in shas.values()})}, "
          f"bytes={sorted({v[0] for v in shas.values()})}, PX appId={sorted({a for v in shas.values() for a in v[2]})}")
    same_app = any(live_body["appId"] in v[2] for v in shas.values())
    print(f"    live PX appId == stored 09-15 page appId: {same_app}")
    rq = json.loads((RT / "bbg-search-contract" / "requests.json").read_text(encoding="utf-8"))
    print("    real headed Chrome probe (bbg-search-contract/requests.json, files 2026-09-14 23:30 local = 09-15 04:30Z):")
    for r in rq:
        print(f"      {r['url'].split('?')[0][8:]} HTTP {r['status']} request header names={len(r['header_names'])} "
              f"(sec-ch-ua={'sec-ch-ua' in r['header_names']}, x-enable-sst={'x-enable-sst' in r['header_names']})")
    browser_403 = [r for r in rq if "/search/query" in r["url"] and r["status"] == 403]
    curl_around = [(e["at"][11:19], e["status"]) for e in sq if e["at"][:10] == "2026-09-15" and "04:00" <= e["at"][11:16] <= "04:47"]
    print(f"    curl_cffi search/query calls on either side of that browser 403 (04:00-04:47Z): {curl_around}")

    # ---- 6. verification / trust-token events --------------------------------------------------------------------
    vdirs = sorted(d for d in glob.glob(str(RT / "verification" / "*-bbg-*")))
    proofs = {}
    for d in vdirs:
        p = Path(d) / "verification-proof.json"
        proofs[Path(d).name] = json.loads(p.read_text(encoding="utf-8")).get("independent_pass") if p.exists() else "no-proof-file"
    succ = [e for e in bbg if e.get("event") == "verification_succeeded"]
    reauth = [e for e in bbg if e.get("event") == "reauth_started"]
    print(f"\n[6] press-and-hold history: {len(vdirs)} verification dirs; verification_succeeded events={len(succ)} "
          f"{[e['at'][:19] for e in succ]}; reauth_started(bbg)={len(reauth)} {[e['at'][:19] for e in reauth]}")
    print(f"    independent_pass values (dirs with a proof file): {collections.Counter(str(v) for v in proofs.values())}")
    post_v = [n for n in proofs if n[:8] > "20260915"]
    print(f"    holds since 09-15: {len(post_v)}; passes among them: {sum(proofs[n] is True for n in post_v)}; "
          f"fresh browser-captured vault session at {cap_vault.isoformat()} then first 403 "
          f"{[r[0] for r in age_rows if r[2] is not None and r[2] >= 0 and r[0] > cap_vault.isoformat()[5:19]][:1]}")

    # ---- 7. the hypothesis table --------------------------------------------------------------------------------------
    print("\n[7] HYPOTHESES")
    H = []

    def row(name, verdict, why):
        H.append((name, verdict))
        print(f"  * {name}: {verdict}\n      {why}")

    row("H1 session age / staleness", "RULED OUT (as the discriminator)",
        f"403s on sessions YOUNGER than the oldest 200: {len(fresh403)} of {len(a403_known)} known-age 403s "
        f"(e.g. {fresh403[:2]}); the 200s and 403s of 09-15 interleave on ONE session (403 at 5 min age between 200s); "
        f"live 403 on a {cap['session_age_hours']} h parked session too. A fresh browser capture (vault {cap_vault.isoformat()}) "
        f"was refused 19 min later. Age does not separate the outcomes in either direction.")
    row("H2 search/query-specific wall (vs the www.bloomberg.com host)", "RULED OUT for 09-15; NOT DISCRIMINATED for now",
        f"the SAME 535-byte refusal hit the article API on www.bloomberg.com on 09-15 ({len(art403)} of {art_total} article calls, "
        f"{[e['at'][11:19] for e in art403]}), so the wall is not confined to search/query. After 09-15 NO www.bloomberg.com path other than "
        f"search/query has been called (producer jobs stop at the search refusal), so host-wide vs search-only is unobserved NOW. "
        f"login.bloomberg.com /user-info answered 200 on {user200 + 1} of {user_total + 1} incl. the live call made seconds before the live 403 "
        f"on the same session -- a different host is not walled, which is host- or PX-scope-consistent.")
    row("H3 query-specific (a particular security or query text)", "RULED OUT",
        f"since 09-15: {len(post)} calls over {len(post_keys)} distinct securities, 0 of {len(post)} returned 200, plus live 'Lenovo' -> "
        f"{live_s['status']}; and securities seen with both outcomes on 09-15: {both_arms}.")
    row("H4 client header / TLS-fingerprint class (curl_cffi chrome impersonation vs a real browser)", "RULED OUT (n=1 browser sample)",
        f"a real headed Chrome with the full browser header set ({len(browser_403[0]['header_names']) if browser_403 else 'n/a'} request header names incl. "
        f"sec-ch-ua, x-enable-sst) was also refused on search/query (and /search/lookup) at ~04:30Z 09-15 while curl_cffi returned "
        f"200 at 04:06Z and 04:41-04:47Z: {curl_around}. The identical transport succeeds and fails on the same session, and a real browser fails. "
        f"CAVEAT: one browser observation, on the 09-15 session.")
    recov = []
    for i, e in enumerate(sq[:-1]):
        if e["status"] == 403:
            nxt = next((x for x in sq[i + 1:] if x["status"] == 200), None)
            if nxt is not None:
                recov.append(f"{(T(nxt['at']) - T(e['at'])).total_seconds() / 60:.1f} min")
    row("H5 burst / rate sensitivity (a retry after a window clears it)", "RULED OUT for the current regime",
        f"post-09-15 calls: min gap {min(pg) / 60:.1f} min (the 900 s cooldown), first gap {(post_ts[0] - last200).total_seconds() / 86400:.1f} d, "
        f"live call {(live_at - post_ts[-1]).total_seconds() / 3600:.1f} h after the last -- {len(post)} + 1 of {len(post) + 1} still 403. "
        f"On 09-15 the 403 -> next-200 recoveries took {recov} -- all inside the window in which 200s still existed.")
    row("H6 vendor-side regime change after 09-15 ~04:47Z (PX policy, source-IP or account risk score)", "SUPPORTED (survives every discriminating observation)",
        f"{len(s200)} of {len(s200)} 200s fall in one {(last200 - first200).total_seconds() / 60:.0f}-min window and "
        f"0 of {len(since) + 1} calls since (incl. live) are 200, across {len(post_keys) + 1} securities and 2 sessions (vault x{len(post)}, parked x1); "
        f"the only real-browser refusal on file is from 09-15, inside the 200 window. NOT DISCRIMINATED among policy change vs source-IP reputation vs account risk: all three predict this data.")
    row("H7 a PX trust token from a fresh sign-in or a passed hold is what unlocks 200", "PARTLY: 'fresh sign-in is sufficient' RULED OUT; 'a passed hold is necessary' NOT DISCRIMINATED",
        f"09-15: reauth {[e['at'][11:19] for e in reauth]} -> 200 within 13 min; verification_succeeded {[e['at'][11:19] for e in succ]} -> 200 the same second. "
        f"But the vault session was browser-captured {cap_vault.isoformat()} and its first search/query 19 min later was 403, and "
        f"{len(post_v)} holds since 09-15 have {sum(proofs[n] is True for n in post_v)} passes. The state 'hold passed, still 403' has never been observed after 09-15, "
        f"so necessity cannot be tested from stored evidence. The pixel trace does not discriminate (order section 1).")

    # ---- 8. verdict ------------------------------------------------------------------------------------------------------
    print("\n[8] VERDICT")
    print("  What the run discriminated: the refusal is NOT explained by session age (H1), query text (H3), header/TLS client class (H4) or "
          "burst rate (H5); the 403 body is a PerimeterX block JSON (appId " + live_body["appId"] + ", same tenant as the 09-15 pages) served at the "
          "Fastly/Varnish edge of www.bloomberg.com; it is not search-specific on 09-15 (H2, article API refused with the same 535 B). "
          "The surviving explanation (H6/H7) is a vendor-side PX risk decision made on something the stored evidence cannot vary "
          "(source IP, account, or a trust token only a passed hold mints).")
    print("  VERDICT: a bbg capture is NOT PLANNABLE from this evidence -- the run could not separate H6 (regime/IP/account) from H7 (trust token). "
          "SINGLE FURTHER OBSERVATION that would discriminate host-wide vs search-only (H2): ONE GET of a www.bloomberg.com article-API route "
          "(/article/api/story/id/<a story id already held from 09-15>) on the same session -- 200 means the wall is search-scoped and a search-free "
          "capture path (known ids) is plannable; 403 means host-wide and bbg is closed until a passed hold or a different source is available. "
          "That call needs its own vendor word (this order's word was ONE /user-info + ONE search/query call).")
    print(f"  hypothesis verdicts: {[(h[0].split(' ')[0], h[1].split(' ')[0]) for h in H]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
