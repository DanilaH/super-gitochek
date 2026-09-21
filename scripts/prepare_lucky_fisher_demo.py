"""Stage the pinned Lucky Fisher source as a standalone static Pages preview.

Run only after checking out the SHA in game-demos-pages.yml. The original
repository is never modified; only the public preview is copied into site/.
"""

from html.parser import HTMLParser
from pathlib import Path
from shutil import copy2, copytree, rmtree
import os
import re

source = Path(os.environ["LUCKY_FISHER_SOURCE"])
target = Path("site/lucky-fisher")

required = (
    "index.html",
    "game-config.js",
    "vendor/phaser.min.js",
    "src/main.js",
    "src/screens/gameplay-screen.js",
    "assets/css/screen.css",
    "assets/ui/star.png",
    "assets/audio/calm-music.mp3",
)
for path in required:
    assert (source / path).is_file(), f"Missing upstream file: {path}"

for folder in ("assets", "src", "vendor"):
    assert not any(p.is_symlink() for p in (source / folder).rglob("*")), (
        f"Unexpected upstream symlink under {folder}"
    )

if target.exists():
    rmtree(target)
target.mkdir(parents=True)
for folder in ("assets", "src", "vendor"):
    copytree(source / folder, target / folder)
for filename in ("index.html", "game-config.js", "CREDITS.md"):
    copy2(source / filename, target / filename)

html = (target / "index.html").read_text(encoding="utf-8")
assert "</head>" in html and "<base" not in html.lower()
html = html.replace(
    "</head>",
    '  <meta name="robots" content="noindex, nofollow">\n</head>',
    1,
)
(target / "index.html").write_text(html, encoding="utf-8")


class DocumentFiles(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        path = attrs.get("src") if tag == "script" else (
            attrs.get("href") if tag == "link" else None
        )
        if path and not path.startswith(("http:", "https:", "data:", "//")):
            self.paths.append(path.split("?", 1)[0])


refs = DocumentFiles()
refs.feed(html)
config = (target / "game-config.js").read_text(encoding="utf-8")
loading = (target / "src/screens/loading-screen.js").read_text(encoding="utf-8")
refs.paths.extend(re.findall(r"['\"](assets/[^'\"]+)['\"]", config))
refs.paths.extend("assets/ui/" + name for name in re.findall(r"['\"]([\w-]+\.png)['\"]", loading.split("class LoadingScreen", 1)[0]))
missing = sorted({path for path in refs.paths if not (target / path).is_file()})
assert not missing, f"Missing static dependencies: {missing}"
assert any("src/main.js" == path for path in refs.paths), "Game entry not linked"
print(f"Prepared Lucky Fisher preview: {len(list(target.rglob('*')))} entries; {len(refs.paths)} checked references")
