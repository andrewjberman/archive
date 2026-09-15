"""Shared PerimeterX-style 'Press & Hold' defeat mechanism -- factored out of sa_harvest_session.py
2026-09-11 so a second site (Bloomberg.com) can reuse it without duplicating hard-won logic or
importing sa_harvest_session.py itself (which runs a full SA login as a MODULE-LEVEL side effect at
import time, making it unsafe to import as a library).

Pure, side-effect-free functions; the caller supplies its own `log(str)` callable so this module has
no logging convention of its own to conflict with a caller's.

ROE: never logs a credential/cookie/token value (this module never sees one).
"""
import io
import random
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

_CENTER_LO, _CENTER_HI = 10, 22  # middle ~37.5% of a 32x32 grid


def press_and_hold(page, x, y, hold_s, log):
    # FIX (live human observation, 2026-09-10): the PerimeterX widget's fill bar DE-FILLS if held
    # too long -- there is a target window, not "longer is safer". Also adds small in-hold jitter:
    # a perfectly stationary press for several seconds is itself a bot signature real vendors check
    # for.
    log(f"press-and-hold at ({x},{y}) for {hold_s}s (with jitter)")
    page.mouse.move(x, y, steps=12)
    time.sleep(0.3)
    page.mouse.down()
    elapsed = 0.0
    step = 0.25
    while elapsed < hold_s:
        time.sleep(step)
        elapsed += step
        jx = x + random.uniform(-1.5, 1.5)
        jy = y + random.uniform(-1.5, 1.5)
        page.mouse.move(jx, jy, steps=1)
    page.mouse.up()


def _crop_scores(page, bbox, baseline_full, baseline_center):
    """Cheap LOCAL pixel-diff signals -- NO Kimi/vision call. Returns (whole_score, center_score):
    mean absolute grayscale difference of the current crop vs. the pre-press baseline, over the
    WHOLE widget and over just its CENTER sub-region. whole_score tracks the fill bar/ring sweeping
    in; center_score is scoped to where a checkmark icon appears -- Andrew-direct 2026-09-10, after
    manually completing a run himself: 'its not enough to wait until the black bar is filled, a
    check mark will appear in the center of the bar, that is the true marker.' A checkmark is a
    small, SUDDEN, localized event, shaped very differently from the bar's smoother, wider fill
    sweep -- whole_score alone can plateau on the sweep whether or not a checkmark ever appears, so
    it needs its own spatially-scoped signal."""
    png = page.screenshot(clip=bbox, timeout=3000)
    px = list(Image.open(io.BytesIO(png)).convert("L").resize((32, 32)).getdata())
    whole = sum(abs(a - b) for a, b in zip(px, baseline_full)) / len(px)
    center_idx = [yy * 32 + xx for yy in range(_CENTER_LO, _CENTER_HI) for xx in range(_CENTER_LO, _CENTER_HI)]
    center_px = [px[i] for i in center_idx]
    center = sum(abs(a - b) for a, b in zip(center_px, baseline_center)) / len(center_px)
    return whole, center


