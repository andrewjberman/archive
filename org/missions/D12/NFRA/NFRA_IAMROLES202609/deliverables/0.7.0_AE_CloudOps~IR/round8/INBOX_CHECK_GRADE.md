# INBOX_CHECK_GRADE -- NFRA_IAMROLES202609.TO-IAM-y-1: the Z-S42 disarm, graded

**Cell:** IAM-y-1 (round 8, E1 -- FIRST, before any WORLD act of this project).
**Executed by:** `0.7.0_AE_CloudOps~IR`. **GO:** the round-8 issuance @`e27d52cb19`.
**Form recorded in:** `.claude/skills/cloud-ops/SKILL.md`, new subsection **18a**, beside rule 18's HALT-gate
caveat. **Measured:** 2026-10-11 ~15:3xZ. **LOCAL: no AWS write.**

---

## 1. THE REQUIRED LINES

```
CHECK-NEGATIVE: ERROR: inbox path absent: org/mcp/inbox/0.7.0_AE_CloudOps/~IR -- this is NOT an empty inbox
CHECK-POSITIVE: unread=1
```

## 2. THE NEGATIVE -- run from a LINKED WORKTREE, which is the Z-S42 case

Run in `C:/tmp/iam-w1b` (a linked worktree: `.git` is a FILE pointing at the main gitdir), with the
worktree-relative path -- exactly the shape the old check was cited with in three round-7 apply records.

```
$ cd /c/tmp/iam-w1b
$ INBOX="org/mcp/inbox/0.7.0_AE_CloudOps/~IR"
$ test -d "$INBOX" || { echo "ERROR: inbox path absent: $INBOX -- this is NOT an empty inbox"; exit 2; }
ERROR: inbox path absent: org/mcp/inbox/0.7.0_AE_CloudOps/~IR -- this is NOT an empty inbox
exit 2 (non-zero)
```

**THE OLD FORM, ON THE SAME PATH IN THE SAME SHELL, FOR CONTRAST:**

```
$ ls -1 "$INBOX" 2>/dev/null | grep -vc '^read$'
0
```

**`0` -- indistinguishable from an empty inbox.** That single character is the whole of Z-S42: the path is not
checked out in a worktree, and rule 14b is what sends a seat to a worktree in the first place, so this was the
normal case rather than an edge.

## 3. THE POSITIVE CONTROL -- and it is the half the negative cannot establish

A guard that ERRORs on everything would pass section 2 and be worthless. So a message was **planted**
(`send_message` to myself, subject `Z-S42 control`, id **33322**) and the PRIMARY limb -- the broker read,
counting every row not `READ` -- was taken **before** any ack:

```
$ get_delivery_state("0.7.0_AE_CloudOps~IR")
  [SENT] id=33322  2026-10-11T15:31:30Z  0.7.0_AE_CloudOps~IR -> 0.7.0_AE_CloudOps~IR
         subj: Z-S42 control            SENT@15:31:31Z
  [READ] id=33318  ... GO round 8 ...   READ@15:24:11Z by 0.7.0_AE_CloudOps~IR
  TOTALS: READ=2, SENT=1  (denominator 3)      -> rows NOT READ = 1
```

then acked, and re-read:

```
  [READ] id=33322  ... READ@2026-10-11T15:39:56Z by 0.7.0_AE_CloudOps~IR
  TOTALS: READ=2  (denominator 2)              -> rows NOT READ = 0
```

**The 1 -> 0 TRANSITION ACROSS THE ACK IS THE PROOF, not the 1 on its own.** It shows the limb tracks
READERSHIP rather than file location, which is the property the whole disarm needs.

### 3a. WHY THE FILE PLANE COULD NOT HAVE DONE THIS -- measured at the same moment

The live Monitor `mv`d the planted message into `read/` **within seconds** of delivery, emitting its `[INBOX]`
event. So at the instant the broker read `1 unread`:

| plane | reading, with a delivered and unacked message |
|---|---|
| broker (primary limb) | **1 not READ** -- correct |
| the message's own location | **already in `read/`** |
| message files directly in the lane inbox | **0** |

**A file-based check goes quiet exactly when mail arrives**, because the watcher moves it before any agent sees
it. That is the `ADHC_HALTGT` orphan shape with a *healthy* watcher, and it is why the broker read is the
primary limb rather than a nicety.

## 4. A DEFECT IN THE FALLBACK FORM THE ORDER SPECIFIED -- found while grading it

The cell specifies the fallback as *"`test -d` ... then `ls -A`, counting files other than `read/`"*. **Run
literally, that counts 3 against an inbox holding ZERO messages:**

```
$ ls -A "$INBOX" | grep -v '^read$'
.unread-deliveries
.watcher.owner
read/                 <- STILL THERE
```

**ROOT CAUSE, and it is the real mechanism behind Z-S42's over-count:** `ls` is aliased here to
**`ls -F --color=auto --show-control-chars`**, and `-F` appends `/` to a directory. So `ls -A` emits `read/`
and `grep -v '^read$'` cannot match it. **The alias defeats `ls -1` and `ls -A` identically** -- switching one
for the other fixes nothing. The two state dotfiles then add two more.

A guard that always reads 3 **cannot fail toward clean**, so it satisfies the cell's stated goal -- but it is a
tripwire that is **always tripped**, and a seat will learn to ignore it. That is a different failure with the
same ending.

**SO THE RECORDED FORM USES `find`, which the rendering cannot fool, and prints BOTH counts:**

```bash
echo "unread=$(find "$INBOX" -maxdepth 1 -type f -name '2026*.md' | wc -l) \
      state_markers=$(find "$INBOX" -maxdepth 1 -type f ! -name '2026*.md' | wc -l)"
# from the main tree, right now:   unread=0 state_markers=2
```

`-type f` excludes `read/` regardless of how it is rendered; the name pattern separates messages from state
markers; and printing both means the number carries its denominator. **This is a deliberate departure from the
cell's literal text, in the direction of its stated intent, and it is reported to the issuer rather than
absorbed** -- the issuer wrote that form and has a defect in it worth knowing about.

## 5. WHAT THE FORM IS, AS RECORDED IN `cloud-ops` 18a

1. **PRIMARY:** `get_delivery_state(<full lane serial>)`, counting every row not `READ`. Sound from any tree;
   survives a live Monitor; `READ` is the only state that claims an AGENT saw a message.
2. **FALLBACK, only if the broker is unreachable:** `test -d` the **REAL** inbox path under the **MAIN**
   workspace root, then the `find` form above. **A missing path is an ERROR, printed, non-zero exit -- NEVER a
   `0`.**

Cost: one broker call. Non-application: a seat that is not `~lane`-scoped can be halted and has HALTGT.

## 6. WHAT THIS GRADE DOES NOT CLAIM

- **It does not re-verify the three round-7 applies.** Those were checked after the fact by reading the
  directory with `ls -a`, and no round-7 apply was taken over unread mail. The defect was in the evidence, not
  the acts, and that finding stands in Z-S42 rather than being re-litigated here.
- **It does not claim the broker limb cannot fail.** If the broker is unreachable the primary limb is simply
  unavailable, which is why limb (b) exists and why its missing-path case ERRORs instead of reading clean.
- **It does not touch `safe-apply.sh`.** The cell's BOUNDS are the skill text and this file; wiring the check
  into the wrapper would be a different act with a different blast radius.
