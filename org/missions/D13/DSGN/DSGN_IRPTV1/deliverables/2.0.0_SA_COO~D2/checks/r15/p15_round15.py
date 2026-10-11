"""DSGN_IRPTV1 round 15 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msgs 4407 and 4427 on the FWD-1 rendered walk's break.

Cell: IV-e-93 the FIRM_BINDING refusal of the reporting summary and manifest placed at the line that emits it; whether it refuses because the
firm selector sat at its default, Global (All); what an Opal user who never touches that selector sees; and the PRD's FWD-1 sentence beside
the walk's hop-7 line for the reviewer. Read-only. (OBJECT_NOT_COVERED was placed by 2.0.0_SA_COO~P2, msg 4414, and ruled in msg 4417.)

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV93-AC1  ~51/FIRM_BINDING_PLACED.json: emitted_at {file, line} is a file at HEAD whose cited line or its 3 neighbours contain
            FIRM_BINDING; routes names the summary and the manifest route templates; condition and reached_because are non-empty;
            because_no_single_firm_selected is YES / NO / NOT_ESTABLISHED with basis [{file, line}]; page_sends {what, source: {file,
            line}} says what firm binding the page puts on those two requests under Global (All); whose is SERVICE / PAGE / BOTH /
            NOT_ESTABLISHED; opal_user_default_sees is non-empty; hop7 {prd_sentence, walk_line} both non-empty. A NOT_ESTABLISHED
            answer carries what_would_establish_it.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~51/"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV15"))
        sys.exit(1)

    if cid != "IV93-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (D + "FIRM_BINDING_PLACED.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    e = r.get("emitted_at") or {}
    f = root / str(e.get("file") or "")
    if not f.is_file() or not isinstance(e.get("line"), int):
        fail("emitted_at %r is not a file and line at HEAD" % e)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if "FIRM_BINDING" not in "\n".join(lines[max(0, e["line"] - 4):min(len(lines), e["line"] + 3)]):
        fail("the cited line %s:%d and its 3 neighbours do not contain FIRM_BINDING" % (e["file"], e["line"]))
    routes = " ".join(str(x) for x in (r.get("routes") or []))
    if "summary" not in routes or "manifest" not in routes:
        fail("routes %r do not name the summary and the manifest" % r.get("routes"))
    for k in ("condition", "reached_because", "opal_user_default_sees"):
        if not str(r.get(k) or "").strip():
            fail("%s is empty" % k)
    ans = r.get("because_no_single_firm_selected")
    if ans not in ("YES", "NO", "NOT_ESTABLISHED"):
        fail("because_no_single_firm_selected %r" % ans)
    if not r.get("basis") or any(not b.get("file") or not isinstance(b.get("line"), int) for b in r["basis"]):
        fail("basis lacks file-and-line entries")
    ps = r.get("page_sends") or {}
    src = ps.get("source") or {}
    if not str(ps.get("what") or "").strip() or not src.get("file") or not isinstance(src.get("line"), int):
        fail("page_sends %r" % ps)
    if r.get("whose") not in ("SERVICE", "PAGE", "BOTH", "NOT_ESTABLISHED"):
        fail("whose %r" % r.get("whose"))
    if "NOT_ESTABLISHED" in (ans, r.get("whose")) and not str(r.get("what_would_establish_it") or "").strip():
        fail("a NOT_ESTABLISHED answer without what_would_establish_it")
    h = r.get("hop7") or {}
    if not str(h.get("prd_sentence") or "").strip() or not str(h.get("walk_line") or "").strip():
        fail("hop7 %r" % h)
    print("OK: FIRM_BINDING placed at %s:%d; because no single firm selected: %s; whose: %s" % (e["file"], e["line"], ans, r["whose"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
