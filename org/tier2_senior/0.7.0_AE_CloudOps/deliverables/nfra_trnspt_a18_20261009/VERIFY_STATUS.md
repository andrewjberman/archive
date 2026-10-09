# NFRA_TRNSPT a18 live verification status

The targeted `safe-apply` completed with `3 added, 1 changed, 0 destroyed`.

Live readback establishes:

- role name `teams-global-transcripts-second-reader-role` exists;
- trust is exactly `arn:aws:iam::313476888478:user/Opal_Terminal`;
- one attached policy grants only `s3:GetObject` on `opal-data-transcripts/*` and `s3:ListBucket` on the bucket;
- the selected object exists and is encrypted by the transcripts KMS key;
- the live KMS policy matches the recorded expected-after document after sorting AWS principal arrays, whose order the KMS API returns nondeterministically;
- only `NamedReadersUseTheKey` differs from the before-image, by the added second-reader role;
- `DellAgentUsersGenerateDataKey` is unchanged;
- live IAM simulation returns `allowed` for the named role's `s3:GetObject` and `implicitDeny` with no missing context for the unnamed `irpt-ycharts-runner-role`;
- live IAM simulation returns `allowed` for `Opal_Terminal` to assume the new role.

The exact object path is not stored here; `live-verification.json` identifies it only as SHA-256 prefix `364e241a0961`. No object content was retained or printed.

The final exercise leg is held because this laptop has no `Opal_Terminal` credential profile. No new credential was created or read. The terminal-owned real `GetObject` admission and Dell2-owned real refusal were routed as status-only probes.

The tag-authorization wrapper could not retain its saved-plan JSON and attempted an unrelated whole-root replan. Before using its audited override, the exact saved plan passed `comp-tagauthz` with zero candidate instances and the tombstone gate with no match. Audit correlation ID: `20261009T095303Z-3890779`.
