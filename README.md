# JMPS 文献追踪与分析网页

这个项目用于追踪 **Journal of the Mechanics and Physics of Solids**
（JMPS）的文献，抓取论文元数据，补充 Elsevier / ScienceDirect 内容，
将全文保存在本地，再通过 OpenAI-compatible API 生成中文文献分析笔记，
最后用 Jekyll / GitHub Pages 生成网页。

核心原则：

```text
Python 管数据
Markdown 管内容
Jekyll 管页面
CSS 管样式
全文只保存在本地
网页只展示元数据、摘要和 AI 分析结果
```

## 项目能做什么

完整流程如下：

1. 从 Crossref 抓取 JMPS 论文元数据。
2. 用 DOI 从 Elsevier / ScienceDirect 补充摘要和可用正文。
3. 将可获取的全文保存到本地 `private/full_text/`。
4. 使用 OpenAI-compatible API 对本地全文做中文分析。
5. 将分析结果保存到 `data/analyses.json`。
6. 生成 Jekyll 可识别的 Markdown 页面。
7. 通过 GitHub Pages 发布网页。

公开网页建议只包含：

```text
论文标题
作者
日期
DOI
摘要
主题标签
AI 生成的中文分析笔记
出版社链接
```

不要公开上传 Elsevier 全文，除非你确认有相应权限。

## 目录结构

```text
.
+-- data/
|   +-- papers.json        # 论文元数据和 Elsevier 补全信息
|   +-- analyses.json      # AI 生成的中文分析结果
+-- docs/
|   +-- _config.yml        # Jekyll 配置
|   +-- _layouts/          # Jekyll 页面模板
|   +-- assets/style.css   # 网页样式
|   +-- index.md           # 自动生成的首页
|   +-- papers/            # 自动生成的月份归档页
|   +-- topics/            # 自动生成的主题分类页
+-- private/
|   +-- full_text/         # 本地全文，已被 Git 忽略
+-- scripts/
|   +-- fetch_crossref.py  # 从 Crossref 抓取任意期刊元数据
|   +-- fetch_jmps.py      # JMPS 专用抓取脚本，兼容旧流程
|   +-- enrich_elsevier.py # 从 Elsevier 补摘要和全文
|   +-- analyze_papers.py  # 调用 AI 生成中文分析
|   +-- render_md.py       # 根据 JSON 生成 Markdown 网页
+-- .gitignore
+-- README.md
```

`private/` 是本地私有目录，不应上传到 GitHub。

## 环境变量

在 PowerShell 中设置 API key：

```powershell
$env:ELSEVIER_API_KEY="你的 Elsevier API Key"
$env:OPENAI_API_KEY="你的 OpenAI-compatible API Key"
```

AI 分析脚本当前默认使用：

```text
Base URL: https://llmapi.paratera.com/v1
Model: DeepSeek-V3.2-Thinking
```

如果需要手动覆盖：

```powershell
$env:OPENAI_BASE_URL="https://llmapi.paratera.com/v1"
$env:OPENAI_MODEL="DeepSeek-V3.2-Thinking"
```

## 常用更新流程

先进入项目根目录：

```powershell
cd C:\Users\zhou\Desktop\test
```

### 1. 抓取期刊元数据

推荐使用通用脚本 `fetch_crossref.py`。以后新增期刊时，只需要提供 ISSN 和期刊显示名称。

例如抓取 JMPS：

```powershell
python scripts\fetch_crossref.py --issn 0022-5096 --journal "Journal of the Mechanics and Physics of Solids" --from-date 2025-01-01 --until-date 2026-07-01 --limit 300
```

如果要加入另一个期刊，例如某个期刊的 ISSN 是 `1234-5678`：

```powershell
python scripts\fetch_crossref.py --issn 1234-5678 --journal "Journal Name" --from-date 2025-01-01 --until-date 2026-07-01 --limit 300
```

旧的 JMPS 专用脚本仍然可用：

按明确日期范围抓取：

```powershell
python scripts\fetch_jmps.py --from-date 2025-01-01 --until-date 2026-07-01 --limit 300 --replace-test-data
```

常用参数：

```text
--from-date YYYY-MM-DD     起始发表日期
--until-date YYYY-MM-DD    结束发表日期
--days N                   抓取最近 N 天
--limit N                  最多抓取多少篇
--replace-test-data        删除测试数据
--dry-run                  只预览，不写入 papers.json
```

输出文件：

```text
data/papers.json
```

