"""TCKT_VNEXT TO-R23-F51 final run, PART 2 (0.7.0_AE_CloudOps~TV2): the two post-claim clips, with the CTO-approved SECOND picker token (msg 11835, a deviation).

Part 1 (r23_fwd5.py, run 03:32Z) filed two tickets, read the board as the picker, wrote the private full-board shots and the committed r23_rows_before clip, and the picker's
claim from the board returned 200; it then stopped on a stale-DOM read (this seat's bug) after clicking In Progress. Its removal wait was stopped at 03:35:19Z so the state
stayed for these clips. This part mints ONE more token for the SAME picker row (10 minutes, GETs only, no claim or write), opens the board as the picker, waits until the
chosen row really reads in progress on the In Progress tab, takes the unaltered clip of the chosen row (r23_rows_claimed) and of the other row on the Open tab, then removes
everything after the token's exp (the removal of r23_fwd5.py reused) and writes the result with the second token stated as a deviation.
"""
from __future__ import annotations

import importlib.util
import json
import re
import struct
import sys
import time
import hashlib
from pathlib import Path

import boto3
import jwt as pyjwt

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r23", str(HERE / "r23_fwd5.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

PICK = "TCK-20261021-cf3af782"
OTHER = "TCK-20261021-1bff6c63"
LIFE2 = 600
OUT1 = (HERE / "run_output.txt").read_text(encoding="utf-8")


def png_info(path):
    raw = open(path, "rb").read()
    w, h = struct.unpack(">II", raw[16:24])
    return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "width": w, "height": h}


def mint_second_token():
    pem = boto3.client("secretsmanager", region_name=m.REGION).get_secret_value(SecretId=m.KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": m.PICKER, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal", "role": "user",
              "userType": "test-filer", "name": m.NAMES[m.PICKER], "iat": iat, "exp": iat + LIFE2}
    tok = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    m.state["exp"].append(iat + LIFE2)
    m.say("SECOND picker token minted (memory only, deviation approved by the CTO msg 11835) iat=%s exp=%s life=%ds" % (m.iso(iat), m.iso(iat + LIFE2), LIFE2))
    return tok, iat


def wait_status(ps, tid, word, secs):
    end = time.time() + secs
    while time.time() < end:
        r = ps.page.locator("tbody tr").filter(has=ps.page.locator("td", has_text=tid))
        if r.count():
            cells = r.first.locator("td").all_inner_texts()
            if len(cells) >= 7 and word in cells[6].lower():
                return True
        time.sleep(0.5)
    return False


def first_run_facts():
    br = {}
    for t, typ, age in re.findall(r"board row (TCK-\d{8}-[0-9a-f]{8}) read as picker: type='([^']*)' age='([^']*)'", OUT1):
        br[t] = {"type_label": typ, "age_text": age}
    basis = re.search(r"picker chooses \S+ over \S+: (.*)", OUT1).group(1).strip()
    head = re.search(r"served checkout \S+ HEAD=(\w+)", OUT1).group(1)
    behind = int(re.search(r"files behind origin/DEV: (\d+)", OUT1).group(1))
    open_before = int(re.search(r"open tickets already on the board table: (\d+) of", OUT1).group(1))
    exp1 = re.search(r"token minted for tckt-r23-picker\S* \(memory only\) iat=\S+ exp=(\S+) life", OUT1).group(1)
    return br, basis, head, behind, open_before, exp1


