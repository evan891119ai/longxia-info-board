#!/usr/bin/env python3
import json
import html
import pathlib
import datetime

root = pathlib.Path(__file__).resolve().parents[1]
docs = root / 'docs'
(docs / 'topics').mkdir(parents=True, exist_ok=True)

topics = json.loads((root / 'topics/topics.json').read_text())
data = json.loads((root / 'data/items.json').read_text())
items = data.get('items', [])
updated = data.get('updatedAt') or datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

topic_names = {t['id']: t.get('name', t['id']) for t in topics}
topic_order = {t['id']: idx for idx, t in enumerate(topics)}
for item in items:
    item.setdefault('topic', 'other')
    item.setdefault('importance', 'medium')
    item.setdefault('foundAt', updated)

by_topic = {t['id']: [] for t in topics}
for item in items:
    by_topic.setdefault(item.get('topic', 'other'), []).append(item)

high_items = [i for i in items if i.get('importance') == 'high'][:6]
recent_items = items[:8]

def esc(value):
    return html.escape(str(value or ''))

css = r'''
:root{color-scheme:light dark;--bg:#0b0d12;--bg2:#11141b;--card:#171b24;--card2:#1d2230;--text:#edf1f7;--muted:#98a3b3;--accent:#ff7a59;--accent2:#8ab4ff;--line:#2a3140;--good:#7ee787;--warn:#ffd166}*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(circle at top left,#1d2433 0,#0b0d12 42%);color:var(--text)}a{color:var(--accent2);text-decoration:none}a:hover{text-decoration:underline}main{max-width:1180px;margin:0 auto;padding:32px 18px 80px}header{margin-bottom:20px}.brand{display:flex;align-items:center;gap:14px}.logo{font-size:44px}.brand h1{font-size:34px;line-height:1.1;margin:0}.brand p{margin:6px 0 0;color:var(--muted)}.topnav{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.navlink{border:1px solid var(--line);border-radius:999px;padding:7px 11px;background:rgba(23,27,36,.7);color:var(--muted)}.dashboard{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:24px 0}.stat{background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--line);border-radius:16px;padding:16px}.stat strong{display:block;font-size:26px}.stat span{color:var(--muted);font-size:13px}.controls{position:sticky;top:0;z-index:10;background:rgba(11,13,18,.9);backdrop-filter:blur(14px);border:1px solid var(--line);border-radius:18px;padding:14px;margin:18px 0 24px}.searchrow{display:grid;grid-template-columns:1fr auto auto;gap:10px}input,select,button{border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--text);font:inherit;padding:10px 12px}button{cursor:pointer}button:hover,.chip:hover,.topic-card:hover{border-color:var(--accent)}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.chip{border:1px solid var(--line);background:var(--card);color:var(--muted);border-radius:999px;padding:7px 11px;cursor:pointer;font-size:14px}.chip.active{background:rgba(255,122,89,.14);color:var(--text);border-color:var(--accent)}.section-title{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:30px 0 12px}.section-title h2{margin:0}.section-title p{margin:0;color:var(--muted);font-size:14px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.item{background:rgba(23,27,36,.92);border:1px solid var(--line);border-radius:16px;padding:16px;min-width:0}.item.hidden{display:none}.item h3{font-size:17px;line-height:1.35;margin:0 0 8px}.meta{display:flex;gap:7px;flex-wrap:wrap;align-items:center;color:var(--muted);font-size:13px}.tag{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:12px;color:var(--muted)}.tag.high{border-color:rgba(255,122,89,.7);color:#ffb199}.tag.medium{border-color:rgba(138,180,255,.6);color:#bcd4ff}.summary{margin:10px 0 0;color:var(--text)}details{margin-top:10px;color:var(--muted)}summary{cursor:pointer;color:var(--accent2)}.note{margin:10px 0 0;border-left:3px solid var(--accent);padding-left:10px;color:var(--text)}.topics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.topic-card{display:block;text-align:left;background:rgba(23,27,36,.84);border:1px solid var(--line);border-radius:16px;padding:14px;color:var(--text)}.topic-card h3{margin:0 0 6px}.topic-card p{margin:0;color:var(--muted);font-size:14px}.list{display:grid;gap:10px}.compact{padding:13px}.compact .summary{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.empty{border:1px dashed var(--line);border-radius:16px;padding:28px;text-align:center;color:var(--muted)}.archive-group{margin:26px 0}.archive-group h2{border-bottom:1px solid var(--line);padding-bottom:8px}.breadcrumb{color:var(--muted);font-size:14px;margin-bottom:12px}footer{margin-top:42px;color:var(--muted);font-size:13px}@media (max-width:800px){main{padding:24px 14px 60px}.dashboard{grid-template-columns:repeat(2,minmax(0,1fr))}.grid,.topics{grid-template-columns:1fr}.searchrow{grid-template-columns:1fr}.controls{position:static}.brand h1{font-size:28px}}
'''

