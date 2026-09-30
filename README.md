# 高性价比人生指南 · 分章节阅读器

把开源书《高性价比人生指南》的全部 **34 章 / 631 条**建议，做成一个按章节阅读的单文件网页。
打开就能读，不用装任何东西，断网也能读。

- **在线阅读：** https://cyc20261.github.io/how-to-live-better-reader/
- **一键导出：** 页面右上角「导出 ▾」可以整站打包带走
- **授权：** 正文为 CC BY 4.0（须署名），不是公有领域 —— 详见文末「授权与署名」

## 页面特性

- **分章节**：左侧 34 章目录，一次读一章；顶栏下拉也能直接跳章
- **上一章 / 下一章**，键盘 `←` `→` 翻章，`/` 聚焦搜索
- **全书搜索**：搜索框输入后按 Enter，跨 631 条查找，点结果跳回原文并高亮
- **字号调节** A- / A+，当前章节与字号自动记住
- **一键导出**：网页单文件 `.html` / Markdown `.md` / 结构化数据 `.json`
- 零外部资源：没有 CDN、没有字体外链、不请求任何接口

## 一键导出怎么用

右上角「导出 ▾」：

| 选项 | 得到什么 | 适合 |
| --- | --- | --- |
| 网页单文件 `.html` | 当前这个页面的完整副本，双击即开、可离线、可转发 | 想自己留一份或发给别人 |
| Markdown `.md` | 按章节排好的纯文本，含成本/收益/备注/来源链接 | 想复制、改写、印成纸质 |
| 结构化数据 `.json` | 34 章 631 条的字段化数据 | 想拿去做自己的应用 |

导出的 `.html` 跟你在线看到的完全一样，不依赖本仓库，拷到 U 盘里也能开。

## 本地使用

直接双击 `index.html`。不用构建、不用连网。

## 重新生成

内容来自上游渲染页（`index.html`），用脚本抽成结构化数据再套模板：

```bash
# 1) 抽取正文为结构化数据
python tools/extract.py <上游 index.html> book.json

# 2) 合成单文件页面（--site 会同时覆盖站点根目录的 index.html）
python tools/build.py --site
```

`tools/template.html` 是页面骨架（样式 + 交互），数据用占位符 `__BOOK_DATA__` 注入。

改完页面后同步到 GitHub：

```bash
python tools/publish.py            # 上传默认清单
python tools/publish.py index.html # 只传改动的那个文件
```

`publish.py` 走 GitHub Contents API，专门给 `git push` 被网络环境挡住的情况备用
（脚本会自动取 `gh auth token`，也可用 `GITHUB_TOKEN` 指定）。

## 授权与署名

**正文内容不是公有领域，转载必须署名。** 本仓库的所有权声明分两层：

| 范围 | 授权 | 文件 |
| --- | --- | --- |
| 书本正文内容（index.html 里的 34 章 631 条） | **CC BY 4.0**（须署名） | `LICENSE` |
| tools/ 下的构建脚本与模板 | Unlicense（公有领域） | `LICENSE-CODE` |

署名人（按 CC BY 4.0 要求保留）：

> 《高性价比人生指南》，原作者见 [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)，
> 采用 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 授权。
> 本仓库在其内容基础上**调整了排版**（分章节、加检索与导出），未改动正文，原文数据与结论均照原样保留。

读者在页面底部、导出的 Markdown 头部都能看到同样的署名与许可链接，所以从本仓库导出再转发也不需要额外再标注。

> 说明：网络上流传的某些转载页把这本书标成「Unlicense / 公有领域」，这与上游仓库当前的 `LICENSE`（CC BY 4.0）**不一致**。
> 本仓库按上游当前的正式声明来，宁可多标一层署名。
