"""CA-l-3: three Teams-chat test files collect and pass ALONE from the repo root (the bare sibling import is repaired, as CA-k-3 did for test_teams_chat_natural.py).

Prints:  M3-BATCH ok=<True|False> arms=<k> of <n>     then one `FAIL <arm>: <reason>` line per failed arm (and `SKIP <arm>: <reason>` for a skipped one).
Run from the ROOT of the checkout under test, by relative path:
    python "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r20/checks/check_m3_batch.py"
The repo is `git rev-parse --show-toplevel` of the CURRENT WORKING DIRECTORY (never this file's location); when the cwd is not a git repo the cwd itself is
the root (a plain mirror directory), and the no_product_change arm is skipped and says so. Reads no AWS; writes nothing (no bytecode, no pytest cache).

Arms (n is 6, or 5 when no_product_change is skipped):
  alone:test_teams_chat_jobs / alone:test_teams_chat_eod_republish / alone:test_teams_chat_stale_eod
      `python -m pytest <file> -q` run ALONE from the root: exit 0, no failed/error, passed >= the number of recorded test names.
  combined: the three plus test_teams_chat_tenant.py and test_teams_chat_natural.py in ONE pytest run: exit 0, no failed/error.
  no_product_change: `git diff --name-only <merge-base HEAD box/laptop> -- data infra .tools` names nothing but the three test files.
  names: each of the three files still defines every test function recorded below from the base files (a deleted test fails here).
Expected on the reference (3 files repaired): alone 14 / 12 / 14 passed, combined 112 passed (the base: every alone arm and the combined arm fail at collection).
"""
import os
import re
import subprocess
import sys

TESTS = "data/transcripts/scripts/tests"
FILES = ("test_teams_chat_jobs", "test_teams_chat_eod_republish", "test_teams_chat_stale_eod")
SIBLINGS = ("test_teams_chat_tenant", "test_teams_chat_natural")
RECORDED = {   # the `def test_` names of the three files at the base (merge-base d6605d65cd), 11 + 12 + 13
    "test_teams_chat_jobs": (
        "test_dev_on_a_chat_opens_a_job_and_drops_the_draft", "test_open_offers_to_every_device_and_sets_the_award_alarm",
        "test_both_bids_award_at_once_to_the_lighter_box", "test_one_bid_wins_at_the_alarm_and_none_parks",
        "test_accept_says_im_on_it_in_the_chat", "test_complete_texts_a_draft_for_the_requester_and_1_sends_it_to_the_chat",
        "test_requester_saying_it_works_closes_the_job", "test_confirm_sends_close_to_the_winner_and_clears_the_chat",
        "test_close_by_text", "test_parse_job_commands", "test_award_rule_ties_go_to_the_earlier_bid"),
    "test_teams_chat_eod_republish": (
        "test_the_draft_records_the_page_it_was_written_from", "test_a_republished_page_redrafts_and_texts_the_next_version",
        "test_the_same_page_changes_nothing", "test_an_approved_post_is_withdrawn_and_waits_for_a_new_1",
        "test_a_1_meant_for_the_old_version_does_not_post_the_new_one", "test_a_posted_or_dropped_day_is_left_alone",
        "test_paused_redrafts_nothing", "test_a_past_day_closes_quietly", "test_the_route_exists",
        "test_poll_queues_with_the_page_it_saw", "test_poll_sends_an_update_once_per_publish",
        "test_poll_is_quiet_when_the_page_has_not_moved"),
    "test_teams_chat_stale_eod": (
        "test_a_live_draft_for_a_past_day_is_never_made", "test_the_draft_sets_its_own_midnight_expiry",
        "test_a_send_or_redraft_the_next_day_is_refused_and_closes_it", "test_a_drop_the_next_day_still_drops",
        "test_an_approved_post_whose_alarm_fires_after_midnight_does_not_post", "test_the_midnight_alarm_closes_it_quietly",
        "test_a_test_draft_takes_a_t_tag_and_never_posts", "test_an_update_three_days_back_on_page_two_is_found",
        "test_a_long_conversation_reply_is_not_the_update", "test_reading_stops_once_a_page_reaches_before_the_day",
        "test_a_thread_it_cannot_read_back_far_enough_refuses", "test_cannot_see_the_day_keeps_the_draft_and_posts_nothing",
        "test_each_text_is_recorded_with_its_route"),
}


