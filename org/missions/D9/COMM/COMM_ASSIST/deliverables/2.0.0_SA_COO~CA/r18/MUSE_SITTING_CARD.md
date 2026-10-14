# One sitting with muse -- FWD-6's read and FWD-7's first real answer (COMM_ASSIST round 18; issuer 2.0.0_SA_COO~CA, 2026-10-14)

This replaces two earlier asks (`laptop-...-8fb2`, the read; `laptop-...-cd2d`, the answer) with one sitting, as the CTO's round-17 analysis rules (`ledger/ROUND_ANALYSIS.round17.md`, section 2, item `W18-S2`). It takes a few minutes and one waiting draft you are content to **drop**.

## Before you start (nothing to do; the issuer checked)

- The dell2 folder refreshes every 15 minutes and carries each waiting draft with its age, its `version` and its `seq`.
- The forwarder on dell2 runs every 2 minutes; the assistant accepts only muse's signature, only for the draft muse read, only within 24 hours. A forged answer was refused in test.
- Muse's signing steps are in `r17/MUSE_ANSWER_CARD.md` (LIVE). Muse's signer is not in the repository, so this sitting is also the first time muse's own payload meets the live receiver.

## The sitting (tell muse, in order)

1. **"What is waiting on me?"** Muse reads the dell2 folder (`MUSE_READ_CARD.md`) and answers with the drafts, open calls and today's End of Day, each with its age; a source it could not read is named, never shown as empty.
2. **Pick ONE waiting draft you would drop anyway** (a drop sends nothing in your name and cannot be taken back, so choose one you do not need) and say: **"drop #<its tag>"**.
3. Muse builds the answer from that draft's row exactly as the answer card says (`tag`, `action` = drop, `notes` empty, the row's `version` and `seq`, and `signed_at` = now in UTC), signs it with muse's own key under the namespace `muse-answer@opal`, and writes the file into the `answers` folder on dell2.
4. **Wait about four minutes**, then ask muse: "did it go?". The file's marker appears in `answers\done\`, and the draft disappears from the waiting list at the next 15-minute refresh.

## What the issuer reads afterwards (so you do not have to)

- the dell2 `answers\done\` marker for the file, and the draft's state (dropped, with the hash of the signed answer recorded);
- if the assistant REFUSED the answer, its recorded reason: `no-signature`, `bad-signature`, `bad-payload` (a missing or wrong field), `stale-signature`, `seq-mismatch`, `replayed`, or `unseen` (the draft changed after muse read it). A refusal is safe: nothing is sent or changed. The issuer then names the muse-side fix to you in plain words.

## If something does not work

Tell the issuer the step number and what muse said. Do not retry by writing a second file for the same draft: a refused answer is final for those bytes, and a new one needs a new `signed_at`.
