"""把 template.html + book.json 合成单文件阅读页，并输出到站点目录。

用法：python build.py          # 只刷新根目录的阅读器
      python build.py --site   # 同时写入 site/index.html
"""
import os, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, 'site')

data = open(os.path.join(BASE, 'book.json'), encoding='utf-8').read()
tpl = open(os.path.join(BASE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('__BOOK_DATA__', data)

targets = [os.path.join(BASE, '高性价比人生指南-阅读器.html')]
if '--site' in sys.argv:
    os.makedirs(SITE, exist_ok=True)
    targets.append(os.path.join(SITE, 'index.html'))

for p in targets:
    open(p, 'w', encoding='utf-8').write(out)
    print('built', p, os.path.getsize(p))
