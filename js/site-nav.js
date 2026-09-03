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
