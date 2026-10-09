import json
import subprocess
pin = "47c3c75f11"
P = "infra/aws/lambda/opal-assets/opal-assets-silver-schwab/"
bm = json.loads(subprocess.check_output(["git", "show", pin + ":" + P + "BUILD_MANIFEST.json"]))
rows = []
for src in bm["vendored_modules"]:
    name = src.rsplit("/", 1)[1]
    a = subprocess.check_output(["git", "show", pin + ":" + src])
    b = subprocess.check_output(["git", "show", pin + ":" + P + name])
    rows.append((src, name, a == b, len(a)))
for r in rows:
    print("%-52s vs package/%-24s equal=%s bytes=%d" % r)
print("vendored_modules in manifest: %d; byte-equal: %d" % (len(rows), sum(1 for r in rows if r[2])))
members = subprocess.check_output(["git", "ls-tree", "--name-only", pin, P]).decode().split()
print("package members at pin:", sorted(m.rsplit('/', 1)[1] for m in members))
