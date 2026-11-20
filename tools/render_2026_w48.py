"""Week 48 (2026): C1 BatSync, W3 Sentry in elk project, A3 AI sorteert aanvragen voor.
Run next to render_example.py, profile_kit.py and stories_example.py (they are loaded via exec)."""
import asyncio
from pathlib import Path

ROOT = Path(__file__).parent
# CSS, page(), logo(), FOOT, OUT, kit_page(), icon(), video_cover()
exec((ROOT / "profile_kit.py").read_text().split("\nasync def main")[0])
# STORY_CSS, SLOT, story()
exec((ROOT / "stories_example.py").read_text().split("stories = {")[0])

from playwright.async_api import async_playwright

W48 = """
.flow { display:flex; align-items:center; gap:22px; margin-top:60px; }
.sys { flex:1; background:#fff; border:2px solid var(--line); border-radius:26px; padding:34px 30px; text-align:center; }
.sys small { display:block; font-family:Fira; font-weight:500; font-size:24px; color:var(--teal); margin-bottom:10px; }
.sys strong { font-size:40px; letter-spacing:-0.03em; font-weight:700; }
.link { flex:none; display:flex; flex-direction:column; align-items:center; gap:10px; }
.link b { width:96px; height:96px; border-radius:20px; background:var(--cyan); display:grid; place-items:center; font-size:46px; }
.link span { font-family:Fira; font-weight:500; font-size:24px; color:var(--teal); }
.steps { display:flex; flex-direction:column; gap:22px; margin-top:52px; }
.step { display:flex; align-items:center; gap:28px; background:#fff; border:2px solid var(--line); border-radius:24px; padding:26px 34px; }
.step.last { border-color:var(--cyan); border-width:3px; }
.step b { flex:none; width:58px; height:58px; border-radius:12px; background:var(--cyan); display:grid; place-items:center; font-size:30px; font-weight:700; }
.step span { font-size:36px; font-weight:600; letter-spacing:-0.02em; line-height:1.2; }
.step small { display:block; font-family:Fira; font-size:24px; color:var(--teal); font-weight:500; letter-spacing:0; margin-bottom:4px; }
.note { margin-top:36px; display:flex; gap:22px; align-items:flex-start; font-size:30px; line-height:1.35; color:var(--body); }
.note svg { flex:none; margin-top:2px; }
"""


def p48(w, h, inner):
    return kit_page(w, h, inner).replace("</style>", W48 + "</style>")


def s48(inner):
    return story(inner).replace("</style>", W48 + "</style>")


S = 1200
IGW, IGH = 1080, 1350

# ---------- C1 BatSync ----------
def flow(left="WooCommerce", right="CycleSoftware"):
    return f"""<div class='flow'>
<div class='sys'><small>webshop</small><strong>{left}</strong></div>
<div class='link'><b>⇄</b><span>BatSync</span></div>
<div class='sys'><small>winkelsoftware</small><strong>{right}</strong></div></div>"""

li_batsync = p48(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; case: batsync</div>
<h1 style='font-size:100px'>Webshop en<br>winkelsoftware<br><mark>praten met elkaar.</mark></h1>
{flow()}</div>
{FOOT.format(left='Voor Webbureau Batman en<br>hun fietswinkelklanten', pill='collisa.be')}</div>""")

ig_batsync = p48(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; case: batsync</div>
<h1 style='font-size:96px'>Webshop en<br>winkelsoftware<br><mark>praten met<br>elkaar.</mark></h1>
{flow()}</div>
{FOOT.format(left='Voor Webbureau Batman<br>en hun fietswinkels', pill='collisa.be')}</div>""")

story_batsync = s48(f"""{logo()}<div class='main'><div class='kicker'>&gt; case: batsync</div>
<h1 style='font-size:100px'>Webshop en<br>winkelsoftware<br><mark>praten samen.</mark></h1>
{flow()}
<p class='sub' style='margin-top:44px'>Een koppeling voor fietswinkels, gebouwd voor Webbureau Batman.</p></div>""")

# ---------- W3 Sentry ----------
def sentry_steps(s3="Ik los het op, vaak voor jij het merkt"):
    return f"""<div class='steps'>
<div class='step'><b>1</b><span><small>er loopt iets mis</small>Een pagina of formulier geeft een fout</span></div>
<div class='step'><b>2</b><span><small>automatisch</small>Ik krijg een melding met de details</span></div>
<div class='step last'><b>3</b><span><small>opgelost</small>{s3}</span></div></div>"""

