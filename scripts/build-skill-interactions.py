#!/usr/bin/env python3
"""Build the committed skill interaction report from reviewed graph data."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "graph"
DOCS = ROOT / "docs"


def load() -> tuple[list[dict], list[dict]]:
    nodes = json.loads((GRAPH / "skills.json").read_text(encoding="utf-8"))["skills"]
    edges = json.loads((GRAPH / "relationships.json").read_text(encoding="utf-8"))["relationships"]
    return nodes, edges


def markdown(nodes: list[dict], edges: list[dict]) -> str:
    direct = [edge for edge in edges if edge["type"] == "direct"]
    indirect = [edge for edge in edges if edge["type"] == "indirect"]
    lines = [
        "# Skill Interactions",
        "",
        f"Inventory: {len(nodes)} skills. Relationships: {len(edges)} reviewed edges.",
        "",
        "Direct edges are explicit invocations, delegation, handoffs, or documented uses. Indirect edges are reviewed composition hypotheses and are intentionally weaker.",
        "",
        "## Direct Relationships",
        "",
        "| Source | Relationship | Target | Basis |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| `{e['source']}` | {e['relation']} | `{e['target']}` | {e['basis']} |"
        for e in direct
    )
    lines += ["", "## Indirect Relationships", "", "| Source | Relationship | Target | Basis |", "| --- | --- | --- | --- |"]
    lines.extend(
        f"| `{e['source']}` | {e['relation']} | `{e['target']}` | {e['basis']} |"
        for e in indirect
    )
    lines += [
        "",
        "## Refresh",
        "",
        "Run `python scripts/build-skill-interactions.py --write` after changing skills or graph data.",
        "Use `--check` in CI to fail when committed HTML or Markdown differs from the source graph.",
        "",
        "## Limitations",
        "",
        "The graph records documented relationships, not runtime telemetry. Indirect edges are hypotheses supported by the stated basis and should be reviewed when workflows change.",
        "",
    ]
    return "\n".join(lines)


def page(nodes: list[dict], edges: list[dict]) -> str:
    payload = json.dumps({"nodes": nodes, "edges": edges}).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skill Interactions</title><style>
:root{{color-scheme:dark;--bg:#10131a;--panel:#191e29;--text:#e8edf5;--muted:#9aa8bc;--direct:#69d2a4;--indirect:#9b8cff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px system-ui,sans-serif}}header{{padding:24px 28px;border-bottom:1px solid #303747}}h1{{margin:0 0 6px;font-size:28px}}p{{color:var(--muted)}}main{{display:grid;grid-template-columns:280px 1fr;min-height:calc(100vh - 110px)}}aside{{padding:20px;border-right:1px solid #303747;background:var(--panel)}}label{{display:block;margin:12px 0;color:var(--muted)}}input,select{{width:100%;padding:9px;background:#10131a;color:var(--text);border:1px solid #414b60;border-radius:6px}}#graph{{position:relative;overflow:auto;padding:28px}}svg{{min-width:900px;min-height:680px;background:radial-gradient(#293142 1px,transparent 1px);background-size:22px 22px;border-radius:10px}}.node{{cursor:pointer}}.node rect{{fill:#252d3b;stroke:#66738b;stroke-width:1.5}}.node text{{fill:var(--text);font-size:12px}}.edge-direct{{stroke:var(--direct);stroke-width:2;fill:none}}.edge-indirect{{stroke:var(--indirect);stroke-width:2;stroke-dasharray:7 6;fill:none;opacity:.75}}#detail{{position:absolute;right:28px;top:28px;width:290px;padding:16px;background:rgba(25,30,41,.96);border:1px solid #414b60;border-radius:8px;display:none}}.legend{{font-size:12px;color:var(--muted);line-height:1.8}}.swatch{{display:inline-block;width:28px;border-top:2px solid var(--direct);vertical-align:middle;margin-right:6px}}.swatch.indirect{{border-top-style:dashed;border-color:var(--indirect)}}@media(max-width:800px){{main{{display:block}}aside{{border-right:0;border-bottom:1px solid #303747}}#detail{{position:fixed;right:12px;top:auto;bottom:12px}}}}
</style></head><body><header><h1>Skill Interactions</h1><p>Solid lines are documented direct relationships. Dashed lines are reviewed composition hypotheses.</p></header><main><aside><label>Search<input id="search" placeholder="skill name"></label><label>Relationship<select id="kind"><option value="all">All</option><option value="direct">Direct</option><option value="indirect">Indirect</option></select></label><div class="legend"><div><span class="swatch"></span>direct</div><div><span class="swatch indirect"></span>indirect</div></div></aside><section id="graph"><svg id="svg" viewBox="0 0 1200 760" role="img" aria-label="Skill interaction graph"></svg><div id="detail"></div></section></main><script>
const data=JSON.parse("{payload}");const svg=document.querySelector('#svg'),detail=document.querySelector('#detail'),search=document.querySelector('#search'),kind=document.querySelector('#kind');
const ns='http://www.w3.org/2000/svg';const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function draw(){{svg.innerHTML='';const q=search.value.toLowerCase(),k=kind.value;const visible=data.nodes.filter(n=>!q||n.id.includes(q));const pos=new Map(visible.map((n,i)=>[n.id,{{x:80+(i%5)*220,y:70+Math.floor(i/5)*115}}]));
data.edges.filter(e=>(k==='all'||e.type===k)&&pos.has(e.source)&&pos.has(e.target)).forEach(e=>{{const a=pos.get(e.source),b=pos.get(e.target),line=document.createElementNS(ns,'line');line.setAttribute('x1',a.x+150);line.setAttribute('y1',a.y+24);line.setAttribute('x2',b.x);line.setAttribute('y2',b.y+24);line.setAttribute('class','edge-'+e.type);svg.appendChild(line)}});
visible.forEach(n=>{{const p=pos.get(n.id),g=document.createElementNS(ns,'g');g.setAttribute('class','node');g.addEventListener('click',()=>{{detail.style.display='block';detail.innerHTML='<strong>'+esc(n.id)+'</strong><p>Kind: '+esc(n.kind)+'</p><p>'+data.edges.filter(e=>e.source===n.id||e.target===n.id).map(e=>esc(e.source+' '+e.relation+' '+e.target+' ('+e.type+')')).join('<br>')+'</p>'}});const r=document.createElementNS(ns,'rect');r.setAttribute('x',p.x);r.setAttribute('y',p.y);r.setAttribute('width',150);r.setAttribute('height',48);r.setAttribute('rx',7);const t=document.createElementNS(ns,'text');t.setAttribute('x',p.x+10);t.setAttribute('y',p.y+29);t.textContent=n.id;g.append(r,t);svg.appendChild(g)}})}}
search.addEventListener('input',draw);kind.addEventListener('change',draw);draw();</script></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    nodes, edges = load()
    outputs = {DOCS / "skill-interactions.md": markdown(nodes, edges), DOCS / "skill-interactions.html": page(nodes, edges)}
    if args.check:
        return 0 if all(path.exists() and path.read_text(encoding="utf-8") == content for path, content in outputs.items()) else 1
    if not args.write:
        parser.error("choose --write or --check")
    DOCS.mkdir(exist_ok=True)
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
