"""CA-i-6: the assistant's agentbus send path stamps from_tailnet with a name the device register holds.

Prints:  I6-STAMP ok=<True|False> stamp=<name|none> verdict=<deliver|refused|unstamped|none> control=<refused|...> reason=<text>
Drives assist.bus_send with a recording stand-in for the SQS client, then asks the agentbus consumer's own classify() (the same rule the
boxes apply) about the message the assistant sent, with the register read from this checkout. The control feeds classify() a message stamped
with a name the register does not hold: it must be refused. No AWS, no network.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))


def consumer():
    spec = importlib.util.spec_from_file_location("agentbus_consumer", ROOT / ".tools" / "agentbus-consumer.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    stamp, verdict, control, why = "none", "none", "none", ""
    try:
        from data.transcripts.scripts.teams_chat import assist as a
        sent = []

        class FakeSqs:
            def get_queue_url(self, QueueName):
                return {"QueueUrl": "https://sqs.example.invalid/000000000000/" + QueueName}

            def send_message(self, **kw):
                sent.append(kw)
                return {"MessageId": "m-1"}

        a.aws = lambda svc: FakeSqs()
        a._BUS_URLS.clear()
        device = sorted(a.DEVICES)[0]
        a.bus_send(device, "a bid", {"type": "job.bid", "job": "J000"})
        if len(sent) != 1:
            raise RuntimeError("bus_send made %d send_message calls" % len(sent))
        attrs = sent[0].get("MessageAttributes") or {}
        stamp = (attrs.get("from_tailnet") or {}).get("StringValue") or "none"
        ab = consumer()
        held = ab.held_tailnet_names()
        verdict = ab.classify({"MessageAttributes": attrs}, held)
        control = ab.classify({"MessageAttributes": {"from_tailnet": {"StringValue": "ldo-not-in-the-register", "DataType": "String"}}}, held)
        if verdict != "deliver":
            why = "the consumer classifies the assistant's message as %r (stamp %r; register holds %s)" % (verdict, stamp, "ldo-001" in held)
        elif control != "refused":
            why = "control: an unheld name is %r, not refused" % control
        elif attrs.get("from", {}).get("StringValue") != a.BUS_FROM:
            why = "the existing from attribute changed"
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I6-STAMP ok=%s stamp=%s verdict=%s control=%s reason=%s" % (not why, stamp, verdict, control, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