### 2. 从 Elsevier 补充摘要和全文

补充前几篇论文：

```powershell
python scripts\enrich_elsevier.py --limit 5
```

将可获取的全文保存到本地：

```powershell
python scripts\enrich_elsevier.py --limit 5 --save-full-text
```

从第 6 篇开始继续处理 20 篇：

```powershell
python scripts\enrich_elsevier.py --limit 20 --offset 5 --save-full-text
```

指定某一篇 DOI：

```powershell
python scripts\enrich_elsevier.py --doi "10.1016/j.jmps.2026.106733" --save-full-text
```

重要区别：

```text
--save-full-text
  推荐使用。将全文保存到 private/full_text/*.txt，
  papers.json 里只记录本地路径。

--include-full-text
  不推荐。会把全文直接写进 data/papers.json。
  如果之后 git add / commit / push，可能把全文上传到 GitHub。
```

推荐默认用法：

```powershell
python scripts\enrich_elsevier.py --limit 20 --save-full-text
```

### 3. 使用 AI 生成中文文献分析

先分析 1 篇测试：

```powershell
python scripts\analyze_papers.py --limit 1
```

继续批量分析：

```powershell
python scripts\analyze_papers.py --limit 5 --offset 1
```

指定 DOI 分析：

```powershell
python scripts\analyze_papers.py --doi "10.1016/j.jmps.2026.106733"
```

重新分析已经分析过的论文：

```powershell
python scripts\analyze_papers.py --doi "10.1016/j.jmps.2026.106733" --overwrite
```

输出文件：

```text
data/analyses.json
```

AI 分析会回答这些问题：

```text
文章做了什么工作
为什么要做这个工作
怎么做的
做得怎么样
主要结论是什么
亮点和创新点是什么
有哪些局限性
可能的发展方向
阅读或使用时的注意事项
关键词
适合哪些读者或研究问题
阅读优先级
阅读优先级理由
```

### 4. 重新生成网页 Markdown

只要更新了 `papers.json` 或 `analyses.json`，就需要运行：

```powershell
python scripts\render_md.py
```

它会更新：

```text
docs/index.md
docs/papers/*.md
docs/topics/*.md
docs/search.md
docs/search-index.json
```

其中 `docs/search-index.json` 是静态搜索索引，包含标题、作者、期刊、DOI、
摘要、关键词、主题和 AI 分析文本。搜索页支持：

```text
全局搜索
关键词/主题搜索
作者搜索
```

### 5. 本地预览 Jekyll 网页

```powershell
cd C:\Users\zhou\Desktop\test\docs
bundle exec jekyll build
bundle exec jekyll serve
```

如果 `docs/_config.yml` 中设置了：

```yaml
baseurl: "/paper"
```

则本地访问：

```text
http://127.0.0.1:4000/paper/
```

如果想临时按根路径预览：

```powershell
bundle exec jekyll serve --baseurl ""
```

然后访问：

```text
http://127.0.0.1:4000/
```

## 发布到 GitHub Pages

提交公开安全的文件：

```powershell
cd C:\Users\zhou\Desktop\test
git status
git add .gitignore README.md data docs scripts
git commit -m "Update JMPS tracker"
git push
```

不要提交：

```text
private/
docs/_site/
docs/.jekyll-cache/
__pycache__/
*.pyc
```

这些已经写入 `.gitignore`。

GitHub Pages 设置：

```text
Settings -> Pages
Source: Deploy from a branch
Branch: main 或 master
Folder: /docs
```

如果 GitHub 仓库地址是：

```text
https://github.com/USERNAME/paper
```

则 `docs/_config.yml` 中应包含：

```yaml
baseurl: "/paper"
```

网页地址一般是：

```text
https://USERNAME.github.io/paper/
```

## 技术细节

### `scripts/fetch_crossref.py`

通用 Crossref 抓取脚本。适合后续跟踪多个期刊。

基本用法：

```powershell
python scripts\fetch_crossref.py --issn 0022-5096 --journal "Journal of the Mechanics and Physics of Solids" --from-date 2025-01-01 --until-date 2026-07-01 --limit 300
```

数据来源：

```text
Crossref API
https://api.crossref.org/journals/{ISSN}/works
```

该脚本会把不同期刊的论文合并到同一个：

```text
data/papers.json
```

网页生成时会自动按期刊和月份分组。

### `scripts/fetch_jmps.py`

JMPS 专用脚本，保留用于兼容之前的工作流。后续更推荐使用 `fetch_crossref.py`。

