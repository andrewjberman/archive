"""COMM_ASSIST round 13, criterion CAe3-AC1 (issuer's check; the worker reads it and never edits it).

A failing channel_poll step must (1) carry the failing call's error in its own `channel_poll` log line, as a non-empty `error`
field, and (2) raise, so the ingress's step wrapper `tenant._safe` logs `ingress_step_failed` with step=channels.
Control: a healthy poll (the gateway answers, no channels) logs `channel_poll` with failed=0 and raises nothing.
A plain script, no network: the gateway, the state store and the log are injected.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r13/checks/check_e3_channel_poll_escalates.py

LAST line: `E3-ESCALATES ok=<True|False>`. At the base the failure is only counted, so it prints ok=False.
"""
import copy
import datetime
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 9)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "terraform", "modules", "ldo", "runtime"))
from data.transcripts.scripts.teams_chat import assist as a  # noqa: E402
from data.transcripts.scripts.teams_chat import channel_mentions as cm  # noqa: E402
from data.transcripts.scripts.teams_chat import tenant  # noqa: E402

NOW = datetime.datetime(2026, 10, 10, 12, 0, 0, tzinfo=a.UTC)


class FailingGW:
    def teams(self, page_token=None, page_size=50):
        raise a.GatewayError(404, "route not found", "teams")

    def channels(self, team_id, page_token=None, page_size=50):
        raise a.GatewayError(404, "route not found", "channels")

    def channel_messages(self, team_id, channel_id, page_token=None, page_size=50):
        raise a.GatewayError(404, "route not found", "channel_messages")


class HealthyGW:
    def teams(self, page_token=None, page_size=50):
        return {"rows": [], "count": 0, "next_page_token": None}

    def channels(self, team_id, page_token=None, page_size=50):
        return {"rows": [], "count": 0, "next_page_token": None}

    def channel_messages(self, team_id, channel_id, page_token=None, page_size=50):
        return {"rows": [], "count": 0, "next_page_token": None}


def run(gw):
    store, logs = {}, []
    a.get_json = lambda key, default=None: copy.deepcopy(store.get(key, default))
    a.put_json = lambda key, obj: store.__setitem__(key, copy.deepcopy(obj))
    a.log = lambda event, **kw: logs.append((event, kw))
    cm.ldo.send = lambda *args, **kw: None
    result = tenant._safe("channels", lambda: cm.poll(gw, "u-me", NOW))
    return result, logs


def main():
    result, logs = run(FailingGW())
    polls = [kw for ev, kw in logs if ev == "channel_poll"]
    steps = [kw for ev, kw in logs if ev == "ingress_step_failed" and kw.get("step") == "channels"]
    err_ok = bool(polls) and bool(str(polls[-1].get("error") or "").strip())
    raise_ok = bool(steps) and result == "failed"
    print("ARM failing channel_poll_lines=%d error_field=%r ingress_step_failed=%d ok=%s"
          % (len(polls), (polls[-1].get("error") if polls else None), len(steps), err_ok and raise_ok))
    result, logs = run(HealthyGW())
    polls = [kw for ev, kw in logs if ev == "channel_poll"]
    steps = [kw for ev, kw in logs if ev == "ingress_step_failed"]
    ctl_ok = bool(polls) and polls[-1].get("failed") == 0 and not steps and result != "failed"
    print("ARM control_healthy failed=%r ingress_step_failed=%d ok=%s"
          % ((polls[-1].get("failed") if polls else None), len(steps), ctl_ok))
    print("E3-ESCALATES ok=%s" % (err_ok and raise_ok and ctl_ok))


if __name__ == "__main__":
    main()
