# NFRA_FIDUPL.TO-FT-s-6 -- the per-G list secret version the schedule will be enabled against

Author 0.7.0_AE_CloudOps~NFRA1, 2026-10-21. No secret value appears in this file; the value was never read (describe-secret only).

secret: fidelity/alongside/perg-list
current_version_id: 8473b6cf-e3c0-4b5b-8dcc-94480a41b57b (stage AWSCURRENT, the only version)
current_version_short: 8473b6cf
read_at: 2026-10-21T02:13:38Z (describe-secret VersionIdsToStages; LastChangedDate 2026-10-20T22:13:23-04:00 = 2026-10-21T02:13:23Z)
before_the_seed: the secret had no version (describe-secret VersionIdsToStages None, read at the FU-s-13 apply)

## The seed run (step 2, once, no retry)

command: /opt/fidelity-uploader/venv/bin/python /opt/fidelity-uploader/perg_seed.py, through SSM on i-028e830f7226cc685 (command id e23c793b-1295-4f4d-a86f-c223b2ae5de3), started after the issuer's GO at 02:10Z
status: Success, exit=0
counts line, verbatim:

    OK: listed=31 distinct_firms=8 unattributed=1

## Step 1b (config pointer)

/opt/fidelity-uploader/config.json gained one line, "perg_secret_id" (the secret's name above); backup /opt/fidelity-uploader/config.json.bak-20261021; the file is valid JSON (venv python -m json.tool); key names now: perg_secret_id profile_dir quo_line_id quo_secret_id quo_sender region repo_root scope wealthscape_secret_id work_dir.

## Not done

Step 4 (the three schedule rules ON) is held for the issuer's ENABLE after the CTO countersign. No schedule, rule, or automation was touched.
