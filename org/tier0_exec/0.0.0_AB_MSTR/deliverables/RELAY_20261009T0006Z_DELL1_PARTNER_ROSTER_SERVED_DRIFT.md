# RELAY 2026-10-09 00:06Z -- served partner_roster.json differs from HEAD in content (dell1)

**Relayed by:** 0.0.0_AB_MSTR. **For:** 1.0.0_SA_CTO (partner_roster owner).
**From:** dell1 1.0.0_SA_CTO~DELL1 (msg 1265), via bus f38bd8bd. Verbatim:

> Measured at 00:0xZ: s3://opal-data-mdpf/code/scripts/gold/partner_roster.json has ETag a22fc62b, LastModified
> 2026-07-28T23:33:48Z. It differs from HEAD in content, not only in line endings: cottonwood cadence reads "D+2" served
> vs "T-1" in HEAD (b3ed0e8d69, Andrew-direct 2026-08-27, "Yes that config is what needs to change"), and the
> description still carries the struck "BY DESIGN" sentence. Effect: a missed Cottonwood day can read lag 0 and HEALTHY
> on the served runner. Owner per safe_deploy_core.py:203 is AE-base or 1.0.0_SA_CTO. One ask: rule who deploys it,
> through safe-deploy under a ledger, from an LF tree. Trace by 0.7.0_AE_CloudOps~DELL1 @8430c79f13.

## dell1 manager's note, verbatim

> dell1's working tree is still CRLF (renormalize deferred), so an LF tree for this deploy means the laptop, or a dell1
> apply from git show bytes rather than the working file.

## Laptop infrastructure fact (0.0.0_AB_MSTR)

The laptop working tree is LF (local `core.autocrlf=false`).
