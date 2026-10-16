import { renderToStaticMarkup } from 'react-dom/server'
import { readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { GatewayView } from './src/pages/gateway/GatewayView'
import { CGROUP_BREAKDOWN } from './src/pages/gateway/gateway.cgroup.fixture'

const css = [
  ...readdirSync('src/styles').filter((f) => f.endsWith('.css')).map((f) => 'src/styles/' + f),
  'src/App.css',
  'src/pages/gateway/gateway.css',
].map((f) => readFileSync(f, 'utf8')).join('\n')
const body = renderToStaticMarkup(<GatewayView data={CGROUP_BREAKDOWN} error={null} />)
writeFileSync(
  process.argv[2],
  `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${css}</style></head><body><div class="mcp-page">${body}</div></body></html>`,
)
console.log('wrote', process.argv[2], body.length)
