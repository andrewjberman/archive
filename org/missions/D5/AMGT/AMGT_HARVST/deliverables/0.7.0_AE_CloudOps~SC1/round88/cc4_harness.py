"""HVST-cc-4 trace harness: ONE local bbg job run through the pin's own code, with events recorded that say WHO ends the page.

Usage (from any directory):
    python cc4_harness.py --arm A|B|C --security-json <file> --runtime-root <scratch root> --out <arm .jsonl>

It imports the pin's lib.opal_data_harvest from PIN (a locked worktree: no file under it is edited) and calls its CLI main()
with the runner's own argument list (backfill_driver.Collector.run_job, lines 275-277); only --runtime-root and the
security file differ from the runner's job. What it hooks (monkeypatch in this process only):
  - playwright BrowserType.launch_persistent_context: attaches page close / crash / popup / framenavigated, context close and
    browser disconnected listeners (simple value records, no page calls in a handler);
  - playwright Page.close, BrowserContext.close, Browser.close and tab_transport.TabSession.close: a RUNNER-SIDE close call is
    recorded with its caller stack (pin frames only), so a close with no such call is not the runner's;
  - tab_transport.TabSession._minimize_window: the pin's own three steps, each timed (Browser.setWindowBounds returned or not);
  - Arm B only: TabSession.__init__ is called with minimize=False (the switch the pin's signature offers);
  - transport.PacedSession._solve_challenge, verification.route_bot_check, verification.solve, verification._press_and_hold_box:
    entry, exit, page.is_closed(), the exception and its traceback;
  - verification._press_and_hold_box, on the first call that FINDS the control: the harness raises HarnessStop BEFORE any
    hold, so no arm ever operates the vendor's challenge control (the runner's job would; this trace does not).
A psutil poller records the main chrome.exe process of the bbg profile (first seen, gone).
No secret is read here; the job reads its own stored session as the runner's job does.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import threading
import time
import traceback
from pathlib import Path

PIN = r"C:\dev\wk-harvest-runner-pin-ddd7dcdc38"
T0 = time.monotonic()
_LOCK = threading.Lock()
_OUT = {"path": None}
_STATE = {"press_box_seen": False, "chrome_pid": None}


class HarnessStop(Exception):
    """Raised by the harness before any hold: the control was found, the page was alive."""


def ev(name, **kw):
    row = {"t_mono": round(time.monotonic() - T0, 4), "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds"),
           "thread": threading.current_thread().name, "ev": name}
    row.update(kw)
    line = json.dumps(row, ensure_ascii=True, default=str)
    with _LOCK:
        if _OUT["path"]:
            with open(_OUT["path"], "a", encoding="ascii", newline="\n") as f:
                f.write(line + "\n")


def pin_stack(limit=12):
    frames = [f for f in traceback.extract_stack() if "wk-harvest-runner-pin" in f.filename or "cc4_harness" in f.filename]
    return ["%s:%d %s" % (Path(f.filename).name, f.lineno, f.name) for f in frames[-limit:]]


def attach_page(page):
    page.on("close", lambda *_: ev("page.close_event"))
    page.on("crash", lambda *_: ev("page.crash_event"))
    page.on("popup", lambda *_: ev("page.popup_event"))
    page.on("framenavigated", lambda frame: ev("page.framenavigated", url=str(getattr(frame, "url", ""))[:120]))
    ev("page.attached")


def attach_context(ctx):
    ctx.on("close", lambda *_: ev("context.close_event"))
    ctx.on("page", lambda p: (ev("context.new_page_event"), attach_page(p)))
    try:
        if ctx.browser is not None:
            ctx.browser.on("disconnected", lambda *_: ev("browser.disconnected_event"))
    except Exception as exc:  # noqa: BLE001
        ev("browser.listener_unavailable", error=repr(exc)[:120])
    for p in list(ctx.pages):
        attach_page(p)
    ev("context.attached")


def poll_chrome(stop):
    import psutil
    seen = {}
    while not stop.is_set():
        now = {}
        for p in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmd = " ".join(p.info["cmdline"] or [])
                if (p.info["name"] or "").lower() == "chrome.exe" and "browser-profiles" in cmd.lower() and "\\bbg" in cmd.lower() and "--type=" not in cmd:
                    now[p.info["pid"]] = True
            except Exception:  # noqa: BLE001
                continue
        for pid in now:
            if pid not in seen:
                seen[pid] = True
                _STATE["chrome_pid"] = pid
                ev("chrome_main.first_seen", pid=pid)
        for pid in list(seen):
            if pid not in now:
                ev("chrome_main.gone", pid=pid)
                del seen[pid]
        time.sleep(0.25)
    ev("chrome_main.final", alive_pids=sorted(seen))


def install(arm):
    sys.path.insert(0, PIN)
    os.chdir(PIN)
    from playwright.sync_api import Browser, BrowserContext, BrowserType, Page
    from lib.opal_data_harvest import tab_transport, transport, verification

    orig_launch = BrowserType.launch_persistent_context

    def launch(self, *a, **k):
        ev("launch_persistent_context.begin", user_data_dir=str(k.get("user_data_dir") or (a[0] if a else ""))[-60:], headless=k.get("headless"))
        ctx = orig_launch(self, *a, **k)
        ev("launch_persistent_context.returned")
        attach_context(ctx)
        return ctx

    BrowserType.launch_persistent_context = launch

    for cls, name in ((Page, "Page.close"), (BrowserContext, "BrowserContext.close"), (Browser, "Browser.close")):
        orig = getattr(cls, "close")

        def make(orig, name):
            def wrapped(self, *a, **k):
                ev("RUNNER_CLOSE_CALL", target=name, stack=pin_stack())
                return orig(self, *a, **k)
            return wrapped

        setattr(cls, "close", make(orig, name))

    orig_tab_close = tab_transport.TabSession.close

    def tab_close(self):
        ev("RUNNER_CLOSE_CALL", target="TabSession.close", stack=pin_stack())
        return orig_tab_close(self)

    tab_transport.TabSession.close = tab_close

    def minimize_logged(self):
        ev("minimize.begin")
        try:
            cdp = self.context.new_cdp_session(self.page)
            ev("minimize.cdp_session_ok")
            window = cdp.send("Browser.getWindowForTarget")
            ev("minimize.getWindowForTarget_ok", window_id=window.get("windowId"))
            cdp.send("Browser.setWindowBounds", {"windowId": window["windowId"], "bounds": {"windowState": "minimized"}})
            ev("minimize.setWindowBounds_returned")
        except Exception as exc:  # noqa: BLE001 -- the pin swallows every failure here too
            ev("minimize.error_swallowed", error=repr(exc)[:200])
        ev("minimize.end")

    tab_transport.TabSession._minimize_window = minimize_logged

    if arm == "B":
        orig_init = tab_transport.TabSession.__init__

        def init_b(self, publisher, profile_root, origin, headless=False, minimize=True):
            ev("TabSession.__init__", minimize_forced_to=False, minimize_passed_in=minimize)
            return orig_init(self, publisher, profile_root, origin, headless=headless, minimize=False)

        tab_transport.TabSession.__init__ = init_b
    else:
        orig_init = tab_transport.TabSession.__init__

        def init_a(self, publisher, profile_root, origin, headless=False, minimize=True):
            ev("TabSession.__init__", minimize=minimize)
            return orig_init(self, publisher, profile_root, origin, headless=headless, minimize=minimize)

        tab_transport.TabSession.__init__ = init_a

    def wrap(obj, attr, label):
        orig = getattr(obj, attr)

        def wrapped(*a, **k):
            ev(label + ".enter")
            try:
                out = orig(*a, **k)
            except BaseException as exc:  # noqa: BLE001
                ev(label + ".raised", error=repr(exc)[:300], tb=traceback.format_exc(limit=8)[-1500:])
                raise
            ev(label + ".exit")
            return out
        setattr(obj, attr, wrapped)

    wrap(transport.PacedSession, "_solve_challenge", "PacedSession._solve_challenge")
    wrap(verification, "route_bot_check", "verification.route_bot_check")
    wrap(verification, "solve", "verification.solve")

    orig_box = verification._press_and_hold_box

    def box(page):
        closed_before = None
        try:
            closed_before = page.is_closed()
        except Exception as exc:  # noqa: BLE001
            closed_before = "is_closed raised %r" % (exc,)
        ev("press_and_hold_box.enter", page_is_closed=closed_before)
        try:
            out = orig_box(page)
        except BaseException as exc:  # noqa: BLE001
            ev("press_and_hold_box.raised", error=repr(exc)[:300], tb=traceback.format_exc(limit=8)[-1500:])
            raise
        ev("press_and_hold_box.exit", found=out is not None, box=out)
        if out is not None:
            _STATE["press_box_seen"] = True
            if not _STATE.get("through_hold"):
                raise HarnessStop("control found with the page alive; stopping BEFORE any hold")
        return out

    verification._press_and_hold_box = box

    if _STATE.get("through_hold"):
        # Arms A' and B' (issuer msg 6866): the job goes THROUGH the hold exactly as the runner's does. The hold library and the
        # DOM capture are wrapped for timing and for the page's state before and after; nothing about their behaviour changes.
        from lib.opal_data_harvest import challenge_capture, publishers
        sys.path.insert(0, str(publishers.SCRIPTS))
        import press_and_hold_lib

        def page_state(page):
            try:
                return {"is_closed": page.is_closed(), "url": str(page.url)[:100]}
            except Exception as exc:  # noqa: BLE001
                return {"state_error": repr(exc)[:120]}

        orig_hold = press_and_hold_lib.press_and_hold_adaptive

        def hold(page, x, y, bbox, log, *a, **k):
            ev("HOLD.enter", x=round(x), y=round(y), state=page_state(page), kwargs={kk: vv for kk, vv in k.items() if isinstance(vv, (int, float, bool))})
            try:
                out = orig_hold(page, x, y, bbox, log, *a, **k)
            except BaseException as exc:  # noqa: BLE001
                ev("HOLD.raised", error=repr(exc)[:300], state=page_state(page), tb=traceback.format_exc(limit=6)[-1200:])
                raise
            ev("HOLD.exit", state=page_state(page))
            return out

        press_and_hold_lib.press_and_hold_adaptive = hold
        orig_cap = challenge_capture.capture_page

        def cap(*a, **k):
            ev("capture_page.enter")
            try:
                out = orig_cap(*a, **k)
            except BaseException as exc:  # noqa: BLE001
                ev("capture_page.raised", error=repr(exc)[:300])
                raise
            ev("capture_page.exit")
            return out

        challenge_capture.capture_page = cap
        orig_solve_hold = verification._solve_press_and_hold

        def solve_hold(page, *a, **k):
            ev("_solve_press_and_hold.enter", state=page_state(page))
            try:
                out = orig_solve_hold(page, *a, **k)
            except BaseException as exc:  # noqa: BLE001
                ev("_solve_press_and_hold.raised", error=repr(exc)[:300], state=page_state(page), tb=traceback.format_exc(limit=8)[-1500:])
                raise
            ev("_solve_press_and_hold.exit", acted=out, state=page_state(page))
            return out

        verification._solve_press_and_hold = solve_hold

    # NO S3 WRITE OF ANY KIND (the order, step 1). The runner's own job persists its run record to the harvest bucket
    # (worker.Worker._persist_run_record, after the job result); Arm C ran WITHOUT this suppression and wrote one such
    # object (declared in cc4_trace.out and row D1-S34). From Arm A on, that persist is suppressed, and a backstop refuses any
    # AWS API call whose operation name is a write, recording it, so a second write path cannot be missed.
    from lib.opal_data_harvest import worker as worker_mod

    def persist_suppressed(self, run_id, started_at, record):
        ev("run_record_persist.SUPPRESSED", run_id=run_id)
        return None

    worker_mod.Worker._persist_run_record = persist_suppressed
    import botocore.client
    write_prefixes = ("Put", "Delete", "Create", "Update", "Copy", "Upload", "Complete", "Restore", "Write", "Send", "Publish", "Invoke", "Start")
    orig_call = botocore.client.BaseClient._make_api_call

    def guarded_call(self, operation_name, api_params):
        if operation_name.startswith(write_prefixes):
            ev("AWS_WRITE_BLOCKED", operation=operation_name, bucket=str((api_params or {}).get("Bucket")), key=str((api_params or {}).get("Key"))[:120])
            raise RuntimeError("cc4 harness blocks the AWS write call %s" % operation_name)
        return orig_call(self, operation_name, api_params)

    botocore.client.BaseClient._make_api_call = guarded_call
    return tab_transport


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=("A", "B", "C"))
    ap.add_argument("--security-json", required=True)
    ap.add_argument("--runtime-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--floor", default="2026-10-15")
    ap.add_argument("--watchdog-s", type=int, default=420)
    ap.add_argument("--through-hold", action="store_true", help="Arms A' and B': do not stop before the hold; the job runs through it as the runner's does")
    args = ap.parse_args()
    _STATE["through_hold"] = args.through_hold
    # install() changes the working directory to the pin, so every path given on the command line is made absolute first.
    args.out = str(Path(args.out).resolve())
    args.security_json = str(Path(args.security_json).resolve())
    args.runtime_root = str(Path(args.runtime_root).resolve())
    _OUT["path"] = args.out
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    open(args.out, "w", encoding="ascii").close()
    ev("harness.begin", arm=args.arm, python=sys.version.split()[0], profile_root_env=os.environ.get("OPAL_HARVEST_PROFILE_ROOT"),
       runtime_root=args.runtime_root, security=Path(args.security_json).name, floor=args.floor)
    watchdog = threading.Timer(args.watchdog_s, lambda: (ev("WATCHDOG_EXIT", after_s=args.watchdog_s), os._exit(3)))
    watchdog.daemon = True
    watchdog.start()
    stop = threading.Event()
    poller = threading.Thread(target=poll_chrome, args=(stop,), name="chrome-poller", daemon=True)
    poller.start()
    install(args.arm)
    from lib.opal_data_harvest import __main__ as cli
    sys.argv = ["lib.opal_data_harvest", "--runtime-root", args.runtime_root, "run", "--harvest-grammar", "--retrieval-mode", "backfill",
                "--floor", args.floor, "--new-only", "--no-sign-in", "--security-json", args.security_json, "--publishers", "bbg",
                "--max-jobs", "1"]
    ev("cli.main.begin", argv=sys.argv[1:])
    rc = None
    try:
        rc = cli.main()
    except SystemExit as exc:
        rc = exc.code
    except BaseException as exc:  # noqa: BLE001
        ev("cli.main.raised", error=repr(exc)[:300], tb=traceback.format_exc(limit=8)[-1500:])
        rc = "raised"
    ev("cli.main.end", rc=rc, press_box_seen=_STATE["press_box_seen"])
    time.sleep(1.0)
    stop.set()
    poller.join(timeout=3)
    ev("harness.end")
    os._exit(0)


if __name__ == "__main__":
    main()
