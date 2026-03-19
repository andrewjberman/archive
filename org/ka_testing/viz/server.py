#!/usr/bin/env python3
"""
Live telemetry dashboard — watches event JSONL and streams to browser.

Usage:
    python server.py <path-to-events-dir>
    python server.py system/registry/macros/MAIN/projects/CREATE/v0001/events

Opens http://localhost:8111 with live agent boxes, KF stage tracking,
tool call streams, and real-time token counters.
"""

import http.server
import json
import os
import sys
import threading
import time
from pathlib import Path

PORT = 8111
events_dir = None
jsonl_path = None


def find_jsonl(d):
    """Find the *-events.jsonl file in the events directory."""
    p = Path(d)
    for f in sorted(p.glob("*-events.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        return f
    return None


def poll_events():
    """Read all events from JSONL, return as list of dicts."""
    global jsonl_path
    # Re-check for new JSONL if none found yet
    if (not jsonl_path or not jsonl_path.exists()) and events_dir:
        jsonl_path = find_jsonl(events_dir)
    if not jsonl_path or not jsonl_path.exists():
        return []
    events = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode())
        elif self.path == "/api/events":
            events = poll_events()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(events).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Runtime Telemetry</title>
<style>
:root {
  --bg: #0a0a0a; --bg1: #111; --bg2: #0d0d0d; --border: #222; --border-active: #4fc3f7;
  --text: #e0e0e0; --dim: #666; --bright: #fff;
  --blue: #4fc3f7; --green: #81c784; --orange: #ffb74d; --red: #ef9a9a;
  --purple: #ce93d8; --cyan: #4dd0e1;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'Consolas','Monaco','Menlo',monospace; font-size: 12px; }

/* Top bar */
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; border-bottom: 1px solid var(--border); background: var(--bg1); position: sticky; top: 0; z-index: 10; }
.topbar h1 { font-size: 13px; color: var(--dim); letter-spacing: 2px; }
.totals { display: flex; gap: 20px; }
.tbox { text-align: center; }
.tbox .label { font-size: 9px; color: var(--dim); text-transform: uppercase; letter-spacing: 1px; }
.tbox .val { font-size: 18px; font-weight: bold; }
.tbox .val.tok { color: var(--blue); }
.tbox .val.cost { color: var(--orange); }
.tbox .val.time { color: var(--green); }
.tbox .val.cnt { color: var(--purple); }

/* Layout */
.main { display: flex; height: calc(100vh - 44px); }
.left { flex: 1; overflow-y: auto; padding: 8px; border-right: 1px solid var(--border); min-width: 0; }
.right { width: 420px; min-width: 420px; overflow-y: auto; padding: 8px; display: flex; flex-direction: column; }

/* Agent cards */
.agent-card { background: var(--bg1); border: 1px solid var(--border); border-radius: 4px; margin-bottom: 8px; overflow: hidden; }
.agent-card.running { border-color: var(--blue); }
.agent-card.complete { border-color: #388e3c; }
.agent-card.failed { border-color: #d32f2f; }
.agent-card.waiting { border-color: var(--orange); border-style: dashed; }

.card-head { display: flex; justify-content: space-between; align-items: center; padding: 6px 10px; background: rgba(255,255,255,0.02); }
.card-name { font-weight: bold; color: var(--bright); font-size: 13px; }
.card-badge { font-size: 10px; padding: 1px 6px; border-radius: 3px; }
.card-badge.running { background: #0d47a1; color: var(--blue); }
.card-badge.complete { background: #1b5e20; color: var(--green); }
.card-badge.failed { background: #b71c1c; color: var(--red); }
.card-badge.waiting { background: #4a3800; color: var(--orange); }

/* Metrics grid */
.metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px 8px; padding: 6px 10px; }
.m { }
.m .ml { font-size: 9px; color: var(--dim); text-transform: uppercase; }
.m .mv { font-size: 14px; color: var(--text); }
.m .mv.hi { color: var(--blue); }

/* KF Stage bar */
.stage-bar { display: flex; height: 20px; margin: 0 10px 4px; border-radius: 3px; overflow: hidden; background: #1a1a1a; }
.stage-seg { display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: bold; color: rgba(255,255,255,0.7); transition: flex 0.3s; min-width: 0; }
.stage-seg.Pe { background: #1565c0; }
.stage-seg.In { background: #6a1b9a; }
.stage-seg.Ac { background: #2e7d32; }
.stage-seg.Ad { background: #e65100; }
.stage-seg.active { outline: 2px solid var(--bright); outline-offset: -2px; }
.stage-seg.done { opacity: 0.5; }

/* Tool stream inside card */
.tool-stream { max-height: 140px; overflow-y: auto; padding: 4px 10px 6px; font-size: 11px; border-top: 1px solid var(--border); }
.tool-line { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.6; }
.tool-line .iter { color: var(--dim); }
.tool-line .stage { font-weight: bold; }
.tool-line .stage.Pe { color: #42a5f5; }
.tool-line .stage.In { color: #ab47bc; }
.tool-line .stage.Ac { color: #66bb6a; }
.tool-line .stage.Ad { color: #ff7043; }
.tool-line .tname { color: var(--orange); }
.tool-line .tpath { color: var(--green); }
.tool-line .fail { color: var(--red); }
.tool-line .block { color: var(--red); font-weight: bold; }
.tool-line .tok { color: var(--dim); }

/* Right panel: event stream */
.event-title { font-size: 11px; color: var(--dim); text-transform: uppercase; letter-spacing: 1px; padding: 4px 0 6px; }
.event-stream { flex: 1; background: var(--bg2); border: 1px solid var(--border); border-radius: 4px; padding: 6px; overflow-y: auto; font-size: 11px; }
.ev { white-space: nowrap; line-height: 1.6; overflow: hidden; text-overflow: ellipsis; }
.ev .seq { color: #555; }
.ev .ts { color: #444; }
.ev .et { color: var(--blue); }
.ev .et.fail { color: var(--red); }
.ev .et.interrupt { color: var(--orange); }
.ev .et.hook { color: var(--purple); }
.ev .et.tool { color: var(--dim); }
.ev .ag { color: var(--purple); }
.ev .info { color: #777; }
</style>
</head>
<body>

<div class="topbar">
  <h1>RUNTIME TELEMETRY</h1>
  <div class="totals">
    <div class="tbox"><div class="label">Input</div><div class="val tok" id="t-in">0</div></div>
    <div class="tbox"><div class="label">Output</div><div class="val tok" id="t-out">0</div></div>
    <div class="tbox"><div class="label">Total</div><div class="val tok" id="t-tot">0</div></div>
    <div class="tbox"><div class="label">Cost</div><div class="val cost" id="t-cost">$0.00</div></div>
    <div class="tbox"><div class="label">Wall</div><div class="val time" id="t-wall">--</div></div>
    <div class="tbox"><div class="label">Agents</div><div class="val cnt" id="t-agents">0</div></div>
    <div class="tbox"><div class="label">Events</div><div class="val cnt" id="t-events">0</div></div>
  </div>
</div>

<div class="main">
  <div class="left" id="agents"></div>
  <div class="right">
    <div class="event-title">Event Stream</div>
    <div class="event-stream" id="events"></div>
  </div>
</div>

<script>
const POLL = 800;
const CI = 3.0/1e6, CO = 15.0/1e6; // sonnet pricing
let seq = 0, agents = {}, pStart = null;
const fmt = n => n.toLocaleString();

function key(e) {
  // For tool/iteration events with no identity, attach to last active worker
  if (!e.identity && !e.serial && (e.event_type||'').startsWith('llm.')) {
    for (const [k,a] of Object.entries(agents)) { if (a.status === 'running' && a.role === 'worker') return k; }
  }
  return e.identity || e.serial || e.node || 'SYS';
}

function proc(e) {
  const k = key(e), d = e.detail||{}, et = e.event_type||'';
  if (et === 'project.started') { pStart = new Date(e.timestamp); return; }
  if (et === 'project.completed' || et === 'project.failed') return;

  if (!agents[k] && k !== 'SYS' && !et.startsWith('project.')) {
    agents[k] = { name: e.serial||e.identity||k, node: e.node||'', role: e.node||'', status: 'running',
      inTok: 0, outTok: 0, wall: 0, iter: 0, maxIter: 0, tools: 0,
      stage: '', stageProgress: {Pe:0,In:0,Ac:0,Ad:0}, stageBudget: {Pe:0,In:0,Ac:0,Ad:0},
      blocked: 0, activity: [] };
  }
  const a = agents[k]; if (!a) return;

  if (et === 'node.started') {
    a.status = 'running'; a.node = e.node||a.node; a.role = e.node||a.role;
    a.activity.push({s:'',t:'Started: '+(d.summary||e.node),c:''});
  }
  else if (et === 'node.completed') {
    a.status = 'complete';
    if (d.wall_time_s) a.wall += d.wall_time_s;
    if (d.input_tokens) a.inTok = Math.max(a.inTok, d.input_tokens);
    if (d.output_tokens) a.outTok = Math.max(a.outTok, d.output_tokens);
    if (d.llm_iterations) a.iter = d.llm_iterations;
    a.activity.push({s:'',t:'DONE wall='+fmt(d.wall_time_s||0)+'s tok='+fmt((d.input_tokens||0)+(d.output_tokens||0)),c:'done'});
  }
  else if (et === 'node.failed') {
    a.status = 'failed';
    a.activity.push({s:'',t:'FAILED: '+(d.error||d.summary||'').slice(0,80),c:'fail'});
  }
  else if (et === 'llm.iteration') {
    a.inTok = d.cumulative_input || a.inTok;
    a.outTok = d.cumulative_output || a.outTok;
    a.iter = d.iteration || a.iter;
    a.maxIter = d.max_iterations || a.maxIter;
    a.status = 'running';
    const st = d.stage || '';
    if (st && st !== a.stage) a.stage = st;
    if (st) { a.stageProgress[st] = (a.stageProgress[st]||0) + 1; }
    // Detect budget from max_iterations spread
    if (a.maxIter && !a.stageBudget._set) {
      // Will be overwritten by actual data as stages progress
    }
    const stop = d.stop_reason||'';
    const tokStr = `in=${fmt(d.input_tokens||0)} out=${fmt(d.output_tokens||0)}`;
    a.activity.push({s:st, t:`iter ${d.iteration||'?'} | ${tokStr}${stop?' | stop='+stop:''}`, c:stop==='tool_use'&&d.iteration>=a.maxIter?'fail':''});
  }
  else if (et === 'llm.tool_call') {
    a.tools++;
    const nm = d.tool_name||'?', fp = (d.tool_path||'').split('/').pop()||'';
    const ok = d.success !== false;
    const st = d.stage||a.stage||'';
    a.activity.push({s:st, t: nm+'('+fp+')' + (ok?'':' FAIL'), c:ok?'tool':'fail'});
  }
  else if (et === 'hook.audit') {
    // silent
  }
  else if ((et||'').startsWith('hook.')) {
    a.activity.push({s:'',t:'HOOK: '+(d.summary||et),c:'block'});
    if (d.hook_point === 'PreToolUse') a.blocked++;
  }
  else if (et === 'interrupt.fired') {
    a.status = 'waiting';
    a.activity.push({s:'',t:'WAIT: '+(d.message||d.authority_type+'/'+d.sub_type).slice(0,60),c:'block'});
  }
  else if (et === 'interrupt.resumed') {
    a.status = 'running';
    a.activity.push({s:'',t:'Resumed: '+(d.summary||''),c:''});
  }
  if (a.activity.length > 50) a.activity = a.activity.slice(-40);
}

function renderAgents() {
  const c = document.getElementById('agents');
  c.innerHTML = '';
  const sorted = Object.entries(agents).sort((a,b) => {
    const order = {running:0,waiting:1,complete:2,failed:3};
    return (order[a[1].status]||9) - (order[b[1].status]||9);
  });
  for (const [k,a] of sorted) {
    const d = document.createElement('div');
    d.className = 'agent-card ' + a.status;

    // KF stage bar
    const stages = ['Pe','In','Ac','Ad'];
    const totalProg = stages.reduce((s,st) => s + (a.stageProgress[st]||0), 0);
    let stageBar = '';
    if (totalProg > 0) {
      stageBar = '<div class="stage-bar">';
      for (const st of stages) {
        const n = a.stageProgress[st]||0;
        if (n === 0 && st !== a.stage) continue;
        const pct = Math.max(8, Math.round(n / Math.max(1,totalProg) * 100));
        const cls = st + (st===a.stage?' active':'') + (stages.indexOf(st)<stages.indexOf(a.stage)?' done':'');
        stageBar += `<div class="stage-seg ${cls}" style="flex:${pct}">${st}:${n}</div>`;
      }
      stageBar += '</div>';
    }

    // Activity
    const actHtml = a.activity.slice(-12).map(l => {
      const stCls = l.s ? `<span class="stage ${l.s}">[${l.s}]</span> ` : '';
      const cls = l.c === 'fail' ? 'fail' : l.c === 'block' ? 'block' : l.c === 'tool' ? 'tname' : l.c === 'done' ? 'tpath' : '';
      return `<div class="tool-line">${stCls}<span class="${cls}">${l.t}</span></div>`;
    }).join('');

    d.innerHTML = `
      <div class="card-head">
        <span class="card-name">${a.name} <span style="color:var(--dim);font-weight:normal;font-size:11px">${a.node||''}</span></span>
        <span class="card-badge ${a.status}">${a.status.toUpperCase()}${a.stage?' / '+a.stage:''}</span>
      </div>
      <div class="metrics">
        <div class="m"><div class="ml">Input</div><div class="mv hi">${fmt(a.inTok)}</div></div>
        <div class="m"><div class="ml">Output</div><div class="mv">${fmt(a.outTok)}</div></div>
        <div class="m"><div class="ml">Iterations</div><div class="mv">${a.iter}${a.maxIter?'/'+a.maxIter:''}</div></div>
        <div class="m"><div class="ml">Tools / Blocked</div><div class="mv">${a.tools}${a.blocked?' / <span style="color:var(--red)">' +a.blocked+'</span>':''}</div></div>
      </div>
      ${stageBar}
      <div class="tool-stream">${actHtml}</div>`;
    c.appendChild(d);
  }
}

function renderEvents(events) {
  const c = document.getElementById('events');
  for (const e of events) {
    if (e.seq <= seq) continue;
    const d = e.detail||{}, et = e.event_type||'';
    let cls = 'et';
    if (et.includes('fail')||et.includes('error')) cls='et fail';
    else if (et.includes('interrupt')) cls='et interrupt';
    else if (et.startsWith('hook.')) cls='et hook';
    else if (et.startsWith('llm.')) cls='et tool';

    const ag = e.serial||(e.identity||'').slice(0,16)||'';
    const ts = (e.timestamp||'').slice(11,19);

    let info = '';
    if (d.wall_time_s) info += ` wall=${d.wall_time_s}s`;
    if (d.input_tokens) info += ` in=${fmt(d.input_tokens)}`;
    if (d.output_tokens) info += ` out=${fmt(d.output_tokens)}`;
    if (d.stage) info += ` [${d.stage}]`;
    if (d.iteration) info += ` i${d.iteration}${d.max_iterations?'/'+d.max_iterations:''}`;
    if (d.tool_name) info += ` ${d.tool_name}(${(d.tool_path||'').split('/').pop()||''})`;
    if (d.success === false) info += ' FAIL';
    if (d.stop_reason) info += ` stop=${d.stop_reason}`;
    if (d.spec_length) info += ` spec=${d.spec_length}ch`;
    if (d.task_count != null) info += ` tasks=${d.task_count}`;
    if (d.deliverable_count != null) info += ` dlvs=${d.deliverable_count}`;
    if (d.violations) info += ` violations=${d.violations.length}`;
    if (d.question) info += ` Q: ${d.question.slice(0,40)}`;
    if (!info && d.summary) info = ' '+d.summary.slice(0,60);
    if (d.error && !info) info = ' '+d.error.slice(0,60);

    const el = document.createElement('div');
    el.className = 'ev';
    el.innerHTML = `<span class="seq">${String(e.seq).padStart(3,'0')}</span> <span class="ts">${ts}</span> <span class="${cls}">${et}</span> <span class="ag">${ag}</span><span class="info">${info}</span>`;
    c.appendChild(el);
    seq = e.seq;
  }
  c.scrollTop = c.scrollHeight;
}

function totals() {
  let ti=0, to=0, na=0;
  for (const a of Object.values(agents)) { ti+=a.inTok; to+=a.outTok; na++; }
  document.getElementById('t-in').textContent = fmt(ti);
  document.getElementById('t-out').textContent = fmt(to);
  document.getElementById('t-tot').textContent = fmt(ti+to);
  document.getElementById('t-cost').textContent = '$'+(ti*CI+to*CO).toFixed(3);
  document.getElementById('t-agents').textContent = na;
  document.getElementById('t-events').textContent = seq;
  if (pStart) {
    const s = Math.round((Date.now()-pStart.getTime())/1000);
    document.getElementById('t-wall').textContent = s>=60?Math.floor(s/60)+'m '+(s%60)+'s':s+'s';
  }
}

async function poll() {
  try {
    const r = await fetch('/api/events');
    const ev = await r.json();
    for (const e of ev) { if (e.seq > seq) proc(e); }
    renderAgents(); renderEvents(ev); totals();
  } catch(e) {}
  setTimeout(poll, POLL);
}
poll();
</script>
</body>
</html>"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <events-dir>")
        print(f"  e.g.: python {sys.argv[0]} system/registry/macros/MAIN/projects/CREATE/v0001/events")
        sys.exit(1)

    events_dir = sys.argv[1]
    jsonl_path = find_jsonl(events_dir)

    if not jsonl_path:
        print(f"Waiting for JSONL in {events_dir}...")
        for _ in range(60):
            jsonl_path = find_jsonl(events_dir)
            if jsonl_path:
                break
            time.sleep(1)

    if jsonl_path:
        print(f"Watching: {jsonl_path}")
    else:
        print(f"WARN: No JSONL found in {events_dir}, will keep checking")

    print(f"Dashboard: http://localhost:{PORT}")
    server = http.server.HTTPServer(("", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
