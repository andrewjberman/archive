"""RIV-d-1 AC1 -- terraform plan of the new etfs-rivalfunds stack: create-only, the five named Lambdas, the bucket's
notification configuration EventBridge-only, the 07:00 America/New_York Mon-Fri schedule, and no alarm/SNS.

Plans against a LOCAL throwaway state (a backend_override.tf written and removed by this check), so the real state
bucket is never touched. Provider plugins cache in <main>/.runtime/tf-plugin-cache; the FIRST run may exceed the
120 s worker timeout while it downloads -- run it again."""
import json
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LAMBDAS = {"etfs-rivalfunds-daily-lambda", "etfs-rivalfunds-fetch-holdings-lambda", "rivalfunds-build-silver-lambda",
           "rivalfunds-build-canonical-shape-lambda", "rivalfunds-publish-page-lambda"}


def run(v):
    root = c.setup_path()
    stack = root / "infra" / "aws" / "terraform" / "etfs-rivalfunds"
    v.check(stack.is_dir(), f"stack exists at {stack.relative_to(root)}")
    if not stack.is_dir():
        return
    subprocess.run([sys.executable, str(root / "infra" / "aws" / "lambda" / "etfs-pipeline" / "rivalfunds_package.py")], check=True)
    cache = c.main_root() / ".runtime" / "tf-plugin-cache"
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TF_PLUGIN_CACHE_DIR=str(cache), TF_IN_AUTOMATION="1")
    tmp = pathlib.Path(c.tmpdir("rv_d1_"))
    override = stack / "backend_override.tf"
    override.write_text('terraform {\n  backend "local" {\n    path = "%s"\n  }\n}\n' % (tmp / "t.tfstate").as_posix(), encoding="utf-8")
    try:
        tf = lambda *a: subprocess.run(["terraform", f"-chdir={stack}", *a], env=env, capture_output=True, text=True)  # noqa: E731
        i = tf("init", "-input=false", "-reconfigure", "-no-color")
        v.check(i.returncode == 0, f"terraform init rc={i.returncode} {i.stderr[-300:]}")
        if i.returncode:
            return
        p = tf("plan", "-input=false", "-lock=false", "-no-color", f"-out={tmp / 'p.bin'}")
        v.check(p.returncode == 0, f"terraform plan rc={p.returncode} {p.stderr[-500:]}")
        if p.returncode:
            return
        s = tf("show", "-json", str(tmp / "p.bin"))
        plan = json.loads(s.stdout)
    finally:
        override.unlink(missing_ok=True)
    rc = [r for r in plan.get("resource_changes", []) if r.get("mode") == "managed"]
    bad = [(r["address"], r["change"]["actions"]) for r in rc if set(r["change"]["actions"]) - {"create", "no-op"}]
    v.check(not bad, f"create-only ({len(rc)} managed changes; non-create: {bad[:5]})")
    after = lambda t: [r["change"]["after"] or {} for r in rc if r["type"] == t]  # noqa: E731
    names = {a.get("function_name") for a in after("aws_lambda_function")}
    v.check(names == LAMBDAS, f"exactly the five named Lambdas ({sorted(n for n in names if n)})")
    notes = after("aws_s3_bucket_notification")
    v.check(len(notes) == 1 and notes[0].get("bucket") == "opal-data-etfs" and notes[0].get("eventbridge") is True
            and not any(notes[0].get(k) for k in ("lambda_function", "queue", "topic")),
            f"one bucket notification on opal-data-etfs, EventBridge only ({notes})")
    sch = {a.get("name"): a for a in after("aws_scheduler_schedule")}
    daily = sch.get("etfs-rivalfunds-daily", {})
    v.check(daily.get("schedule_expression_timezone") == "America/New_York" and "cron(0 7 ? * MON-FRI *)" == daily.get("schedule_expression"),
            f"schedule etfs-rivalfunds-daily at cron(0 7 ? * MON-FRI *) America/New_York ({daily.get('schedule_expression')}, {daily.get('schedule_expression_timezone')})")
    forbidden = [r["address"] for r in rc if r["type"] in ("aws_cloudwatch_metric_alarm", "aws_sns_topic", "aws_sns_topic_subscription")]
    v.check(not forbidden, f"no alarm or SNS (standing moratorium) ({forbidden})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
