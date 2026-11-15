"""Instagram start stories (1080x1920) in the collisa.be brand style.
Safe zone: Instagram UI covers roughly the top 250px and bottom 340px, so content sits between."""
import asyncio
from pathlib import Path

ROOT = Path(__file__).parent
exec((ROOT / "profile_kit.py").read_text().split("# 1. Highlight covers")[0])  # CSS, page(), icon(), kit_page(), FOOT

from playwright.async_api import async_playwright

STORY_CSS = """
.story { padding: 260px 96px 660px; }
.slot { position:absolute; left:96px; right:96px; top:1330px; text-align:center; font-family:Fira; font-weight:500; font-size:30px; color:var(--teal); }
.slot i { display:block; font-style:normal; font-size:44px; margin-top:4px; }
.sticker { margin-top: 56px; height: 120px; border: 4px dashed var(--line-strong, #d0d0d0); border-radius: 24px;
  display:flex; align-items:center; justify-content:center; font-family:Fira; font-size:26px; color:#8a8a8a; }
.cases { list-style:none; margin-top:36px; display:flex; flex-direction:column; gap:14px; }
.cases li { background:#fff; border:2px solid var(--line); border-radius:22px; padding:20px 30px; }
.cases li strong { display:block; font-size:34px; letter-spacing:-0.02em; }
.cases li span { font-size:25px; color:var(--body); }
.keys { display:flex; gap:18px; margin-top:44px; }
.keys kbd { font-family:Fira; font-weight:500; font-size:34px; background:#fff; border:3px solid var(--ink); border-bottom-width:8px;
  border-radius:16px; padding:14px 26px; }
"""


SLOT = "<div class='slot'>meer op collisa.be<i>↓</i></div>"


def story(inner, slot=True):
    return kit_page(1080, 1920, f"<div class='page story'>{inner}{SLOT if slot else ''}</div>").replace("</style>", STORY_CSS + "</style>")


STICKER = ""

stories = {
    "story-over-mij": story(f"""{logo()}<div class='main'>
<img class='photo' style='width:340px;height:420px' src='file://{PHOTO}' alt=''>
<div class='kicker' style='margin-top:56px;margin-bottom:16px'>&gt; over mij</div>
<h1 style='font-size:112px'>Hoi, ik ben <mark>Lisa.</mark></h1>
<p class='sub' style='margin-top:32px'>Freelance webdeveloper in Geel. Ik bouw websites, webapps en koppelingen, en leg alles uit in gewone taal.</p></div>"""),
    "story-cases": story(f"""{logo()}<div class='main'><div class='kicker'>&gt; cases</div>
<h1 style='font-size:96px'>Wat ik <mark>bouwde.</mark></h1>
<ul class='cases'>
<li><strong>Gymna Elexeo Compass</strong><span>begeleide keuzetool in 7 talen</span></li>
<li><strong>kia-ora.be</strong><span>toegankelijke site, getoetst aan WCAG 2.1 AA</span></li>
<li><strong>BatSync</strong><span>WooCommerce gekoppeld aan CycleSoftware</span></li>
<li><strong>MediFootz TextMeet</strong><span>agenda met automatische herinneringen</span></li></ul></div>"""),
    "story-care": story(f"""{logo()}<div class='main'><div class='kicker'>&gt; collisa care</div>
<h1 style='font-size:110px'>De website<br>is klaar.<br><mark>En nu?</mark></h1>
<ul class='checks'>
<li><b>✓</b>Fouten opgevolgd vóór jij ze ziet</li>
<li><b>✓</b>Updates en kleine aanpassingen geregeld</li>
<li><b>✓</b>Ongebruikte uren schuiven een maand door</li>
<li><b>✓</b>Nette overdracht als je ooit stopt</li></ul></div>"""),
    "story-tips": story(f"""{logo()}<div class='main'><div class='kicker'>&gt; tip</div>
<h1 style='font-size:104px'>Test je site<br>eens <mark>zonder muis.</mark></h1>
<div class='keys'><kbd>Tab</kbd><kbd>Shift + Tab</kbd><kbd>Enter</kbd></div>
<p class='sub' style='margin-top:44px'>Zie je altijd waar je bent? Kun je elk menu en formulier gebruiken? Zo niet, dan lopen ook bezoekers met een toetsenbord of schermlezer vast.</p></div>"""),
    "story-contact": story(f"""{logo()}<div class='main'><div class='kicker'>&gt; contact</div>
<h1 style='font-size:110px'>Een website<br>of webapp<br><mark>in gedachten?</mark></h1>
<p class='sub' style='margin-top:40px'>Stuur me een bericht. Je krijgt antwoord binnen 1 werkdag, in gewone taal.</p>
</div>"""),
}


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for name, html in stories.items():
            f = ROOT / f"{name}.html"
            f.write_text(html)
            pg = await browser.new_page(viewport={"width": 1080, "height": 1920})
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(OUT / f"{name}-v2.png"))
        await browser.close()


asyncio.run(main())