def press_and_hold_adaptive(page, x, y, bbox, log, max_hold_s=8.0, poll_interval=0.15,
                            trace_dir=None, release_on_pixel_peak=True):
    """Andrew-direct 2026-09-10: Kimi is far too slow (10-20s/call, measured) to close this loop --
    the fill/checkmark/de-fill animation runs in a few seconds -- so Kimi's (or a site's DOM's) role
    stops at LOCATING the button; release timing is a purely LOCAL, fast pixel-diff loop with zero
    network calls during the hold. PRIMARY release trigger is a sudden, sharp jump in the
    CENTER-region signal -- the checkmark appearing, per Andrew's direct ground-truth correction
    after manually finishing a run and watching it happen. FALLBACK trigger (if no such spike is
    ever seen) is the whole-crop fill signal peaking, as before -- kept so a checkmark too small/
    subtle for a 32x32 crop to resolve does not strand the hold forever.

    PROVEN LIVE 2026-09-11 against Seeking Alpha's real PerimeterX widget (three real attempts: two
    hit the max_hold_s safety net with the fill delta still climbing -- released anyway, no
    fabricated peak -- and the third genuinely peaked at 4.12s and released right there)."""
    if Image is None or bbox is None:
        log("adaptive press-and-hold unavailable (no PIL or no bbox) -- falling back to a fixed hold")
        press_and_hold(page, x, y, random.uniform(1.8, 3.2), log)
        return
    try:
        baseline_png = page.screenshot(clip=bbox, timeout=3000)
        baseline_full = list(Image.open(io.BytesIO(baseline_png)).convert("L").resize((32, 32)).getdata())
        center_idx = [yy * 32 + xx for yy in range(_CENTER_LO, _CENTER_HI) for xx in range(_CENTER_LO, _CENTER_HI)]
        baseline_center = [baseline_full[i] for i in center_idx]
    except Exception as e:
        log(f"adaptive press-and-hold: baseline crop failed {type(e).__name__} -- falling back to a fixed hold")
        press_and_hold(page, x, y, random.uniform(1.8, 3.2), log)
        return
    mode = "pixel-peak release" if release_on_pixel_peak else "drain -> release -> partial fall -> re-press"
    log(f"adaptive press-and-hold at ({x:.0f},{y:.0f}) -- {mode}")
    page.mouse.move(x, y, steps=12)
    time.sleep(0.2)
    page.mouse.down()
    is_pressed = True
    whole_scores, center_scores = [], []
    started = time.monotonic()
    trace_path = Path(trace_dir) if trace_dir else None
    if trace_path:
        trace_path.mkdir(parents=True, exist_ok=True)
    trace_index = 0
    recoveries = 0
    MAX_RECOVERIES = 4
    try:
        while time.monotonic() - started < max_hold_s:
            time.sleep(poll_interval)
            if is_pressed:
                page.mouse.move(x + random.uniform(-1.0, 1.0), y + random.uniform(-1.0, 1.0), steps=1)
            try:
                w, c = _crop_scores(page, bbox, baseline_full, baseline_center)
            except Exception:
                continue
            whole_scores.append(w)
            center_scores.append(c)
            elapsed = time.monotonic() - started
            if trace_path:
                page.screenshot(path=str(trace_path / f"widget-{trace_index:03d}.png"), clip=bbox, timeout=3000)
                with (trace_path / "pixels.csv").open("a", encoding="utf-8") as fh:
                    fh.write(f"{trace_index},{elapsed:.3f},{w:.3f},{c:.3f}\n")
                trace_index += 1
            if release_on_pixel_peak and len(center_scores) >= 2 and center_scores[-1] > 18 and center_scores[-1] > center_scores[-2] * 1.4:
                log(f"CHECKMARK signal: center delta jumped {center_scores[-2]:.1f} -> {center_scores[-1]:.1f} "
                    f"after {elapsed:.2f}s -- releasing")
                page.mouse.up()
                is_pressed = False
                break
            # Andrew-direct 2026-09-11: "there are some cases where even as you hold it, they start
            # pushing the black bar all the way back to 0. the key if you see the black bar
            # diminishing is you have to let go of the pressing for a beat or two and then press
            # again, holding until you see the check mark." This is DIFFERENT from a natural peak/
            # plateau (the fallback signal below) -- a SHARP drop (losing >30% of the fill signal in
            # one poll) while still holding means the widget is actively being drained, and the
            # right response is to physically release, pause, and re-press -- not just pick a
            # different moment to release once. Capped at MAX_RECOVERIES so a widget that drains
            # forever doesn't hold the process hostage.
            recent_peak = max(whole_scores[-8:])
            if is_pressed and len(whole_scores) >= 3 and recent_peak > 15 \
                    and whole_scores[-1] < recent_peak * (0.85 if trace_path else 0.7) and recoveries < MAX_RECOVERIES:
                recoveries += 1
                log(f"DRAIN signal: whole-bar delta fell from recent peak {recent_peak:.1f} -> {whole_scores[-1]:.1f} "
                    f"after {elapsed:.2f}s -- releasing for a beat, then pressing again "
                    f"(recovery {recoveries}/{MAX_RECOVERIES})")
                page.mouse.up()
                is_pressed = False
                time.sleep(random.uniform(0.4, 0.8))
                if trace_path:
                    # Andrew's live Bloomberg correction: allow a visible partial fall
                    # while released before pressing again. Preserve the original
                    # baseline until that fall is measured, then reset for the new hold.
                    release_score = whole_scores[-1]
                    for pause_index in range(8):
                        try:
                            released_w, _ = _crop_scores(page, bbox, baseline_full, baseline_center)
                            page.screenshot(path=str(trace_path / f"release-{recoveries}-{pause_index}.png"),
                                            clip=bbox, timeout=3000)
                            if released_w < release_score * 0.85:
                                log(f"PARTIAL FALL while released: {release_score:.1f} -> {released_w:.1f}; re-pressing")
                                break
                        except Exception:
                            break
                        time.sleep(poll_interval)
                    else:
                        log("release pause bounded out without a measured partial fall; re-pressing for next observation")
                try:
                    baseline_png = page.screenshot(clip=bbox, timeout=3000)
                    baseline_full = list(Image.open(io.BytesIO(baseline_png)).convert("L").resize((32, 32)).getdata())
                    baseline_center = [baseline_full[i] for i in center_idx]
                except Exception:
                    pass  # keep the old baseline rather than abort -- still better than nothing
                page.mouse.move(x, y, steps=8)
                page.mouse.down()
                is_pressed = True
                whole_scores, center_scores = [], []  # reset series against the fresh baseline
                continue
            if release_on_pixel_peak and is_pressed and len(whole_scores) >= 3 and whole_scores[-1] <= whole_scores[-2] and whole_scores[-2] >= whole_scores[-3]:
                log(f"fallback signal: whole-bar delta peaked at {whole_scores[-2]:.1f} after {elapsed:.2f}s "
                    f"(no checkmark spike seen) -- releasing")
                break
        else:
            log(f"adaptive press-and-hold: no checkmark or peak detected within {max_hold_s}s "
                f"(whole tail={whole_scores[-5:]}, center tail={center_scores[-5:]}, recoveries={recoveries}) -- releasing anyway")
    finally:
        if is_pressed:
            page.mouse.up()
