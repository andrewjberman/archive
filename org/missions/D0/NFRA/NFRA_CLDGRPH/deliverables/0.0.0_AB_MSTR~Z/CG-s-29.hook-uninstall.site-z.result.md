# CG-s-29 — stitch-refresh post-commit hook UNINSTALL, SITE-Z half

**THIS IS THE SITE-Z HALF; THE LAPTOP'S RECORD IS THE OTHER HALF; THE PAIR IS GRADED AT L9.**

Seat: `0.0.0_AB_MSTR~Z` (site Z integrator — a device act on site Z is site Z's integrator's).
Authority: `1.0.0_SA_CTO` ruling S71 (PRD v0.7 @`a46abe413a`, merged @`764439e1d8`, R16), carried to
this device by `0.0.0_AB_MSTR` over the agentbus (id `2a5b3ff5-b3d1-4d32-b4a0-385b609ce5dd`), on
Andrew's 2026-09-02 ratification superseding his 2026-07-07 local-hook word.
Face: `2.0.0_SA_COO~A`'s F-9. Not an integrate leg.

---

## VERDICT

**PASS.** The two stitch-refresh lines are gone from this clone's `.git/hooks/post-commit`, every
other hook entry survives, and a real trigger-class commit produced **no local write** to the cloud
stitch marker.

**REMOVAL INSTANT: `2026-09-09T19:58:27.757Z`.**

---

## 1. BEFORE / AFTER

| | BEFORE | AFTER |
|---|---|---|
| total lines | 17 | 15 |
| lines naming `stitch-refresh` | **2 of 17** | **0 of 15** |
| `_ws=` hook entries (positive control) | 5 | **4** |
| file mode | 755 | 755 (unchanged) |
| `bash -n` | clean | clean |
| `sh -n` | clean | clean |
| CRLF count | 0 | 0 |

**The two lines removed, verbatim:**
```
# stitch-refresh-post-commit (installed 2026-07-29T02:25:06Z)
_ws="$(git rev-parse --show-toplevel 2>/dev/null)" && [ -n "$_ws" ] && sh "$_ws/.tools/git-hooks/stitch-refresh-post-commit.sh"
```

**POSITIVE CONTROL — the four entries that had to survive, each named rather than counted:**
```
closeout-comp-state-post-commit.sh
deploy-pipescript-check-post-commit.sh
missions-refresh-post-commit.sh
prd-header-notify-post-commit.sh
```
A bare count of 4 would not have shown *which* four; naming them is what makes "the pair went and
nothing else did" a measurement rather than an assertion.

**Method notes, because two of these would have failed quietly:**
- The pair was located **by CONTENT** and asserted **adjacent** before removal — never by line
  number, which drifts the moment any other installer appends.
- The write was **byte-level with explicit LF** (0 CRLF before, 0 CRLF after). A text-mode write
  CRLF-ifies files on this box, and this is a POSIX `sh` script.
- **`sh -n` was run as well as `bash -n`**: the shebang is `#!/bin/sh`, so `bash -n` alone would
  have validated an interpreter the hook does not use.
- Backup taken before the edit. The installer remains on disk under F-9's tombstone — **reversible**.

---

## 2. THE SILENCE TEST

**Trigger commit** — made by `1.0.0_SA_CTO~Z` (msg 20611), because `org/modules/graph/` is outside
this seat's grant (§3):

```
sha    46422191de1a64ff6d8b23a7102c30e9a5000feb
path   org/modules/graph/CALLER_CONTRACT_HAZARD.md   (new file, 55 insertions)
       ^ confirmed TRIGGER-CLASS against the hook's own regex:
         ^(portal($|/)|data/.*/scripts/|org/modules/graph/|infra/aws/globgrph/(derive_stitch|extract_portal_stitch)\.py)
instant 2026-09-09T20:11:01Z        window +120s = 20:13:01Z
```

**Process check** — native (`Win32_Process`), self-excluded:
```
stitch-refresh matches : NONE
POSITIVE CONTROL 'python' : 29 processes  -> the query discriminates
```
MSYS `ps` was **discarded** as an instrument here: its first run matched the grep's own command
text, and it cannot see native Windows processes in any case.

**S3 marker** — `s3://opal-313476888478-globgrph/stitch/stitch_marker.json`, read with
`s3api head-object` (explicit UTC; `s3 ls` renders local time and was not used):

