"""Tests for clamp_precheck.py. Every outside read is replaced by a fake: no AWS, no network, no git."""
import base64
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clamp_precheck as cp  # noqa: E402

TICKET = "opal-ticket-api"
IRPT_A = "irpt-narrative"
IRPT_B = "irpt-served"
COMMIT = "da431554186bd74759f3d85bc4423f42a6c4a8f9"
SRC_DIR = "infra/aws/lambda/ticket_center"

HANDLER_TEMPLATE = '''
def {name}(event, *rest):
    refused = {call}(event, "x")
    return refused
'''

ROUTE_LINE = "    if event.get('route') == '{name}':\n        return {name}(event)\n"
ROUTER_TEMPLATE = "def lambda_handler(event, context):\n{routes}    return _resp(404, {{}})\n"


def ticket_source(drop_helper=None, uncall=None):
    """A small stand-in for the ticket handler: three helpers, two wrappers, seven handlers."""
    parts = ['def _profile_scope(actor):\n    return None, None\n',
             'def _resolve_scope(actor, pc):\n    return _profile_scope(actor)[1]\n',
             'def _in_profile_scope(actor, firm):\n    return True\n',
             'def _firm_allowed(actor, firm):\n    return True\n',
             'def _create_firm_allowed(pc, actor, firm):\n    return _firm_allowed(actor, firm) and _in_profile_scope(actor, firm)\n']
    parts = [p for p in parts if not (drop_helper and p.startswith("def %s(" % drop_helper))]
    for h in cp.HANDLERS:
        call = "_unrelated" if h == uncall else ("_create_firm_allowed" if h == "create_ticket" else "_resolve_scope")
        parts.append(HANDLER_TEMPLATE.format(name=h, call=call))
    parts.append(ROUTER_TEMPLATE.format(routes="".join(ROUTE_LINE.format(name=h) for h in cp.HANDLERS)))  # TO-R5-pc2: a router
    return "\n".join(parts).encode("utf-8")


def zip_of(members):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for k, v in members.items():
            z.writestr(k, v)
    return buf.getvalue()


def b64(b):
    return base64.b64encode(hashlib.sha256(b).digest()).decode("ascii")


def hexsha(b):
    return hashlib.sha256(b).hexdigest()


def entry_for(live_sha="LIVE-SHA"):
    return {"source_dir": SRC_DIR, "files": ["lambda_function.py"], "artifact_sha256": live_sha,
            "last_deployed_commit": COMMIT}


def decide(deployed, recorded, map_sha="LIVE-SHA", live_sha="LIVE-SHA", member="lambda_function.py"):
    cfg = {"CodeSha256": live_sha, "LastModified": "2026-10-11T00:00:00.000+0000"}
    calls = []

    def git_reader(commit, path):
        calls.append((commit, path))
        if isinstance(recorded, Exception):
            raise recorded
        return recorded

    out = cp.ticket_decision(cfg, zip_of({member: deployed}), entry_for(map_sha), git_reader)
    return out, calls


# ---- AC1: the ticket host ---------------------------------------------------------------------------------------------------

def test_map_live_and_commit_agree_and_clamp_present_is_clamped():
    src = ticket_source()
    (verdict, detail, h), calls = decide(src, src)
    assert verdict == "CLAMPED", detail
    assert h == hexsha(src)
    assert calls == [(COMMIT, SRC_DIR + "/lambda_function.py")]


def test_live_build_not_the_maps_is_map_stale_and_not_clamped():
    src = ticket_source()
    (verdict, _d, _h), calls = decide(src, src, map_sha="THE-MAPS", live_sha="SOMETHING-ELSE")
    assert verdict == "MAP-STALE"
    assert verdict != "CLAMPED"


def test_member_not_the_recorded_commits_file_is_refused():
    deployed = ticket_source()
    recorded = ticket_source(uncall="metrics")  # a different file at the recorded commit
    (verdict, _d, _h), _ = decide(deployed, recorded)
    assert verdict == "NOT-THE-RECORDED-FILE"


def test_a_clamp_helper_removed_is_not_clamped():
    for helper in cp.CLAMP_HELPERS:
        src = ticket_source(drop_helper=helper)
        (verdict, detail, _h), _ = decide(src, src)
        assert verdict == "CLAMP-ABSENT", helper
        assert helper in detail


