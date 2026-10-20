set -u
R=/opt/irpt-resident/0485393f3a-r34o
for f in SHA256SUMS reports/resident_bindings.json; do echo "V1M $f $(sha256sum $R/$f | cut -d' ' -f1)"; done
