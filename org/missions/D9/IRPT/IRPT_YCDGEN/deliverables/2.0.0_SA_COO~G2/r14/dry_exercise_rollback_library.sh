set -u
# Ledger: none (READ of two host files plus writes ONLY inside a new temp directory). IRPT_YCDGEN round 14, cell YCD-c-14.
# A DRY EXERCISE of the st32 rollback's library step (remove_st32_to_st31.sh lines: the kept-copy check, the install of the
# kept copy over the library, the sha256 read) on COPIES in a temp directory. The unit, the real library, the receipt and
# the resident roots are not touched. Operator 0.7.0_AE_CloudOps~YC2 for 2.0.0_SA_COO~G2.
NEW=0485393f3a-st32
REAL=/opt/investor-reporting-ycharts
OLD_LIB=857d90b81960d69a7a6700be6fffe33d86628694aef95f8cfb64aca7a82cb839
NEW_LIB=a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841
UNIT=irpt-analysis-resident.service
echo "X0 at $(date -u +%Y-%m-%dT%H:%M:%SZ) unit active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "X0 real library before: $(sha256sum $REAL/ycharts_session.js | cut -d' ' -f1) kept copy: $(sha256sum $REAL/ycharts_session.js.before-$NEW | cut -d' ' -f1)"
H=$(mktemp -d /tmp/st32-rollback-dry.XXXXXX)
cp -p $REAL/ycharts_session.js $H/ycharts_session.js
cp -p $REAL/ycharts_session.js.before-$NEW $H/ycharts_session.js.before-$NEW
echo "X0 temp dir $H holds: library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) kept $(sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1)"
# ---- the rollback's own three lines, with H pointing at the temp directory
[ "$(sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1)" = "$OLD_LIB" ] || { echo "ERROR: the kept old library is absent or is not st31's; nothing moved"; echo "X1 DRY RESULT: FAIL at the kept-copy check"; rm -rf $H; exit 12; }
install -m 0644 -o root -g root $H/ycharts_session.js.before-$NEW $H/ycharts_session.js
echo "X1 library restored: $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) (want $OLD_LIB)"
[ "$(sha256sum $H/ycharts_session.js | cut -d' ' -f1)" = "$OLD_LIB" ] && echo "X1 DRY RESULT: PASS -- the step leaves st31's library in place of st32's" || echo "X1 DRY RESULT: FAIL -- the restored file is not st31's"
echo "X1 restored file mode and owner: $(stat -c '%a %U:%G' $H/ycharts_session.js) (want 644 root:root)"
# ---- negative control: the same check against a kept copy that is NOT st31's must refuse
cp -p $REAL/ycharts_session.js $H/ycharts_session.js.before-$NEW
[ "$(sha256sum $H/ycharts_session.js.before-$NEW | cut -d' ' -f1)" = "$OLD_LIB" ] && echo "X2 NEGATIVE CONTROL: FAIL -- a wrong kept copy was accepted" || echo "X2 NEGATIVE CONTROL: PASS -- a kept copy that is not st31's is refused before anything moves"
rm -rf $H
echo "X3 temp dir removed: $(test -e $H && echo no || echo yes)"
echo "X3 real library after: $(sha256sum $REAL/ycharts_session.js | cut -d' ' -f1) (want $NEW_LIB) kept copy: $(sha256sum $REAL/ycharts_session.js.before-$NEW | cut -d' ' -f1) (want $OLD_LIB)"
echo "X3 unit active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value) root=$(systemctl show $UNIT -p ExecStart | grep -o '/opt/irpt-resident/[0-9a-z-]*' | head -1)"
echo "END"
