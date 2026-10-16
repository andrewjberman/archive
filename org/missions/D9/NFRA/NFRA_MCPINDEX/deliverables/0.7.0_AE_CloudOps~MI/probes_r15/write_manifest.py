"""write_manifest.py: record MX-r-14 in EC2_MANIFEST.json services.opal-gateway, in ONE write.

Asserts the precondition (deployed_commit still ee23dd004c, so a concurrent write is not overwritten), changes only the
five fields below by textual replacement inside the opal-gateway block (the rest of the file stays byte-for-byte), and
refuses if any other field of that block, or any other service, differs after the edit.
"""

import json
import re
import sys

F = "infra/aws/ec2/EC2_MANIFEST.json"
OLD = "06cfb6db6471972c7304cd3d7a5b93e6f521ad72"
NEW = "c4c106aea1cc47d15f81397208226bd9b292c9dc"
NOTE = (
    "NFRA_MCPINDEX MX-r-14 (round 17 chain tail; the round 17 catalog release): release commit " + NEW + " (deploy-only, "
    "never merged, never pushed; TWO files vs " + OLD + ": app/refs/DATA_CATALOG.yaml blob b97c59e6ac and "
    "app/integrations/opal_discover/integration.py blob 92ca8b57f7, both at trunk 7cfd0b09ec) deployed 2026-10-15T19:50:39Z "
    "with DEPLOY_BASE_REF=" + OLD + " (the stale-base guard read the live ref at both checkpoints and it was equal both "
    "times); SSM 663c8355-e719-4224-aaeb-117be2529521 Success. The catalog carries 44 derived nl_tags marked inferred and a "
    "firm field on 24 firm-scoped table rows (304 rows, nl_tags on all 304); the discover module shows a firm-scoped row to "
    "its own firm's principals only and gives a string never_sum_rules at most one caveat line. NO tool, grant, key or "
    "integration id is added: tools 99 = 99 by name, .env keys 57 = 57, ENABLED_INTEGRATIONS 7 = 7. The MC Portal per-tool "
    "link counts moved 33 tools / 112 links -> 39 / 119, as ruled (six etfs_* and mdpf_* tools gain a catalog link; a count "
    "of catalog rows naming tools the gateway already serves). Read-back on the installed code: /health 200; host bytes 121 "
    "of 121 equal to the cut (DIFFER 2 against " + OLD[:10] + " = exactly the two files); the host's real reader reads "
    "39 / 119; r13.AC2 PASS (sum 99 of 99, definitions 99 of 99), r13.AC3 PASS, r14.AC4 PASS (host catalog md5 equal to the "
    "tree's). NOT exercised on the host: a firm principal's view of the 24 rows (the issuer's f1 checks grade it on the "
    "tree). Rollback: redeploy " + OLD + " through safe-ec2-deploy.sh with DEPLOY_BASE_REF=" + NEW + " from a clean tree "
    "at " + OLD[:10] + ", never further; the rollback key opal-gateway-" + OLD[:10] + ".tar.gz is 734,698 B, ETag d8470277. "
    "Ledger nfra-mcpindex-r14-catalog-release. ||| PREVIOUS: "
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
blk2 = sub("deployed_at", "2026-10-15T19:50:39Z", blk2)
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
