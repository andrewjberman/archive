"""CA-n-1 AC1: an @mention of Andrew posted as a REPLY inside an older channel thread becomes one event.

The blind spot (2026-10-16, CTO ruling on call 446a): the channel poller reads the newest pages of top-level posts and the
replies embedded in them, and stops at the first page with nothing newer than its cursor. A reply under an older post (the
End of Day Updates channel keeps one parent post that everyone replies under) is never read, so Alyssa Keith's real
@mention was never seen. The fix reads the replies of a bounded set of THREADS per channel through the gateway's replies
route: the pinned End of Day parent, and every post with activity in the last THREAD_DAYS days.

PASS needs all eight arms, against data/transcripts/scripts/teams_chat/channel_mentions.py as the repository holds it:
  1. pinned_eod_reply   a reply that mentions Andrew under the End of Day parent (a.EOD_PARENT_ID in a.EOD_TEAM_ID /
                        a.EOD_CHANNEL_ID), which is on no page the poller reads, becomes ONE event, oid
                        "chan:<team>|<channel>|<parent>", event id "mention-<reply id>", kind teams.channel_mention;
  2. recent_root_reply  a post created within THREAD_DAYS, seen on page 1 with NO embedded replies, gets a reply that
                        mentions Andrew which only the replies route returns: ONE event for it;
  3. first_read_silent  the first read of a thread sends nothing, even when a reply in it already mentions Andrew;
  4. no_repeat          a later poll with no new reply sends nothing more;
  5. not_him            replies that mention someone else, mention nobody, come from Andrew himself or are deleted send
                        nothing; the difference control (the same reply with his id added) sends one;
  6. stale_dropped      a post whose newest activity is older than THREAD_DAYS is not read through the replies route
                        (no replies call for it); the pinned parent is read whatever its age;
  7. budget             one poll over many channels and threads makes at most cm.MAX_CALLS gateway calls;
  8. thread_failure_isolated  a thread whose replies call keeps failing costs only that thread: the channel's new top-level
                        mention is still sent once and its cursor still moves.
Prints one line per arm and N1-THREADS ok=True|False arms=<passed> of 8.
Finds the repository from the current directory's git toplevel, never from this file's location; the seam N1_ROOT points
it at another copy (a scratch reference). No network, no AWS: the gateway, store, ldo.send and text sender are injected.
"""
import copy
import datetime
import os
import subprocess
import sys

ROOT = os.environ.get("N1_ROOT") or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                                   text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "terraform", "modules", "ldo", "runtime"))
from data.transcripts.scripts.teams_chat import assist as a  # noqa: E402
from data.transcripts.scripts.teams_chat import channel_mentions as cm  # noqa: E402

ME = "u-me"
T0 = datetime.datetime(2026, 10, 16, 12, 0, 0, tzinfo=a.UTC)
OLD = "2026-08-07T13:00:00Z"            # the End of Day parent's own age
RECENT = "2026-10-15T09:00:00Z"         # a day old: inside any THREAD_DAYS
STALE = "2026-09-01T09:00:00Z"          # 45 days old: outside a 14-day window
EOD = (a.EOD_TEAM_ID, a.EOD_CHANNEL_ID, a.EOD_PARENT_ID)


def at(seconds):
    return T0 + datetime.timedelta(seconds=seconds)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def msg(mid, created, who="u-other", mentions=(), deleted=False, replies=None):
    m = {"id": mid, "created": created, "last_modified": created, "from_name": "Sender One", "from_user_id": who,
         "from_app": None, "reply_to_id": None, "message_type": "message", "deleted": deleted,
         "body_html": "<p>hello</p>", "attachments": [], "mentions": [{"user_id": u, "name": "N"} for u in mentions]}
    if replies is not None:
        m["replies"] = replies
    return m


