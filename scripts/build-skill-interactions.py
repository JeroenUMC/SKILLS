#!/usr/bin/env python3
"""Build the skill interaction report from relationships declared in SKILL.md frontmatter."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "graph"
DOCS = ROOT / "docs"

RELATION_CATEGORIES = {
    "invokes": "directional",
    "delegates": "directional",
    "hands-off-to": "directional",
    "uses": "directional",
    "composes-well": "non-directional",
    "vocabulary": "non-directional",
    "optional-companion": "non-directional",
}
CONTROL_RELATIONS = {"invokes", "delegates", "hands-off-to"}


def parse_skill(path: Path) -> tuple[str, dict[str, list[str]]]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing frontmatter: {path}")
    block = match.group(1)
    name_match = re.search(r"^name:\s*(\S+)\s*$", block, re.MULTILINE)
    if not name_match:
        raise ValueError(f"missing name: {path}")
    relationships: dict[str, list[str]] = {}
    relation_match = re.search(r"^relationships:\n((?:  [^\n]+\n?)*)", block, re.MULTILINE)
    if relation_match:
        for line in relation_match.group(1).splitlines():
            relation, values = line.strip().split(":", 1)
            relationships[relation] = re.findall(r"[A-Za-z0-9_-]+", values)
    return name_match.group(1), relationships


def load() -> tuple[list[dict], list[dict]]:
    nodes = json.loads((GRAPH / "skills.json").read_text(encoding="utf-8"))["skills"]
    known = {node["id"] for node in nodes}
    edges: list[dict] = []
    paths: set[Path] = set()
    for node in nodes:
        skill_path = ROOT / node["kind"] / node["id"] / "SKILL.md"
        if not skill_path.is_file():
            raise ValueError(f"missing skill file for {node['id']}: {skill_path}")
        paths.add(skill_path)
        source, relationships = parse_skill(skill_path)
        if source != node["id"]:
            raise ValueError(f"frontmatter name {source} does not match graph id {node['id']}")
        for relation, targets in relationships.items():
            if relation not in RELATION_CATEGORIES:
                raise ValueError(f"unknown relationship {relation} in {skill_path}")
            for target in targets:
                if target not in known:
                    raise ValueError(f"unknown target {target} in {skill_path}")
                if target == source:
                    raise ValueError(f"self relationship {source} in {skill_path}")
                edges.append({
                    "source": source,
                    "target": target,
                    "relation": relation,
                    "category": RELATION_CATEGORIES[relation],
                })
    unexpected = sorted(ROOT.glob("*/SKILL.md"))
    unexpected += sorted(path for path in ROOT.glob("*/*/SKILL.md") if path not in paths)
    if unexpected:
        raise ValueError(f"skill files are not declared in graph/skills.json: {unexpected}")
    return nodes, edges


def markdown(nodes: list[dict], edges: list[dict]) -> str:
    directional = [edge for edge in edges if edge["category"] == "directional"]
    non_directional = [edge for edge in edges if edge["category"] == "non-directional"]
    lines = [
        "# Skill Interactions",
        "",
        f"Inventory: {len(nodes)} skills. Relationships: {len(edges)} declared edges.",
        "",
        "Directional edges describe workflow or dependency direction. Non-directional edges describe compatible skills or supporting vocabulary and do not imply sequence.",
        "",
        "## Directional Relationships",
        "",
        "| Source | Relationship | Target |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| `{e['source']}` | {e['relation']} | `{e['target']}` |" for e in directional)
    lines += ["", "## Non-Directional Relationships", "", "| Source | Relationship | Target |", "| --- | --- | --- |"]
    lines.extend(f"| `{e['source']}` | {e['relation']} | `{e['target']}` |" for e in non_directional)
    lines += [
        "",
        "## Refresh",
        "",
        "Run `python scripts/build-skill-interactions.py --write` after changing skill frontmatter or graph/skills.json.",
        "Use `--check` in CI to fail when committed HTML or Markdown differs from the source.",
        "",
        "## Limitations",
        "",
        "Relationships are declared in skill frontmatter, not inferred from prose. Directional edges are not a complete ordering: `uses` means dependency or consultation, while `invokes`, `delegates`, and `hands-off-to` represent control transfer.",
        "",
    ]
    return "\n".join(lines)


def page(nodes: list[dict], edges: list[dict]) -> str:
    payload = json.dumps({"nodes": nodes, "edges": edges}).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skill Interactions</title><style>
:root{{--bg:#10131a;--panel:#191e29;--text:#e8edf5;--muted:#9aa8bc;--directional:#69d2a4;--nondirectional:#9b8cff;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px system-ui,sans-serif}}header{{padding:24px 28px;border-bottom:1px solid #303747}}h1{{margin:0 0 6px;font-size:28px}}p{{color:var(--muted)}}main{{display:grid;grid-template-columns:280px 1fr;min-height:calc(100vh - 110px)}}aside{{padding:20px;border-right:1px solid #303747;background:var(--panel)}}label{{display:block;margin:12px 0;color:var(--muted)}}input,select{{width:100%;padding:9px;background:#10131a;color:var(--text);border:1px solid #414b60;border-radius:6px}}#graph{{position:relative;overflow:auto;padding:28px}}svg{{min-width:900px;min-height:680px;background:radial-gradient(#293142 1px,transparent 1px);background-size:22px 22px;border-radius:10px}}.node{{cursor:pointer;transition:opacity .18s}}.node rect{{fill:#252d3b;stroke:#66738b;stroke-width:1.5}}.node text{{fill:var(--text);font-size:12px}}.node.is-selected rect{{stroke:#fff;stroke-width:3;filter:drop-shadow(0 0 8px #69d2a4)}}.node.is-muted{{opacity:.16}}.edge-directional{{stroke:var(--directional);stroke-width:2;fill:none;marker-end:url(#arrow)}}.edge-non-directional{{stroke:var(--nondirectional);stroke-width:2;stroke-dasharray:7 6;fill:none;opacity:.75}}.is-muted{{opacity:.08}}#focus{{display:none;margin:14px 0;padding:9px 10px;background:#253d3a;border:1px solid #69d2a4;border-radius:6px;line-height:1.35}}#detail{{position:absolute;right:28px;top:28px;width:290px;padding:16px;background:rgba(25,30,41,.96);border:1px solid #414b60;border-radius:8px;display:none}}.legend{{font-size:12px;color:var(--muted);line-height:1.8}}.swatch{{display:inline-block;width:28px;border-top:2px solid var(--directional);vertical-align:middle;margin-right:6px}}.swatch.nondirectional{{border-top-style:dashed;border-color:var(--nondirectional)}}@media(max-width:800px){{main{{display:block}}aside{{border-right:0;border-bottom:1px solid #303747}}#detail{{position:fixed;right:12px;top:auto;bottom:12px}}}}
</style></head><body><header><h1>Skill Interactions</h1><p>Arrows show directional workflow/dependency relations. Dashed lines show non-directional composition or vocabulary support.</p></header><main><aside><label>Search<input id="search" placeholder="skill name"></label><label>Relationship<select id="kind"><option value="all">All</option><option value="directional">Directional</option><option value="non-directional">Non-directional</option></select></label><div id="focus">Focused: <strong id="focus-name"></strong><br>Connected skills stay bright. Press Escape or click empty space to clear.</div><div class="legend"><div><span class="swatch"></span>directional</div><div><span class="swatch nondirectional"></span>non-directional</div></div></aside><section id="graph"><svg id="svg" viewBox="0 0 1200 760" role="img" aria-label="Skill interaction graph"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="var(--directional)"></path></marker></defs></svg><div id="detail"></div></section></main><script>
const data={payload};const svg=document.querySelector('#svg'),detail=document.querySelector('#detail'),search=document.querySelector('#search'),kind=document.querySelector('#kind'),focus=document.querySelector('#focus'),focusName=document.querySelector('#focus-name');let selected=null;
const ns='http://www.w3.org/2000/svg';const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function draw(){{svg.querySelectorAll('.edge,.node').forEach(el=>el.remove());const q=search.value.toLowerCase(),k=kind.value;const visible=data.nodes.filter(n=>!q||n.id.includes(q));const pos=new Map(visible.map((n,i)=>[n.id,{{x:80+(i%5)*220,y:70+Math.floor(i/5)*115}}]));const connected=new Set(selected?[selected]:[]);data.edges.forEach(e=>{{if(e.source===selected)connected.add(e.target);if(e.target===selected)connected.add(e.source)}});focus.style.display=selected?'block':'none';focusName.textContent=selected||'';
data.edges.filter(e=>(k==='all'||e.category===k)&&pos.has(e.source)&&pos.has(e.target)).forEach(e=>{{const a=pos.get(e.source),b=pos.get(e.target),line=document.createElementNS(ns,'line');line.setAttribute('x1',a.x+150);line.setAttribute('y1',a.y+24);line.setAttribute('x2',b.x);line.setAttribute('y2',b.y+24);line.setAttribute('class','edge '+(e.category==='directional'?'edge-directional':'edge-non-directional')+((selected&&e.source!==selected&&e.target!==selected)?' is-muted':''));if(e.category==='directional')line.setAttribute('marker-end','url(#arrow)');svg.appendChild(line)}});
visible.forEach(n=>{{const p=pos.get(n.id),g=document.createElementNS(ns,'g');g.setAttribute('class','node'+(selected===n.id?' is-selected':'')+(selected&&!connected.has(n.id)?' is-muted':''));g.addEventListener('click',event=>{{event.stopPropagation();selected=selected===n.id?null:n.id;detail.style.display=selected?'block':'none';detail.innerHTML=selected?'<strong>'+esc(n.id)+'</strong><p>Kind: '+esc(n.kind)+'</p><p>'+data.edges.filter(e=>e.source===n.id||e.target===n.id).map(e=>esc(e.source+' '+e.relation+' '+e.target+' ('+e.category+')')).join('<br>')+'</p>':'';draw()}});const r=document.createElementNS(ns,'rect');r.setAttribute('x',p.x);r.setAttribute('y',p.y);r.setAttribute('width',150);r.setAttribute('height',48);r.setAttribute('rx',7);const t=document.createElementNS(ns,'text');t.setAttribute('x',p.x+10);t.setAttribute('y',p.y+29);t.textContent=n.id;g.append(r,t);svg.appendChild(g)}})}}
svg.addEventListener('click',()=>{{selected=null;detail.style.display='none';draw()}});document.addEventListener('keydown',event=>{{if(event.key==='Escape'){{selected=null;detail.style.display='none';draw()}}}});search.addEventListener('input',draw);kind.addEventListener('change',draw);draw();</script></body></html>"""


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
