// W58 (DSGN_IRPTV1 TO-IV-e-103): does the ~53 driver's oneBody() change the all-accounts body it later serves?
// Replicates oneBody() from holdings-face-driver.mjs verbatim; MODE=shared is the ~53 line, MODE=copied is the fixed line.
import { readFileSync } from 'node:fs'
const [fixturePath, mode] = process.argv.slice(2)
const fixtures = JSON.parse(readFileSync(fixturePath, 'utf8'))
const HKEY = Object.keys(fixtures).find((key) => key.includes('/holdings/'))
const ALL_BODY = fixtures[HKEY]
const ACCOUNT_NODES = ALL_BODY.data.nodes.filter((n) => n.parent_node_id === null)
const show = (label) => console.log(label, JSON.stringify(ALL_BODY.data.nodes.filter((n) => n.node_id.endsWith('-SEC') || n.node_id.endsWith('-CLI')).map((n) => [n.node_id, n.amount.value, n.amount.denominator.value, n.percentages.of_total])))
const oneBody = (k) => {
  const nodes = ALL_BODY.data.nodes
  const body = JSON.parse(JSON.stringify(ALL_BODY))
  const keep = new Set([ACCOUNT_NODES[k].node_id])
  for (let grew = true; grew;) { grew = false; for (const n of nodes) if (!keep.has(n.node_id) && keep.has(n.parent_node_id)) { keep.add(n.node_id); grew = true } }
  body.data.nodes = nodes.filter((n) => keep.has(n.node_id))
  if (mode === 'copied') body.data.nodes = body.data.nodes.map((n) => JSON.parse(JSON.stringify(n)))
  const total = body.data.nodes[0].amount.value
  for (const n of body.data.nodes) { n.amount.denominator.value = total; n.percentages.of_total = n.amount.value / total }
  return body
}
show('ALL_BODY before oneBody:')
ACCOUNT_NODES.map((_, k) => oneBody(k))
show('ALL_BODY after  oneBody (' + mode + '):')
const sgm = ALL_BODY.data.nodes.filter((n) => n.node_id.endsWith('-SEC')).reduce((s, n) => s + n.percentages.of_total, 0)
console.log('SGM1 of_total sum across both accounts in the served all-accounts body =', sgm)
