import re, json, html, os, sys

# 用法：python extract.py <源 index.html> [输出 book.json]
SRC = sys.argv[1] if len(sys.argv) > 1 else r'index.html'
s = open(SRC, encoding='utf-8', errors='replace').read()

main = s[s.find('<main>'): s.find('</main>')]

def strip_tags(t):
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

def clean_html(t):
    # 保留 <a>，其余标签去掉
    t = re.sub(r'<(?!/?a\b)[^>]+>', '', t)
    return html.unescape(t).strip()

sections = re.split(r'<section id="sec\d+">', main)[1:]
data = []
for sec in sections:
    m = re.search(r'<h2>(.*?)</h2>', sec, re.S)
    title = strip_tags(m.group(1))
    intro = ''
    mi = re.search(r'<p class="intro">(.*?)</p>', sec, re.S)
    if mi:
        intro = strip_tags(mi.group(1))
    items = []
    for art in re.split(r'<article class="card"', sec)[1:]:
        d = {}
        mid = re.search(r'id="(s[\d\-]+)"', art)
        d['id'] = mid.group(1) if mid else ''
        mg = re.search(r'data-grade="([^"]*)"', art)
        d['grade'] = mg.group(1) if mg else ''
        mr = re.search(r'data-ratio="([^"]*)"', art)
        d['ratio'] = mr.group(1) if mr else ''
        mn = re.search(r'<span class="num">(.*?)</span>', art, re.S)
        d['num'] = strip_tags(mn.group(1)) if mn else ''
        mh = re.search(r'<h3>(.*?)</h3>', art, re.S)
        d['title'] = strip_tags(mh.group(1)) if mh else ''
        mp = re.search(r'<p class="plain">(.*?)</p>', art, re.S)
        d['plain'] = strip_tags(mp.group(1)) if mp else ''
        fields = []
        for fm in re.finditer(r'<div class="f[^"]*"><b>(.*?)</b><div>(.*?)</div></div>', art, re.S):
            fields.append({'k': strip_tags(fm.group(1)), 'v': strip_tags(fm.group(2))})
        d['fields'] = fields
        ms = re.search(r'<details class="src"><summary>(.*?)</summary><div class="sbody">(.*?)</div></details>', art, re.S)
        if ms:
            d['srcSummary'] = strip_tags(ms.group(1))
            d['src'] = clean_html(ms.group(2))
        else:
            d['srcSummary'] = ''
            d['src'] = ''
        items.append(d)
    data.append({'title': title, 'intro': intro, 'items': items})

print('sections', len(data), 'items', sum(len(x['items']) for x in data))
out = sys.argv[2] if len(sys.argv) > 2 else 'book.json'
json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('written', out, os.path.getsize(out))
