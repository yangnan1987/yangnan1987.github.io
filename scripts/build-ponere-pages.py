# -*- coding: utf-8 -*-
"""Generate Ponere beauty sub-pages from structured data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{title}｜ポネレ美容提案</title>
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
<div class="eyebrow">Ponere Beauty Proposal</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
</section>
<div class="beauty-wrap">
"""

FOOT = """
</div>
<footer class="beauty-footer">&copy; 2025 New Life Development Co., Ltd.</footer>
<script src="premium-medical-beauty-nav.js"></script>
</body>
</html>
"""


def gallery(pages):
    items = "".join(
        f'<a href="ponere/pages/{p}.webp" data-lightbox><img src="ponere/pages/{p}.webp" alt="原稿 p{p[1:]}" loading="lazy"></a>'
        for p in pages
    )
    return f"""<details class="doc-gallery">
<summary>詳細資料（原稿画像）</summary>
<div class="doc-grid">{items}</div>
</details>"""


def price_table(rows, note="表示価格はすべて税込です。"):
    body = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td></tr>" if len(r) == 2 else
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
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


def treatment(t):
    bullets = "".join(f"<li>{b}</li>" for b in t["bullets"])
    price = t.get("price_html", "")
    return f"""<article class="treatment" id="{t['id']}">
<div class="treatment-head">
<h2>{t['title']}</h2>
<div class="en">{t.get('en','')}</div>
</div>
<div class="treatment-body">
<p class="intro">{t['intro']}</p>
<ul class="points">{bullets}</ul>
{price}
{gallery(t['pages'])}
</div>
</article>"""