class FakeGW:
    """teams: {team: [channel, ...]}; posts: {(team, channel): [roots newest first]}; thread: {(team, channel, root):
    [replies newest first]}. per_page splits a channel's roots into pages. Every call is counted."""

    def __init__(self, teams, per_page=50):
        self.teams_map, self.posts, self.thread, self.per_page = teams, {}, {}, per_page
        self.calls, self.reply_reads = 0, []

    def teams(self, page_token=None, page_size=50):
        self.calls += 1
        return {"rows": [{"team_id": t, "display_name": "Team " + t} for t in self.teams_map], "next_page_token": None}

    def channels(self, team_id, page_token=None, page_size=50):
        self.calls += 1
        return {"rows": [{"channel_id": c, "display_name": "Chan " + c} for c in self.teams_map[team_id]],
                "next_page_token": None}

    def channel_messages(self, team_id, channel_id, page_token=None, page_size=50):
        self.calls += 1
        rows = self.posts.get((team_id, channel_id), [])
        start = int(page_token or 0)
        nxt = str(start + self.per_page) if start + self.per_page < len(rows) else None
        return {"rows": copy.deepcopy(rows[start:start + self.per_page]), "next_page_token": nxt}

    def replies(self, team_id, channel_id, message_id, page_token=None, page_size=50):
        self.calls += 1
        self.reply_reads.append(message_id)
        if message_id in getattr(self, "fail_threads", ()):
            raise a.GatewayError(404, "gone", "replies")
        return {"rows": copy.deepcopy(self.thread.get((team_id, channel_id, message_id), [])), "next_page_token": None}


class World:
    def __init__(self):
        self.store, self.events = {}, []
        a.get_json = lambda key, default=None: copy.deepcopy(self.store.get(key, default))
        a.put_json = lambda key, obj: self.store.__setitem__(key, copy.deepcopy(obj))
        a.assistant_on = lambda: True
        a.send_sms = lambda text, tag: ["m"]
        a.log = lambda event, **kw: None
        cm.ldo.send = lambda oid, kind, payload=None, event_id=None: self.events.append((oid, kind, payload, event_id))


def eod_world(per_page=1):
    """The End of Day channel: a newer post on page 1, the parent nowhere on the pages the poller reads."""
    w, gw = World(), FakeGW({EOD[0]: [EOD[1]]}, per_page=per_page)
    gw.posts[(EOD[0], EOD[1])] = [msg("bot1", iso(T0 - datetime.timedelta(days=11))),
                                  msg("bot0", iso(T0 - datetime.timedelta(days=12)))]
    gw.thread[EOD] = [msg("e0", RECENT)]
    return w, gw


def arm_pinned_eod_reply():
    w, gw = eod_world()
    cm.poll(gw, ME, T0)
    gw.thread[EOD] = [msg("e1", iso(at(200)), mentions=[ME]), msg("e0", RECENT)]
    cm.poll(gw, ME, at(300))
    hits = [e for e in w.events if e[3] == "mention-e1"]
    return (len(w.events) == 1 and len(hits) == 1 and hits[0][0] == "chan:%s|%s|%s" % EOD
            and hits[0][1] == "teams.channel_mention" and hits[0][2]["message"]["id"] == "e1")


def arm_recent_root_reply():
    w, gw = World(), FakeGW({"t1": ["c1"]})
    gw.posts[("t1", "c1")] = [msg("p1", RECENT, replies=[])]
    gw.thread[("t1", "c1", "p1")] = []
    cm.poll(gw, ME, T0)
    cm.poll(gw, ME, at(300))                      # the thread is now known and read once with nothing in it
    gw.thread[("t1", "c1", "p1")] = [msg("r1", iso(at(500)), mentions=[ME])]
    cm.poll(gw, ME, at(600))
    return len(w.events) == 1 and w.events[0][3] == "mention-r1" and w.events[0][0] == "chan:t1|c1|p1"


def arm_first_read_silent():
    w, gw = eod_world()
    gw.thread[EOD] = [msg("e5", RECENT, mentions=[ME])]
    cm.poll(gw, ME, T0)
    cm.poll(gw, ME, at(300))
    return len(w.events) == 0 and EOD[2] in gw.reply_reads


def arm_no_repeat():
    w, gw = eod_world()
    cm.poll(gw, ME, T0)
    gw.thread[EOD] = [msg("e1", iso(at(200)), mentions=[ME]), msg("e0", RECENT)]
    cm.poll(gw, ME, at(300))
    cm.poll(gw, ME, at(600))
    cm.poll(gw, ME, at(900))
    return len(w.events) == 1


