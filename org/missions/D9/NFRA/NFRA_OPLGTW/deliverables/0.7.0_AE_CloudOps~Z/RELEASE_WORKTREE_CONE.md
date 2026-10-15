# The release-worktree sparse cone for an NFRA_OPLGTW gateway release

Written by `0.7.0_AE_CloudOps~Z`, 2026-10-15, to make the CTO half's condition 2 on `OG-ap-20`
("add `org/mcp/naming-gate.enforce` to every release worktree cone from now on") a thing a later cut
READS rather than a thing someone has to remember. Row `Z-S142` is why it exists; row `Z-S144` records
what the cone does and does not fix.

A full checkout is not an option here: it OOMs under memory pressure on this device.

## The cone

```bash
git worktree add --no-checkout <abs-path> -b rel-<slug> <base_sha>
git -C <abs-path> sparse-checkout init --cone
git -C <abs-path> sparse-checkout set \
    .tools \
    data/transcripts/scripts/teams \
    infra/aws/ec2/opal-gateway \
    infra/aws/terraform \
    infra/logic \
    lib \
    org/mcp \
    org/missions \
    org/modules/graph \
    org/standards \
    org/tier2_senior/<your base serial>
git -C <abs-path> checkout
```

## Why each entry is there, because a cone entry nobody can justify is the one that gets dropped

| entry | what fails closed without it |
|---|---|
| `.tools` | `safe-commit.sh`, `commit-gate.sh`, the gates |
| `infra/aws/ec2/opal-gateway` | the release source itself |
| `infra/aws/terraform` | the grant files a release carries |
| `infra/logic` | `safe-apply`'s naming limb resolves `infra/logic/registry/root_map.json` against the CWD and REFUSES fail-closed without it (row `Z-S132`); `deploy-to-ec2.sh` needs it too |
| `lib` | `lib/opal_naming.py` for the naming limb, and `lib/trading_calendar.py` is the one file the artifact ships as host `lib/` |
| **`org/mcp`** | **the naming gate's ENFORCE sentinel `org/mcp/naming-gate.enforce`. Absent, the gate silently grades in WARN and says so only in a parenthetical inside a passing commit (row `Z-S142`).** 154 tracked files, 5.6 MB at this base -- the inbox is untracked, so this is cheap |
| `org/missions` | the order, the checks, `DIRECTIVES.yaml` |
| `org/modules/graph` | `deploy-to-ec2.sh`'s preflight names `org/modules/graph/*_cli.py` |
| `org/standards` | schemas a gate reads |
| `org/tier2_senior/<base>` | `safe-apply`'s HALT gate refuses with `SERIAL RESOLVES TO NO KNOWN AGENT` when no `org/tier*_*/<base>*` matches your serial |

## What the cone does NOT fix

**The release branch runs the gate CODE of its base.** A base cut before a gate clause merged carries the
pre-clause gate: at `1b18b94979` `.tools/naming-gate.py` is md5 `7be9e4ede2760451207c8a93166cb8ac` against
trunk's `8798c2dca5ba305550dbf27418edec29`, and it does not accept `--staged-paths` at all (argparse exit
2), so the `OG-ng-1` S3PREFIX clause cannot run there **at any mode**. Mode and code version are two
separate axes; the cone only fixes the mode.

**A clause keyed on what else a commit stages cannot grade a release commit.** The S3PREFIX clause derives
the committing project from the staged paths and needs one under `org/missions/D9/NFRA/NFRA_OPLGTW/`; a
release commit stages the release's files and the grant only, by the order's own bound. Graded in ENFORCE
the release commit refuses by construction, not on the merit of the name. The authoritative grading of a
grant's bytes is the TRUNK commit that introduces it. Row `Z-S144`, evidence `W/G5A_NAMING_ENFORCE.json`.