def main():
    m.GATES.mkdir(exist_ok=True)
    out, stop, removed, review = {"shots": {}, "extra": {}}, None, None, False
    m.state["written"] = [m.FILER, m.PICKER]
    m.state["tickets"] = {PICK: "service_request", OTHER: "other"}
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright
        for t, want in ((PICK, "in_progress"), (OTHER, "open")):
            it = m.item_of(m.TICKETS, {"ticket_id": {"S": t}})
            if it is None or it["status"]["S"] != want:
                raise m.Stop("ticket %s is not in the expected state %s" % (t, want))
        if m.item_of(m.USERS, m.key_of(m.PICKER)) is None:
            raise m.Stop("the picker row is gone")
        tok, iat2 = mint_second_token()
        out["iat2"] = iat2
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        ps = m.Session(browser, m.PICKER, tok)
        ps.open_board()
        ps.tab("In Progress")
        if not wait_status(ps, PICK, "progress", 40):
            raise m.Stop("the chosen row never read in progress on the In Progress tab")
        after = ps.read_row(PICK)
        m.say("In Progress tab, chosen row read: type=%r status=%r (the stale Open row of part 1 is not this)" % (after["type_label"], after["status_text"]))
        ps.clip_shot("r23_rows_claimed", [PICK], "chosen_row", out["shots"])
        ps.tab("Open")
        if not wait_status(ps, OTHER, "open", 40):
            raise m.Stop("the other row did not read open on the Open tab")
        ps.clip_shot("r23_other_row_after_claim", [OTHER], "other_row", out["extra"])
        if m.state["engine"] or ps.failed:
            raise m.Stop("an engine call or a refused request was seen")
        m.say("MILESTONE CLIPS_DONE (second token used for GETs only)")
    except m.Stop as e:
        stop = "STOP: %s" % e
        m.say(stop)
    except Exception as e:  # noqa: BLE001
        stop = "STOP (unexpected %s): %s" % (type(e).__name__, re.sub(r"\?\S+", "?<redacted>", str(e))[:300])
        m.say(stop)
    finally:
        try:
            if browser is not None:
                browser.close()
            if pw is not None:
                pw.stop()
        except Exception:  # noqa: BLE001
            pass
        removed = m.remove_all()
        if stop is None:
            review = m.wait_review(time.time() + 1500)
    (HERE / "R23_FWD5_TRACE_part2.json").write_text(json.dumps({"stop": stop, "removed": removed, "trace": m.trace}, indent=1, default=str) + "\n", encoding="utf-8")
    if stop is None and removed and removed["tickets_absent_after"] and removed["rows_absent_after"] and review:
        br, basis, head, behind, open_before, exp1 = first_run_facts()
        before = HERE / "r23_rows_before__tckt-r23-picker-20261021__localhost-5174.png"
        shots = {"r23_rows_before": {"path": m.SHOT_DIR_REL + before.name, "bytes": before.stat().st_size, "origin": m.ORIGIN, "viewer": m.PICKER,
                                     "clipped_to": "two_synthetic_rows", "rows_visible": 2}}
        shots.update(out["shots"])
        private = {r: png_info(m.PRIVATE_DIR + r + ".png") for r in ("r23_board_full", "r23_board_claimed")}
        earlier = list(m.EARLIER)
        earlier.append({"attempt": 4, "at": "2026-10-21T03:32:42Z", "stopped": "PART 1 of this final run: two tickets, board read, private shots, r23_rows_before and the claim from the board (200) all done; the script then read the stale Open row after clicking In Progress (this seat's bug) and stopped before the two post-claim clips; PART 2 (this result) completed them", "record": "run_output.txt (part 1), run_output_clips.txt (part 2)"})
        res = {"claim": "measured", "browser_origin": m.ORIGIN, "filer": m.FILER, "picker": m.PICKER, "chosen_ticket": PICK, "other_ticket": OTHER, "board_read": br,
               "chosen_basis": basis, "claim_via": "board", "opened_before_claim": False, "shots": shots, "extra_shots": out["extra"], "private_board": private,
               "token_exp": m.iso(max(m.state["exp"])), "rows_deleted_at": removed["rows_deleted_at"], "tickets_deleted_at": removed["tickets_deleted_at"],
               "tickets_absent_after": True, "rows_absent_after": True, "no_engine_call": True, "token_printed": False, "shot_data_reviewed": True,
               "served_head": head, "behind_origin_dev_files": behind, "open_tickets_before": open_before,
               "identity_shape": "firmId opal-capital, scope_all_firms BOOL true, no allowedFirmIds (AMENDMENT 1)", "earlier_attempts": earlier,
               "deviation_second_picker_token": {"approved_by": "1.0.0_SA_CTO~DELL2 msg 11835 (V2 records it as AMENDMENT 4)", "why": "part 1 stopped on this seat's stale-DOM read before the two post-claim clips",
                                                 "first_picker_token_exp": exp1, "second_token_iat": m.iso(out["iat2"]), "second_token_exp": m.iso(out["iat2"] + LIFE2),
                                                 "use": "GETs only (board list and metrics); no claim, no create, no write"},
               "note_private_board": "the full-board shots are outside the repo; only sha256, bytes and pixel size are recorded"}
        (HERE / "R23_FWD5_RESULT.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        m.say("result written: R23_FWD5_RESULT.json")
        return 0
    m.say("part 2 ended without a result (stop=%s review_ok=%s)" % (stop, review))
    return 1


if __name__ == "__main__":
    sys.exit(main())
