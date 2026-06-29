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
const BASE = 'https://newlife-dev-group.com';
const DEFAULT_OG_IMAGE = `${BASE}/hero-bg.jpg`;

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

function parseDateToIso(dateStr) {
  if (!dateStr) return new Date().toISOString().slice(0, 10);
  const normalized = String(dateStr)
    .replace(/年/g, '-')
    .replace(/月/g, '-')
    .replace(/日/g, '')
    .replace(/\./g, '-')
    .trim();
  const parts = normalized.split('-').filter(Boolean);
  if (parts.length >= 3) {
    const y = parts[0];
    const m = String(parts[1]).padStart(2, '0');
    const d = String(parts[2]).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }
  return new Date().toISOString().slice(0, 10);
}

function extractFirstImage(content) {
  const m = String(content || '').match(/src="images\/([^"]+)"/);
  if (m) return `${BASE}/images/${m[1]}`;
  return DEFAULT_OG_IMAGE;
}

function fileLastmod(relativePath) {
  try {
    return fs.statSync(path.join(ROOT, relativePath)).mtime.toISOString().slice(0, 10);
  } catch {
    return new Date().toISOString().slice(0, 10);
  }
}

function getTagClass(tag) {
  if (tag === 'お知らせ') return 'tag-internal';
  if (tag === 'ニュース') return 'tag-news';
  if (tag === '活動レポート' || tag === '研究レポート') return 'tag-event';
  return '';
}

function stripExistingSeoMeta(html) {
  return html
    .replace(/\s*<meta\s+name="robots"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<meta\s+name="description"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<link\s+rel="canonical"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<meta\s+property="og:[^"]*"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<meta\s+property="article:[^"]*"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<meta\s+name="twitter:[^"]*"[^>]*>\s*/gi, '\n    ')
    .replace(/\s*<script\s+type="application\/ld\+json">[\s\S]*?<\/script>\s*/gi, '\n    ');
}

function buildArticleSeoBlock(item, id, title, desc) {
  const pageUrl = `${BASE}/news/${id}.html`;
  const ogImage = extractFirstImage(item.content);
  const datePublished = parseDateToIso(item.date);

  const ogTwitter = `    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="${escapeHtml(title)}">
    <meta property="og:description" content="${escapeHtml(desc)}">
    <meta property="og:url" content="${pageUrl}">
    <meta property="og:image" content="${ogImage}">
    <meta property="og:site_name" content="ニューライフ開発株式会社">
    <meta property="og:locale" content="ja_JP">
    <meta property="article:published_time" content="${datePublished}">
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${escapeHtml(title)}">
    <meta name="twitter:description" content="${escapeHtml(desc)}">
    <meta name="twitter:image" content="${ogImage}">`;

  const jsonLd = `    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": ${JSON.stringify(title)},
      "description": ${JSON.stringify(desc)},
      "datePublished": "${datePublished}",
      "dateModified": "${datePublished}",
      "url": "${pageUrl}",
      "image": "${ogImage}",
      "author": {
        "@type": "Organization",
        "name": "ニューライフ開発株式会社"
      },
      "publisher": {
        "@type": "Organization",
        "name": "ニューライフ開発株式会社",
        "logo": {
          "@type": "ImageObject",
          "url": "${DEFAULT_OG_IMAGE}"
        }
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "${pageUrl}"
      }
    }
    </script>`;

  return { ogTwitter, jsonLd, datePublished };
}

