"""Instagram/TikTok profile kit in the collisa.be brand style: highlight covers, video cover, intro posts."""
import asyncio
import re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "render_example.py").read_text()
exec(src.split("async def main")[0])  # CSS, page(), logo(), FOOT, fonts, OUT

from playwright.async_api import async_playwright

ICONS = Path("/home/claude/fonts/lucide/icons")
PHOTO = Path("/mnt/user-data/uploads/collisa-website/public/images/lisa-collignon.jpg")


def icon(name, size, stroke="#141414", width=2):
    svg = (ICONS / f"{name}.svg").read_text()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = svg.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
    svg = svg.replace('stroke="currentColor"', f'stroke="{stroke}"').replace('stroke-width="2"', f'stroke-width="{width}"')
    return svg


EXTRA = """
.center { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }
.hl { width:660px; height:660px; border-radius:150px; background:var(--cyan); display:grid; place-items:center; }
.vc .main { align-items:flex-start; }
.steps { list-style:none; margin-top:44px; display:flex; flex-direction:column; gap:20px; }
.steps li { display:flex; gap:24px; align-items:center; font-size:34px; color:var(--body); font-weight:500; }
.steps li b { flex:none; width:58px; height:58px; border-radius:12px; background:var(--cyan); color:var(--ink);
  font-family:Fira; font-size:28px; display:grid; place-items:center; }
.steps li span small { display:block; font-size:24px; color:var(--muted); font-weight:400; }
.photo { width:360px; height:450px; border-radius:28px; object-fit:cover; object-position:62% 25%;
  border:6px solid var(--cyan); }
.row { display:flex; gap:56px; align-items:center; }
.tags { display:flex; flex-wrap:wrap; gap:14px; margin-top:40px; }
.tags span { font-family:Fira; font-size:26px; padding:10px 20px; border-radius:999px; border:2px solid var(--line); background:#fff; color:var(--teal); }
"""


def kit_page(w, h, inner):
    return page(w, h, inner).replace("</style>", EXTRA + "</style>")


# 1. Highlight covers (1080x1920, icon centred in the circle crop)
HIGHLIGHTS = {
    "cases": "briefcase",
    "care": "shield-check",
    "tips": "lightbulb",
    "over-mij": "user",
    "contact": "mail",
}
highlights = {
    name: kit_page(1080, 1920, f"<div class='page'><div class='center'><div class='hl'>{icon(ic, 360, width=1.6)}</div></div></div>")
    for name, ic in HIGHLIGHTS.items()
}

# 2. Video cover template (TikTok / Reels, 1080x1920). Text stays inside the centred 3:4 crop (y 240-1680)
#    and clear of the TikTok UI (top ~180px, bottom ~420px, right ~140px).
def video_cover(kicker, title_html, size=120):
    return kit_page(1080, 1920, f"""<div class='page vc' style='padding:300px 160px 460px 96px'>
{logo()}<div class='main'><div class='kicker'>&gt; {kicker}</div>
<h1 style='font-size:{size}px'>{title_html}</h1></div>
<div class='foot'><span></span><span class='pill'>collisa.be</span></div></div>""")

cover_example = video_cover("toegankelijkheid", "Een website<br>gebruiken<br><mark>zonder muis?</mark>")

# 3. Intro posts to pin (Instagram 1080x1350)
intro_lisa = kit_page(1080, 1350, f"""<div class='page'>{logo()}
<div class='main'><div class='row'><img class='photo' src='file://{PHOTO}' alt=''>
<div><div class='kicker' style='margin-bottom:20px'>&gt; hoi, ik ben</div>
<h1 style='font-size:96px'>Lisa.</h1>
<p style='font-size:32px;line-height:1.4;color:var(--body);margin-top:20px'>Freelance webdeveloper in Geel.</p></div></div>
<h1 style='font-size:84px;margin-top:64px'>Als het kan,<br><mark>bouw ik het.</mark></h1>
<div class='tags'><span>websites</span><span>webapps</span><span>API-koppelingen</span><span>onderhoud</span></div></div>
{FOOT.format(left='In gewone taal, zonder jargon', pill='collisa.be')}</div>""")

intro_gymna = kit_page(1080, 1350, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; case: gymna elexeo compass</div>
<h1 style='font-size:100px'>Stap voor stap<br>naar de juiste<br><mark>opstelling.</mark></h1>
<p class='sub' style='margin-top:40px'>Een begeleide keuzetool voor Gymna: kies een behandeling, bekijk de opstelling, download een PDF of vraag een offerte aan bij je dealer.</p>
<div class='tags'><span>7 talen</span><span>PDF op maat</span><span>leads naar dealers</span><span>eigen beheer</span></div></div>
{FOOT.format(left='Laravel · Filament · Livewire', pill='collisa.be')}</div>""")

intro_traject = kit_page(1080, 1350, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; samenwerken</div>
<h1 style='font-size:96px'>Zo werkt<br><mark>een traject.</mark></h1>
<ol class='steps'>
<li><b>01</b><span>Kennismaking<small>online, op een moment dat jou past</small></span></li>
<li><b>02</b><span>Offerte<small>duidelijk en 30 dagen geldig</small></span></li>
<li><b>03</b><span>Bouwen<small>met tussentijdse updates in gewone taal</small></span></li>
<li><b>04</b><span>Oplevering<small>10 werkdagen om alles na te kijken</small></span></li>
<li><b>05</b><span>3 maanden garantie<small>en daarna optioneel Collisa Care</small></span></li></ol></div>
{FOOT.format(left='Antwoord binnen 1 werkdag', pill='collisa.be')}</div>""")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])

        async def shot(html, name, w, h):
            f = ROOT / f"{name}.html"
            f.write_text(html)
            pg = await browser.new_page(viewport={"width": w, "height": h})
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT / f"{name}.png"))

        for name, html in highlights.items():
            await shot(html, f"highlight-{name}", 1080, 1920)
        await shot(cover_example, "videocover-zonder-muis", 1080, 1920)
        await shot(intro_lisa, "ig-pin-1-lisa", 1080, 1350)
        await shot(intro_gymna, "ig-pin-2-gymna", 1080, 1350)
        await shot(intro_traject, "ig-pin-3-traject", 1080, 1350)
        await browser.close()


asyncio.run(main())
