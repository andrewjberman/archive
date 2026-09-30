"""Round 24 AC (IB-pr-242) -- inf-ec2-launch-monitor never suppresses a stop whose StateTransitionReason reads EMPTY
(row S216; WK~81's diagnosis @0b5cdb06f9: NORMAL_PATTERNS carried '', which substring-matches every reason, so 09-29's
Server.InternalError, read before AWS populated the reason, was suppressed and never handed to the retry Lambda).

Usage: python p24_2_ac1_monitor_empty_reason.py <worktree root>
Imports the worktree's infra/aws/lambda/inf-pipeline/inf-ec2-launch-monitor/lambda_function.py with the EC2, SNS and
Lambda clients replaced by in-memory fakes (no AWS call), sets RETRY_FUNCTION_NAME, and drives lambda_handler with a
'stopped' EventBridge event under four arms:
  A. reason ''                   , launched 5 s ago  -> handed to retry (NOT suppressed)
  B. reason ''                   , launched 2 h ago  -> NOT suppressed as a normal shutdown (hand-off or named unknown)
  C. reason 'User initiated'     , launched 2 h ago  -> suppressed (a real normal stop stays quiet)
  D. reason 'Server.InternalError', launched 5 s ago -> handed to retry
Pass: all four.
"""
import datetime as dt
import importlib.util
import os
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
src = root / "infra/aws/lambda/inf-pipeline/inf-ec2-launch-monitor/lambda_function.py"
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ["RETRY_FUNCTION_NAME"] = "inf-ec2-retry-launch"
os.environ.setdefault("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:000000000000:check-only")
spec = importlib.util.spec_from_file_location("monitor_under_test", src)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
if hasattr(mod, "RETRY_FUNCTION_NAME"):
    mod.RETRY_FUNCTION_NAME = "inf-ec2-retry-launch"


class FakeEC2:
    def __init__(self):
        self.inst = {}

    def describe_instances(self, InstanceIds):
        return {"Reservations": [{"Instances": [self.inst]}]}


class FakeLambda:
    def __init__(self):
        self.calls = []

    def invoke(self, **kw):
        self.calls.append(kw)
        return {"StatusCode": 202}


class FakeSNS:
    def __init__(self):
        self.calls = []

    def publish(self, **kw):
        self.calls.append(kw)
        return {"MessageId": "x"}


def run(reason, launched_ago_s):
    ec2, lam, sns = FakeEC2(), FakeLambda(), FakeSNS()
    mod.ec2, mod.lambda_client, mod.sns = ec2, lam, sns
    ec2.inst = {"InstanceId": "i-test", "StateTransitionReason": reason,
                "Tags": [{"Key": "Name", "Value": "inf-bronze-runner"}],
                "LaunchTime": dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=launched_ago_s)}
    out = mod.lambda_handler({"detail": {"instance-id": "i-test", "state": "stopped"}}, None)
    return str(out.get("body")), len(lam.calls)


arms = {
    "A empty reason, 5 s": run("", 5),
    "B empty reason, 2 h": run("", 7200),
    "C 'User initiated', 2 h": run("User initiated (2026-09-29 11:30:00 GMT)", 7200),
    "D Server.InternalError, 5 s": run("Server.InternalError: Internal error on launch", 5),
}
for k, v in arms.items():
    print("%-30s -> body %-32s retry invocations %d" % (k, v[0], v[1]))
ok = (arms["A empty reason, 5 s"][1] == 1
      and "suppressed-normal" not in arms["B empty reason, 2 h"][0]
      and arms["C 'User initiated', 2 h"][0].startswith("suppressed") and arms["C 'User initiated', 2 h"][1] == 0
      and arms["D Server.InternalError, 5 s"][1] == 1)
print("P24-2-AC1 PASS" if ok else "P24-2-AC1 FAIL")
sys.exit(0 if ok else 1)
