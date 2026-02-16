/**
 * 根据 news-data.json 为 internal/event 类型新闻生成静态 HTML（便于搜索引擎收录）
 * 运行：node build-news-static.js
 */
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const NEWS_DATA_PATH = path.join(ROOT, 'news-data.json');
const NEWS_DIR = path.join(ROOT, 'news');
const TEMPLATE_PATH = path.join(ROOT, 'news-detail.html');

function escapeHtml(s) {
  if (!s) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function stripHtml(html) {
  if (!html) return '';
  return String(html).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 160);
}

if (!fs.existsSync(NEWS_DIR)) {
  fs.mkdirSync(NEWS_DIR, { recursive: true });
}

const data = JSON.parse(fs.readFileSync(NEWS_DATA_PATH, 'utf8'));
const template = fs.readFileSync(TEMPLATE_PATH, 'utf8');

const items = data.filter((item) => item.type === 'internal' || item.type === 'event');

for (const item of items) {
  const id = item.id;
  const title = item.title || '';
  const desc = stripHtml(item.content) || title;
  const contentHtml = (item.content || '').replace(/src="images\//g, 'src="../images/');
  const innerHtml = `
    <div class="news-detail-header">
        <h1 class="news-detail-title">${escapeHtml(title)}</h1>
        <div class="news-detail-meta">
            <span class="news-detail-date">${escapeHtml(item.date)}</span>
            <span class="news-detail-tag">${escapeHtml(item.tag)}</span>
        </div>
    </div>
    <div class="news-detail-content">${contentHtml}</div>`;

  let html = template
    .replace('<title>NEWS 詳細 - NEW LIFE DEVELOPMENT</title>', `<title>${escapeHtml(title)} - NEW LIFE DEVELOPMENT</title>`)
    .replace(
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
      `<meta name="description" content="${escapeHtml(desc)}">\n    <link rel="canonical" href="https://newlife-dev-group.com/news/${id}.html">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">`
    );

  // 导航链接：从 news/ 子目录指向根目录
  html = html
    .replace(/href="index\.html"/g, 'href="../index.html"')
    .replace(/href="news\.html"/g, 'href="../news.html"')
    .replace(/href="service-asset\.html"/g, 'href="../service-asset.html"')
    .replace(/href="service-ma\.html"/g, 'href="../service-ma.html"')
    .replace(/href="service-trade\.html"/g, 'href="../service-trade.html"')
    .replace(/href="service-welfare\.html"/g, 'href="../service-welfare.html"')
    .replace(/href="service-dental\.html"/g, 'href="../service-dental.html"')
    .replace(/href="service-beauty\.html"/g, 'href="../service-beauty.html"')
    .replace(/href="index\.html#contact"/g, 'href="../index.html#contact"');

  const containerStart = '<div class="container">';
  const scriptEnd = '</script>';
  const idx1 = html.indexOf(containerStart);
  const idx2 = html.indexOf(scriptEnd);
  if (idx1 === -1 || idx2 === -1) {
    console.error('Template structure changed, skip', id);
    continue;
  }

  const before = html.slice(0, idx1);
  const after = html.slice(idx2 + scriptEnd.length);
  const newBlock = `${containerStart}
    <div id="news-detail-container">
${innerHtml}
    </div>
    <div class="back-home">
        <a href="../news.html" class="btn">ニュース一覧に戻る</a>
    </div>
</div>
`;
  html = before + newBlock + after;

  // 移除原来的 script 块（在 newBlock 之后、footer 之前可能还有 script）
  const scriptStart = html.indexOf('<script>', html.indexOf('</div>'));
  if (scriptStart !== -1) {
    const end = html.indexOf('</script>', scriptStart) + '</script>'.length;
    html = html.slice(0, scriptStart) + html.slice(end);
  }

  const outPath = path.join(NEWS_DIR, `${id}.html`);
  fs.writeFileSync(outPath, html, 'utf8');
  console.log('Generated:', outPath);
}

// 自动生成 sitemap.xml（固定页 + 当前所有静态新闻）
const BASE = 'https://newlife-dev-group.com';
const fixedUrls = [
  { loc: `${BASE}/`, changefreq: 'weekly', priority: '1.0' },
  { loc: `${BASE}/index.html`, changefreq: 'weekly', priority: '1.0' },
  { loc: `${BASE}/news.html`, changefreq: 'weekly', priority: '0.9' },
  { loc: `${BASE}/service-asset.html`, changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-ma.html`, changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-trade.html`, changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-welfare.html`, changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-dental.html`, changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-beauty.html`, changefreq: 'monthly', priority: '0.8' },
];
const newsUrls = items.map((item) => ({
  loc: `${BASE}/news/${item.id}.html`,
  changefreq: 'monthly',
  priority: item.type === 'internal' ? '0.6' : '0.7',
}));
const sitemapLines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...fixedUrls.map((u) => `  <url>\n    <loc>${u.loc}</loc>\n    <changefreq>${u.changefreq}</changefreq>\n    <priority>${u.priority}</priority>\n  </url>`),
  ...newsUrls.map((u) => `  <url>\n    <loc>${u.loc}</loc>\n    <changefreq>${u.changefreq}</changefreq>\n    <priority>${u.priority}</priority>\n  </url>`),
  '</urlset>',
];
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemapLines.join('\n'), 'utf8');
console.log('Updated sitemap.xml with', fixedUrls.length + newsUrls.length, 'URLs.');

console.log('Done. Generated', items.length, 'static news pages.');
