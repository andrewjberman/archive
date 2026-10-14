"""CA-j-4 (seat row D2-S1): the forwarder creates answers/, answers/done/ and answers/rejected/ when they are absent, and disturbs nothing that is there.

Prints:  J4-DIRS ok=<True|False> arms=<n> of 3 failed=<names|none> reason=<text>
Calls forwarder.forward(root, send, now) on a reader folder that has a drafts.json and NO answers/ folder, then on one that already holds an answer file. No AWS, no network.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
NOW = "2026-10-14T03:00:00Z"


def main():
    failed, why = [], ""
    try:
        from data.transcripts.scripts.muse_reader import forwarder as fw

        def root(with_answers):
            d = Path(tempfile.mkdtemp())
            (d / "drafts.json").write_text(json.dumps({"source": "drafts", "items": []}), encoding="utf-8")
            if with_answers:
                (d / "answers").mkdir()
            return d

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:60]))

        def creates_all_three():
            d = root(False)
            fw.forward(d, lambda *args: args[3], NOW)
            return all((d / "answers" / s).is_dir() for s in ("", "done", "rejected"))

        def leaves_an_answer_file_and_markers_alone():
            d = root(True)
            keep = d / "answers" / "keep.json"
            keep.write_text("{not json", encoding="utf-8")
            fw.forward(d, lambda *args: args[3], NOW)
            fw.forward(d, lambda *args: args[3], NOW)
            return keep.read_text(encoding="utf-8") == "{not json" and len(list((d / "answers" / "rejected").glob("*.json"))) == 1

        def runs_twice_without_error_on_a_fresh_folder():
            d = root(False)
            fw.forward(d, lambda *args: args[3], NOW)
            fw.forward(d, lambda *args: args[3], NOW)
            return (d / "answers" / "done").is_dir()

        for name, fn in (("creates-all-three-when-absent", creates_all_three), ("answer-file-and-markers-untouched", leaves_an_answer_file_and_markers_alone),
                         ("second-run-on-a-fresh-folder-ok", runs_twice_without_error_on_a_fresh_folder)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("import")
    print("J4-DIRS ok=%s arms=%d of 3 failed=%s reason=%s" % (not failed, 0 if "import" in failed else 3 - len(failed), ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
