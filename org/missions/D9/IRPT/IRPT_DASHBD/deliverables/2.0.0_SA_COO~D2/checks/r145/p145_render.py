#!/usr/bin/env python3
"""Round 145, workstream B-49F (issuer 2.0.0_SA_COO~D2), DIRECT ACT: the RENDER CHECK of the 49 Financial disclosure placeholder (CTO ROUND ANALYSIS rounds 142 and 144, msg 8762, item 2:
"print the 49F report from the candidate and read the last sheet for the exact placeholder text"). The candidate is the portal branch wk-IRPT_DASHBD-224-portal, named by commit (p144's CANDIDATE).

This script RENDERS the candidate's 49 Financial performance report from the private household sample with the committed harness (render_sample.ts, bun), into a fresh private folder, then READS the export HTML:
the LAST sheet, its placeholder text, its page counter against the sheet count, the pointer line's count, and the PDF's page count. It prints counts and the placeholder words only: no figure, name or account id.

Run as:  python -I <this file> <repo_root> DB145-1-AC1          renders and grades (several minutes)
         python -I <this file> --selftest                       the pure clauses on synthetic HTML
"""
import atexit
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p144", str(HERE.parent / "r144" / "p144_placeholder.py"))
p144 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p144)

HARNESS_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~180/render_sample.ts"
SAMPLE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~180/HOUSEHOLD_SAMPLE.json"
SAMPLE_SHA256 = "1451db41043958c3a22564ed96b7e028b0d23c360df0d4528c6a8bcc6e2bd70f"
OUT_DIR = "C:/dev/_irpt_private_evidence_20261009/fwd21_sample_r145"
RECORD_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/reads/RD_DISCLOSURE_RENDER_R145.json"
WORDS = p144.WORDS
POINTER = p144.POINTER


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def strip_tags(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


def read_sheets(html):
    """Split the export document into its sheets: each starts at an element carrying data-report-page. -> list of (page id, markup)."""
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'data-report-page="([^"]*)"', html)]
    out = []
    for i, (pos, pid) in enumerate(marks):
        start = html.rfind("<div", 0, pos)
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        out.append((pid, html[start:end]))
    return out


def grade(html, pdf_pages):
    sheets = read_sheets(html)
    n = len(sheets)
    need(n >= 9, "the export must hold at least nine sheets (eight sections and the disclosure sheet), found %d" % n)
    need("49 Financial" in strip_tags(sheets[0][1]), "the first sheet must carry the 49 Financial title (the report is the 49 Financial one)")
    ids = [pid for pid, _ in sheets]
    need(ids.count("disclosures") == 1 and ids[-1] == "disclosures", "exactly one sheet is 'disclosures' and it is the LAST: %s" % ids[-3:])
    last = sheets[-1][1]
    ph = re.findall(r"<[^>]*data-disclosure-placeholder[^>]*>(.*?)</", last, re.S)
    need(len(ph) == 1 and strip_tags(ph[0]) == WORDS, "the last sheet must hold ONE placeholder reading exactly %r, read %r" % (WORDS, [strip_tags(x) for x in ph]))
    need('data-slot="disclosure"' in last and 'data-slot-state="unfilled"' in last, "the last sheet's slot must carry data-slot=disclosure and data-slot-state=unfilled")
    text = strip_tags(last)
    need(POINTER.lower() not in text.lower(), "the pointer line must NOT print on the disclosure sheet itself")
    m = re.findall(r"Page (\d+) of (\d+)", text)
    need(m == [(str(n), str(n))], "the last sheet's footer must read Page %d of %d, read %s" % (n, n, m))
    totals = {x for _, mk in sheets for x in re.findall(r"Page \d+ of (\d+)", strip_tags(mk))}
    need(totals == {str(n)}, "every sheet's page total must be %d, read %s" % (n, sorted(totals)))
    pointers = sum(1 for _, mk in sheets[:-1] if POINTER.lower() in strip_tags(mk).lower())
    need(pointers == n - 1, "the pointer line must print on each of the %d earlier sheets, read %d" % (n - 1, pointers))
    need(pdf_pages == n, "the PDF must have %d pages (one per sheet), read %s" % (n, pdf_pages))
    return {"sheets": n, "last_sheet": "disclosures", "placeholder": WORDS, "placeholder_count_in_last_sheet": 1, "pointer_sheets": pointers, "pdf_pages": pdf_pages}


