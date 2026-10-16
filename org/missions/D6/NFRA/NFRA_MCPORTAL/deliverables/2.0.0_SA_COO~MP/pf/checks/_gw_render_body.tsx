// MP-pf-9 real-run helper (the issuer's). COPIED into the mcportal checkout as .pf9_render.tsx and run there with bun, so it resolves react and the page from that tree.
// argv[2] = output html. argv[3] = the SERVED breakdown body as JSON (holders already redacted by s1_served_body.sh). Prints only a count, never a name.
import { renderToStaticMarkup } from 'react-dom/server'
import { readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { GatewayView } from './src/pages/gateway/GatewayView'

const data = JSON.parse(readFileSync(process.argv[3], 'utf8'))
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
console.log('rendered served body: channels', data.channels.length, 'bytes', body.length)
