"""write_manifest.py: record MX-r-15 v2 in EC2_MANIFEST.json services.opal-gateway, in ONE write.

Asserts the precondition (deployed_commit still 0cb4a87bcb, so a concurrent write is not overwritten), changes only the
five fields below by textual replacement inside the opal-gateway block (the rest of the file stays byte-for-byte), and
refuses if any other field of that block, or any other service, differs after the edit.
"""

import json
import re
import sys

F = "infra/aws/ec2/EC2_MANIFEST.json"
OLD = "0cb4a87bcb8df4adbb71d095f0818b0f50c562f1"
NEW = "1bc2df0b1383e424571aaa19c195928f449be31b"
NOTE = (
    "NFRA_MCPINDEX MX-r-15 v2 (A3; the re-measured round 18 catalog): release commit " + NEW + " (deploy-only, never merged, "
    "never pushed; ONE file vs " + OLD + ": app/refs/DATA_CATALOG.yaml blob 4c27b28171, md5 983464f8, at trunk 58ae2c5417; it "
    "differs from the landed blob cf7616c08e only in tool_index history_depth, freshness and the built_at_git_head stamp, 0 of "
    "280 rows change) deployed 2026-10-16T11:30:12Z with DEPLOY_BASE_REF=" + OLD + " (the stale-base guard read the live ref at "
    "both checkpoints and it was equal both times); SSM 1021a229-e7b5-4724-973d-b3525e489017 Success. NO tool, grant, key or "
    "integration id is added: tools 127 = 127 by name, .env keys 64 = 64, ENABLED_INTEGRATIONS 7 = 7, link counts 65 / 192 "
    "equal to the cut. Read-back on the installed code: /health 200; host bytes 141 of 141 equal to the cut (DIFFER 1 against "
    + OLD[:10] + " = the catalog); r13.AC2 PASS, r15.AC4 PASS (host md5 983464f8 equal to the tree's). r13.AC3 FAIL at the apply "
    "AGAIN: the daily publish moved data_as_of from 2026-10-14 to 2026-10-15 on 7 measured rows after the 10:58Z re-measure "
    "(not a deploy effect; the issuer re-measures). Rollback: redeploy " + OLD + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF="
    + NEW + " from a clean tree at " + OLD[:10] + ", never further; the rollback key opal-gateway-" + OLD[:10] + ".tar.gz is 883,376 B, "
    "ETag e0041310. Ledger nfra-mcpindex-r15-catalog-release-v2. ||| PREVIOUS: "
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
blk2 = sub("deployed_at", "2026-10-16T11:30:12Z", blk2)
blk2 = sub("deployed_by", "0.7.0_AE_CloudOps~MI", blk2)
blk2 = sub("release_note", NOTE + old_note, blk2)
new_text = text[:start] + blk2 + text[end:]
after = json.loads(new_text)
a, b = before["services"]["opal-gateway"], after["services"]["opal-gateway"]
changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
want = ["deployed_at", "deployed_commit", "previous_deployed_commit", "release_note"]   # deployed_by already reads this seat from the first apply (v2: four fields change)
assert changed == sorted(want), changed
assert {k: v for k, v in before["services"].items() if k != "opal-gateway"} == {
    k: v for k, v in after["services"].items() if k != "opal-gateway"
}
assert {k: v for k, v in before.items() if k != "services"} == {k: v for k, v in after.items() if k != "services"}
assert b["mcportal_commit"] == a["mcportal_commit"]
open(F, "w", encoding="utf-8", newline="").write(new_text)
print("OK: changed fields", changed, "| services", len(after["services"]), "| non-ascii", sum(1 for ch in new_text if ord(ch) > 127))
sys.exit(0)