def render(root):
    root = Path(root).resolve()
    portal_main = root / "portal"
    need(Path(SAMPLE).is_file(), "the private sample is missing: %s" % SAMPLE)
    import hashlib
    need(hashlib.sha256(Path(SAMPLE).read_bytes()).hexdigest() == SAMPLE_SHA256, "the private sample's sha256 differs from the one this check was written on")
    tmp = Path(tempfile.mkdtemp(prefix="p145_", dir="C:/dev"))
    wt = tmp / "portal"
    r = subprocess.run(["git", "-C", str(portal_main), "worktree", "add", "--detach", str(wt), p144.CANDIDATE], capture_output=True, text=True, timeout=300)
    need(r.returncode == 0, "could not make the candidate worktree: %s" % r.stderr.strip()[:200])
    nm = portal_main / "node_modules"
    if nm.exists():
        subprocess.run(["cmd", "/c", "mklink", "/J", str(wt / "node_modules"), str(nm)], capture_output=True, timeout=60)

    def cleanup():
        if (wt / "node_modules").exists():
            subprocess.run(["cmd", "/c", "rmdir", str(wt / "node_modules")], capture_output=True, timeout=60)
        subprocess.run(["git", "-C", str(portal_main), "worktree", "remove", "--force", str(wt)], capture_output=True, timeout=300)
        shutil.rmtree(str(tmp), ignore_errors=True)
    atexit.register(cleanup)
    hdir = tmp / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/render"
    hdir.mkdir(parents=True)
    # the harness prints the PDF through headless Edge; with another Edge or WebView2 process alive the spawned instance can hand off and never exit, so the COPY
    # of the harness (never the committed file) gets its own throwaway profile directory, which makes the print a separate instance that exits
    src = (root / HARNESS_REL).read_text(encoding="utf-8")
    prof = (tmp / "edge_profile").as_posix()
    need(src.count("'--headless', ") == 1, "the harness's Edge arguments are not the expected shape")
    need(src.count("const FIRM_ID = 'inflection'") == 1, "the harness's firm id line is not the expected shape")
    # the committed harness renders the Inflection title; the 49 Financial report is the same document under the firm id 49financial (the title is read from the registry by that id)
    src = src.replace("const FIRM_ID = 'inflection'", "const FIRM_ID = '49financial'")
    (hdir / "render_sample.ts").write_text(src.replace("'--headless', ", "'--headless', '--user-data-dir=%s', " % prof), encoding="utf-8")
    out = Path(OUT_DIR)
    shutil.rmtree(str(out), ignore_errors=True)
    b = shutil.which("bun")
    need(b, "bun is not on PATH")
    try:
        p = subprocess.run([b, str(hdir / "render_sample.ts"), SAMPLE, str(out)], cwd=str(tmp), capture_output=True, text=True, timeout=600)
        need(p.returncode == 0, "the harness failed (rc %d): %s" % (p.returncode, (p.stderr or p.stdout)[-300:].replace("\n", " | ")))
    except subprocess.TimeoutExpired:
        pass  # the print step can hang after both files are written: the files are read below and a missing or unreadable one fails the clause
    hp, pp = out / "FWD21_EXPORT_49F_SAMPLE.html", out / "FWD21_EXPORT_49F_SAMPLE.pdf"
    need(hp.is_file() and pp.is_file(), "the harness wrote no export HTML and PDF")
    pdf_pages = len(re.findall(rb"/Type\s*/Page[^s]", pp.read_bytes()))
    return hp.read_text(encoding="utf-8"), pdf_pages