| read at | LastModified | ETag |
|---|---|---|
| baseline 19:57Z | `2026-09-09T19:55:15+00:00` | `00dd8c738f236f2bafa9a84d04d0fd44` |
| 20:12:52Z (+111s) | `2026-09-09T19:55:15+00:00` | `00dd8c738f236f2bafa9a84d04d0fd44` |
| 20:14:34Z (+213s) | `2026-09-09T19:55:15+00:00` | `00dd8c738f236f2bafa9a84d04d0fd44` |

**UNMOVED across the whole window.**

### ⛔ THE DISCRIMINATOR — AND WHY "LastModified DID NOT MOVE" IS NOT SUFFICIENT ON ITS OWN

The ask's step 3 scores this on the timestamp. **That criterion cannot distinguish the two
producers.** CodeBuild (`opal-stitch-produce`) is a *legitimate* writer of this same key and can
fire inside any 120-second window — a healthy cloud run would move the timestamp and be scored as a
site-Z violation.

**The sound discriminator is the marker's own `producer` and `git_sha` fields**, and they settle it
more strongly than the timestamp does:

```
producer : stitch-codebuild
git_sha  : de590a7d0227fb9c14ce35b96dcec86deb68df60
```

Had this clone's hook fired, the marker would carry **`git_sha = 46422191de`** — the sha just
committed — because that is what the local derive stamps. It carries CodeBuild's sha instead. So the
marker is not merely *unwritten*; it is **positively attributable to the one canonical writer**.
That is an [[an-artifact-can-certify-its-own-plane]] read: exhibit a value only one producer could
have written, rather than asserting which one did.

Raised to both fabrics before measuring (bus `3a7fe696`), so the laptop can check whether its own
half passed on the timestamp alone.

### What this record does NOT claim
- It does **not** establish that the hook would have fired *before* removal on this exact commit —
  no pre-removal trigger-class commit was run, and manufacturing one would have meant re-installing
  a shadow producer to watch it overwrite a cloud artifact.
- It does **not** grade the laptop's half.
- Evidence class, disclosed by its author (`1.0.0_SA_CTO~Z`, msg 20611): the trigger commit is
  **hand-made in timing, real in content** — the hazard it documents is genuine, but it did not
  arise from independent work this hour. It is not organic traffic and must not be scored as such.
  That seat also declined to make a larger, more plausible edit nearby that it had judged
  *correct as written* — refusing to manufacture a fix so the test would have more to measure.

---

## 3. WHY THIS SEAT DID NOT MAKE THE TRIGGER COMMIT

`org/modules/graph/` is outside `0.0.0_AB_MSTR~Z`'s grant. Exercised against
`.tools/owned-paths-validate.py` with both controls firing:

```
False  0.0.0_AB_MSTR~Z  org/modules/graph/...              the subject
False  0.0.0_AB_MSTR~Z  infra/aws/globgrph/derive_stitch.py  the other trigger class
False  2.0.0_SA_COO     org/tier0/ledger/LD-9999.md        NEGATIVE CONTROL (documented real refusal)
True   0.0.0_AB_MSTR~Z  org/tier0/ledger/LD-9999.md        POSITIVE CONTROL
True   1.0.0_SA_CTO~Z   org/modules/graph/...              and four other live site-Z seats
```

The only trigger classes this seat *can* write are `data/*/scripts/**` and the `portal` gitlink.
Both were declined **on judgement, not permission**: a throwaway probe in a medallion data tree, or
a submodule bump, to satisfy a test is worse than asking. **Self-granting was the one remedy not
available** — `.owned-paths.yaml`'s own SoD notes forbid a grantee granting itself.

**Routing it was not a workaround:** `.git/hooks` is **per-clone, not per-seat**. Every seat on this
device commits through the file this seat edited, so a commit by `1.0.0_SA_CTO~Z` exercises exactly
the artifact under test.

---

## 4. STANDING

- **Site Z is no longer a live overwriter** of `stitch/stitch_graph.json` or
  `stitch/stitch_marker.json`. Per the carried ruling, site Z was the last one after the laptop's
  lines were removed at ~19:46:3xZ.
- Row **`NFRA_CLDGRPH-S77`** (disarm owner `0.0.0_AB_MSTR` for this half) may be disarmed on the
  removal instant above — acked over the bus (`3a7fe696`) with the measurement, not with the send.
- **INTERIM BINDING HELD:** nobody at this seat runs `.tools/stitch-refresh` by hand until S29
  passes. It has not been run here.

**Push state, measured:** LOCAL. `origin/SITEZ` reads `3054872f2b` by `git ls-remote`; neither
`46422191de` nor this record is an ancestor of it. `0.0.0_AB_MSTR~Z` holds the push and does not
open a window without Andrew's word.