def test_a_route_handler_that_stops_calling_the_clamp_is_not_clamped():
    for handler in cp.HANDLERS:
        src = ticket_source(uncall=handler)
        (verdict, detail, _h), _ = decide(src, src)
        assert verdict == "CLAMP-ABSENT", handler
        assert handler in detail


def test_a_handler_reaching_the_clamp_through_a_wrapper_is_clamped_and_a_dead_wrapper_is_not():
    # create_ticket reaches the clamp only through _create_firm_allowed in this fixture variant
    src = ticket_source().decode("utf-8")
    assert 'refused = _create_firm_allowed(event, "x")' in src
    assert cp.clamp_absent(src) is None
    # a wrapper that no longer calls a helper is not a path to the clamp
    dead = src.replace("return _firm_allowed(actor, firm) and _in_profile_scope(actor, firm)", "return _firm_allowed(actor, firm)")
    why = cp.clamp_absent(dead)
    assert why is not None and "create_ticket" in why
    # a firm check alone is not the clamp: _firm_allowed calls none of the helpers
    only_firm = src.replace('refused = _create_firm_allowed(event', 'refused = _firm_allowed(event')
    assert "create_ticket" in cp.clamp_absent(only_firm)


def test_unreadable_pieces_are_unreadable_and_never_clamped():
    src = ticket_source()
    (v1, _d, _h), _ = decide(src, RuntimeError("no such commit"))
    assert v1 == "UNREADABLE"
    cfg = {"CodeSha256": "LIVE-SHA"}
    assert cp.ticket_decision(cfg, b"not a zip", entry_for(), lambda c, p: src)[0] == "UNREADABLE"
    assert cp.ticket_decision(cfg, zip_of({"other.py": b"x"}), entry_for(), lambda c, p: src)[0] == "UNREADABLE"
    assert cp.ticket_decision(cfg, zip_of({"lambda_function.py": src}), {"source_dir": SRC_DIR}, lambda c, p: src)[0] == "UNREADABLE"
    assert cp.ticket_decision(cfg, zip_of({"lambda_function.py": src}), None, lambda c, p: src)[0] == "UNREADABLE"
    assert cp.clamp_absent("def broken(:") is not None


def test_the_code_at_head_has_the_clamp_by_this_rule():
    root = Path(__file__).resolve().parents[8]
    head_file = root / SRC_DIR / "lambda_function.py"
    if not head_file.exists():
        pytest.skip("handler file not present in this checkout")
    assert cp.clamp_absent(head_file.read_text(encoding="utf-8")) is None


def test_the_source_carries_no_typed_list_of_ticket_builds():
    text = (Path(__file__).resolve().parent / "clamp_precheck.py").read_text(encoding="utf-8")
    assert "TICKET_OK" not in text
    assert all(ord(c) < 128 for c in text)


def test_import_makes_no_outside_call():
    # a fresh import with every outside entry point poisoned must still succeed
    import importlib
    import subprocess
    import urllib.request
    saved = (subprocess.run, urllib.request.urlopen)

    def boom(*a, **k):
        raise AssertionError("outside call at import")

    subprocess.run, urllib.request.urlopen = boom, boom
    try:
        importlib.reload(cp)
    finally:
        subprocess.run, urllib.request.urlopen = saved
        importlib.reload(cp)


# ---- AC2: the IRPT hosts, the totals line, the exit code ----------------------------------------------------------------------

RELEASE_HASH = sorted(cp.SERVED_RELEASES)[0]


