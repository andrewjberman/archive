"""CA-h-3 AC1: the FWD-7 signed-answer design is one document with its six sections. Mechanical shape only; whether it is
sound is the CVO's judgment (AC2). Prints H3-DESIGN sections=<n> of 6 lines=<n> ok=<bool>."""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[9]
DOC = REPO / "org/missions/D9/COMM/COMM_ASSIST/deliverables/0.9.0_WK_COMM_ASSIST~8/MUSE_ANSWER_PATH_DESIGN.md"
HEADS = ["## 1. How muse's answer is shown to come from muse", "## 2. How the forwarder verifies it",
         "## 3. What is recorded on a refusal", "## 4. The stale-version refusal",
         "## 5. The write entry and the grant it needs", "## 6. The forged-answer test that must refuse"]
if not DOC.is_file():
    print("H3-DESIGN sections=0 of 6 lines=0 ok=False reason=absent")
    sys.exit(0)
lines = DOC.read_text(encoding="utf-8").splitlines()
have = [h for h in HEADS if h in lines]
text = "\n".join(lines)
entry = any(e in text for e in ("sms.reply", "owner.text"))
ok = len(have) == 6 and len(lines) <= 140 and entry and "version" in text.lower()
print("H3-DESIGN sections=%d of 6 lines=%d entry_named=%s ok=%s" % (len(have), len(lines), entry, ok))
