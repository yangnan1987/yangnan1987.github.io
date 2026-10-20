/*
 * Cloudflare Web Analytics 与 Microsoft Clarity。
 * noindex 与未公开页面不加载。不要加入其他统计工具。
 */
(function () {
  var cfToken = "b2c1ecf2019f4cf1a4d0984d094269e5";
  var clarityId = "z0va23d3w2";
  var cfPlaceholder = ["CF_WEB", "ANALYTICS_TOKEN"].join("_");
  var clarityPlaceholder = ["CLARITY", "PROJECT_ID"].join("_");

  function configured(value, placeholder) {
    if (typeof value !== "string") return "";
    var trimmed = value.trim();
    if (!trimmed || trimmed === placeholder) return "";
    return trimmed;
  }

  function isNoindexPage() {
    var metas = document.querySelectorAll("meta[name='robots']");
    for (var i = 0; i < metas.length; i++) {
      var content = (metas[i].getAttribute("content") || "").toLowerCase();
      if (content.indexOf("noindex") !== -1) return true;
    }
    return false;
  }

  // 站内未公开、也未放入 sitemap 的页面。公开后从这里去掉文件名即可。
  function isUnpublishedPage() {
    var file = (location.pathname || "").split("/").pop();
    return file === "service-beauty.html" || file === "service-trade.html" || file === "service-welfare.html";
  }

  if (!document.head || isNoindexPage() || isUnpublishedPage()) return;

  var token = configured(cfToken, cfPlaceholder);
  if (token) {
    var beacon = document.createElement("script");
    beacon.defer = true;
    beacon.src = "https://static.cloudflareinsights.com/beacon.min.js";
    beacon.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
    document.head.appendChild(beacon);
  }

  var projectId = configured(clarityId, clarityPlaceholder);
  if (projectId) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", projectId);
  }
})();

(function () {
  window.formatNewsTitle = function (title) {
    var raw = String(title || "");
    var chars = Array.from(raw);
    var keep = 4;
    function esc(s) {
      return String(s)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }
    if (chars.length <= keep + 10) return esc(raw);
    var head = chars.slice(0, -keep).join("");
    var tail = chars.slice(-keep).join("");
    var withBreaks = esc(head)
      .replace(/——/g, "——<wbr>")
      .replace(/：/g, "：<wbr>");
    return withBreaks + '<span class="title-nowrap">' + esc(tail) + "</span>";
  };

  var viewport = document.querySelector('meta[name="viewport"]');
  if (viewport && viewport.content.indexOf("viewport-fit") === -1) {
    viewport.content += ", viewport-fit=cover";
  }

  var header = document.querySelector("header");
  if (!header) return;
  var nav = header.querySelector("nav");
  if (!nav) return;
  if (header.querySelector(".nav-toggle")) return;

  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "nav-toggle";
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "site-nav-panel");
  btn.setAttribute("aria-label", "メニューを開く");
  btn.innerHTML = "<span></span><span></span><span></span>";

  if (!nav.id) nav.id = "site-nav-panel";
  header.insertBefore(btn, nav);

  var overlay = document.createElement("div");
  overlay.className = "nav-overlay";
  overlay.setAttribute("hidden", "");
  document.body.appendChild(overlay);

  function setOpen(open) {
    document.body.classList.toggle("nav-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", open ? "メニューを閉じる" : "メニューを開く");
    if (open) overlay.removeAttribute("hidden");
    else overlay.setAttribute("hidden", "");
  }

  function close() {
    setOpen(false);
  }

  btn.addEventListener("click", function () {
    setOpen(!document.body.classList.contains("nav-open"));
  });
  overlay.addEventListener("click", close);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") close();
  });
  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", close);
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 900) close();
  });

  document.querySelectorAll("table").forEach(function (table) {
    if (table.parentElement && table.parentElement.classList.contains("table-scroll")) return;
    var wrap = document.createElement("div");
    wrap.className = "table-scroll";
    table.parentNode.insertBefore(wrap, table);
    wrap.appendChild(table);
  });
})();
