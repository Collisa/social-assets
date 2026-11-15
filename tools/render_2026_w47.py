"""Week 47 (2026): Gymna Elexeo Compass, duidelijke afspraken, AI in mijn workflow."""
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

EXTRA = """
.steps { display: flex; flex-direction: column; gap: 22px; margin-top: 52px; }
.step { display: flex; align-items: center; gap: 28px; background: #fff; border: 2px solid var(--line); border-radius: 24px; padding: 26px 34px; }
.step.last { border-color: var(--cyan); border-width: 3px; }
.step b { flex: none; width: 58px; height: 58px; border-radius: 12px; background: var(--cyan); display: grid; place-items: center; font-size: 30px; font-weight: 700; }
.step span { font-size: 36px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.2; }
.step small { display: block; font-family: Fira; font-size: 24px; color: var(--teal); font-weight: 500; letter-spacing: 0; margin-bottom: 4px; }
.nums { display: flex; gap: 26px; margin-top: 56px; }
.num { flex: 1; background: #fff; border: 2px solid var(--line); border-radius: 26px; padding: 34px 30px; }
.num strong { display: block; font-size: 112px; font-weight: 700; letter-spacing: -0.05em; line-height: 1; }
.num strong em { font-style: normal; background: linear-gradient(transparent 55%, var(--cyan) 55%, var(--cyan) 92%, transparent 92%); padding: 0 6px; margin: 0 -6px; }
.num p { font-size: 29px; line-height: 1.3; color: var(--body); margin-top: 18px; font-weight: 500; }
.big { font-size: 300px; font-weight: 700; letter-spacing: -0.06em; line-height: 0.9; }
.big em { font-style: normal; background: linear-gradient(transparent 52%, var(--cyan) 52%, var(--cyan) 80%, transparent 80%); padding: 0 12px; margin: 0 -12px; }
.unit { font-size: 64px; font-weight: 700; letter-spacing: -0.04em; margin-top: 44px; line-height: 1.1; }
"""
CSS2 = CSS + EXTRA


def page(w, h, inner):
    return f"<html><head><style>{CSS2}</style></head><body style='--w:{w}px;--h:{h}px'>{inner}</body></html>"


FOOT = """<div class='foot'><p>{left}</p><span class='pill'>{pill}</span></div>"""
S = 1200
IGW, IGH = 1080, 1350

# ---------- C6 Gymna Elexeo Compass ----------
def gymna_steps(last='Download een PDF of vraag een offerte aan'):
    return f"""<div class='steps'>
<div class='step'><b>1</b><span><small>stap 1</small>Kies een behandelgroep</span></div>
<div class='step'><b>2</b><span><small>stap 2</small>Kies een indicatiegroep</span></div>
<div class='step last'><b>3</b><span><small>klaar</small>{last}</span></div></div>"""

li_gymna = page(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; case: gymna elexeo compass</div>
<h1 style='font-size:92px'>Stap voor stap naar<br><mark>de juiste opstelling.</mark></h1>
{gymna_steps()}</div>
{FOOT.format(left='7 talen · Gymna beheert alles zelf', pill='collisa.be')}</div>""")

ig_gymna = page(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; case: gymna elexeo compass</div>
<h1 style='font-size:92px'>Stap voor stap<br>naar de juiste<br><mark>opstelling.</mark></h1>
{gymna_steps('PDF downloaden of<br>offerte aanvragen')}</div>
{FOOT.format(left='7 talen · Gymna beheert<br>alles zelf', pill='collisa.be')}</div>""")

# ---------- W6 Duidelijke afspraken ----------
li_afspraken = page(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; duidelijke afspraken</div>
<h1 style='font-size:96px'>Drie getallen die<br><mark>vooraf vastliggen.</mark></h1>
<div class='nums'>
<div class='num'><strong><em>30</em></strong><p>dagen blijft een offerte geldig</p></div>
<div class='num'><strong><em>10</em></strong><p>werkdagen om de oplevering na te kijken</p></div>
<div class='num'><strong><em>3</em></strong><p>maanden garantie na de oplevering</p></div></div></div>
{FOOT.format(left='Geen verrassingen achteraf', pill='collisa.be')}</div>""")

def num_slide(n, big, unit, sub):
    return page(IGW, IGH, f"""<div class='page'>{logo(f'0{n}/04')}
<div class='main'><div class='kicker'>&gt; afspraak {n-1}</div>
<div class='big'><em>{big}</em></div>
<div class='unit'>{unit}</div>
<p class='sub'>{sub}</p></div>
{FOOT.format(left='Duidelijke afspraken', pill='collisa.be')}</div>""")

ig_afspraken = [
    page(IGW, IGH, f"""<div class='page'>{logo('01/04')}
<div class='main'><div class='kicker'>&gt; duidelijke afspraken</div>
<h1 style='font-size:120px'>30, 10<br>en 3.</h1>
<p class='sub'>Drie getallen die bij mij <b style='font-weight:600;color:var(--ink)'>vooraf vastliggen</b>, nog voor er een regel code geschreven is.</p></div>
{FOOT.format(left='Swipe →', pill='collisa.be')}</div>"""),
    num_slide(2, "30", "dagen geldig", "Zo lang blijft een offerte geldig. Je hebt tijd om rustig na te denken of intern te overleggen."),
    num_slide(3, "10", "werkdagen", "Zoveel tijd krijg je om een oplevering na te kijken. Test alles op je eigen toestellen."),
    num_slide(4, "3", "maanden garantie", "Zo lang loopt de garantie na de oplevering."),
]

# ---------- A1 AI in mijn workflow ----------
ai_checks = """<ul class='checks'>
<li><b>✓</b>Vaste stappen: plannen, bouwen, testen</li>
<li><b>✓</b>Testdocumentatie in het Nederlands voor de overdracht</li>
<li><b>✓</b>AI maakt fouten, dus ik kijk alles na</li></ul>"""

li_ai = page(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; ai in mijn workflow</div>
<h1 style='font-size:120px'>AI bouwt mee.<br><mark>Ik beslis.</mark></h1>
{ai_checks}</div>
{FOOT.format(left='Sneller en consequenter,<br>zonder de controle te verliezen', pill='collisa.be')}</div>""")

ig_ai = page(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; ai in mijn workflow</div>
<h1 style='font-size:108px'>AI bouwt mee.<br><mark>Ik beslis.</mark></h1>
{ai_checks}</div>
{FOOT.format(left='Sneller en consequenter', pill='collisa.be')}</div>""")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        async def shot(html, name, w, h):
            f = OUT / f"{name}.html"
            f.write_text(html)
            pg = await browser.new_page(viewport={"width": w, "height": h})
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png"))
            await pg.close()
        await shot(li_gymna, "linkedin-gymna-compass", S, S)
        await shot(ig_gymna, "ig-gymna-compass", IGW, IGH)
        await shot(li_afspraken, "linkedin-duidelijke-afspraken", S, S)
        for i, s in enumerate(ig_afspraken, 1):
            await shot(s, f"ig-duidelijke-afspraken-{i}", IGW, IGH)
        await shot(li_ai, "linkedin-ai-workflow", S, S)
        await shot(ig_ai, "ig-ai-workflow", IGW, IGH)
        await browser.close()


asyncio.run(main())