def arm_not_him():
    w, gw = eod_world()
    cm.poll(gw, ME, T0)
    gw.thread[EOD] = [msg("n1", iso(at(250)), mentions=["u-someone"]), msg("n2", iso(at(240))),
                      msg("n3", iso(at(230)), who=ME, mentions=[ME]),
                      msg("n4", iso(at(220)), mentions=[ME], deleted=True), msg("e0", RECENT)]
    cm.poll(gw, ME, at(300))
    none_sent = len(w.events) == 0
    w2, gw2 = eod_world()
    cm.poll(gw2, ME, T0)
    gw2.thread[EOD] = [msg("n1", iso(at(250)), mentions=["u-someone", ME]), msg("e0", RECENT)]
    cm.poll(gw2, ME, at(300))
    return none_sent and len(w2.events) == 1 and w2.events[0][3] == "mention-n1"


def arm_stale_dropped():
    w, gw = World(), FakeGW({"t1": ["c1"]})
    gw.posts[("t1", "c1")] = [msg("old1", STALE, replies=[msg("old1r", STALE)])]
    gw.thread[("t1", "c1", "old1")] = [msg("x1", iso(at(500)), mentions=[ME])]
    cm.poll(gw, ME, T0)
    cm.poll(gw, ME, at(300))
    cm.poll(gw, ME, at(600))
    stale_ok = "old1" not in gw.reply_reads and len(w.events) == 0
    w2, gw2 = eod_world()                          # the pinned parent is read although it is 70 days old
    cm.poll(gw2, ME, T0)
    cm.poll(gw2, ME, at(300))
    return stale_ok and EOD[2] in gw2.reply_reads


def arm_budget():
    World()
    teams = {"t%d" % i: ["c%d" % j for j in range(4)] for i in range(4)}
    teams[EOD[0]] = [EOD[1]]
    gw = FakeGW(teams)
    for t, cs in teams.items():
        for c in cs:
            gw.posts[(t, c)] = [msg("%s-%s-%d" % (t, c, k), RECENT, replies=[]) for k in range(12)]
            for k in range(12):
                gw.thread[(t, c, "%s-%s-%d" % (t, c, k))] = [msg("rr-%s-%s-%d" % (t, c, k), RECENT)]
    gw.thread[EOD] = [msg("e0", RECENT)]
    worst = 0
    for n in range(6):
        before = gw.calls
        cm.poll(gw, ME, at(300 * n))
        worst = max(worst, gw.calls - before)
    return worst <= cm.MAX_CALLS


def _poll_quiet(gw, now):
    """A poll that met a failed gateway call raises RuntimeError after saving its cursors; the arm reads the effects."""
    try:
        cm.poll(gw, ME, now)
    except RuntimeError:
        pass


def arm_thread_failure_isolated():
    """A thread whose replies call keeps failing (a deleted post: 404) costs only that thread: the channel's own new
    top-level mention is still sent once, and the channel's cursor still moves (no repeat on the next poll)."""
    w, gw = eod_world()
    cm.poll(gw, ME, T0)
    gw.fail_threads = {EOD[2]}
    gw.posts[(EOD[0], EOD[1])] = [msg("top1", iso(at(250)), mentions=[ME])] + gw.posts[(EOD[0], EOD[1])]
    _poll_quiet(gw, at(300))
    _poll_quiet(gw, at(600))
    return len(w.events) == 1 and w.events[0][3] == "mention-top1"


ARMS = [("pinned_eod_reply", arm_pinned_eod_reply), ("recent_root_reply", arm_recent_root_reply),
        ("first_read_silent", arm_first_read_silent), ("no_repeat", arm_no_repeat), ("not_him", arm_not_him),
        ("stale_dropped", arm_stale_dropped), ("budget", arm_budget),
        ("thread_failure_isolated", arm_thread_failure_isolated)]


def main():
    passed = 0
    for name, fn in ARMS:
        try:
            ok = bool(fn())
        except Exception as exc:  # an arm that raises has failed; say which and why
            print("ARM %s raised %s: %s" % (name, type(exc).__name__, str(exc)[:200]))
            ok = False
        print("ARM %s ok=%s" % (name, ok))
        passed += ok
    allok = passed == len(ARMS)
    print("N1-THREADS ok=%s arms=%d of %d" % (allok, passed, len(ARMS)))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
