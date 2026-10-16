# ANDREW_DIRECT 2026-10-16 ~06:4xZ -- the /fideles Gmail app password is stored in Secrets Manager

Channel: the laptop `1.0.0_SA_CTO` terminal. Recorded by 1.0.0_SA_CTO, same turn. **No credential value appears in this file or in
any commit.**

## His words, VERBATIM

> go ahead thats fine, store it

He was answering this seat's question whether to store the app password he gave in session.

## The act and its read-back

- Created the Secrets Manager secret `fideles/imap-app-password` in account 313476888478, us-east-1:
  `arn:aws:secretsmanager:us-east-1:313476888478:secret:fideles/imap-app-password-NbjAil`.
- It is a raw string, which `.tools/fideles-watch.py` `app_password()` accepts.
- The value was passed straight to `create-secret`. It was not written to any file.
- Read back with `describe-secret`: Name `fideles/imap-app-password`, 1 version. The value itself was not read back.
- His earlier word on the first credential he gave ("do not save that or commit that anywhere") stands. That credential is
  stored nowhere, and he was advised to change it, because the session transcript holds it.

## Next, owned by dell1 (`/fideles install`, LIVE_ARMS row @f4ff08b6fb)

1. `0.0.0_AB_MSTR~DELL1` sets the User variable `FIDELES_IMAP_SECRET=fideles/imap-app-password`.
2. It runs `python .tools/fideles-watch.py status`. An AWS denial on `secretsmanager:GetSecretValue` for this ARN is a grant to
   ask for, never a zero.
3. It registers the scheduled task; `~DELL2` then does the same as standby.
