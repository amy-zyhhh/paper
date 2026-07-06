---
layout: default
title: "搜索"
permalink: /search/
---

# 搜索

<div class="search-panel">
<input id="search-input" class="search-input" type="search" placeholder="输入标题、作者、关键词、主题、DOI 或 AI 分析内容">
<div class="search-modes" role="radiogroup" aria-label="搜索模式">
<label><input type="radio" name="search-mode" value="global" checked> 全局搜索</label>
<label><input type="radio" name="search-mode" value="keyword"> 关键词/主题</label>
<label><input type="radio" name="search-mode" value="author"> 作者</label>
</div>
<p id="search-count" class="meta">请输入搜索词。</p>
</div>
<div id="search-results"></div>
<script src="{{ '/assets/search.js' | relative_url }}"></script>
