"""AMGT_RESAPP round-99 PREP -- give each Security Analysis harness fixture the model-side copy of `fiscal_year_figures` that the live payload carries.

  python r99_fixture_model_copy.py <portal worktree root>

The captured fixtures (`tabsFixture.*.json` `.thesis`, `thesisBundle*.json`) predate the model block: they carry the top-level `fiscal_year_figures` and no `model`. The repoint reads
`model.fiscal_year_figures`, so each fixture whose top-level list is non-empty gets `model.fiscal_year_figures` set to an EQUAL copy (the live payload serves the two equal, 95 of 95
names, `r99_fy_figures_equal.py`). Nothing else moves: the file is parsed, one key is added, and it is written back in the SAME serialisation it was read in (each of the eight files
round-trips byte-exact: indent, separators, CRLF and trailing newline are detected, and a file that does not round-trip is refused, never rewritten). A fixture with an empty top-level
list is left as it is. Prints one line per file and `fixtures changed N of M`.
"""
import glob
import json
import os
import sys

SA = os.path.join("src", "pages", "SecurityAnalysis", "__harness__")


def serialisation(raw):
    d = json.loads(raw)
    for indent in (None, 1, 2, 4):
        for sep in ((", ", ": "), (",", ": ")):
            for tail in ("", "\n", "\r\n"):
                out = json.dumps(d, indent=indent, separators=sep, ensure_ascii=True).replace("\n", "\r\n")
                if out + tail == raw:
                    return indent, sep, tail
    return None


def main(argv):
    root = argv[0]
    files = sorted(glob.glob(os.path.join(root, SA, "tabsFixture.*.json")) + glob.glob(os.path.join(root, SA, "thesisBundle*.json")))
    changed = 0
    for path in files:
        raw = open(path, "rb").read().decode("utf-8")
        ser = serialisation(raw)
        name = os.path.basename(path)
        if ser is None:
            print("REFUSED %s: does not round-trip in a known serialisation" % name)
            return 1
        doc = json.loads(raw)
        thesis = doc.get("thesis", doc)
        figures = thesis.get("fiscal_year_figures") or []
        if not figures:
            print("SKIP    %s: top-level fiscal_year_figures empty" % name)
            continue
        model = thesis.get("model")
        if model is None:
            model = {}
            thesis["model"] = model
        elif not isinstance(model, dict):
            print("REFUSED %s: model is %s" % (name, type(model).__name__))
            return 1
        if model.get("fiscal_year_figures") == figures:
            print("SAME    %s" % name)
            continue
        model["fiscal_year_figures"] = json.loads(json.dumps(figures))
        indent, sep, tail = ser
        out = json.dumps(doc, indent=indent, separators=sep, ensure_ascii=True).replace("\n", "\r\n") + tail
        with open(path, "wb") as fh:
            fh.write(out.encode("utf-8"))
        changed += 1
        print("WROTE   %s: model.fiscal_year_figures = %d figures" % (name, len(figures)))
    print("fixtures changed %d of %d" % (changed, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
