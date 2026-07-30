#!/usr/bin/env bash
# STAGED -- DO NOT EXECUTE. Runs only on COO's explicit word, and only AFTER step 1 has LANDED.
#
# AUG-1 ETFS clock, STEP 2 of 2: deploy the per-partner carried-forward disclosure to the RENDERER.
# Owner: 0.7.0_AE_CloudOps~A (assigned COO 20260730T073541Z). Gap found by 0.4.0_DE_ClientPlatform.
#
#   step 1 (0.4.0_DE) : git apply patch @75c66b8733 + safe-commit under DE's author line
#   step 2 (THIS, ME) : re-upload render_month_end.py to ARTIFACT_PREFIX + verify
#
# WHY THIS STEP EXISTS AT ALL -- the failure mode if it is forgotten:
#   The renderer is NOT Terraform-deployed. lambda_function.py:114 has the transient EC2 box
#   `aws s3 cp` it from ARTIFACT_PREFIX **at run time**. So A RE-UPLOAD *IS* THE DEPLOY.
#   If the GO stops at "land the commit": Aug-1 pulls the 2026-07-07 artifact, renders WITHOUT the
#   disclosure, uploads a PDF, sends the email, and exits 0. A GREEN RUN AND A DELIVERED REPORT WITH
#   THE REMEDY ABSENT -- and the run path logs nothing, so nothing records the absence either.
#   DEPLOYED = downloaded AND imported. A commit is neither.
#
# ORDERING IS NOT OPTIONAL AND NOT PARALLELISABLE: the verify compares against the LANDED HEAD blob,
# so step 1's commit must exist first. Budget for it if the GO lands close to the fire.
#
# IF ANDREW DECLINES the disclosure there is NO step 2 -- the deployed artifact stays as it is, which
# is the currently-correct state (in sync with HEAD).

set -euo pipefail

REPO="/cygdrive/c/Users/AndrewBerman/Desktop/ajb_workspace"
SRC="data/etfs/scripts/presentation/render_month_end.py"
BUCKET="opal-313476888478-lambda-artifacts"
KEY="ec2/etfs-reports/render_month_end.py"
TMP="$(mktemp -d)"

# PRE-STATE captured 2026-07-30T07:3xZ, BEFORE any upload -- this is the ROLLBACK TARGET.
# Bucket versioning is ENABLED, so the prior artifact is recoverable by VersionId.
ROLLBACK_VERSION="chTZ82VfoorkM2F7oUOTcTNFyos6JUDu"
ROLLBACK_MD5="d618e3b9931bde32c2d672363f8587ff"
ROLLBACK_SIZE="36767"

cd "$REPO"

echo "=== 0. PRECONDITION: step 1 must have LANDED. Verify, do not assume. ==="
git status --porcelain "$SRC" | grep . && {
  echo "*** STOP: working tree is DIRTY for $SRC. Step 2 verifies against the LANDED blob;"
  echo "*** an uncommitted change means what you would upload is not what landed. Tell COO."
  exit 1
}
echo "  tree clean vs HEAD: OK"
echo "  most recent commit touching the renderer:"
git log --format='    %h %an %ad %s' --date=iso-strict -1 -- "$SRC"
echo "  >> CONFIRM the above is DE's disclosure commit, not an older one. If it is not, STOP."
echo "  disclosure string present in the LANDED blob:"
MSYS_NO_PATHCONV=1 git show "HEAD:$SRC" | grep -c 'carried forward at the last known value' || {
  echo "*** STOP: the landed blob does NOT contain the disclosure. Step 1 did not land what we think."
  exit 1
}

echo "=== 1a. SELF-CHECK THE ASSUMPTION THAT MAKES A BYTE-EXACT COMPARISON VALID ==="
# Do NOT trust a note written hours before the run -- that is precisely how the 49F watch script
# fired a verdict frozen at authoring time. CHECK the attribute AT RUN TIME.
#
# WHY THIS MATTERS: `core.autocrlf` is TRUE in this repo, so a text file WITHOUT an explicit eol
# attribute checks out CRLF while `git show` emits LF -- a pure line-ending delta that reads as a
# content mismatch. (0.4.0_DE hit exactly that on 2026-07-30 and advised normalising before
# comparing.) For THIS file an explicit `eol=lf` attribute OVERRIDES autocrlf, so both sides are LF
# and the comparison is byte-exact.
# **DO NOT ADD A NORMALISATION STEP.** Normalising would mask a REAL CRLF corruption in the uploaded
# artifact -- it weakens the check rather than hardening it. Instead, PROVE no normalisation is needed:
EOL_ATTR="$(MSYS_NO_PATHCONV=1 git check-attr eol -- "$SRC" | awk '{print $NF}')"
echo "  git check-attr eol -> $EOL_ATTR   (core.autocrlf=$(git config --get core.autocrlf || echo unset))"
if [ "$EOL_ATTR" != "lf" ]; then
  echo "*** STOP: this file does NOT carry eol=lf, so a checkout may be CRLF while the blob is LF."
  echo "*** A byte-exact md5 comparison would mismatch SPURIOUSLY and you cannot tell that from real"
  echo "*** corruption on the clock. Do NOT normalise to make it pass -- tell COO and re-scope the verify."
  exit 1
