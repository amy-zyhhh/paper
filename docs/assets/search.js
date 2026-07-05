(function () {
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var count = document.getElementById("search-count");
  var papers = [];
  var script = document.currentScript || document.querySelector("script[src$='search.js']");
  var baseUrl = "";

  if (script) {
    baseUrl = script.getAttribute("src").replace(/\/assets\/search\.js(?:\?.*)?$/, "");
  }

  function getMode() {
    var checked = document.querySelector("input[name='search-mode']:checked");
    return checked ? checked.value : "global";
  }

  function normalize(value) {
    return String(value || "").toLowerCase();
  }

  function joinList(values) {
    return Array.isArray(values) ? values.join(" ") : "";
  }

  function searchableText(paper, mode) {
    if (mode === "author") {
      return joinList(paper.authors);
    }
    if (mode === "keyword") {
      return [joinList(paper.keywords), joinList(paper.topics)].join(" ");
    }
    return [
      paper.title,
      joinList(paper.authors),
      paper.date,
      paper.journal,
      paper.doi,
      paper.abstract,
      joinList(paper.keywords),
      joinList(paper.topics),
      paper.ai_text
    ].join(" ");
  }

  function resultHtml(paper) {
    var authors = Array.isArray(paper.authors) ? paper.authors.join(", ") : "";
    var topics = Array.isArray(paper.topics) ? paper.topics.join(", ") : "";
    var url = paper.url && paper.url.charAt(0) === "/" ? baseUrl + paper.url : paper.url;
    return [
      '<article class="paper-summary">',
      '<h2><a href="' + url + '">' + escapeHtml(paper.title || "Untitled paper") + "</a></h2>",
      '<p class="meta"><strong>作者：</strong>' + escapeHtml(authors || "未知作者") + "</p>",
      '<p class="meta"><strong>期刊：</strong>' + escapeHtml(paper.journal || "") + "</p>",
      '<p class="meta"><strong>日期：</strong>' + escapeHtml(paper.date || "") + "</p>",
      '<p class="meta"><strong>DOI：</strong>' + escapeHtml(paper.doi || "") + "</p>",
      '<p>' + escapeHtml(paper.description || paper.abstract || "") + "</p>",
      topics ? '<span class="badge">主题：' + escapeHtml(topics) + "</span>" : "",
      "</article>"
    ].join("");
  }

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function runSearch() {
    var query = normalize(input.value).trim();
    var mode = getMode();
    if (!query) {
      results.innerHTML = "";
      count.textContent = "请输入搜索词。";
      return;
    }

    var tokens = query.split(/\s+/).filter(Boolean);
    var matched = papers.filter(function (paper) {
      var text = normalize(searchableText(paper, mode));
      return tokens.every(function (token) {
        return text.indexOf(token) !== -1;
      });
    });

    count.textContent = "找到 " + matched.length + " 条结果。";
    results.innerHTML = matched.slice(0, 200).map(resultHtml).join("");
  }

  function applyUrlParams() {
    var params = new URLSearchParams(window.location.search);
    var mode = params.get("mode");
    var q = params.get("q") || params.get("author") || params.get("keyword") || "";
    if (params.get("author")) {
      mode = "author";
    }
    if (params.get("keyword")) {
      mode = "keyword";
    }
    if (mode) {
      var radio = document.querySelector("input[name='search-mode'][value='" + mode + "']");
      if (radio) {
        radio.checked = true;
      }
    }
    if (q) {
      input.value = q;
    }
  }

  fetch(baseUrl + "/search-index.json")
    .then(function (response) { return response.json(); })
    .then(function (data) {
      papers = data;
      applyUrlParams();
      runSearch();
    })
    .catch(function () {
      count.textContent = "搜索索引加载失败。";
    });

  input.addEventListener("input", runSearch);
  document.querySelectorAll("input[name='search-mode']").forEach(function (radio) {
    radio.addEventListener("change", runSearch);
  });
}());
