# muse's SSH public key -- the record (COMM_ASSIST round 17, item 1; closes row COMM_ASSIST-W8-S7)

Written by `2.0.0_SA_COO~CA`, 2026-10-13 ~22:3xZ. This file holds a FINGERPRINT only; a fingerprint is not a secret and the key body is not
kept in git. Row W8-S7 said the key was in no repo file: the fingerprint is now.

| fact | value | evidence |
|---|---|---|
| fingerprint | `SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ` (ED25519, comment `muse`) | `0.0.0_AB_MSTR` msg 108706 (Andrew passed muse's key at the laptop terminal), repeated in `org/devices/state/laptop/ssh_enable_20261013T004127270Z.json` ("keys added ssh-ed25519 muse") |
| on dell2 | present, listed twice (one distinct key) | CA-h-2's AC3 line, `H2-SSH ok=True ... keys=3 ...` in `deliverables/0.7.0_AE_CloudOps~CA2/REPORT_TO-CA-h-2.md` (commit 161b3cf8b7) |
| on the laptop | the laptop's own key `SHA256:Ysgq86UGf/r7GargduCa/3yzyl6wb0wgKbzUpsc9kMg` is the other distinct key on dell2; the laptop is not muse | `ssh-keygen -lf ~/.ssh/id_ed25519.pub` on the laptop |
| where the key body is | `C:\ProgramData\ssh\administrators_authorized_keys` on each box (line commented `muse`), and `SSH_ADD_MUSE_KEY_all_boxes.txt` on the laptop Desktop (not in git) | MSTR msg 108706 |

**How a later cell pins it.** The receiver pin (`MUSE_ANSWER_PUBKEY`, round 17 CA-i-2) takes the one `ssh-ed25519 AAAA...` line whose fingerprint equals
the one above; the deploy cell reads that line from dell2's key file, prints `ssh-keygen -lf` of the line it chose, and refuses if the fingerprint
differs from this record. A key rotation is a change-managed deploy (PRD v0.7, the stated limit), and this record is updated in the same change.

**Not shown here:** that muse itself can log in to dell2 and read the folder. That is the FWD-6 exercise, Andrew's act, carded on the laptop list.
