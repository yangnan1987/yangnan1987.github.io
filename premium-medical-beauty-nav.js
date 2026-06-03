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
})();
