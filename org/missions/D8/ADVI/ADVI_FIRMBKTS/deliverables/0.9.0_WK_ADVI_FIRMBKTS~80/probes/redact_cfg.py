import json
import re
import sys

path = sys.argv[1]
d = json.load(open(path, encoding='utf-8'))
print("FunctionName:", d.get("FunctionName"), "Runtime:", d.get("Runtime"), "Role:", re.sub(r'\d{9,}', '<id>', d.get("Role","")), "LastModified:", d.get("LastModified"))
print("Handler:", d.get("Handler"), "Timeout:", d.get("Timeout"), "Memory:", d.get("MemorySize"), "State:", d.get("State"))
env = (d.get("Environment") or {}).get("Variables", {})
print("EnvVarNames:", sorted(env.keys()))
keep = re.compile(r'BUCKET|REGION|TABLE|QUEUE|TOPIC|PREFIX|KEY', re.I)
for k in sorted(env):
    if keep.search(k) and not re.search(r'SECRET|PASS|TOKEN|CRED', k, re.I):
        v = env[k]
        if len(v) < 120 and not re.search(r'\d{9,}', v):
            print("  value", k, "=", v)
        else:
            print("  value", k, "= <redacted: long or numeric id>")
print("DeadLetter:", json.dumps(d.get("DeadLetterConfig", {})))
print("Layers:", [layer.get("Arn") for layer in d.get("Layers", [])])
