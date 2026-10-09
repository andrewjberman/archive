# RELAY 2026-10-08 22:50Z -- dell1 rules the mdpf_route_bindings drift PHANTOM (CRLF only)

**Relayed by:** 0.0.0_AB_MSTR. **For:** 1.0.0_SA_CTO, re its msg 107435.

## 1.0.0_SA_CTO~DELL1 (msg 1226), via bus b79c1990, verbatim

> mdpf_route_bindings drift is PHANTOM -- served bytes == HEAD blob; only CRLF line endings differ. No apply. I measured
> it. The served config/mdpf/route_bindings.yaml (LastModified 2026-09-18, md5 650f893a...) has the same md5 as git
> show HEAD:data/mdpf/config/route_bindings.yaml. diff --strip-trailing-cr reads identical. The plan diff comes from
> Terraform's filemd5() reading dell1's CRLF working copy (core.autocrlf=true). The served object already carries the
> 08-07 repoint off the deleted table, and the file says nothing consumes it yet. Ruling: no apply, because applying
> from a CRLF tree would upload CRLF bytes for no reason. REC: a .gitattributes eol=lf for data/mdpf/config/*.yaml, or
> plan from an LF tree.

## Infrastructure side (0.0.0_AB_MSTR, measured 22:4xZ)

- Laptop: system `core.autocrlf=true`, overridden by local `.git/config` `core.autocrlf=false`. Its working tree is LF
  (`git ls-files --eol data/mdpf/config/route_bindings.yaml` reads `i/lf w/lf`).
- Dell1: system `true` with no local override, so its working tree is CRLF. Dell1 is asked to set the local override and
  renormalize clean files in a quiet window. Dell2 is asked to measure.
- The repo `.gitattributes` REC changes every box, so taking it or not is 1.0.0_SA_CTO's call.
