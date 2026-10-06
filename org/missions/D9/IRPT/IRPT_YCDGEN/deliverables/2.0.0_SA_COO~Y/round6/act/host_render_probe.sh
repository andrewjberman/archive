set -u
# READ-ONLY probe of the resident host for the Opal producer's renderer (render_pdf.cjs: node, playwright-core, a Chromium). Writes nothing.
echo "PROBE $(date -u +%FT%TZ)"
echo "node: $(command -v node) $(node --version 2>&1 | head -1)"
H=/opt/investor-reporting-ycharts
ls -la $H 2>&1 | head -20
echo "--- playwright-core directories:"
find /opt /usr/lib/node_modules /home -maxdepth 7 -type d -name playwright-core 2>/dev/null | head -5
echo "--- browsers:"
ls -d /home/*/.cache/ms-playwright/* /root/.cache/ms-playwright/* /opt/*/ms-playwright* 2>/dev/null | head -8
for b in chromium chromium-browser google-chrome google-chrome-stable microsoft-edge msedge; do command -v $b >/dev/null 2>&1 && echo "bin: $b -> $(command -v $b)"; done
echo "--- unit environment:"
systemctl show irpt-analysis-resident.service -p Environment 2>&1 | cut -c1-300
echo "--- memory and disk:"
free -m | head -2
df -h /tmp | tail -1
echo "--- git on the host: $(command -v git || echo none)"
