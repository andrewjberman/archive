"""Offline tests of release_census.py on synthetic zips (IRPT_BCKEND IB-pr-323)."""
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "release_census.py"
sys.path.insert(0, str(HERE.parent))

import release_census as rc  # noqa: E402


def _zip(path, members):
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return str(path)


def _rules(path, mapping):
    path.write_text(json.dumps({"rules": [{"pattern": k, "order": v} for k, v in mapping.items()]}), encoding="utf-8")
    return str(path)


def _row(result, name):
    return next(m for m in result["members"] if m["member"] == name)


def test_added_member_is_listed_added(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "1"})
    built = _zip(tmp_path / "built.zip", {"a.py": "1", "new.py": "2"})
    res = rc.census(built, live)
    assert _row(res, "new.py")["status"] == "added"
    assert _row(res, "a.py")["status"] == "unchanged"
    assert res["counts"]["added"] == 1


def test_removed_member_is_listed_removed(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "1", "gone.py": "2"})
    built = _zip(tmp_path / "built.zip", {"a.py": "1"})
    res = rc.census(built, live)
    assert _row(res, "gone.py")["status"] == "removed"
    assert res["counts"]["removed"] == 1


def test_changed_member_is_listed_changed_by_sha256(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "old", "b.py": "same"})
    built = _zip(tmp_path / "built.zip", {"a.py": "new", "b.py": "same"})
    res = rc.census(built, live)
    row = _row(res, "a.py")
    assert row["status"] == "changed"
    assert row["built_sha256"] != row["live_sha256"]
    assert _row(res, "b.py")["status"] == "unchanged"
    assert res["counts"]["changed"] == 1 and res["counts"]["unchanged"] == 1


def test_attributed_change_passes_with_exit_0(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "old", "keep.py": "k"})
    built = _zip(tmp_path / "built.zip", {"a.py": "new", "keep.py": "k", "added.py": "x"})
    rules = _rules(tmp_path / "rules.json", {"a.py": "IB-pr-317", "added.*": "IB-pr-320"})
    out = tmp_path / "out.json"
    r = subprocess.run([sys.executable, str(TOOL), "census", built, live, "--rules", rules, "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    res = json.loads(out.read_text(encoding="utf-8"))
    assert _row(res, "a.py")["attribution"] == "IB-pr-317"
    assert _row(res, "added.py")["attribution"] == "IB-pr-320"
    assert res["riders"] == [] and res["counts"]["riders"] == 0


def test_unattributed_change_is_a_RIDER_with_exit_1(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "old", "b.py": "old"})
    built = _zip(tmp_path / "built.zip", {"a.py": "new", "b.py": "new"})
    rules = _rules(tmp_path / "rules.json", {"a.py": "IB-pr-321"})
    out = tmp_path / "out.json"
    r = subprocess.run([sys.executable, str(TOOL), "census", built, live, "--rules", rules, "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 1
    res = json.loads(out.read_text(encoding="utf-8"))
    assert res["riders"] == ["b.py"]
    assert _row(res, "b.py")["attribution"] == "RIDER"
    assert _row(res, "a.py")["attribution"] == "IB-pr-321"


def test_no_rules_file_marks_every_difference_RIDER_and_identical_zips_pass(tmp_path):
    live = _zip(tmp_path / "live.zip", {"a.py": "1"})
    built = _zip(tmp_path / "built.zip", {"a.py": "2"})
    same = _zip(tmp_path / "same.zip", {"a.py": "1"})
    assert subprocess.run([sys.executable, str(TOOL), "census", built, live], capture_output=True).returncode == 1
    assert subprocess.run([sys.executable, str(TOOL), "census", same, live], capture_output=True).returncode == 0


def test_signed_url_is_scrubbed_from_error_text():
    scrubbed = rc._scrub("HTTP 403 for https://bucket.s3.amazonaws.com/x?X-Amz-Signature=abc123&X-Amz-Credential=zzz done")
    assert "Signature" not in scrubbed and "https://" not in scrubbed and "<url-redacted>" in scrubbed
