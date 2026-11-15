"""Render Collisa social visuals from HTML in the collisa.be brand style."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
FONTS = Path("/home/claude/fonts")
POP = next(FONTS.glob("fontsource-poppins-*/files"))
FIRA = next(FONTS.glob("fontsource-fira-code-*/files"))
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

CSS = f"""
@font-face {{ font-family: Poppins; font-weight: 400; src: url('file://{POP}/poppins-latin-400-normal.woff2'); }}
@font-face {{ font-family: Poppins; font-weight: 500; src: url('file://{POP}/poppins-latin-500-normal.woff2'); }}
@font-face {{ font-family: Poppins; font-weight: 600; src: url('file://{POP}/poppins-latin-600-normal.woff2'); }}
@font-face {{ font-family: Poppins; font-weight: 700; src: url('file://{POP}/poppins-latin-700-normal.woff2'); }}
@font-face {{ font-family: Poppins; font-weight: 800; src: url('file://{POP}/poppins-latin-800-normal.woff2'); }}
@font-face {{ font-family: Fira; font-weight: 400; src: url('file://{FIRA}/fira-code-latin-400-normal.woff2'); }}
@font-face {{ font-family: Fira; font-weight: 500; src: url('file://{FIRA}/fira-code-latin-500-normal.woff2'); }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ --ink:#141414; --paper:#f7f7f7; --body:#3a3a3a; --muted:#5f5f5f; --cyan:#5ce1e6; --teal:#0b6e75; --grid:#d9d9d9; --line:#e6e6e6; }}
body {{ width: var(--w); height: var(--h); font-family: Poppins; color: var(--ink); }}
.page {{ position: relative; width: var(--w); height: var(--h); padding: 96px; background: var(--paper);
  background-image: radial-gradient(var(--grid) 2px, transparent 2px); background-size: 40px 40px;
  display: flex; flex-direction: column; overflow: hidden; }}
.logo {{ display: flex; align-items: center; gap: 20px; font-weight: 700; font-size: 46px; letter-spacing: -0.02em; }}
.logo i {{ width: 40px; height: 40px; border-radius: 9px; background: var(--cyan); display: block; }}
.count {{ margin-left: auto; font-family: Fira; font-size: 28px; color: var(--muted); }}
.main {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
h1 {{ font-weight: 700; letter-spacing: -0.045em; line-height: 1.02; }}
mark {{ background: linear-gradient(transparent 52%, var(--cyan) 52%, var(--cyan) 94%, transparent 94%); color: inherit; padding: 0 6px; margin: 0 -6px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
.kicker {{ font-family: Fira; font-weight: 500; font-size: 30px; color: var(--teal); margin-bottom: 36px; letter-spacing: 0.02em; }}
.sub {{ font-size: 36px; line-height: 1.45; color: var(--body); margin-top: 48px; }}
.foot {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 40px; }}
.foot p {{ font-size: 30px; line-height: 1.45; color: var(--body); }}
.pill {{ background: var(--ink); color: #fff; font-weight: 700; font-size: 32px; padding: 22px 44px; border-radius: 999px; white-space: nowrap; }}
ul.checks {{ list-style: none; margin-top: 56px; display: flex; flex-direction: column; gap: 26px; }}
ul.checks li {{ display: flex; gap: 26px; align-items: flex-start; font-size: 38px; line-height: 1.3; color: var(--body); font-weight: 500; }}
ul.checks li b {{ flex: none; width: 46px; height: 46px; border-radius: 10px; background: var(--cyan); color: var(--ink);
  display: grid; place-items: center; font-size: 28px; margin-top: 2px; }}
.card {{ background: #fff; border: 2px solid var(--line); border-radius: 28px; padding: 44px 48px; }}
.label {{ font-family: Fira; font-weight: 500; font-size: 28px; color: var(--teal); margin-bottom: 14px; }}
.card p {{ font-size: 42px; line-height: 1.25; font-weight: 600; letter-spacing: -0.02em; }}
.card.fix {{ border-color: var(--cyan); border-width: 3px; }}
.stack {{ display: flex; flex-direction: column; gap: 32px; margin-top: 56px; }}
.swatch {{ display: flex; gap: 28px; margin-top: 28px; }}
.field {{ flex: 1; height: 92px; border-radius: 16px; background: #fff; display: flex; align-items: center; padding: 0 30px;
  font-size: 30px; color: #6b6b6b; }}
.ratio {{ font-family: Fira; font-weight: 500; font-size: 34px; align-self: center; width: 170px; text-align: right; }}
"""


def page(w, h, inner):
    return f"<html><head><style>{CSS}</style></head><body style='--w:{w}px;--h:{h}px'>{inner}</body></html>"


LOGO = "<div class='logo'><i></i>collisa{count}</div>"


def logo(count=""):
    return LOGO.format(count=f"<span class='count'>{count}</span>" if count else "")


FOOT = """<div class='foot'><p>{left}</p><span class='pill'>{pill}</span></div>"""

S = 1200  # square LinkedIn image
IGW, IGH = 1080, 1350

launch = page(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; nieuwe website</div>
<h1 style='font-size:124px'>De nieuwe<br>collisa.be<br><mark>is live.</mark></h1>
<p class='sub'>Websites, webapps en API-koppelingen op maat.<br>Communicatie in gewone taal.</p></div>
{FOOT.format(left='Lisa Collignon · Geel', pill='collisa.be')}</div>""")

care = page(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; collisa care</div>
<h1 style='font-size:104px'>De website<br>is klaar.<br><mark>En nu?</mark></h1>
<ul class='checks'>
<li><b>✓</b>Fouten opgevolgd vóór jij ze ziet</li>
<li><b>✓</b>Updates en kleine aanpassingen geregeld</li>
<li><b>✓</b>Ongebruikte uren schuiven een maand door</li>
<li><b>✓</b>Nette overdracht als je ooit stopt</li></ul></div>
{FOOT.format(left='Onderhoud zonder verrassingen', pill='collisa.be')}</div>""")

CW, CH = 1080, 1350  # carousel slides, portrait

def problem(n, probleem, oplossing, extra=""):
    return page(CW, CH, f"""<div class='page'>{logo(f'0{n+1}/05')}
<div class='main'><div class='kicker'>&gt; probleem {n}</div>
<div class='stack'>
<div class='card'><div class='label'>Wat misliep</div><p>{probleem}</p>{extra}</div>
<div class='card fix'><div class='label'>Oplossing</div><p>{oplossing}</p></div></div></div>
{FOOT.format(left='Webtoegankelijkheid · kia-ora.be', pill='collisa.be')}</div>""")

contrast_extra = """<div class='swatch'><div class='field' style='border:3px solid #cdcdcd'>Voornaam</div><div class='ratio' style='color:#b42318'>1,58:1</div></div>"""
contrast_fix = """Donkerdere rand.<div class='swatch'><div class='field' style='border:3px solid #8d8d8d'>Voornaam</div><div class='ratio' style='color:#0b6e75'>3,32:1</div></div>"""

slides = [
    page(CW, CH, f"""<div class='page'>{logo('01/05')}
<div class='main'><div class='kicker'>&gt; case: kia-ora.be</div>
<h1 style='font-size:108px'>De testtool vond <mark>0 problemen.</mark><br>Toch faalden 8 criteria.</h1>
<p class='sub'>Wat ik leerde bij het toetsen van een website aan WCAG 2.1 AA.</p></div>
{FOOT.format(left='Swipe →', pill='collisa.be')}</div>"""),
    problem(1, "Na het verzenden van een formulier sprong de focus naar de bovenkant van de pagina.",
            "De focus gaat naar de foutmelding of de bevestiging."),
    problem(2, "Elke pagina had dezelfde titel. Voor een schermlezer zijn ze dan niet te onderscheiden.",
            "Elke pagina een eigen titel."),
    problem(3, "Randen van invulvelden waren te licht.", contrast_fix, contrast_extra),
    page(CW, CH, f"""<div class='page'>{logo('05/05')}
<div class='main'><div class='kicker'>&gt; de les</div>
<h1 style='font-size:96px'>Een tool is een begin.<br><mark>Test zoals je bezoekers.</mark></h1>
<p class='sub'>Zonder muis, met een schermlezer, met vergrote tekst. Daar zitten de echte problemen.</p></div>
{FOOT.format(left='Twijfel je over jouw site?<br>Stuur me een berichtje.', pill='collisa.be')}</div>"""),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        async def shot(html, name, w, h):
            f = ROOT / f"{name}.html"
            f.write_text(html)
            pg = await browser.new_page(viewport={"width": w, "height": h})
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.screenshot(path=str(OUT / f"{name}.png"))
            return pg
        await shot(launch, "ig-lancering", IGW, IGH)
        await shot(care, "ig-care", IGW, IGH)
        for i, s in enumerate(slides, 1):
            await shot(s, f"carousel-{i}", CW, CH)
        # PDF of the carousel: one slide per page
        pages_html = "".join(f"<iframe src='carousel-{i}.html' style='width:{CW}px;height:{CH}px;border:0;display:block;page-break-after:always'></iframe>" for i in range(1, 6))
        await browser.close()


asyncio.run(main())
