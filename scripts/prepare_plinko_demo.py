"""Stage a pinned Plinko checkout as a minimal, ad-free Pages preview.

Run only in the Pages build after checking out the upstream commit named by
PLINKO_SHA in game-demos-pages.yml. This does not modify the upstream clone.
"""

from pathlib import Path
from shutil import copy2, copytree, ignore_patterns, rmtree
import os
import re

source = Path(os.environ["PLINKO_SOURCE"])
target = Path("site/plinko")
assert (source / "index.html").is_file()
assert (source / "JS/main.js").is_file()
assert (source / "assets/images/balls.png").is_file()

if target.exists():
    rmtree(target)
target.mkdir(parents=True)
copytree(source / "JS", target / "JS", ignore=ignore_patterns("star.js", "analytics.js", "game.js"))
copytree(source / "assets/images", target / "assets/images", ignore=ignore_patterns("*.xcf"))

html = (source / "index.html").read_text(encoding="utf-8")
assert 'src="JS/star.js"' in html
html, marker, _ = html.partition("    <!-- Ad Integration Script -->")
assert marker, "Upstream page structure changed; review before updating the mirror"
html, count = re.subn(r'(?m)^\s*<script src="JS/star\.js"[^\n]*</script>\s*$', "", html)
assert count == 1, "Expected precisely one optional ad loader"

responsive = """
    <meta name="robots" content="noindex, nofollow">
    <style>
      html, body { margin: 0; background: #101115; overflow: hidden; overscroll-behavior: none; }
      #wrapperContainer { width: 100vw; height: 100dvh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
      #wrapper canvas { display: block; width: min(100vw, 1108px, calc(100dvh * 1108 / 595)) !important; height: auto !important; touch-action: none; }
      .orientation-hint { display: none; position: fixed; top: 8px; left: 8px; right: 8px; z-index: 5; text-align: center; color: white; font: 13px/1.4 system-ui, sans-serif; pointer-events: none; text-shadow: 0 1px 4px #000; }
      @media (orientation: portrait) and (max-width: 700px) { .orientation-hint { display: block; } }
    </style>
"""
assert "</head>" in html and "<body " in html
html = html.replace("</head>", responsive + "  </head>", 1)
html = html.replace('<body style="margin: 0; padding: 0; overflow: hidden;">', '<body style="margin: 0; padding: 0; overflow: hidden;">\n    <div class="orientation-hint">Поверни телефон горизонтально: исходная игра рассчитана на широкий экран.</div>', 1)
html += """
    <!-- Local preview: grant the optional reward without loading third-party ads. -->
    <script>
      function displayRewardedVideo() {
        window.scene?.adManager?.completeAd();
      }
    </script>
  </body>
</html>
"""
(target / "index.html").write_text(html, encoding="utf-8")

bonus = target / "JS/managers/BonusManager.js"
text = bonus.read_text(encoding="utf-8")
assert "this.bottomText.setText('Watch Ad');" in text
bonus.write_text(text.replace("this.bottomText.setText('Watch Ad');", "this.bottomText.setText('Free Bonus');"), encoding="utf-8")

assert not (target / "JS/star.js").exists()
assert not (target / "JS/analytics.js").exists()
assert not (target / "assets/fonts").exists()
print("Prepared Plinko preview:", len(list(target.rglob("*"))), "entries")
