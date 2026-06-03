# -*- coding: utf-8 -*-
"""Generate partner clinic menu pages from beauty-menu-data.yaml."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).resolve().parent / "beauty-menu-data.yaml"

DISCLAIMER = (
    "掲載内容はニューライフ開発株式会社が整理した参考情報です。"
    "施術内容・料金は提携クリニックの最新情報を優先し、予約時にご確認ください。"
)

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{title}｜提携クリニック 施術メニュー</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap" rel="stylesheet">
<link href="premium-medical-beauty.css" rel="stylesheet">
</head>
<body>
<div class="beauty-topbar">
<div class="beauty-topbar-inner">
<a class="beauty-back" href="premium-medical.html">← プレミアム・メディカル事業トップ</a>
<nav class="beauty-nav" id="beauty-nav"></nav>
</div>
</div>
<section class="beauty-hero">
<div class="eyebrow">Partner Clinic Menu</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
</section>
<div class="beauty-wrap">
"""

FOOT = f"""
</div>
<footer class="beauty-footer">
<p class="beauty-disclaimer">{DISCLAIMER}</p>
<p>&copy; 2025 New Life Development Co., Ltd.</p>
</footer>
<script src="premium-medical-beauty-nav.js"></script>
</body>
</html>
"""


def price_table(rows, note="表示価格はすべて税込です。"):
    if not rows:
        return ""
    body = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>"
        if len(r) == 2
        else f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in rows
    )
    if rows and len(rows[0]) == 3:
        head = "<tr><th>施術・内容</th><th>1回</th><th>5回</th></tr>"
    else:
        head = "<tr><th>項目</th><th>料金（税込）</th></tr>"
    return f"""<div class="price-block">
<h3>料金表</h3>
<table class="price-table"><thead>{head}</thead><tbody>{body}</tbody></table>
<p class="price-note">{note}</p>
</div>"""


def meta_block(meta):
    if not meta:
        return ""
    items = []
    labels = [
        ("duration", "施術時間"),
        ("downtime", "ダウンタイム"),
        ("sessions", "目安回数"),
    ]
    for key, label in labels:
        if meta.get(key):
            items.append(f'<div class="meta-item"><span class="meta-label">{label}</span><span class="meta-val">{meta[key]}</span></div>')
    if not items:
        return ""
    return f'<div class="treatment-meta">{"".join(items)}</div>'


def treatment(t):
    bullets = "".join(f"<li>{b}</li>" for b in t["bullets"])
    price = price_table(t.get("price_rows", []), t.get("price_note", "表示価格はすべて税込です。"))
    meta = meta_block(t.get("meta"))
    return f"""<article class="treatment" id="{t['id']}">
<div class="treatment-head">
<h2>{t['title']}</h2>
<div class="en">{t.get('en', '')}</div>
</div>
<div class="treatment-body">
<p class="intro">{t['intro']}</p>
{meta}
<ul class="points">{bullets}</ul>
{price}
</div>
</article>"""


def main():
    with DATA_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for fname, page in data["pages"].items():
        body = "".join(treatment(t) for t in page["treatments"])
        html = HEAD.format(title=page["title"], h1=page["h1"], lead=page["lead"]) + body + FOOT
        (ROOT / fname).write_text(html, encoding="utf-8")
        print("wrote", fname)


if __name__ == "__main__":
    main()
