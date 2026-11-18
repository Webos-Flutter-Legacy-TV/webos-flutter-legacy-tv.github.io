// Shared header/footer, active nav link, mobile menu, copy buttons, TOC highlight.
(function () {
  var GH = 'https://github.com/Webos-Flutter-Legacy-TV';
  var pages = [
    ['index.html', 'Home'], ['compatibility.html', 'Compatibility'], ['get-started.html', 'Get started'],
    ['development.html', 'Development'], ['how-it-works.html', 'How it works'], ['contribute.html', 'Contribute']
  ];
  var here = location.pathname.split('/').pop() || 'index.html';

  var header = document.querySelector('header.top');
  if (header) {
    header.innerHTML = '<div class="wrap"><a class="brand" href="index.html"><img src="assets/logo.svg" alt="">Webos Flutter Legacy TV</a>' +
      '<button class="menu-btn" aria-label="Menu" aria-expanded="false">Menu</button><nav class="nav">' +
      pages.map(function (p) { return '<a href="' + p[0] + '"' + (p[0] === here ? ' class="active" aria-current="page"' : '') + '>' + p[1] + '</a>'; }).join('') +
      '<a class="gh" href="' + GH + '">GitHub</a></nav></div>';
    var btn = header.querySelector('.menu-btn'), nav = header.querySelector('.nav');
    btn.addEventListener('click', function () { var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o); });
  }

  var footer = document.querySelector('footer');
  if (footer) {
    footer.innerHTML = '<div class="wrap cols">' +
      '<div><h4>Webos Flutter Legacy TV</h4><p>Flutter apps built with LG\'s flutter-webos SDK, running on older webOS TV releases.</p>' +
      '<p>Community project, not affiliated with or endorsed by LG Electronics. webOS and LG are trademarks of LG Electronics. Flutter is a trademark of Google LLC.</p></div>' +
      '<div><h4>Docs</h4><a href="get-started.html">Get started</a><a href="development.html">Development setup</a><a href="compatibility.html">Compatibility</a><a href="how-it-works.html">How it works</a>' +
      '<a href="' + GH + '/flutter-webos/blob/main/legacy-webos/docs/PORTING-GUIDE.md">Porting guide</a></div>' +
      '<div><h4>Code</h4><a href="' + GH + '/flutter-webos">flutter-webos</a><a href="' + GH + '/plugins">plugins</a><a href="' + GH + '/ndk">ndk</a><a href="' + GH + '">All repositories</a></div>' +
      '<div><h4>Community</h4><a href="contribute.html">Contribute</a><a href="' + GH + '/flutter-webos/issues/new/choose">Open an issue</a>' +
      '<a href="' + GH + '/.github/blob/main/SECURITY.md">Security</a><a href="' + GH + '/.github/blob/main/CODE_OF_CONDUCT.md">Code of Conduct</a></div></div>';
  }

  document.querySelectorAll('pre').forEach(function (pre) {
    var b = document.createElement('button');
    b.className = 'copy'; b.type = 'button'; b.textContent = 'Copy';
    b.addEventListener('click', function () {
      var text = pre.querySelector('code').innerText.split('\n')
        .map(function (l) { return l.replace(/\s+#.*$/, ''); }).join('\n').trim();
      navigator.clipboard.writeText(text).then(function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1400); });
    });
    pre.appendChild(b);
  });

  var toc = document.querySelectorAll('.toc a[href^="#"]');
  if (toc.length && 'IntersectionObserver' in window) {
    var map = {};
    toc.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { toc.forEach(function (a) { a.classList.remove('on'); }); var a = map[e.target.id]; if (a) a.classList.add('on'); }
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }
})();