数据来源：

```text
Crossref API
https://api.crossref.org/journals/0022-5096/works
```

JMPS ISSN：

```text
0022-5096
```

主要抓取字段：

```text
title
authors
doi
date
journal
volume
issue
article_number
page
url
abstract
keywords
topics
```

其中 `topics` 是脚本根据标题和摘要中的关键词自动匹配得到的。
通用抓取流程中，规则在 `fetch_crossref.py` 的 `TOPIC_KEYWORDS` 中修改。

### `scripts/enrich_elsevier.py`

通过 DOI 请求 Elsevier Article Retrieval：

```text
https://api.elsevier.com/content/article/doi/{doi}?httpAccept=application/json
```

可能获得：

```text
摘要
关键词
全文文本
正文长度统计
本地全文路径
```

注意：Elsevier API 能否返回全文，取决于文章状态、权限和 API 可用性。

### `scripts/analyze_papers.py`

使用 OpenAI-compatible Chat Completions 接口：

```text
{OPENAI_BASE_URL}/chat/completions
```

当前默认：

```text
https://llmapi.paratera.com/v1/chat/completions
```

当前默认模型：

```text
DeepSeek-V3.2-Thinking
```

脚本会把以下内容发给模型：

```text
标题
DOI
日期
作者
作者单位
摘要
本地全文或正文片段
```

然后将模型返回的 JSON 分析保存到：

```text
data/analyses.json
```

### `scripts/render_md.py`

读取：

```text
data/papers.json
data/analyses.json
```

生成：

```text
docs/index.md
docs/papers/*.md
docs/topics/*.md
docs/search.md
docs/search-index.json
```

如果某篇论文有 AI 分析结果，网页会在该论文下面显示 `AI Notes` 区块。
搜索功能由 `docs/assets/search.js` 在浏览器端完成，不需要服务器。

## 内容安全建议

可以上传到 GitHub Pages 的内容：

```text
论文元数据
摘要
AI 生成的分析笔记
出版社链接
主题标签
```

应只保存在本地的内容：

```text
Elsevier 全文
原始下载正文
API key
任何受版权或订阅限制的内容
```

不要将 `private/` 上传到 GitHub。
不要轻易使用 `--include-full-text`。

## 推荐完整更新流程

一般更新时可以按下面顺序：

```powershell
cd C:\Users\zhou\Desktop\test
python scripts\fetch_crossref.py --issn 0022-5096 --journal "Journal of the Mechanics and Physics of Solids" --from-date 2025-01-01 --until-date 2026-07-01 --limit 300
python scripts\enrich_elsevier.py --limit 20 --save-full-text
python scripts\analyze_papers.py --limit 5
python scripts\render_md.py
cd docs
bundle exec jekyll build
bundle exec jekyll serve
```

确认本地网页没问题后，再提交并推送。

## 常见问题

### 网页还是旧内容

通常是 Markdown 或 Jekyll 没重新生成。

运行：

```powershell
cd C:\Users\zhou\Desktop\test
python scripts\render_md.py
cd docs
bundle exec jekyll build
bundle exec jekyll serve
```

如果设置了 `baseurl: "/paper"`，访问：

```text
http://127.0.0.1:4000/paper/
```

### Elsevier 返回 404

这不一定是错误。可能原因：

```text
Crossref 已有 DOI，但 Elsevier API 尚未同步
该文章暂时不支持 Article Retrieval
权限不足
文章过新
```

可以换一个较早的 DOI 测试。

### AI API 返回 JSON 或兼容性错误

当前 `analyze_papers.py` 使用：

```text
/chat/completions
response_format: {"type": "json_object"}
```

如果服务商不支持 `response_format`，可以在 `request_openai()` 中删除该字段，
然后依靠提示词要求模型“只输出 JSON”。

### 不小心把全文写进 `papers.json`

如果运行过：

```powershell
python scripts\enrich_elsevier.py --include-full-text
```

提交前务必检查 `data/papers.json`。

推荐只使用：

```powershell
python scripts\enrich_elsevier.py --save-full-text
```

## 后续可改进方向

可以考虑继续增加：

```text
每篇论文单独详情页
按阅读优先级筛选
按关键词搜索
按年份/月份/主题过滤
AI 自动生成主题标签
GitHub Actions 定时更新元数据
更精细的论文推荐评分
```

如果以后要大规模分析全文，建议控制批量大小，先用 `--limit 1`
测试输出质量，再逐步扩大。

