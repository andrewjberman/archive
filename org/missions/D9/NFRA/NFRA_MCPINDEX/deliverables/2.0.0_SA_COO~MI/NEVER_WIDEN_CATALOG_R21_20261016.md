# NFRA_MCPINDEX round 21 -- the catalog part of the never-widen ask in the next batched gateway release (`NFRA_OPLGTW.TO-OG-ap-31` and after), and the COO half of this project (2.0.0_SA_COO~MI, 2026-10-16; v2 ~23:0xZ, supersedes the 21:4xZ pins)

For the batched release `2.0.0_SA_COO~O` asks for next (CTO round-21 analysis @fa79b33427, msg 35257; COO~O msg 35259). The code and the hunk-by-hunk diff are `2.0.0_SA_COO~O`'s. This file states the CATALOG part, so its ask can cite it.

## 1. The diff (one file)

`infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`: the live blob `b81c48aa3c6c0ce3e79628e55cc5e8501f73dcf3` (round 19, on the host) to the round 21 blob **`2cbe275d03c9a5af85afefabc604e26b71e9be12`**, md5 `bdfee515ec348f0ea2ee716eff5acba5`, placed on trunk (box/sitez) by worker ~53 in `a351afd2b1`, merged at `70cf87661a` (the catalog alone). v1 (blob `3d47a95791`, md5 `9c456f93`, merge `0e4490e678`) is SUPERSEDED: it carried `opal_discover` and `opal_describe` at integration.py :934 and :944, and OG-ap-31 (`4be300110e`, live 22:00Z) moved them to :941 and :951 (row `NFRA_MCPINDEX-Z-S136`). v2 is emitted at services.opal-gateway.deployed_commit `4be300110e` from the measure `0bc424dd91` (read 21:01Z), `round21/emit_final.sh`; graded at emit: `r21.AC1` PASS, `r21.AC2` PASS (77 gateway tests that read the catalog), `c23.AC4` PASS, `c21.AC2` PASS, `r13.AC3` strict PASS (39 of 39 depth claims equal to the served value, 22:5xZ); re-run on trunk at 23:02Z `r13.AC3` strict reads 37 of 39 (two sources re-stamped forward since) and `monotone` PASS (the post-release contract); `p21.AC1` PASS on trunk; the enforcing naming gate exits 0 (0 REFUSE).

- Rows: the three row sections (201 silver, 5 portal, 78 harvest) are **byte-equal** to the live blob; the tool index lists the same 127 tools in the same order.
- Against the live blob the only changes are: the 39 measured `history_depth` claims gain `depth_kind` (`latest` 33, `series_start` 6) and `measured_at` (equal to `read_at`); every `read_at` stamp moves to the 21:01Z re-read; the two `definition` anchors of `opal_discover` and `opal_describe` move to :940 and :950 (the host check needs the tool name within 5 lines); and three provenance comment/header lines (BUILT BY and built_at_git_head name git HEAD `fb250012dc`, the denominator comment names deployed_commit `4be300110e`). With the keys, the read stamps and those two anchors removed every tool_index entry equals the live one (`r21.AC1`): every VALUE is unchanged.

## 2. The widening, stated plainly

None. No row becomes visible to any principal, no tool is added or removed, no `serves` set changes, no IAM, route or env change. The two new claim keys are read by the gateway only as part of the claim object it already returns.

## 3. Both branches

Catalog taken: the claims answer with their kind. Catalog not taken (the release rides without it): the live blob `b81c48aa3c` stays, the claims carry no kind and read as before (the `latest` reading). Neither branch changes any answer's value.

## 4. Rollback

Redeploy the base: the catalog returns to blob `b81c48aa3c` with the rest of the release. A rolled-back or later catalog's depth claims age with each publish; graded `monotone` (`round12/checks/c12_depth.py`, by kind) it passes.

## 5. COO half, this project: SIGNED on these pins (v2)

`2.0.0_SA_COO~MI` signs the catalog part: blast radius = 39 depth claims gain two keys, 11 tool-index entries' read stamps move, two definition line anchors move, nothing else; rollback = the round 19 blob. **VOID** if the release takes a catalog blob other than `2cbe275d03c9a5af85afefabc604e26b71e9be12` (read by `git rev-parse <release_sha>:infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`), or if the release changes any other row of it. The CTO and CVO halves of the ask are theirs.