def nav(prefix=''):
    return f'''<nav class="topnav">
<a class="navlink" href="{prefix}index.html">Dashboard</a>
<a class="navlink" href="{prefix}archive.html">Archive</a>
<a class="navlink" href="{prefix}data/items.json">Raw JSON</a>
</nav>'''

def page_start(title, subtitle, prefix=''):
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><style>{css}</style></head><body><main>
<header><div class="brand"><div class="logo">🦞</div><div><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div></div>{nav(prefix)}</header>'''

def page_end(extra_script=''):
    return f'<footer>Generated by Longxia 🦞. Sources are linked to original publishers. Last updated: {esc(updated)}</footer>{extra_script}</main></body></html>'

def render_item(item, compact=False, prefix=''):
    topic_id = item.get('topic')
    topic = esc(topic_names.get(topic_id, topic_id or 'Other'))
    importance = esc(item.get('importance') or 'medium')
    cls = 'item compact' if compact else 'item'
    note = item.get('longxiaNote') or ''
    topic_href = f'{prefix}topics/{esc(topic_id)}.html' if topic_id in topic_names else '#'
    details = f'<details><summary>龍蝦判斷</summary><p class="note">{esc(note)}</p></details>' if note else ''
    return f'''<article class="{cls}" data-topic="{esc(topic_id)}" data-importance="{importance}">
<h3><a href="{esc(item.get('url') or '#')}" rel="noopener noreferrer" target="_blank">{esc(item.get('title') or '(untitled)')}</a></h3>
<div class="meta"><a href="{topic_href}">{topic}</a><span>·</span><span>{esc(item.get('published') or item.get('foundAt') or '')}</span><span>·</span><span>{esc(item.get('source') or '')}</span><span class="tag {importance}">{importance}</span></div>
<p class="summary">{esc(item.get('summary') or '')}</p>{details}
</article>'''

def build_index():
    payload = []
    for item in items:
        payload.append({
            'topic': item.get('topic', 'other'),
            'importance': item.get('importance') or 'medium',
            'searchText': ' '.join([
                item.get('title') or '', item.get('source') or '', item.get('summary') or '',
                item.get('longxiaNote') or '', topic_names.get(item.get('topic'), item.get('topic', '')),
            ]).lower(),
        })
    parts = [page_start('Longxia Info Board', f'自動搜尋、整理、去重的資訊看板。最後更新：{updated}')]
    parts.append(f'''<section class="dashboard">
  <div class="stat"><strong>{len(items)}</strong><span>總資料</span></div>
  <div class="stat"><strong>{len(topics)}</strong><span>追蹤主題</span></div>
  <div class="stat"><strong>{len(high_items)}</strong><span>高重要性</span></div>
  <div class="stat"><strong id="visibleCount">{len(items)}</strong><span>目前顯示</span></div>
</section>
<section class="controls" aria-label="filters">
  <div class="searchrow">
    <input id="search" type="search" placeholder="搜尋標題、來源、摘要、龍蝦判斷…" autocomplete="off">
    <select id="importance"><option value="all">全部重要性</option><option value="high">high</option><option value="medium">medium</option><option value="low">low</option></select>
    <button id="reset" type="button">重設</button>
  </div>
  <div class="chips" id="chips"><button class="chip active" data-topic="all">All</button>''')
    for topic in topics:
        count = len(by_topic.get(topic['id'], []))
        parts.append(f'<button class="chip" data-topic="{esc(topic["id"])}">{esc(topic["name"])} <span>({count})</span></button>')
    parts.append('</div></section>')

    parts.append('<section class="section-title"><div><h2>🔥 高重要性</h2><p>優先查看最可能需要追蹤的變化。</p></div></section><section class="grid" id="highlights">')
    for item in high_items:
        parts.append(render_item(item, compact=True))
    parts.append('</section>')

    parts.append('<section class="section-title"><div><h2>🕒 最近更新</h2><p>最新收進看板的資訊。</p></div></section><section class="grid" id="recent">')
    for item in recent_items:
        parts.append(render_item(item, compact=True))
    parts.append('</section>')

    parts.append('<section class="section-title"><div><h2>📚 Topics</h2><p>快速進入獨立主題頁；主題變多也不怕一路往下找。</p></div></section><section class="topics">')
    for topic in topics:
        rows = by_topic.get(topic['id'], [])
        latest = rows[0].get('published') if rows else '尚無資料'
        parts.append(f'<a class="topic-card" href="topics/{esc(topic["id"])}.html"><h3>{esc(topic["name"])} · {len(rows)}</h3><p>最新：{esc(latest)}</p></a>')
    parts.append('</section>')

    parts.append('<section class="section-title"><div><h2>全部資訊</h2><p>可用搜尋、topic、importance 即時篩選；完整歷史請看 Archive。</p></div><a class="navlink" href="archive.html">開啟 Archive</a></section><section class="list" id="allItems">')
    for item in items:
        parts.append(render_item(item))
    parts.append('</section><div class="empty" id="empty" hidden>找不到符合條件的資訊。</div>')

    json_payload = json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')
    js = f'''<script>
