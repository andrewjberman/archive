import json
import subprocess
print(subprocess.run(["systemctl", "cat", "opal-gateway"], capture_output=True, text=True).stdout)
print("systemd version", subprocess.run(["systemctl", "--version"], capture_output=True, text=True).stdout.split("\n")[0])
pid = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
env = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if b"=" in kv:
        k, v = kv.split(b"=", 1)
        env[k.decode()] = v.decode("utf-8", "replace")
for k in ("FIRM_ROLE_ARNS", "OTP_BEARER", "OTP_BEARER_LABELS", "ENABLED_INTEGRATIONS"):
    v = env.get(k)
    if v is None:
        print("PROC %s ABSENT" % k)
        continue
    try:
        j = json.loads(v)
        js = "json_ok type=%s keys=%d" % (type(j).__name__, len(j)) if isinstance(j, dict) else "json_ok"
    except ValueError:
        js = "json_FAIL"
    print("PROC %s len=%d has_space=%s has_dquote=%s has_backslash=%s %s tokens=%d" % (k, len(v), " " in v, '"' in v, "\\" in v, js, len(v.split())))
