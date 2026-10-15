"""HVST-cb-5, the issuer's real run: one wsj job, with every Chrome top-level window sampled for IsIconic.

Run from the root of the checkout that carries the cb-5 merge (the main tree after the merge). It starts one
collector job (publisher wsj, ticker COST, no upload) as a subprocess and, every half second until it ends, lists the
visible top-level windows of chrome.exe (class Chrome_WidgetWin_1, non-empty title) and whether each is minimised.
Last line: `CB5 RESULT: PASS`, `CB5 RESULT: FAIL <why>`. Window titles are never printed (they can carry article text).
"""

import ctypes
import json
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

PUBLISHER = "wsj"
TICKER = "COST"
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
ENUM = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def exe_of(pid):
    handle = kernel32.OpenProcess(0x1000, False, pid)
    if not handle:
        return ""
    try:
        size = wintypes.DWORD(520)
        buffer = ctypes.create_unicode_buffer(520)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return buffer.value.lower()
        return ""
    finally:
        kernel32.CloseHandle(handle)


def chrome_windows():
    found = []

    def visit(hwnd, _):
        if not user32.IsWindowVisible(hwnd) and not user32.IsIconic(hwnd):
            return True
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(hwnd, cls, 64)
        if cls.value != "Chrome_WidgetWin_1" or user32.GetWindowTextLengthW(hwnd) == 0:
            return True
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if exe_of(pid.value).endswith("chrome.exe"):
            found.append((hwnd, bool(user32.IsIconic(hwnd))))
        return True

    user32.EnumWindows(ENUM(visit), 0)
    return found


def newest_run(runtime):
    rows = sorted((runtime / "runs").glob("*-" + PUBLISHER + "-*.json"), key=lambda p: p.stat().st_mtime)
    return json.loads(rows[-1].read_text(encoding="utf-8")) if rows else None


def main():
    root = Path.cwd().resolve()
    runtime = root / ".runtime" / "opal-data-harvest"
    command = [sys.executable, "-m", "lib.opal_data_harvest", "run", "--tickers", TICKER, "--publishers", PUBLISHER,
               "--max-jobs", "1"]
    # Windows the box already had open (the operator's own Chrome) are not the runner's: record them first.
    before = {hwnd for hwnd, _ in chrome_windows()}
    proc = subprocess.Popen(command, cwd=str(root))
    seen, iconic, normal, flash = {}, 0, 0, 0
    deadline = time.time() + 1500
    while proc.poll() is None and time.time() < deadline:
        now = time.time()
        for hwnd, minimised in chrome_windows():
            if hwnd in before:
                continue
            seen.setdefault(hwnd, now)
            if minimised:
                iconic += 1
            elif now - seen[hwnd] <= 3.0:
                flash += 1  # the launch flash: a new window has 3 seconds to be minimised
            else:
                normal += 1
        time.sleep(0.5)
    proc.wait(timeout=60)
    run = newest_run(runtime)
    status = run.get("status") if run else None
    accepted = len(run.get("accepted") or []) if run else 0
    print("WINDOWS_SEEN=%d SAMPLES_MINIMISED=%d SAMPLES_LAUNCH_FLASH=%d SAMPLES_NOT_MINIMISED=%d STATUS=%s ACCEPTED=%d" % (
        len(seen), iconic, flash, normal, status, accepted))
    if not seen:
        print("CB5 RESULT: FAIL no runner window was seen at all (the probe cannot grade)")
        return 1
    ok = normal == 0 and status == "complete_candidates" and accepted > 0
    print("CB5 RESULT: PASS" if ok else "CB5 RESULT: FAIL %d samples not minimised, status %s, accepted %d" % (normal, status, accepted))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