def fake_world(tmp_path, monkeypatch, irpt_payload, ticket_ok=True, break_irpt_b=False):
    """Census with two IRPT hosts (3+2 routes) and the ticket host (2 routes); fakes for the three readers."""
    rows = []
    for fn, n in ((IRPT_A, 3), (IRPT_B, 2), (TICKET, 2)):
        for i in range(n):
            rows.append({"route": "/r/%s/%d" % (fn, i), "method": "GET", "function": fn,
                         "per_token": {"T": {"verdict": "MORE_THAN_ONE"}}})
    rows.append({"route": "/skipped", "method": "GET", "function": IRPT_A, "per_token": {"T": {"verdict": "ONE_FIRM"}}})
    census = tmp_path / "census.json"
    census.write_text(json.dumps({"rows": rows}), encoding="utf-8")
    smap = tmp_path / "map.json"
    smap.write_text(json.dumps({"functions": {TICKET: entry_for("LIVE-SHA")}}), encoding="utf-8")
    src = ticket_source() if ticket_ok else ticket_source(uncall="metrics")  # recorded file == deployed file

    def fake_function(name):
        if name == IRPT_B and break_irpt_b:
            raise RuntimeError("function unreadable")
        if name == TICKET:
            return {"CodeSha256": "LIVE-SHA", "LastModified": "2026-10-11T01:02:03.000+0000"}, zip_of(
                {"lambda_function.py": src})
        return {"CodeSha256": "X", "LastModified": "2026-10-11T01:02:03.000+0000"}, zip_of({"served.py": irpt_payload})

    monkeypatch.setattr(cp, "read_function", fake_function)
    monkeypatch.setattr(cp, "read_git_file", lambda commit, path: src)
    monkeypatch.setattr(cp, "read_source_map", lambda p: json.loads(Path(p).read_text(encoding="utf-8")))
    return census, smap


def release_payload():
    # find bytes hashing to a release member is impossible; patch the release set to the fake payload instead
    return b"served release build bytes"


def test_irpt_host_on_a_release_build_is_clamped(tmp_path, monkeypatch, capsys):
    payload = release_payload()
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(payload): "FAKE-RELEASE"})
    census, smap = fake_world(tmp_path, monkeypatch, payload)
    out = tmp_path / "t.json"
    rc = cp.main(["--out", str(out), "--census", str(census), "--source-map", str(smap)])
    text = capsys.readouterr().out
    assert rc == 0, text
    assert "READ27 7/7" in text
    lines = [ln for ln in text.splitlines() if ln.startswith(IRPT_A)]
    assert len(lines) == 1 and lines[0].endswith("CLAMPED")
    table = json.loads(out.read_text(encoding="utf-8"))
    assert {t["function"]: t["release"] for t in table}[IRPT_A] == "FAKE-RELEASE"


def test_irpt_host_off_the_release_set_is_not_released(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(b"some other build"): "OTHER"})
    census, smap = fake_world(tmp_path, monkeypatch, release_payload())
    rc = cp.main(["--out", str(tmp_path / "t.json"), "--census", str(census), "--source-map", str(smap)])
    text = capsys.readouterr().out
    assert rc == 1
    assert IRPT_A in text and "NOT-RELEASED" in text
    assert "READ27 2/7" in text  # only the ticket host (2 routes) is clamped


def test_unreadable_host_is_named_and_the_total_is_not_full(tmp_path, monkeypatch, capsys):
    payload = release_payload()
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(payload): "FAKE-RELEASE"})
    census, smap = fake_world(tmp_path, monkeypatch, payload, break_irpt_b=True)
    out = tmp_path / "t.json"
    rc = cp.main(["--out", str(out), "--census", str(census), "--source-map", str(smap)])
    text = capsys.readouterr().out
    line = [ln for ln in text.splitlines() if ln.startswith(IRPT_B)][0]
    assert "UNREADABLE" in line
    assert "READ27 5/7" in text
    assert rc == 1
    assert [t["clamp_live"] for t in json.loads(out.read_text(encoding="utf-8")) if t["function"] == IRPT_B] == [False]


def test_exit_zero_only_when_every_route_is_clamped(tmp_path, monkeypatch, capsys):
    payload = release_payload()
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(payload): "FAKE-RELEASE"})
    census, smap = fake_world(tmp_path, monkeypatch, payload)
    assert cp.main(["--out", str(tmp_path / "a.json"), "--census", str(census), "--source-map", str(smap)]) == 0
    census, smap = fake_world(tmp_path, monkeypatch, payload, ticket_ok=False)
    assert cp.main(["--out", str(tmp_path / "b.json"), "--census", str(census), "--source-map", str(smap)]) == 1
    text = capsys.readouterr().out
    assert "CLAMP-ABSENT" in text and "READ27 5/7" in text


def test_a_missing_source_map_makes_the_ticket_host_unreadable(tmp_path, monkeypatch, capsys):
    payload = release_payload()
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(payload): "FAKE-RELEASE"})
    census, _smap = fake_world(tmp_path, monkeypatch, payload)

    def no_map(p):
        raise FileNotFoundError(p)

    monkeypatch.setattr(cp, "read_source_map", no_map)
    assert cp.main(["--out", str(tmp_path / "c.json"), "--census", str(census), "--source-map", "absent.json"]) == 1
    assert "UNREADABLE" in capsys.readouterr().out


