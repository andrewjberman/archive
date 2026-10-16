"""write_manifest.py: record MX-r-15 in EC2_MANIFEST.json services.opal-gateway, in ONE write.

Asserts the precondition (deployed_commit still 3d5c9c8bf1, so a concurrent write is not overwritten), changes only the
five fields below by textual replacement inside the opal-gateway block (the rest of the file stays byte-for-byte), and
refuses if any other field of that block, or any other service, differs after the edit.
"""

import json
import re
import sys

F = "infra/aws/ec2/EC2_MANIFEST.json"
OLD = "3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4"
NEW = "0cb4a87bcb8df4adbb71d095f0818b0f50c562f1"
NOTE = (
    "NFRA_MCPINDEX MX-r-15 (round 18 release tail; the round 18 catalog release): release commit " + NEW + " (deploy-only, "
    "never merged, never pushed; TWO files vs " + OLD + ": app/refs/DATA_CATALOG.yaml blob cf7616c08e and "
    "infra/logic/registry/scopes.json blob dde73e4bd0, the bytes the host already served, so the host's changed set was the "
    "catalog alone; both at trunk 739786b974) deployed 2026-10-16T10:38:53Z with DEPLOY_BASE_REF=" + OLD + " (the stale-base "
    "guard read the live ref before the upload and it was equal); SSM af86ef3c-a8cd-4371-a977-88ab8e822388 Success. The catalog "
    "carries a C-GROUP bucket on all 280 rows and 127 tools, vendor and firm on 136 rows, 0 inferred nl_tags, the 12 Schwab dim "
    "rows, 61 read_tool names. NO tool, grant, key or integration id is added: tools 127 = 127 by name, .env keys 64 = 64, "
    "ENABLED_INTEGRATIONS 7 = 7. The MC Portal per-tool link counts moved 39 tools / 119 links -> 65 / 192, as ruled. Read-back "
    "on the installed code: /health 200; host bytes 141 of 141 equal to the cut (DIFFER 2 against " + OLD[:10] + " = the "
    "catalog and scopes.json); the host's real reader reads 65 / 192; r13.AC2 PASS (sum 127 of 127, definitions 127 of 127), "
    "r15.AC4 PASS (host catalog md5 9519ebce equal to the tree's). r13.AC3 FAIL at the apply: ONE catalog claim went stale, "
    "mac.04.yield-curve-fred generated_at (catalog 2026-10-14, served 2026-10-15), and the old catalog fails the same way, so "
    "it is not a deploy effect; the issuer re-measures. NOT exercised on the host: a firm principal's view of the 96 newly "
    "visible rows (the issuer's matrix). Rollback: redeploy " + OLD + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + NEW + " "
    "from a clean tree at " + OLD[:10] + ", never further; the rollback key opal-gateway-" + OLD[:10] + ".tar.gz is 893,303 B, "
    "ETag d43206bf (it carries the live ref's own scopes.json d0f83d17db). Ledger nfra-mcpindex-r15-catalog-release. ||| PREVIOUS: "
)
NOTE.encode("ascii")

text = open(F, encoding="utf-8", newline="").read()
before = json.loads(text)
svc = before["services"]["opal-gateway"]
assert svc["deployed_commit"] == OLD, ("PRECONDITION: block no longer reads " + OLD, svc["deployed_commit"])
assert svc["previous_deployed_commit"] != OLD

start = text.index('"opal-gateway": {', text.index('"services"'))
end = text.index("\n    }", start) if "\n    }" in text[start:] else None
# the block ends at the first line that closes it at the service indent (6 spaces for the key, 6 for the closing brace)
m = re.compile(r"\n    \},?\n").search(text, start)
end = m.start()
blk = text[start:end]


def sub(key, value, blk):
    pat = re.compile(r'("%s": )(".*?"|null)(,?)(\n|$)' % re.escape(key))
    hits = pat.findall(blk)
    assert len(hits) == 1, (key, len(hits))
    return pat.sub(lambda mo: mo.group(1) + json.dumps(value, ensure_ascii=True) + mo.group(3) + mo.group(4), blk, count=1)


old_note = svc["release_note"]
blk2 = sub("deployed_commit", NEW, blk)
blk2 = sub("previous_deployed_commit", OLD, blk2)
blk2 = sub("deployed_at", "2026-10-16T10:38:53Z", blk2)
blk2 = sub("deployed_by", "0.7.0_AE_CloudOps~MI", blk2)
blk2 = sub("release_note", NOTE + old_note, blk2)
new_text = text[:start] + blk2 + text[end:]
after = json.loads(new_text)
a, b = before["services"]["opal-gateway"], after["services"]["opal-gateway"]
changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
want = ["deployed_at", "deployed_by", "deployed_commit", "previous_deployed_commit", "release_note"]
assert changed == sorted(want), changed
assert {k: v for k, v in before["services"].items() if k != "opal-gateway"} == {
    k: v for k, v in after["services"].items() if k != "opal-gateway"
}
assert {k: v for k, v in before.items() if k != "services"} == {k: v for k, v in after.items() if k != "services"}
assert b["mcportal_commit"] == a["mcportal_commit"]
open(F, "w", encoding="utf-8", newline="").write(new_text)
print("OK: changed fields", changed, "| services", len(after["services"]), "| non-ascii", sum(1 for ch in new_text if ord(ch) > 127))
sys.exit(0)
