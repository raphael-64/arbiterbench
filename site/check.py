#!/usr/bin/env python3
"""Check the website's public-data boundary, links, and metric fidelity."""
import collections
import html.parser
import json
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
data = json.loads((OUT / 'data.json').read_text())
items = {r['case_id']: r for r in map(json.loads, (ROOT / 'data/items.jsonl').read_text().splitlines())}
assert {c['id'] for c in data['cases']} == set(items)
assert len(data['cases']) == len(items) == 36
assert data['canary'] == next(iter(items.values()))['canary']
for split, path in [('full','full_set_metrics.json'),('public','metrics.json')]:
 assert data[split] == json.loads((ROOT / 'results' / path).read_text()), split
 assert all(j in data['judges'] for j in data[split]['judges'])
trials = [json.loads(line) for line in (ROOT / 'results/trials.jsonl').read_text().splitlines()]
for c in data['cases']:
 assert re.fullmatch(r'jf_[0-9a-f]{12}', c['id'])
 assert items[c['id']]['split'] == 'public' and c['gold'] == items[c['id']]['gold']
 for j, score in c['records'].items():
  ts = [t for t in trials if t['case_id'] == c['id'] and t['judge'] == j and t.get('verdict') in ('pass','fail')]
  assert score == {'total':len(ts),'correct':sum(t['verdict'] == c['gold'] for t in ts)}
 for m in c['mechanisms']:
  p = ROOT / m['path']
  assert p.is_relative_to(ROOT / 'results/judge_outputs' / c['id']) and p.is_file()
  assert re.sub(r'\s+', ' ', m['quote']) in re.sub(r'\s+', ' ', p.read_text())

class Links(html.parser.HTMLParser):
 def __init__(self):
  super().__init__(); self.links=[]; self.ids=[]
 def handle_starttag(self, tag, attrs):
  attrs=dict(attrs)
  if 'id' in attrs:self.ids.append(attrs['id'])
  for a in ('href','src'):
   if a in attrs:self.links.append(attrs[a])
  if tag=='meta' and attrs.get('property')=='og:image':
   assert (OUT / urllib.parse.urlparse(attrs['content']).path.lstrip('/')).is_file()

page=Links(); page.feed((OUT / 'index.html').read_text())
assert len(page.ids)==len(set(page.ids)), 'Duplicate HTML ids'
for link in page.links:
 url=urllib.parse.urlparse(link)
 if url.scheme:continue
 if url.path:assert (OUT/url.path).is_file(), link
 elif url.fragment and not url.fragment.startswith('case-'):assert url.fragment in page.ids,link
expected={'index.html','fonts.css','style.css','app.js','favicon.svg','data.json','.nojekyll','robots.txt','sitemap.xml','assets/case_gcode_plot.png','assets/who_misses_what.svg','assets/label_audit_funnel.svg','assets/social.png'}
expected |= {str(p.relative_to(ROOT/'site')) for d in ('icons','fonts') for p in (ROOT/'site/assets'/d).rglob('*') if p.is_file()}
assert {str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()} == expected, 'Unexpected deployment files'
print('Website checks passed: 36 public cases, exact released metrics, trial counts, evidence links, and deployment allowlist.')
