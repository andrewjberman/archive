set -u
# Renderer smoke on the resident host, as the service user. Writes only under /tmp/r6-render-smoke, makes no AWS call, touches no service.
# It runs the same mechanism render_pdf.cjs uses (playwright-core, headless Chromium, set HTML from a local string, page.pdf) with
# IRPT_PLAYWRIGHT_CORE set the way the branch B install will set it.
T=/tmp/r6-render-smoke
rm -rf $T; mkdir -p $T; chmod 777 $T
cat > $T/smoke.cjs <<'JS'
const fs = require('node:fs')
const core = process.env.IRPT_PLAYWRIGHT_CORE
if (!core) throw new Error('IRPT_PLAYWRIGHT_CORE unset')
const pkg = JSON.parse(fs.readFileSync(core + '/package.json', 'utf8'))
console.log('playwright-core version', pkg.version)
const { chromium } = require(core)
;(async () => {
  const channel = process.env.IRPT_CHROMIUM_CHANNEL || 'msedge'
  let browser, how
  try { browser = await chromium.launch({ channel, headless: true }); how = 'channel ' + channel } catch (first) {
    try { browser = await chromium.launch({ headless: true }); how = 'bundled chromium (channel ' + channel + ' failed: ' + first.message.split('\n')[0].slice(0, 90) + ')' } catch (second) {
      console.log('NO BROWSER:', second.message.split('\n')[0].slice(0, 200)); process.exit(3)
    }
  }
  console.log('launched via', how, 'browser version', browser.version())
  const page = await browser.newPage()
  await page.setContent('<html><body><h1>Opal smoke</h1><p>Not available in this version.</p></body></html>')
  await page.pdf({ path: '/tmp/r6-render-smoke/out.pdf', format: 'Letter', printBackground: true })
  await browser.close()
  const b = fs.readFileSync('/tmp/r6-render-smoke/out.pdf')
  console.log('pdf bytes', b.length, 'header', b.slice(0, 5).toString())
})().catch(e => { console.log('FAILED', e.message.split('\n')[0].slice(0, 240)); process.exit(4) })
JS
chmod 644 $T/smoke.cjs
echo "--- as ec2-user, IRPT_PLAYWRIGHT_CORE set (the branch B install's line):"
sudo -u ec2-user env IRPT_PLAYWRIGHT_CORE=/opt/investor-reporting-ycharts/node_modules/playwright-core HOME=/home/ec2-user timeout 120 node $T/smoke.cjs 2>&1 | tail -8
echo "rc=$?"
echo "--- control: without the variable (what the unit does today):"
sudo -u ec2-user HOME=/home/ec2-user timeout 30 node $T/smoke.cjs 2>&1 | tail -2
ls -la $T | tail -3
rm -rf $T
echo "smoke dir removed"