const items = {json_payload};
const search = document.querySelector('#search');
const importance = document.querySelector('#importance');
const chips = [...document.querySelectorAll('.chip')];
const cards = [...document.querySelectorAll('#allItems .item')];
const visibleCount = document.querySelector('#visibleCount');
const empty = document.querySelector('#empty');
let activeTopic = 'all';
function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  const imp = importance.value;
  let shown = 0;
  cards.forEach((card, idx) => {{
    const item = items[idx];
    const okTopic = activeTopic === 'all' || item.topic === activeTopic;
    const okImp = imp === 'all' || item.importance === imp;
    const okQ = !q || item.searchText.includes(q);
    const show = okTopic && okImp && okQ;
    card.classList.toggle('hidden', !show);
    if (show) shown++;
  }});
  visibleCount.textContent = shown;
  empty.hidden = shown !== 0;
}}
chips.forEach(chip => chip.addEventListener('click', () => {{
  activeTopic = chip.dataset.topic;
  chips.forEach(c => c.classList.toggle('active', c === chip));
  applyFilters();
  document.querySelector('#allItems').scrollIntoView({{behavior:'smooth', block:'start'}});
}}));
search.addEventListener('input', applyFilters);
importance.addEventListener('change', applyFilters);
document.querySelector('#reset').addEventListener('click', () => {{
  search.value = '';
  importance.value = 'all';
  activeTopic = 'all';
  chips.forEach(c => c.classList.toggle('active', c.dataset.topic === 'all'));
  applyFilters();
}});
</script>'''
    parts.append(page_end(js))
    (docs / 'index.html').write_text('\n'.join(parts))

def build_archive():
    parts = [page_start('Longxia Info Board Archive', f'完整歷史資料。最後更新：{updated}')]
    parts.append(f'<section class="dashboard"><div class="stat"><strong>{len(items)}</strong><span>總資料</span></div><div class="stat"><strong>{len(topics)}</strong><span>主題</span></div><div class="stat"><strong>{len(high_items)}</strong><span>高重要性</span></div><div class="stat"><strong>{updated[:10]}</strong><span>更新日期</span></div></section>')
    for topic in topics:
        rows = by_topic.get(topic['id'], [])
        parts.append(f'<section class="archive-group" id="{esc(topic["id"])}"><h2>{esc(topic["name"])} · {len(rows)}</h2><div class="list">')
        if not rows:
            parts.append('<p class="empty">尚無資料。</p>')
        for item in rows:
            parts.append(render_item(item))
        parts.append('</div></section>')
    parts.append(page_end())
    (docs / 'archive.html').write_text('\n'.join(parts))

def build_topic_pages():
    for topic in topics:
        rows = by_topic.get(topic['id'], [])
        parts = [page_start(f'{topic["name"]} · Longxia Info Board', f'{len(rows)} 則資訊。最後更新：{updated}', prefix='../')]
        parts.append(f'<p class="breadcrumb"><a href="../index.html">Dashboard</a> / {esc(topic["name"])}</p>')
        parts.append('<section class="list">')
        if not rows:
            parts.append('<p class="empty">尚無資料，下一次自動更新後會出現。</p>')
        for item in rows:
            # prefix points back from topics/*.html to topics/*.html would be wrong for self, but acceptable topic link not central here.
            parts.append(render_item(item, prefix='../'))
        parts.append('</section>')
        parts.append(page_end())
        (docs / 'topics' / f'{topic["id"]}.html').write_text('\n'.join(parts))

build_index()
build_archive()
build_topic_pages()
(docs / '.nojekyll').touch()