def run(args, cwd, timeout=900):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)


def repo_root():
    try:
        r = run(["git", "rev-parse", "--show-toplevel"], os.getcwd(), 60)
        out = r.stdout.decode("utf-8", "replace").strip()
        if r.returncode == 0 and out:
            return out, True
    except (OSError, subprocess.SubprocessError):
        pass
    return os.getcwd(), False


def pytest_arm(root, files, expect_min):
    """Return an empty string when the run passed, else the reason."""
    for f in files:
        if not os.path.isfile(os.path.join(root, TESTS, f + ".py")):
            return "%s.py is missing" % f
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + ["%s/%s.py" % (TESTS, f) for f in files]
    try:
        r = run(cmd, root)
    except (OSError, subprocess.SubprocessError) as e:
        return "pytest did not run: %s" % e
    text = re.sub(r"\[[0-9;]*m", "", r.stdout.decode("utf-8", "replace"))   # a pytest plugin colours the output despite --color=no
    tail = [ln for ln in text.splitlines() if ln.strip()][-1:] or ["(no output)"]
    m = re.search(r"(\d+) passed", text)
    passed = int(m.group(1)) if m else 0
    if r.returncode != 0 or re.search(r"\d+ (failed|error)", tail[0]):
        err = [ln.strip() for ln in text.splitlines() if ln.startswith("E ")][:1]
        return "pytest rc=%d, %s%s" % (r.returncode, tail[0].strip("= "), (" | " + err[0]) if err else "")
    if passed < expect_min:
        return "only %d passed, expected at least %d" % (passed, expect_min)
    return ""


def names_arm(root):
    bad = []
    for f in FILES:
        try:
            with open(os.path.join(root, TESTS, f + ".py"), encoding="utf-8") as fh:
                have = set(re.findall(r"^\s*(?:async\s+)?def (test_\w+)", fh.read(), re.M))
        except OSError as e:
            bad.append("%s unreadable (%s)" % (f, e))
            continue
        gone = [n for n in RECORDED[f] if n not in have]
        if gone:
            bad.append("%s lost %s" % (f, ", ".join(gone)))
    return "; ".join(bad)


def product_arm(root):
    """Return a reason when something outside the three test files differs from the merge-base, else an empty string."""
    r = run(["git", "merge-base", "HEAD", "box/laptop"], root, 60)
    mb = r.stdout.decode("utf-8", "replace").strip()
    if r.returncode != 0 or not mb:
        return "no merge-base with box/laptop (rc=%d): %s" % (r.returncode, mb[:120])
    r = run(["git", "diff", "--name-only", mb, "--", "data", "infra", ".tools"], root, 120)
    if r.returncode != 0:
        return "git diff rc=%d" % r.returncode
    changed = [ln.strip() for ln in r.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]
    allowed = {"%s/%s.py" % (TESTS, f) for f in FILES}
    extra = [c for c in changed if c not in allowed]
    return ("differs from the merge-base: %s" % ", ".join(extra)) if extra else ""


def main():
    root, is_git = repo_root()
    results = []   # (arm, reason or "")
    skipped = []
    for f in FILES:
        results.append(("alone:" + f, pytest_arm(root, [f], len(RECORDED[f]))))
    results.append(("combined", pytest_arm(root, list(FILES) + list(SIBLINGS), sum(len(v) for v in RECORDED.values()))))
    if is_git:
        results.append(("no_product_change", product_arm(root)))
    else:
        skipped.append(("no_product_change", "cwd is not a git repo (mirror), no merge-base to diff"))
    results.append(("names", names_arm(root)))
    good = sum(1 for _, why in results if not why)
    print("M3-BATCH ok=%s arms=%d of %d" % (good == len(results), good, len(results)))
    for arm, why in results:
        if why:
            print("FAIL %s: %s" % (arm, why))
    for arm, why in skipped:
        print("SKIP %s: %s" % (arm, why))
    return 0 if good == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
