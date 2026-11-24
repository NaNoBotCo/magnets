"""Wrap page.html (the artifact body) into docs/index.html with the head GitHub Pages needs."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
page = (root / "page.html").read_text()
title = re.search(r"<title>(.*?)</title>", page).group(1)
page = page.replace(f"<title>{title}</title>\n", "", 1)
url = "https://nanobotco.github.io/magnets/"
desc = "How magnets work, as carnival toys: two magnets to grab, an electron shelf to load, a crowd of atoms that lines up, a hatchet, a nail to wrap, a speaker to thump. English and Thai."
head = f"""<!doctype html>
<html lang="en" translate="no" class="notranslate">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="google" content="notranslate">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="NaNoBotCo">
<meta property="og:title" content="Fucking Magnets · แม่เหล็กแม่งเจ๋ง">
<meta property="og:description" content="Here's how they work. Whoop whoop. · มันทำงานแบบนี้ไง วู้ป วู้ป">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{url}card.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A carnival at night under a giant horseshoe magnet, with the words Fucking Magnets, here's how they work.">
<meta property="og:locale" content="en_US"><meta property="og:locale:alternate" content="th_TH">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{url}card.jpg">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
"""
i = page.index("<!--body-->")
out = head + page[:i] + "</head>\n<body>\n" + page[i + len("<!--body-->"):] + "\n</body>\n</html>\n"
docs = root / "docs"
docs.mkdir(exist_ok=True)
(docs / "index.html").write_text(out)
import datetime
(docs / "sitemap.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{url}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>
</urlset>
""")
(docs / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {url}sitemap.xml\n")
(docs / "llms.txt").write_text(f"""# Fucking Magnets · แม่เหล็กแม่งเจ๋ง

How magnets work, told with love for the Juggalo family. One page, eight toys for playing with the math, in English and Thai.

- Grab 'em: two bar magnets to drag and flip; each pole pushes or pulls as strength ÷ distance².
- The shelf: electrons loaded into five seats by Hund's rule, scandium to zinc; an iron atom has four unpaired.
- The family: a two-dimensional Ising grid with a heat slider in iron's °C; order ends at 770°C.
- The chop: a 5 cm bar cut in half 28 times, 2ⁿ pieces, a north and a south on each.
- Back up: pull between two magnets falls as 1 ÷ d⁴, drawn against 1 ÷ d².
- Wrap a nail: field = μ₀ × turns per meter × amps, about ×90 with an iron core, full near 2 tesla.
- Shake it, and the speaker: volts = turns × rate of change of flux; the same coil and magnet run backwards.
- The strong ladder: brain (10⁻¹² T) to magnetar (10¹¹ T) on a log ruler.

Sources: Feynman, Fun to Imagine, BBC, 1983; Berry & Geim, Eur. J. Phys. 18, 307 (1997); Hahn et al., Nature 570, 496 (2019); Kittel, Introduction to Solid State Physics.

Page: {url}
Repo: https://github.com/NaNoBotCo/magnets

Text CC BY 4.0, code MIT.
""")
print(docs / "index.html")