def test_out_is_required(tmp_path):
    with pytest.raises(SystemExit) as e:
        cp.main([])
    assert e.value.code == 2


# ---- TO-R5-pc2: the second read -- every handler lambda_handler dispatches to, each with a class -----------------------------

REAL_HANDLER_FILE = Path(__file__).resolve().parents[8] / SRC_DIR / "lambda_function.py"


def _with_extra_handler(body):
    """ticket_source() plus one more dispatched handler, `extra_ticket`, whose body is `body`."""
    extra = "\ndef extra_ticket(event, *rest):\n%s\n" % body
    # a later lambda_handler wins, so this router dispatches to the seven and to the extra one
    router = ROUTER_TEMPLATE.format(routes="".join(ROUTE_LINE.format(name=h) for h in cp.HANDLERS + ("extra_ticket",)))
    return ticket_source() + extra.encode("utf-8") + router.encode("utf-8")


def _fake_ticket_world(tmp_path, monkeypatch, src):
    payload = release_payload()
    monkeypatch.setattr(cp, "SERVED_RELEASES", {hexsha(payload): "FAKE-RELEASE"})
    census, smap = fake_world(tmp_path, monkeypatch, payload)
    cfg = {"CodeSha256": "LIVE-SHA", "LastModified": "2026-10-11T01:02:03.000+0000"}
    real = cp.read_function
    monkeypatch.setattr(cp, "read_function",
                        lambda name: (cfg, zip_of({"lambda_function.py": src})) if name == TICKET else real(name))
    monkeypatch.setattr(cp, "read_git_file", lambda commit, path: src)
    return census, smap


def test_every_dispatched_ticket_handler_is_listed_with_a_class(tmp_path, monkeypatch, capsys):
    src = ("def _resolve_scope(a, pc):\n    return None\n"
           "def _helper_not_dispatched(x):\n    return x\n"
           "def alpha(event):\n    return _resolve_scope(event, 'x')\n"
           "def beta(event, tid):\n    return _resolve_scope(event, tid)\n"
           "def gamma(event):\n    return _resolve_scope(event, 'g')\n"
           "def delta(event):\n    return _resolve_scope(event, 'd')\n"
           "def lambda_handler(event, context):\n"
           "    if event.get('a'):\n        return alpha(event)\n"
           "    elif event.get('b'):\n        return beta(event, 'T')\n"
           "    if event.get('c'):\n        return gamma(event)\n"
           "    if event.get('d'):\n        return delta(event)\n"
           "    return _resp(404, {})\n").encode("utf-8")
    rows, why = cp.ticket_handler_rows(src)
    assert why == ""
    assert [r["handler"] for r in rows] == ["alpha", "beta", "gamma", "delta"]   # N dispatched -> N rows; _resp and the helper are not
    assert all(r["class"] == "PROFILE_SCOPE" for r in rows)
    # the same through main: the old lines first, then one line per handler and the totals line
    census, smap = _fake_ticket_world(tmp_path, monkeypatch, ticket_source())
    rc = cp.main(["--out", str(tmp_path / "t.json"), "--census", str(census), "--source-map", str(smap)])
    lines = capsys.readouterr().out.splitlines()
    k = lines.index("READ27 7/7")
    assert lines[k + 1:] == ["handler %s PROFILE_SCOPE" % h for h in cp.HANDLERS] + ["TICKET_HANDLERS 7/7"]
    assert rc == 0
    side = json.loads((tmp_path / "t_ticket_handlers.json").read_text(encoding="utf-8"))
    assert side["dispatched"] == 7 and side["classed"] == 7 and len(side["ticket_handlers"]) == 7
    # no lambda_handler (or one that dispatches nothing) is never an empty pass
    assert cp.ticket_handler_rows(b"def f(event):\n    return 1\n")[0] is None
    assert cp.ticket_handler_rows(b"def lambda_handler(event, context):\n    return _resp(404, {})\n")[0] is None
    assert cp.ticket_handler_rows(None)[0] is None


