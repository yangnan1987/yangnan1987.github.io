(function () {
    var NAV = [
        { href: 'premium-medical-beauty-laser.html', label: 'レーザー・光治療' },
        { href: 'premium-medical-beauty-skin.html', label: '肌再生・HIFU' },
        { href: 'premium-medical-beauty-injection.html', label: '注入・ボトックス' },
        { href: 'premium-medical-beauty-drip.html', label: '美容点滴' },
        { href: 'premium-medical-beauty-advanced.html', label: '再生・栄養医療' }
    ];
    var path = location.pathname.split('/').pop() || '';
    var nav = document.getElementById('beauty-nav');
    if (nav) {
        NAV.forEach(function (item) {
            var a = document.createElement('a');
            a.href = item.href;
            a.textContent = item.label;
            if (item.href === path) a.className = 'active';
            nav.appendChild(a);
        });
    }
    var lb = document.getElementById('lightbox');
    if (!lb) {
        lb = document.createElement('div');
        lb.id = 'lightbox';
        lb.innerHTML = '<span class="lb-close" aria-label="閉じる">&times;</span><img src="" alt="">';
        document.body.appendChild(lb);
    }
    var lbImg = lb.querySelector('img');
    var close = function () { lb.classList.remove('open'); lbImg.src = ''; };
    lb.querySelector('.lb-close').onclick = close;
    lb.onclick = function (e) { if (e.target === lb) close(); };
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.querySelectorAll('[data-lightbox]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            e.preventDefault();
            lbImg.src = el.getAttribute('href') || el.dataset.lightbox;
            lbImg.alt = el.querySelector('img') ? el.querySelector('img').alt : '';
            lb.classList.add('open');
        });
    });
})();
