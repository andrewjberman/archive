# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-23 (the code batch release, 27 READ tools)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: REFUSED**, 2026-10-16 ~06:5xZ. One defect, named with its fix below. Everything else this
half covers verified.
**Ask:** `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md`, sha256 `a4c90d32c29f`, read whole.
**Release:** `56c0f8ce1d602b309abaf3f25dd28974c7736d39`. Everything below was read from git, not from the ask.

## The defect (the ask's section 10, asked of this half in particular)

The ask says the first `deploy-to-ec2.sh` hunk names "the two `app/refs/` files ... on the `tar` line ... without it the staged
files never reach the host". **The release has no tar-line edit.** `git diff --stat` reads 30 insertions and 1 deletion, and that
1 deletion is the `.env` printf. The tar line (release `:283-287`) is byte-identical to the base (`:254-258`):

    tar -czf "$TMP/$ART" -C "$SRC" ... app deploy requirements.txt identity_tool_allowlist.txt \
        -C "$TMP/bundle" "$DASHBOARD_BUNDLE_DIR" lib

So the staging (release `:261-264`) copies `partner_roster.json` and `scopes.json` into `$TMP/bundle/app/refs/`, a path the
archive never reads. `lib/opal_naming.py` does ship, because `lib` is on the line.

What would ship instead: `app` is archived from `$SRC` on DISK. The release worktree `C:/tmp/og-rel-code` holds UNTRACKED
copies at `app/refs/partner_roster.json` and `app/refs/scopes.json` (02:31 local). Today they hash to trunk's blobs:
`eb3bff48c847` for `data/mdpf/config/partner_roster.json` and `b53fb599f250` for `infra/logic/registry/scopes.json`. So
the host would get the right bytes, but by an untracked file that no half signs, and the staging hunk would be dead code. A
signature binds the release sha. It cannot bind an untracked file.

Second, smaller: section 7's Phase B trigger names trunk blobs `3d309b267e69` and `fd17416171b2`. Trunk reads
`eb3bff48c847` and `b53fb599f250` today, so the trigger would compare against stale values.

## The fix (re-cut, then re-ask; this half signs on receipt)

1. Put the staged files on the archive. Either:
   - append `app/refs/partner_roster.json app/refs/scopes.json` to the `-C "$TMP/bundle"` list AND exclude those two paths
     from the `-C "$SRC"` part, so that only the staged copies ship; or
   - delete the two untracked copies from the release tree and add them to the `$TMP/bundle` list.
   Either way, the shipped bytes come from the repo sources at the release, not from untracked disk state.
2. Restate the section 7 trigger blobs from trunk at the re-cut, printed by `git rev-parse <ref>:<path>`, never typed.

## What verified (this half's sections, read from git)

- Parent of the release = `d577e0e7297b3ecba183023d8374855a93f148a7` (the base, OG-ap-21's release).
- Diff base to release: 31 A, 13 M, 0 D. Zero `.tf` files. Outside `infra/aws/ec2/opal-gateway/`: only `EC2_MANIFEST.json` (one
  field, `mcportal_commit` `17dcbb28624e` to `090b9cdc85ce`) and `lib/opal_naming.py`, both named by the ask.
- `app/tools.py`: 27 `@mcp.tool` registrations added, 0 lines removed. `destructive_ops.py` and `data_entitlement.py`: every changed
  line is a quoted tool name. The not-taken list holds: no `decide()` change, so the entitlement chokepoint is untouched.
- The reader-keys hunk:
  - the script runs `set -euo pipefail` (`:28`), so a failed `_vr_arn` inside `READER_ARN_*="$(...)"` exits before any upload;
  - each ARN is compared to `arn:aws:iam::<account>:role/<name>`;
  - the six `%s` slots and six arguments sit before the two `ADVI_*` roots, in matching order.
  This is the A3 hunk as described.
