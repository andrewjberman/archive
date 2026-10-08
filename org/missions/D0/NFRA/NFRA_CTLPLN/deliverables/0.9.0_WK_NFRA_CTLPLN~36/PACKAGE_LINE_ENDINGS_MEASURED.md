# PACKAGE_LINE_ENDINGS_MEASURED -- NFRA_CTLPLN.TO-CT-i-8 (0.9.0_WK_NFRA_CTLPLN~36)

All reads; nothing deployed, no AWS call, nothing changed in the shared tree. Worktree: wk-NFRA_CTLPLN-36 at dbd75257ee.
Shared tree (main worktree from `git worktree list --porcelain`): C:/Users/AndrewBerman/Desktop/ajb_workspace, HEAD 9431eb0e57.

## 1. Every file build.sh copies: `git ls-files --eol` in both trees

The package holds 28 files (the zip's name list from one build; handlers.py and ldo.py sit at the zip root, their sources are
infra/aws/lambda/teams-chat-assist/handlers.py and infra/aws/terraform/modules/ldo/runtime/ldo.py). The table below is those 28
sources; read with `git ls-files --eol <path>` in each tree.

| file (repo path) | index / worktree / attr (THIS worktree) | index / worktree / attr (shared tree) |
|---|---|---|
| daily_reports/eod/VOICE.md | i/lf w/lf attr/ | i/lf w/lf attr/ |
| daily_reports/eod/post_format.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/NAMES.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| data/transcripts/scripts/teams_chat/__init__.py | i/none w/none attr/text eol=lf | i/none w/none attr/text eol=lf |
| data/transcripts/scripts/teams_chat/andrew_voice.md | i/lf w/lf attr/ | i/lf w/lf attr/ |
| data/transcripts/scripts/teams_chat/assist.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/gen_bus_devices.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/mail_requests.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/seed_from_session.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/tenant.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| data/transcripts/scripts/teams_chat/voice.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| infra/aws/lambda/teams-chat-assist/handlers.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| infra/aws/terraform/modules/ldo/runtime/ldo.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| infra/logic/registry/event_rules.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/exemptions.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/key_rulings.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/legacy_addresses.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/mail_parties.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/name_rulings.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/remediations.json | i/lf w/lf attr/ | i/lf w/crlf attr/ **DIFFERS** |
| infra/logic/registry/reporting_policies.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/resources.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/root_map.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/scopes.json | i/lf w/lf attr/ | i/lf w/crlf attr/ **DIFFERS** |
| infra/logic/registry/systems.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| infra/logic/registry/tiers.json | i/lf w/lf attr/ | i/lf w/lf attr/ |
| lib/opal_naming.py | i/lf w/lf attr/text eol=lf | i/lf w/lf attr/text eol=lf |
| org/standards/NAMING_SCHEMA.json | i/-text w/-text attr/ | i/-text w/-text attr/ |

Denominator: 28 of 28 package sources read in each tree. Rows that differ between the trees: 2 of 28.

## 2. The files that differed, and the cause

Differing files: `infra/logic/registry/remediations.json` and `infra/logic/registry/scopes.json` -- index `i/lf` in both trees; the
working copy is `w/lf` in this worktree and `w/crlf` in the shared tree. These are the two files the row (NFRA_CTLPLN-S27) named.

Cause, from reads:
- `git check-attr -a` on both files prints nothing in either tree: no attribute governs them (.gitattributes has `text eol=lf`
  rules for code files but none for infra/logic/registry/*.json).
- `git config --show-origin --get-all core.autocrlf`: system file (C:/Program Files/Git/etc/gitconfig) = true, repo file
  (.git/config) = false, in BOTH trees (a linked worktree shares .git/config). The effective value is false in both. `core.eol` is unset.
  So no setting converts line endings on checkout or add, in either tree; a fresh checkout of an LF blob is LF.
- `git hash-object --no-filters` on the shared tree's two files gives 5a17b3a317... (remediations) and 08abb888a6... (scopes);
  the index blobs are 0f40e0683e... and d0f83d17db...: the shared tree's bytes are NOT the index's bytes. Their mtimes are Sep 30
  03:40 and 11:34, and `git status --short -- infra/logic/registry` prints nothing for them (git trusts its stat cache).
- Reading: the CRLF is a working-copy write (an editor or a tool writing the file with CRLF on this Windows box) with no
  git-level rule to correct it. It is an inference from the reads above; I did not find the writer.
- Related, not a difference between the trees: `org/standards/NAMING_SCHEMA.json` is `i/-text w/-text` in both trees because it
  holds ONE lone CR (not CRLF) after a closing quote inside the document's history list. build.sh's change replaces only CRLF pairs, so that
  lone CR is kept in the package, in either tree.

## 3. Package SHA-256 (one build each, `bash infra/aws/lambda/teams-chat-assist/build.sh`, 28 files)

| build | SHA-256 |
|---|---|
| BEFORE the change, this worktree as it is (all inputs LF on disk) | 42659e79f3f8b7ef1512398703e0d2cac9ef2e6ce871e4601a686606f3d23f47 |
| AFTER the change, this worktree as it is | 42659e79f3f8b7ef1512398703e0d2cac9ef2e6ce871e4601a686606f3d23f47 |
| BEFORE the change, every text input converted to CRLF (temporary copy) | d142c653452ef2084f56f7b295209fd18736f4b64563ddd22a42830afc0361a5 |
| BEFORE the change, LF inputs but the shared tree's two CRLF registry files (temporary copy) | 61858efddc4fc7248fa5a00f9abf8587166d4019e40a12784861a7b6fbef32be |
| AFTER the change, the same temporary copy with the shared tree's two CRLF registry files | 42659e79f3f8b7ef1512398703e0d2cac9ef2e6ce871e4601a686606f3d23f47 |

The defect is reproduced: the old script gives different packages for LF and CRLF inputs. After the change the CRLF-input,
LF-input and unmodified-worktree builds give one hash (the test's last line: crlf_sha=lf_sha=worktree_sha=42659e79f3f8).

## 4. What the change means for the deployed function

The package a build makes from LF inputs is unchanged by this change (same hash before and after in this worktree). So the next
deploy's package hash equals the hash of an LF build of the deployed commit, whichever tree it is built in. It will differ from
the live one if the live one was built from CRLF inputs. My measurement does not read the live hash (no AWS call was allowed, so
I did not read the live function's source_code_hash), so it does not show which line endings the live package was built with. It
shows the mechanism and is consistent with the row's account: a package built by the OLD script in the shared tree (with its two
CRLF registry files) has hash 61858efddc..., which differs from the LF build 42659e79f3... of the same commit's sources. If the
live package was built that way (the row says a fresh-checkout rebuild of 55cb79f93c differed from the deployed hash), then the
next deploy shows a hash change and a one-time function code update with no source change; it is the LF form, and from then
on every build of that source gives that one hash. The registry JSON is read by the function as data, so CRLF vs LF in it
changes bytes, not parsed content; I did not run the function to confirm that.
