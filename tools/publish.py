"""把本仓库的文件同步到 GitHub（不依赖 git push）。

为什么需要它：某些网络环境下 git 的 HTTPS 传输被代理拦掉（github.com 走不通），
但 api.github.com 是通的。这个脚本改走 GitHub Contents API 逐文件上传。

用法：在仓库根目录执行
    python tools/publish.py                 # 上传默认文件清单
    python tools/publish.py index.html      # 只上传指定文件

可选环境变量：GITHUB_TOKEN（默认取本机 `gh auth token`）
"""
import os, sys, base64, json, subprocess, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)

try:
    with open(os.path.join(BASE, '.github_repo')) as f:
        OWNER, REPO = f.read().strip().split('/')
except Exception:
    OWNER, REPO = 'cyc20261', 'how-to-live-better-reader'

DEFAULT = ['README.md', 'LICENSE', '.nojekyll', 'index.html',
           'tools/extract.py', 'tools/template.html', 'tools/build.py',
           'tools/publish.py']

token = os.environ.get('GITHUB_TOKEN') or subprocess.run(
    ['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
handlers = [urllib.request.ProxyHandler({'https': proxy, 'http': proxy})] if proxy else []
op = urllib.request.build_opener(*handlers)


def api(path, data=None, method='GET'):
    req = urllib.request.Request('https://api.github.com' + path,
                                 data=json.dumps(data).encode() if data else None,
                                 method=method)
    req.add_header('Authorization', 'Bearer ' + token)
    req.add_header('Accept', 'application/vnd.github+json')
    if data:
        req.add_header('Content-Type', 'application/json')
    with op.open(req, timeout=300) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def sha_of(path):
    try:
        return api(f'/repos/{OWNER}/{REPO}/contents/{urllib.parse.quote(path)}?ref=main').get('sha')
    except Exception:
        return None


files = sys.argv[1:] or DEFAULT
for f in files:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        print('skip (missing)', f)
        continue
    b64 = base64.b64encode(open(p, 'rb').read()).decode()
    try:
        res = api(f'/repos/{OWNER}/{REPO}/contents/{urllib.parse.quote(f)}',
                  {'message': f'update {f}', 'content': b64, 'branch': 'main',
                   **({'sha': sha_of(f)} if sha_of(f) else {})}, 'PUT')
        print('ok', f, '->', res['commit']['sha'][:7])
    except Exception as e:
        print('FAIL', f, e)