function buildNewsCardHtml(item, variant) {
  const linkHref =
    item.type === 'internal' || item.type === 'event'
      ? `news/${item.id}.html`
      : item.url || '#';
  const linkTarget = item.type === 'internal' || item.type === 'event' ? '' : ' target="_blank" rel="noopener noreferrer"';
  const linkText = item.type === 'internal' || item.type === 'event' ? '詳細を見る' : '記事を読む';
  const tagClass = getTagClass(item.tag);
  const title = escapeHtml(item.title || '');
  const date = escapeHtml(item.date || '');
  const tag = escapeHtml(item.tag || '');

  if (variant === 'home') {
    return `                <div class="news-card-home">
                    <div class="news-info-home">
                        <span class="news-date-home">${date}</span>
                        <span class="news-tag-home ${tagClass}">${tag}</span>
                        <div class="news-title-home">${title}</div>
                    </div>
                    <a href="${linkHref}" class="news-link-btn-home"${linkTarget}>${linkText}</a>
                </div>`;
  }

  return `                <div class="news-card">
                    <div class="news-info">
                        <span class="news-date">${date}</span>
                        <span class="news-tag ${tagClass}">${tag}</span>
                        <div class="news-title">${title}</div>
                    </div>
                    <a href="${linkHref}" class="news-link-btn"${linkTarget}>${linkText}</a>
                </div>`;
}

function buildCrawlNewsList(data, limit) {
  const list = limit ? data.slice(0, limit) : data;
  const cards = list.map((item) => buildNewsCardHtml(item, limit ? 'home' : 'list')).join('\n');
  return `${cards}
                <noscript><p><a href="news.html">ニュース一覧を見る</a></p></noscript>`;
}

function injectBetweenMarkers(filePath, startMarker, endMarker, content) {
  const html = fs.readFileSync(filePath, 'utf8');
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker);
  if (start === -1 || end === -1 || end <= start) {
    console.warn('Markers not found in', filePath);
    return;
  }
  const updated =
    html.slice(0, start + startMarker.length) +
    '\n' +
    content +
    '\n' +
    html.slice(end);
  fs.writeFileSync(filePath, updated, 'utf8');
  console.log('Injected crawl links into', path.basename(filePath));
}

function markOrphanNewsPages(activeIds) {
  if (!fs.existsSync(NEWS_DIR)) return;
  const files = fs.readdirSync(NEWS_DIR).filter((f) => f.endsWith('.html'));
  for (const file of files) {
    const id = file.replace(/\.html$/, '');
    if (activeIds.has(id)) continue;
    const filePath = path.join(NEWS_DIR, file);
    let html = fs.readFileSync(filePath, 'utf8');
    if (!/name="robots"\s+content="[^"]*noindex/i.test(html)) {
      html = html.replace(
        '<meta charset="UTF-8">',
        '<meta charset="UTF-8">\n    <meta name="robots" content="noindex, follow">'
      );
    }
    const canonicalCount = (html.match(/<link\s+rel="canonical"/gi) || []).length;
    if (canonicalCount > 1) {
      html = html.replace(/\s*<link\s+rel="canonical"[^>]*>\s*/gi, '\n    ');
      html = html.replace(
        '<meta charset="UTF-8">',
        `<meta charset="UTF-8">\n    <link rel="canonical" href="${BASE}/news/${id}.html">`
      );
    }
    fs.writeFileSync(filePath, html, 'utf8');
    console.log('Marked orphan as noindex:', file);
  }
}

if (!fs.existsSync(NEWS_DIR)) {
  fs.mkdirSync(NEWS_DIR, { recursive: true });
}

const data = JSON.parse(fs.readFileSync(NEWS_DATA_PATH, 'utf8'));
const template = fs.readFileSync(TEMPLATE_PATH, 'utf8');
const items = data.filter((item) => item.type === 'internal' || item.type === 'event');
const activeIds = new Set(items.map((item) => item.id));