def test_a_handler_that_calls_a_clamp_helper_is_classed_profile_scope():
    src = ("def _in_profile_scope(a, f):\n    return True\n"
           "def _firm_allowed(a, f):\n    return True\n"
           "def via_helper(event):\n    return _in_profile_scope(event, 'x')\n"
           "def via_wrapper(event):\n    return _firm_allowed(event, 'x')\n"
           "def both(event):\n    return _in_profile_scope(event, 'x') and ('x' not in COMMENTARY_ALLOWED_FIRMS)\n"
           "def lambda_handler(event, context):\n"
           "    if event.get('a'):\n        return via_helper(event)\n"
           "    if event.get('b'):\n        return via_wrapper(event)\n"
           "    if event.get('c'):\n        return both(event)\n").encode("utf-8")
    rows, _why = cp.ticket_handler_rows(src)
    by = {r["handler"]: r for r in rows}
    assert by["via_helper"]["class"] == "PROFILE_SCOPE"
    assert by["via_wrapper"]["class"] == "PROFILE_SCOPE"
    # more than one rule holds: the FIRST in the order is the class and the others are listed in the row
    assert by["both"]["class"] == "PROFILE_SCOPE" and by["both"]["also"] == ["ENV_FIRM_LIST"]


def test_the_two_commentary_handlers_are_listed_and_classed():
    if not REAL_HANDLER_FILE.exists():
        pytest.skip("handler file not present in this checkout")
    rows, why = cp.ticket_handler_rows(REAL_HANDLER_FILE.read_bytes())
    assert rows, why
    for r in rows:
        print("handler %-26s %-20s also=%s  %s" % (r["handler"], r["class"], r["also"], r["basis"]))
    by = {r["handler"]: r["class"] for r in rows}
    assert "commentary_draft_ticket" in by and "commentary_sent_ticket" in by
    assert by["commentary_draft_ticket"] != "UNCLASSED"
    assert by["commentary_sent_ticket"] != "UNCLASSED"


def test_a_dispatched_handler_with_no_class_makes_the_exit_nonzero(tmp_path, monkeypatch, capsys):
    census, smap = _fake_ticket_world(tmp_path, monkeypatch, _with_extra_handler("    return _resp(200, {})"))
    rc = cp.main(["--out", str(tmp_path / "u.json"), "--census", str(census), "--source-map", str(smap)])
    text = capsys.readouterr().out
    assert "READ27 7/7" in text            # the first read is full ...
    assert "handler extra_ticket UNCLASSED" in text
    assert "TICKET_HANDLERS 7/8 UNCLASSED extra_ticket" in text.splitlines()   # ... and the line says which handler
    assert rc != 0                         # ... and the exit is still non-zero
    # the control: the same extra handler once it is classed leaves the exit at zero
    census, smap = _fake_ticket_world(tmp_path, monkeypatch, _with_extra_handler("    return _resolve_scope(event, 'x')"))
    rc = cp.main(["--out", str(tmp_path / "v.json"), "--census", str(census), "--source-map", str(smap)])
    text = capsys.readouterr().out
    assert rc == 0 and "TICKET_HANDLERS 8/8" in text.splitlines()


def test_the_read27_line_and_its_table_rows_are_unchanged(tmp_path, monkeypatch, capsys):
    census, smap = _fake_ticket_world(tmp_path, monkeypatch, ticket_source())
    # the pre-pc2 call shape still works and gives the rows the old main wrote
    expected_table = cp.build_table(cp.census_routes(str(census)), str(smap))
    rc = cp.main(["--out", str(tmp_path / "w.json"), "--census", str(census), "--source-map", str(smap)])
    lines = capsys.readouterr().out.splitlines()
    assert rc == 0
    assert (tmp_path / "w.json").read_text(encoding="utf-8") == json.dumps(expected_table, indent=1) + "\n"
    assert isinstance(expected_table, list) and all(t["function"] for t in expected_table)
    old = ["%-26s %d %s %s %s%s" % (t["function"], t["n_routes"], (t["last_modified"] or "-")[:19],
                                    (t["member_sha256"] or "ABSENT")[:8], t["verdict"],
                                    (" " + t["detail"]) if t["verdict"] != "CLAMPED" and t["detail"] else "")
           for t in expected_table]
    assert lines[:len(old) + 1] == old + ["READ27 7/7"]          # the old lines, byte for byte, are first
    assert all(ln.startswith(("handler ", "TICKET_HANDLERS ")) for ln in lines[len(old) + 1:])   # everything new comes after
