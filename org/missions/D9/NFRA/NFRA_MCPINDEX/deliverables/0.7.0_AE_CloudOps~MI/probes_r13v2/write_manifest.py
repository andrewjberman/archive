"""write_manifest.py: record MX-r-13 (v2) in EC2_MANIFEST.json services.opal-gateway, in ONE write.

Asserts the precondition (deployed_commit still ee23dd004c, so a concurrent write is not overwritten), changes only the
five fields below by textual replacement inside the opal-gateway block (the rest of the file stays byte-for-byte), and
refuses if any other field of that block, or any other service, differs after the edit.
"""

import json
import re
import sys

F = "infra/aws/ec2/EC2_MANIFEST.json"
OLD = "ee23dd004c985c46d479908db46d2ad9b4f3b1c8"
NEW = "1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0"
NOTE = (
    "NFRA_MCPINDEX MX-r-13 (round 12 chain tail; the catalog v0.5 release): release commit " + NEW + " (deploy-only, never "
    "merged, never pushed; TWO files vs " + OLD + ": app/refs/DATA_CATALOG.yaml blob e5096b5d6c and "
    "app/integrations/opal_discover/integration.py blob f3cf344cc3, both at trunk 32d0bc608a) deployed 2026-10-15T07:54:33Z "
    "with DEPLOY_BASE_REF=" + OLD + " (the stale-base guard read the live ref at both checkpoints and it was equal both "
    "times); SSM 9fedb84f-8099-417c-b4b2-d938c7e5c10b Success. The catalog is v0.5: 78 harvest rows, 216 table rows each "
    "with a key_template, 5 retired, 29 distinct read_tools all served by the deployed commit. NO tool, grant, key or "
    "integration id is added: tools 93 = 93 by name, .env keys 57 = 57, ENABLED_INTEGRATIONS 7 = 7. The MC Portal per-tool "
    "link counts moved 11 tools / 14 links -> 33 / 112, as ruled (a count of catalog rows naming tools the gateway already "
    "serves). Read-back on the installed code: /health 200; host bytes 118 of 118 equal to the cut (DIFFER 2 against "
    + OLD[:10] + " = exactly the two files); the host's real reader reads 33 / 112; r13.AC2 PASS (sum 93 of 93, definitions "
    "93 of 93), r13.AC3 PASS, r13.AC4 PASS (host catalog md5 equal to the tree's). A FIRST ATTEMPT, d020bee315, deployed "
    "2026-10-15T06:35Z, failed r13.AC2 and was rolled back to " + OLD[:10] + " at 06:46Z (ledger "
    "nfra-mcpindex-r12-catalog-release, rows NFRA_MCPINDEX-Z-S118 and Z-S119, both causes the issuer's and fixed); that "
    "rollback re-uploaded opal-gateway-" + OLD[:10] + ".tar.gz (629,787 B, ETag 3cd90347). Rollback of THIS release: "
    "redeploy " + OLD + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + NEW + " from a clean tree at " + OLD[:10]
    + " (C:/tmp/mx-dep-r13-rb), which leaves the host as it was; never further. Ledger nfra-mcpindex-r12-catalog-release-v2. "
    "||| PREVIOUS: "
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
blk2 = sub("deployed_at", "2026-10-15T07:54:33Z", blk2)
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