fi
CR_WT="$(tr -cd '\r' < "$SRC" | wc -c)"
CR_BLOB="$(MSYS_NO_PATHCONV=1 git show "HEAD:$SRC" | tr -cd '\r' | wc -c)"
echo "  CR bytes -- working tree: $CR_WT   blob: $CR_BLOB   (both MUST be 0)"
[ "$CR_WT" -eq 0 ] && [ "$CR_BLOB" -eq 0 ] || { echo "*** STOP: CR bytes present despite eol=lf. Tell COO."; exit 1; }

echo "=== 1b. THE LANDED BLOB is the source of truth for this verify ==="
# Verify against the BLOB, never a working-tree read: this is a SHARED worktree that has been swept
# before, so a working-tree copy could carry another agent's concurrent edit and you would md5-verify
# a file that is not what DE committed. (0.4.0_DE made this point explicitly at 105512Z.)
LANDED_MD5="$(MSYS_NO_PATHCONV=1 git show "HEAD:$SRC" | md5sum | awk '{print $1}')"
WT_MD5="$(md5sum "$SRC" | awk '{print $1}')"
echo "  landed blob md5 : $LANDED_MD5"
echo "  working tree md5: $WT_MD5"
[ "$LANDED_MD5" = "$WT_MD5" ] || { echo "*** STOP: tree != landed blob. Do not upload."; exit 1; }

echo "=== 2. PRE-STATE of the live object (prove what we are replacing) ==="
aws s3api head-object --bucket "$BUCKET" --key "$KEY" \
  --query '{ETag:ETag,Size:ContentLength,Modified:LastModified,VersionId:VersionId}' --output json

echo "=== 3. THE UPLOAD (the deploy) ==="
aws s3 cp "$SRC" "s3://${BUCKET}/${KEY}" --content-type text/x-python
echo "  upload returned rc=0 -- WHICH IS NOT THE CLAIM. Verify below."

echo "=== 4. VERIFY: download it BACK and compare to the LANDED blob ==="
# Round-tripping proves TRANSPORT fidelity. `aws s3 cp --quiet` has hung silently in this estate
# before (the aws-shim regression), so an unverified upload rc is never acceptance.
aws s3 cp "s3://${BUCKET}/${KEY}" "$TMP/roundtrip.py" --only-show-errors
RT_MD5="$(md5sum "$TMP/roundtrip.py" | awk '{print $1}')"
echo "  round-trip md5  : $RT_MD5"
echo "  landed blob md5 : $LANDED_MD5"
if [ "$RT_MD5" != "$LANDED_MD5" ]; then
  echo "*** MISMATCH. STOP. DO NOT RETRY BLINDLY. ***"
  echo "*** A mismatched artifact on a PAYMENT PATH at hour ~24 is a STOP, not a loop."
  echo "*** Report to 2.0.0_SA_COO immediately with both hashes."
  echo "*** ROLLBACK (only on COO's word):"
  echo "***   aws s3api copy-object --bucket $BUCKET --key $KEY \\"
  echo "***     --copy-source '${BUCKET}/${KEY}?versionId=${ROLLBACK_VERSION}'"
  echo "***   then re-verify md5 == $ROLLBACK_MD5, size == $ROLLBACK_SIZE"
  exit 1
fi
echo "  TRANSPORT VERIFIED (md5 equal)."

echo "=== 5. CONTENT verify on the DOWNLOADED copy -- the runtime claim, not a file claim ==="
# An md5 match proves the bytes travelled. Grepping the DOWNLOADED artifact for the symbol proves
# the thing the EC2 will actually execute contains the change. (0.7.0_AE base's RAVC point: the
# symbol check on the downloaded copy is the runtime claim; size/md5 alone is only a file claim.)
grep -c 'carried forward at the last known value' "$TMP/roundtrip.py" || {
  echo "*** STOP: md5 matched but the disclosure string is ABSENT from the downloaded artifact."
  echo "*** That would mean the landed blob itself lacks it -- step 1 is wrong, not the upload."
  exit 1
}
echo "  CONTENT VERIFIED: the artifact the EC2 will pull contains the disclosure."

echo "=== 6. REPORT LINE for COO ==="
echo "  STEP 2 COMPLETE: s3://${BUCKET}/${KEY}"
echo "    was  md5 $ROLLBACK_MD5 (version $ROLLBACK_VERSION, 2026-07-07)"
echo "    now  md5 $RT_MD5 == landed HEAD blob, disclosure string present in the downloaded copy"
rm -rf "$TMP"