PAGES = {
    "premium-medical-beauty-laser.html": {
        "title": "レーザー・光治療",
        "h1": "レーザー・光治療",
        "lead": "ピコ秒レーザー、IPL、医療脱毛など、最新光治療機器による肌質改善・シミ・脱毛プログラム。アジア人の肌質に配慮した施術メニューです。",
        "treatments": [
            {
                "id": "picoway",
                "title": "Pico Way（ピコウェイ）",
                "en": "Ultra Picosecond Laser",
                "intro": "超ピコ秒レーザーでメラニンを極短時間で粉砕。コラーゲン生成を促し、ダウンタイムを抑えながらシミ・肝斑・刺青・毛穴・小ジワの改善を目指します。",
                "bullets": [
                    "シミ・そばかす・肌色ムラ・肝斑・刺青除去",
                    "小ジワ・肌のハリ改善",
                    "ニキビ痕・毛穴の引き締め",
                    "肌のトーンアップ・全体リジュビネーション",
                ],
                "pages": ["p01", "p02", "p03"],
            },
            {
                "id": "ipl",
                "title": "IPL xeo / IPL360",
                "en": "Genesis + Limelight",
                "intro": "アジア人の肌向けに開発された光治療。GenesisレーザーとLimelightを組み合わせ、シミ・赤み・毛穴・細かいシワを総合的に改善します。",
                "bullets": [
                    "シミ・そばかす・赤ら顔・毛穴・小ジワ",
                    "施術時間が短く、ダウンタイムが少ない",
                    "メイク・外出が可能な「ノーダウンタイム」",
                    "痛みが軽い施術",
                ],
                "pages": ["p04", "p05", "p06"],
            },
            {
                "id": "gentlemax",
                "title": "GentleMax Pro Plus",
                "en": "Medical Laser Hair Removal",
                "intro": "Candela製最新脱毛レーザー。755nmアレキサンドライトと1064nm YAGを搭載し、産毛から硬毛まで効率的に処理。冷却機能で快適な施術を実現します。",
                "bullets": [
                    "短期間での永久脱毛",
                    "毛穴・肌質改善も期待",
                    "ほぼ全肌質・毛質に対応",
                    "痛みが少なく安全",
                ],
                "pages": ["p07", "p08", "p09"],
            },
        ],
    },
    "premium-medical-beauty-skin.html": {
        "title": "肌再生・HIFU・ピーリング",
        "h1": "肌再生・HIFU・ピーリング",
        "lead": "マイクロニードル、水光注射、HIFU、マッサージピール、イオン導入など、肌の再生と引き締めを目的とした施術ラインアップ。",
        "treatments": [
            {
                "id": "dermapen",
                "title": "Dermapen 4（ダーマペン4）",
                "en": "Microneedling",
                "intro": "極細針で微小創傷を作り、肌本来の再生力を引き出すマイクロニードリング。ニキビ痕・毛穴・小ジワ・ストレッチマークに対応。",
                "bullets": [
                    "ニキビ痕・毛穴・小ジワ・肌のハリ改善",
                    "人間幹細胞上清液・PRP・Massage Peelとの併用可",
                    "麻酔・針具代込み",
                    "ダウンタイム1〜2日程度",
                ],
                "pages": ["p10", "p11", "p12"],
                "price_html": price_table([
                    ("ダーマペン＋人間幹細胞培養上清液", "¥47,300", "¥189,200"),
                    ("ダーマペン＋PRP（多血小板血漿）", "¥88,000", "¥352,000"),
                    ("ダーマペン＋Massage Peel", "¥41,800", "¥167,200"),
                ]),
            },
            {
                "id": "dds",
                "title": "水光注射 / Drug Delivery System",
                "en": "Skin Booster Injection",
                "intro": "ヒアルロン酸ベースの美容成分を直接真皮層へ注入。Filorga、Rejuran、PRX-T33など、肌質に合わせた薬剤を選択できます。",
                "bullets": [
                    "乾燥・小ジワ・毛穴・くすみの改善",
                    "9本針水光ガンで均一・低痛施術",
                    "ダウンタイムが短い",
                    "内側からの潤いと透明感",
                ],
                "pages": ["p13", "p14", "p15"],
            },
            {
                "id": "hifu",
                "title": "Cinderella HIFU",
                "en": "High-Intensity Focused Ultrasound",
                "intro": "医療用HIFUでSMAS層まで熱エネルギーを集中。切らないリフトアップで、フェイスライン・たるみ・法令線の改善を目指します。",
                "bullets": [
                    "たるみ・フェイスライン・二重あご",
                    "1回約10分の高効率施術",
                    "基本ダウンタイムなし",
                    "痛みが少なく麻酔不要",
                ],
                "pages": ["p16", "p17", "p18"],
            },
            {
                "id": "massagepeel",
                "title": "Massage Peel PRX-T33",
                "en": "Non-invasive Peel",
                "intro": "TCA・過酸化水素・コウジ酸配合のピーリング。表皮を剥がさず真皮から肌再生を促進。ハリ・シワ・くすみ・ニキビ痕に。",
                "bullets": [
                    "肌のハリ・深いシワ・たるみ・ストレッチマーク",
                    "くすみ・シミ・透明感の向上",
                    "ニキビ痕・毛穴の引き締め",
                    "痛みが少なくダウンタイム短",
                ],
                "pages": ["p25", "p26", "p27"],
            },
            {
                "id": "electro",
                "title": "Electroporation（イオン導入）",
                "en": "Electroporation",
                "intro": "高電圧パルスで一時的な細胞膜孔を形成し、ビタミンC・成長因子・幹細胞上清液などを真皮層へ効率よく浸透させます。",
                "bullets": [
                    "高分子成分の深部浸透",
                    "施術10〜20分・低ダウンタイム",
                    "副作用リスクが低い",
                    "他施術との組み合わせに最適",
                ],
                "pages": ["p28", "p29", "p30"],
            },
        ],
    },
    "premium-medical-beauty-injection.html": {
        "title": "注入・ボトックス",
        "h1": "注入・ボトックス",
        "lead": "ヒアルロン酸（ジュビダーム）による輪郭形成と、ボトックスビスタ／NABOTAによる表情ジワ・エラ張り改善。厚労省認可製剤を使用。",
        "treatments": [
            {
                "id": "filler",
                "title": "ヒアルロン酸注入（Juvéderm Vista）",
                "en": "Dermal Filler",
                "intro": "アラガン社製ジュビダーム。低吸水性・高硬度でリフト・輪郭形成・シワ改善に。額・涙袋・頬・法令線・顎など部位別にデザイン。",
                "bullets": [
                    "深いシワ・ボリュームロス・輪郭形成",
                    "鈍針使用で安全性・自然な仕上がり",
                    "即効性・ダウンタイム最小",
                    "6〜12ヶ月で吸収・メンテナンス可能",
                ],
                "pages": ["p19", "p20", "p21"],
                "price_html": price_table([
                    ("Juvéderm volumaXC / voliftXC / voluxXC 1ml（1本目）", "¥93,500"),
                    ("同シリーズ 1ml（2本目）", "¥82,500"),
                    ("同シリーズ 1ml（3本目以降）", "¥71,500"),
                    ("無菌カニューレ針 1本", "¥2,200"),
                    ("表面麻酔", "¥3,300"),
                    ("ヒアルロン酸分解酶 0.5ml（1本目）", "¥11,000"),
                    ("同 0.5ml（2本目）", "¥17,600"),
                ]),
            },
            {
                "id": "botox",
                "title": "ボトックス注射",
                "en": "Botulinum Toxin",
                "intro": "アラガン社ボトックスビスタ®（A型ボツリヌス毒素）。表情筋を弛緩させシワ改善、エラ張り・多汗症にも。NABOTA®も選択可。",
                "bullets": [
                    "額・眉間・目尻・鼻・顎・ガミースマイル等",
                    "エラ張り（小顔）・多汗症",
                    "ランチタイム施術・ダウンタイムほぼなし",
                    "効果持続約4〜6ヶ月",
                ],
                "pages": ["p22", "p23", "p24"],
                "price_html": price_table([
                    ("額・眉間・鼻・目尻・唇等（セット部位）", "¥22,000"),
                    ("両側咬筋", "¥44,000"),
                    ("下顎シワ", "¥88,000"),
                    ("ボトックスビスタ 50単位", "¥66,000"),
                    ("同 100単位", "¥118,800"),
                    ("同 150単位", "¥168,300"),
                    ("同 200単位", "¥211,200"),
                    ("NABOTA 100単位", "¥77,000"),
                    ("NABOTA 200単位", "¥123,200"),
                    ("表面麻酔", "¥3,300"),
                ]),
            },
        ],
    },
    "premium-medical-beauty-drip.html": {
        "title": "美容点滴・NMN",
        "h1": "美容点滴・NMN",
        "lead": "ビタミンC・NMN・白玉点滴・幹細胞上清液など、血管から直接美容成分を補給。疲労回復・美白・アンチエイジングをサポート。",
        "treatments": [
            {
                "id": "drip",
                "title": "美容点滴・注射",
                "en": "Beauty Drip",
                "intro": "経口サプリより吸収率が高く、全身へ均一に成分を行き渡らせます。高濃度ビタミンC、プラセンタ、白玉（グルタチオン）、NMNなど豊富なラインナップ。",
                "bullets": [
                    "高濃度ビタミンC・プラセンタ・NMN",
                    "グルタチオン解毒・美白点滴",
                    "マイヤーズカクテル・抗老化点滴",
                    "ダウンタイムほぼなし",
                ],
                "pages": ["p31", "p32"],
                "price_html": price_table([
                    ("グルタチオン解毒点滴 800mg", "¥6,600"),
                    ("同 1200mg", "¥8,250"),
                    ("同 1600mg", "¥9,900"),
                    ("同 2000mg", "¥11,550"),
                    ("マイヤーズカクテル", "¥8,800"),
                    ("マイヤーズ＋グルタチオン", "¥9,350"),
                    ("抗老化点滴", "¥9,900"),
                    ("白玉点滴", "¥10,230"),
                    ("美髪点滴", "¥5,500"),
                    ("二日酔い点滴", "¥3,850"),
                    ("疲労回復点滴 Level1〜4", "¥4,189〜¥14,960"),
                    ("プラセンタ注射 1A", "¥1,100"),
                    ("プラセンタ注射 2A", "¥1,980"),
                ]),
            },
            {
                "id": "vc",
                "title": "高濃度ビタミンC点滴",
                "en": "High-dose Vitamin C",
                "intro": "Mylan製・オーストラリア製など、用量に応じた高濃度ビタミンC点滴。抗酸化・美白・免疫サポート。",
                "bullets": [
                    "25g〜100g（Mylan）／30g〜60g（豪州製）",
                    "5回コース割引あり",
                    "αリポ酸追加オプション可",
                    "G6PD検査推奨",
                ],
                "pages": ["p32"],
                "price_html": price_table([
                    ("Mylan 25g（1回 / 5回）", "¥14,300 / ¥64,350"),
                    ("Mylan 50g（1回 / 5回）", "¥22,000 / ¥99,000"),
                    ("Mylan 75g（1回 / 5回）", "¥27,500 / ¥123,750"),
                    ("Mylan 100g（1回 / 5回）", "¥33,000 / ¥148,500"),
                    ("豪州製 30g（1回 / 5回）", "¥14,300 / ¥64,350"),
                    ("豪州製 60g（1回 / 5回）", "¥22,000 / ¥99,000"),
                    ("αリポ酸 100mg / 300mg", "¥1,320 / ¥2,420"),
                    ("G6PD血液検査", "¥3,300"),
                ]),
            },
            {
                "id": "nmn",
                "title": "NMN点滴",
                "en": "Nicotinamide Mononucleotide",
                "intro": "NAD+前駆体NMNを直接補給。細胞エネルギー代謝・長寿遺伝子（サーチュイン）活性化をサポートする次世代アンチエイジング点滴。",
                "bullets": [
                    "100mg / 200mg コース",
                    "5回パックあり",
                    "点滴前採血 ¥3,300",
                    "全身のエネルギー・睡眠・代謝改善",
                ],
                "pages": ["p33", "p34"],
                "price_html": price_table([
                    ("NMN 100mg（1回 / 5回）", "¥41,800 / ¥167,200"),
                    ("NMN 200mg（1回 / 5回）", "¥77,000 / ¥308,000"),
                    ("NMN点滴前採血", "¥3,300"),
                ]),
            },
            {
                "id": "stemsup-drip",
                "title": "StemSup® 幹細胞上清液点滴",
                "en": "Stem Cell Supernatant",
                "intro": "乳歯髄・脂肪・臍帯由来の幹細胞培養上清液。1A〜3Aの用量で肌再生・全身アンチエイジング。",
                "bullets": [
                    "StemSup-DP（乳歯髄由来）",
                    "StemSup-A（脂肪由来）",
                    "StemSup-Uc（臍帯由来）",
                    "上清液点滴前採血 ¥3,300",
                ],
                "pages": ["p32"],
                "price_html": price_table([
                    ("StemSup-DP 1A / 2A / 3A", "¥66,000 / ¥118,800 / ¥168,300"),
                    ("StemSup-A 1A / 2A / 3A", "¥66,000 / ¥118,800 / ¥168,300"),
                    ("StemSup-Uc 1A / 2A / 3A", "¥82,500 / ¥148,500 / ¥210,375"),
                ]),
            },
        ],
    },
    "premium-medical-beauty-advanced.html": {
        "title": "再生医療・栄養療法",
        "h1": "再生医療・正分子栄養",
        "lead": "正分子栄養療法、遅延型食物アレルギー検査、間葉系幹細胞・線維芽細胞移植など、根本からの健康と美容を目指す先端医療。",
        "treatments": [
            {
                "id": "ortho",
                "title": "正分子栄養療法",
                "en": "Orthomolecular Medicine",
                "intro": "薬に頼らず、栄養と食事の最適化で体質改善。詳細な血液検査に基づき、専門医がサプリメント・食事指導を個別設計。",
                "bullets": [
                    "慢性疲労・不定愁訴の原因究明",
                    "一般健診より詳細な栄養状態分析",
                    "食事・サプリ・生活習慣の三位一体",
                    "3〜6ヶ月で体感しやすい",
                ],
                "pages": ["p35", "p36"],
            },
            {
                "id": "allergy",
                "title": "遅発性食物アレルギー検査",
                "en": "Delayed Food Allergy Test",
                "intro": "1滴の血液で96項目以上の食物反応をスクリーニング。数時間〜数日後に現れる遅延型アレルギーの原因特定と除去食プログラム。",
                "bullets": [
                    "頭痛・疲労・肌荒れ・消化器症状",
                    "個別除去食・再導入プログラム",
                    "3〜6ヶ月の調整期間",
                    "科学的根拠に基づく食事戦略",
                ],
                "pages": ["p37"],
            },
            {
                "id": "regen",
                "title": "再生医療・幹細胞治療",
                "en": "Regenerative Medicine",
                "intro": "間葉系幹細胞、線維芽細胞移植、PRP、免疫細胞療法など。組織修復・抗老化・美容再生を統合的にサポート。",
                "bullets": [
                    "間葉系幹細胞・線維芽細胞・PRP",
                    "肌再生・全身アンチエイジング",
                    "iNKT・免疫細胞療法",
                    "早期がん検査オプション",
                ],
                "pages": ["p38", "p39", "p40", "p41", "p42"],
                "price_html": price_table([
                    ("StemSup-DP 1A〜5A", "¥66,000〜¥247,500"),
                    ("StemSup-A 1A〜5A", "¥66,000〜¥247,500"),
                    ("StemSup-Uc 1A〜5A", "¥82,500〜¥309,375"),
                    ("上清液点滴前採血", "¥3,300"),
                ]),
            },
        ],
    },
}


def main():
    for fname, data in PAGES.items():
        body = "".join(treatment(t) for t in data["treatments"])
        html = HEAD.format(title=data["title"], h1=data["h1"], lead=data["lead"]) + body + FOOT
        (ROOT / fname).write_text(html, encoding="utf-8")
        print("wrote", fname)


if __name__ == "__main__":
    main()
