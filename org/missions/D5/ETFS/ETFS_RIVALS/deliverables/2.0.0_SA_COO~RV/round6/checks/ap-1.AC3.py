"""RIV-ap-1 AC3: only the daily Lambda can read the dedicated secret, and only it carries the AI gate.
`infra/aws/terraform/etfs-rivalfunds/gen_policies.py` spec():
- the daily role's policy grants `secretsmanager:GetSecretValue` on exactly ONE secret ARN, and no other role's policy grants any
  secretsmanager action;
- the generated `lambdas` map gives the daily Lambda an `environment` with RIVALFUNDS_AI_ENABLE = "1" and
  RIVALFUNDS_OPENAI_SECRET = the secret's name, and no other Lambda carries either variable."""
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    p = c.ROOT / "infra" / "aws" / "terraform" / "etfs-rivalfunds" / "gen_policies.py"
    spec = importlib.util.spec_from_file_location("rv_gen_policies", p)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    tfvars, policies = g.spec()
    grants = {}
    for name, doc in policies.items():
        for st in doc.get("Statement", []):
            acts = st.get("Action") if isinstance(st.get("Action"), list) else [st.get("Action")]
            if any(str(a).startswith("secretsmanager:") for a in acts):
                res = st.get("Resource") if isinstance(st.get("Resource"), list) else [st.get("Resource")]
                grants.setdefault(name, []).append((sorted(acts), res))
    print("secretsmanager grants:", json.dumps(grants)[:400])
    daily = [k for k in grants if "daily" in k]
    v.check(len(grants) == 1 and len(daily) == 1 and grants[daily[0]][0][0] == ["secretsmanager:GetSecretValue"]
            and len(grants[daily[0]][0][1]) == 1, "only the daily role reads secrets: GetSecretValue on exactly one ARN")
    env = {fn: (cfg.get("environment") or {}) for fn, cfg in (tfvars.get("lambdas") or {}).items()}
    with_ai = {fn for fn, e in env.items() if "RIVALFUNDS_AI_ENABLE" in e or "RIVALFUNDS_OPENAI_SECRET" in e}
    print("lambdas carrying the AI variables:", sorted(with_ai))
    d = env.get("etfs-rivalfunds-daily-lambda", {})
    v.check(with_ai == {"etfs-rivalfunds-daily-lambda"} and d.get("RIVALFUNDS_AI_ENABLE") == "1"
            and bool(d.get("RIVALFUNDS_OPENAI_SECRET")), "only the daily Lambda carries the gate and the secret name")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