for (const item of items) {
  const id = item.id;
  const title = item.title || '';
  const desc = stripHtml(item.content) || title;
  const tagClass = getTagClass(item.tag);
  const { ogTwitter, jsonLd } = buildArticleSeoBlock(item, id, title, desc);
  const contentHtml = (item.content || '')
    .replace(/src="images\//g, 'src="../images/')
    .replace(/data-lightbox-src="images\//g, 'data-lightbox-src="../images/');
  const innerHtml = `
    <div class="news-detail-header">
        <h1 class="news-detail-title">${escapeHtml(title)}</h1>
        <div class="news-detail-meta">
            <span class="news-detail-date">${escapeHtml(item.date)}</span>
            <span class="news-detail-tag ${tagClass}">${escapeHtml(item.tag)}</span>
        </div>
    </div>
    <div class="news-detail-content">${contentHtml}</div>`;

  let html = stripExistingSeoMeta(template)
    .replace('<title>NEWS 詳細 - NEW LIFE DEVELOPMENT</title>', `<title>${escapeHtml(title)} - NEW LIFE DEVELOPMENT</title>`)
    .replace(
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
      `<meta name="description" content="${escapeHtml(desc)}">
    <link rel="canonical" href="${BASE}/news/${id}.html">
${ogTwitter}
${jsonLd}
    <meta name="viewport" content="width=device-width, initial-scale=1.0">`
    );

  html = html
    .replace(/href="index\.html"/g, 'href="../index.html"')
    .replace(/href="news\.html"/g, 'href="../news.html"')
    .replace(/href="service-asset\.html"/g, 'href="../service-asset.html"')
    .replace(/href="service-ma\.html"/g, 'href="../service-ma.html"')
    .replace(/href="service-dental\.html"/g, 'href="../service-dental.html"')
    .replace(/href="service-management\.html"/g, 'href="../service-management.html"')
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

  const dynamicMarker = "urlParams.get('id')";
  let searchPos = 0;
  while (true) {
    const s = html.indexOf('<script>', searchPos);
    if (s === -1) break;
    const e = html.indexOf('</script>', s);
    if (e === -1) break;
    const blockEnd = e + '</script>'.length;
    const block = html.slice(s, blockEnd);
    if (block.includes(dynamicMarker)) {
      html = html.slice(0, s) + html.slice(blockEnd);
      break;
    }
    searchPos = s + 1;
  }

  const outPath = path.join(NEWS_DIR, `${id}.html`);
  fs.writeFileSync(outPath, html, 'utf8');
  console.log('Generated:', outPath);
}

const fixedUrls = [
  { loc: `${BASE}/`, file: 'index.html', changefreq: 'weekly', priority: '1.0' },
  { loc: `${BASE}/news.html`, file: 'news.html', changefreq: 'weekly', priority: '0.9' },
  { loc: `${BASE}/service-asset.html`, file: 'service-asset.html', changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-ma.html`, file: 'service-ma.html', changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-dental.html`, file: 'service-dental.html', changefreq: 'monthly', priority: '0.8' },
  { loc: `${BASE}/service-management.html`, file: 'service-management.html', changefreq: 'monthly', priority: '0.8' },
].map((u) => ({ ...u, lastmod: fileLastmod(u.file) }));

const newsUrls = items.map((item) => ({
  loc: `${BASE}/news/${item.id}.html`,
  changefreq: 'monthly',
  priority: item.type === 'internal' ? '0.6' : '0.7',
  lastmod: parseDateToIso(item.date),
}));

function sitemapUrlEntry(u) {
  return `  <url>
    <loc>${u.loc}</loc>
    <lastmod>${u.lastmod}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`;
}

const sitemapLines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...fixedUrls.map(sitemapUrlEntry),
  ...newsUrls.map(sitemapUrlEntry),
  '</urlset>',
];
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemapLines.join('\n'), 'utf8');
console.log('Updated sitemap.xml with', fixedUrls.length + newsUrls.length, 'URLs.');

const fullListHtml = buildCrawlNewsList(data, 0);
injectBetweenMarkers(
  path.join(ROOT, 'news.html'),
  '<!-- BUILD:NEWS_LIST_START -->',
  '<!-- BUILD:NEWS_LIST_END -->',
  fullListHtml
);

const homeListHtml = buildCrawlNewsList(data, 5);
injectBetweenMarkers(
  path.join(ROOT, 'index.html'),
  '<!-- BUILD:HOME_NEWS_START -->',
  '<!-- BUILD:HOME_NEWS_END -->',
  homeListHtml
);

markOrphanNewsPages(activeIds);

console.log('Done. Generated', items.length, 'static news pages.');
