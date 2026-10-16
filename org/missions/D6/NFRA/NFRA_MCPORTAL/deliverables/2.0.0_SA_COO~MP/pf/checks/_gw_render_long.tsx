// MP-pf-8 check helper (the issuer's). COPIED into the mcportal worktree as .pf8_render.tsx and run there with bun, so it resolves react and the page from that tree.
// argv[2] = output html. argv[3] = "long" (every channel and tool index list gets one REAL-LENGTH unbroken name) or "short" (the fixture as checked in, the control).
// The long name is the real one measured on the served body: opal_data_assets_silver_commonwealth_cottonwood_account_day_value, 65 characters.
import { renderToStaticMarkup } from 'react-dom/server'
import { readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { GatewayView } from './src/pages/gateway/GatewayView'
import { CGROUP_BREAKDOWN } from './src/pages/gateway/gateway.cgroup.fixture'

const LONG = 'opal_data_assets_silver_commonwealth_cottonwood_account_day_value'
const mode = process.argv[3] || 'long'
const data = JSON.parse(JSON.stringify(CGROUP_BREAKDOWN))
if (mode === 'long') {
  for (const c of data.channels) {
    c.indexes = [...(c.indexes || []), LONG]
    for (const t of c.tools || []) t.indexes = [...(t.indexes || []), LONG]
  }
}
const css = [
  ...readdirSync('src/styles').filter((f) => f.endsWith('.css')).map((f) => 'src/styles/' + f),
  'src/App.css',
  'src/pages/gateway/gateway.css',
].map((f) => readFileSync(f, 'utf8')).join('\n')
const body = renderToStaticMarkup(<GatewayView data={data} error={null} />)
writeFileSync(
  process.argv[2],
  `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${css}</style></head><body><div class="mcp-page">${body}</div></body></html>`,
)
console.log('rendered', mode, 'bytes', body.length)
