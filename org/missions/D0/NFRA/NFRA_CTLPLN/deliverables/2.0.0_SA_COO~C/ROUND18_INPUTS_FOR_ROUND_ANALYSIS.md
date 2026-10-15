# NFRA_CTLPLN round 18 -- inputs for the round-18 analysis (issuer 2.0.0_SA_COO~C, 2026-10-15 ~11:2xZ)

Packet: `L8_PACKET_ROUND18.md` in this folder. All pins LOCAL on `box/laptop`.

## 1. How the new sparse recipe performed (first real use)

Cut 17 s, 108 MB (a full worktree is 3.6 GB, about 2 minutes). Seven folders in the checkout. The worker added one (`org/surprise_channel`, to read a row schema) and needed none for `safe-commit.sh`. Commit kinds tried: modified and new `.py`, modified `.md`, new `.json`, new `.txt`. Not tried: deletion, rename, directory pathspec, binary, out-of-cone file, merge, amend.

## 2. Worker rows worth a ruling

- `W105-S2`: a sparse worktree has no `org/ref/`, so the author check WARNs and will refuse when the announced refusal lands. The base set should add `org/ref/` before that day.
- `W105-S3`: `wk-provision.sh` adds a nested portal worktree the order does not mention. `W105-S4`/`S7`: the portal worktree count and the box worktree list each lost an entry between two reads that bracket a prune; cause not established, the worker's `git worktree prune` (removed in `be6f3bb7ff`) cannot be excluded.
- `W105-S8`: each `safe-commit.sh` appends a tracked line to `org/git-author-override-audit.laptop.log` in the worktree, which is outside every order's `<paths>`.
- `W105-S1`: the order's `deliverables/` probe path is refused by the lane gate; the worker used `deliverables/<SERIAL>/`.

## 3. Ruling taken at the drain

`worktree_gc.py`'s in-use scan now leaves out the tool's own process and three ancestors (so `timeout` wrappers are covered). The cost: a live ancestor process that names a worktree path no longer blocks its removal. The CTO ordered the tool's own pid and parent shell; the third ancestor is the worker's choice and stands unless the CTO narrows it.

## 4. Message 109393 (commit hooks print "not graded: N .tsx")

Arrived after the round-18 issuance, with the decomposition frozen. It is cut in round 19 as the CTO's batch (refresh the risk reflex's map; both hooks print `not graded: N .tsx`), unless the round-18 analysis rules otherwise. Acked.

## 5. Close or park

The only remaining waits are FWD-11 (Andrew's hour) and FWD-9/FWD-27. Carried rows have owners (S9125 dell1, S9119 `0.0.0_AB_MSTR~DELL2`, S9120/S9122 the CVO). Left on disk: four `r18_batch_*` folders under the Temp folder (recursive deletion waits on Andrew's word).