li_sentry = p48(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; foutopvolging in elk project</div>
<h1 style='font-size:96px'>Een fout op je site?<br><mark>Ik krijg een seintje.</mark></h1>
{sentry_steps()}</div>
{FOOT.format(left='In elk project en elk Care-pakket', pill='collisa.be')}</div>""")

ig_sentry = p48(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; foutopvolging</div>
<h1 style='font-size:84px'>Een fout op je site?<br><mark>Ik krijg een seintje.</mark></h1>
{sentry_steps('Ik los het op, vaak<br>voor jij het merkt')}</div>
{FOOT.format(left='In elk project en<br>elk Care-pakket', pill='collisa.be')}</div>""")

story_sentry = s48(f"""{logo()}<div class='main'><div class='kicker'>&gt; foutopvolging</div>
<h1 style='font-size:104px'>Een fout op<br>je site?<br><mark>Ik krijg een<br>seintje.</mark></h1>
<p class='sub' style='margin-top:44px'>Automatische foutopvolging zit in elk project en elk Care-pakket.</p></div>""")

# ---------- A3 AI sorteert aanvragen voor ----------
ai_checks = """<ul class='checks'>
<li><b>✓</b>Een lange mail samenvatten</li>
<li><b>✓</b>Een label geven: offerte, vraag, klacht</li>
<li><b>✓</b>Een conceptantwoord klaarzetten</li></ul>"""
ai_note = f"""<div class='note'>{icon('shield-alert', 40, stroke='#0b6e75')}<span>Let op privacy en blijf zelf nalezen: AI maakt fouten.</span></div>"""

li_ai = p48(S, S, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; ai voor kmo's</div>
<h1 style='font-size:112px'>AI sorteert voor.<br><mark>Jij beslist.</mark></h1>
{ai_checks}{ai_note}</div>
{FOOT.format(left='Minder tijd in je inbox,<br>zonder de controle te verliezen', pill='collisa.be')}</div>""")

ig_ai = p48(IGW, IGH, f"""<div class='page'>{logo()}
<div class='main'><div class='kicker'>&gt; ai voor kmo's</div>
<h1 style='font-size:100px'>AI sorteert voor.<br><mark>Jij beslist.</mark></h1>
{ai_checks}{ai_note}</div>
{FOOT.format(left='Minder tijd in je inbox', pill='collisa.be')}</div>""")

story_ai = s48(f"""{logo()}<div class='main'><div class='kicker'>&gt; tip: ai voor kmo's</div>
<h1 style='font-size:104px'>AI sorteert<br>je mails voor.<br><mark>Jij beslist.</mark></h1>
<p class='sub' style='margin-top:44px'>Samenvatten, labelen, een concept klaarzetten. Jij leest na en verstuurt.</p></div>""")

# ---------- TikTok cover (W3) ----------
cover_sentry = video_cover("foutopvolging", "Je website<br>geeft een fout.<br><mark>Wie merkt het?</mark>", size=112)

JOBS = [
    (li_batsync, "linkedin-batsync", S, S), (ig_batsync, "ig-batsync", IGW, IGH), (story_batsync, "story-batsync", 1080, 1920),
    (li_sentry, "linkedin-sentry", S, S), (ig_sentry, "ig-sentry", IGW, IGH), (story_sentry, "story-sentry", 1080, 1920),
    (li_ai, "linkedin-ai-mails", S, S), (ig_ai, "ig-ai-mails", IGW, IGH), (story_ai, "story-ai-mails", 1080, 1920),
    (cover_sentry, "tiktok-cover-sentry", 1080, 1920),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        for html, name, w, h in JOBS:
            f = OUT / f"{name}.html"
            f.write_text(html)
            pg = await browser.new_page(viewport={"width": w, "height": h})
            await pg.goto(f.as_uri())
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(300)
            if name.startswith("story"):
                # content must end above y=1260 and nothing may enter the slot/sticker zone
                bottom = await pg.evaluate("Math.max(...[...document.querySelectorAll('.main *')].map(e => e.getBoundingClientRect().bottom))")
                print(name, "content bottom", round(bottom))
            over = await pg.evaluate("[...document.querySelectorAll('.page *')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible').length")
            await pg.screenshot(path=str(OUT / f"{name}.png"))
            await pg.close()
        await browser.close()


asyncio.run(main())