def run(root, record=False):
    html, pdf_pages = render(root)
    res = grade(html, pdf_pages)
    if record:
        rec = {"claim": "measured", "check": "DB145-1-AC1", "candidate_commit": p144.CANDIDATE, "sample_sha256": SAMPLE_SHA256, "private_folder": OUT_DIR, **res,
               "words": "The 49 Financial performance report (the household sample, under the firm id 49financial) was rendered from the candidate portal branch by commit with the committed harness and read: the export has %d sheets, the last is the disclosures sheet and prints the placeholder exactly once, "
                        "its footer reads Page %d of %d, the pointer line prints on each of the %d earlier sheets and not on the disclosure sheet, and the PDF has %d pages. Nothing from the sample is recorded." % (res["sheets"], res["sheets"], res["sheets"], res["sheets"] - 1, res["pdf_pages"])}
        Path(root, RECORD_REL).write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    return res


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)

    def sheet(pid, n, total, body="", pointer=True):
        return ('<div class="ir-page" data-report-page="%s">%s<footer>Page %d of %d</footer>%s</div>' % (pid, body, n, total, ("<p>" + POINTER + "</p>") if pointer else ""))
    total = 9
    ok = "".join(sheet("s%d" % i, i, total, "49 Financial Performance Report" if i == 1 else "") for i in range(1, 9)) + sheet("disclosures", 9, total, '<div data-slot="disclosure" data-slot-state="unfilled"><p data-disclosure-placeholder="true">%s</p></div>' % WORDS, pointer=False)
    assert grade(ok, 9)["sheets"] == 9
    red(lambda: grade(ok, 8), "pdf pages differ")
    red(lambda: grade(ok.replace(WORDS, "Disclosure page pendng"), 9), "placeholder words differ")
    red(lambda: grade(ok.replace("49 Financial", "Inflection Wealth Management"), 9), "wrong firm title")
    red(lambda: grade(ok.replace("data-disclosure-placeholder", "x"), 9), "no placeholder mark")
    red(lambda: grade(ok.replace('data-slot-state="unfilled"', 'data-slot-state="filled"'), 9), "slot state")
    red(lambda: grade(ok.replace('data-report-page="disclosures"', 'data-report-page="s0"'), 9), "no disclosures sheet")
    red(lambda: grade(ok.replace("Page 9 of 9", "Page 9 of 8"), 9), "page total differs")
    red(lambda: grade(ok.replace("Page 3 of 9", "Page 3 of 8"), 9), "an earlier sheet's total differs")
    red(lambda: grade(sheet("disclosures", 9, 9, '<div data-slot="disclosure" data-slot-state="unfilled"><p data-disclosure-placeholder="true">%s</p></div>' % WORDS), 9), "too few sheets")
    red(lambda: grade(ok.replace('<p data-disclosure-placeholder="true">', '<p>' + POINTER + '</p><p data-disclosure-placeholder="true">'), 9), "pointer on the disclosure sheet")
    red(lambda: grade(ok.replace("<p>" + POINTER + "</p>", "", 1), 9), "a pointer line missing")
    print("selftest: render grade (10 red arms) clauses behave")
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        if len(sys.argv) < 3 or sys.argv[2] != "DB145-1-AC1":
            print("usage: p145_render.py <root> DB145-1-AC1 [--record]")
            sys.exit(2)
        r = run(sys.argv[1], record="--record" in sys.argv)
        print("OK: rendered from the candidate %s: %d sheets, the last is `disclosures` and prints %r once, its footer reads Page %d of %d, the pointer line prints on the %d earlier sheets and not on it, the PDF has %d pages"
              % (p144.CANDIDATE, r["sheets"], WORDS, r["sheets"], r["sheets"], r["pointer_sheets"], r["pdf_pages"]))
        print("DB145-1-AC1 PASS")
    except Exception as e:  # a failed render or clause is a FAIL, not a traceback
        print("FAIL: %s" % e)
        print("DB145-1-AC1 FAIL")
        sys.exit(1)
