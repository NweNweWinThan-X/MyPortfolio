#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render version1 of the CV to print-ready A4 HTML.

Navy header band with portrait, grey sidebar with rated skills.
SIDEBAR_PAGE2 lists the sidebar sections that must start on page two.
Render with: Chrome --headless --print-to-pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_data as D  # noqa: E402

# Sidebar sections pushed to page 2. Empty list == single continuous sidebar.
SIDEBAR_PAGE2 = ('Learning', 'Certifications')

# Index into EXPERIENCE of the entry that opens page 2, so the main column
# starts level with the sidebar. None == let it break wherever it lands.
MAIN_PAGE2_FROM = 2


def icon(path, color="#ffffff", size=11):
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" '
            f'stroke-linejoin="round">{path}</svg>')


P_PHONE = '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
P_MAIL = '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><polyline points="22,6 12,13 2,6"/>'
P_PIN = '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
P_LINK = '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>'
P_GIT = '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9a3.4 3.4 0 0 0-1-2.6c3.3-.4 6.8-1.6 6.8-7.3A5.7 5.7 0 0 0 20.3 4a5.3 5.3 0 0 0-.1-4S18.9-.4 16 1.5a13.4 13.4 0 0 0-7 0C6.1-.4 4.8 0 4.8 0a5.3 5.3 0 0 0-.1 4A5.7 5.7 0 0 0 3.2 8.2c0 5.7 3.5 6.9 6.8 7.3a3.4 3.4 0 0 0-1 2.6V22"/>'
P_CAL = '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>'
P_SHIELD = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'


def dots(n, total=5, cls="d"):
    return ''.join(f'<span class="{cls} {"on" if i < n else "off"}"></span>'
                   for i in range(total))


def ul(items):
    return '<ul>' + ''.join(f'<li>{b}</li>' for b in items) + '</ul>'


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
       font-size: 7.95pt; line-height: 1.24; color: #22262b; }
.band { background: #14365c; color: #fff; padding: 10mm 11mm 7mm;
        display: flex; align-items: center; gap: 9mm; }
.band .txt { flex: 1; }
.band img { width: 28mm; height: 28mm; border-radius: 50%; object-fit: cover;
            flex: 0 0 28mm; border: 1mm solid rgba(255,255,255,.92); }
.band h1 { font-size: 26pt; font-weight: 800; letter-spacing: .4px; line-height: 1; }
.band .role { font-size: 12pt; font-weight: 400; margin-top: 2.6mm; color: #cfe0f2; }
.wrap { display: flex; align-items: stretch; min-height: 244mm; }
.main { width: 68%; padding: 6mm 6mm 8mm 11mm; }
.side { width: 32%; background: #eef1f4; padding: 7mm 8mm 8mm 6mm; }
/* The sidebar is one grey column per page. Sections after the split sit in
   .side-2, which the page-2 band positions below the page boundary. */
h2 { font-size: 10.2pt; color: #14365c; font-weight: 700; margin: 3.8mm 0 1.6mm;
     padding-bottom: 1mm; border-bottom: .9pt solid #c3ccd6; }
h2:first-child { margin-top: 0; }
.side h2 { font-size: 10.5pt; }
.row { display: flex; gap: 4mm; margin-bottom: 2.6mm; page-break-inside: avoid; }
.when { width: 15mm; flex: 0 0 15mm; font-weight: 700; color: #3c4854; font-size: 8pt;
        padding-top: .4mm; }
.what { flex: 1; }
.what h3 { font-size: 9.4pt; font-weight: 700; color: #1d2630; }
.org { font-style: italic; color: #4e5a66; font-size: 8.6pt; margin-bottom: .6mm; }
.proj { font-size: 7.9pt; color: #14365c; font-weight: 600; margin-bottom: 1mm; }
ul { list-style: none; }
li { position: relative; padding-left: 3.4mm; margin-bottom: .7mm; text-align: justify; }
li::before { content: "•"; position: absolute; left: 0; color: #14365c; font-weight: 700; }
.tech { font-size: 7.6pt; color: #6a7580; font-style: italic; margin-top: 1mm; }
.sum { text-align: justify; margin-bottom: 1mm; }
.ks { margin-bottom: 1.1mm; page-break-inside: avoid; }
.ks b { color: #14365c; }
.pi { margin-bottom: 2.6mm; }
.pi .lbl { font-weight: 700; color: #1d2630; font-size: 8.4pt; display: flex;
           align-items: center; gap: 1.6mm; }
.pi .val { color: #4e5a66; font-size: 8pt; word-break: break-word; }
.sk { margin-bottom: 2.3mm; }
.sk .nm { font-size: 8.2pt; margin-bottom: 1mm; }
.d { display: inline-block; width: 2.5mm; height: 2.5mm; border-radius: 50%; margin-left: 1mm; }
.d.on { background: #14365c; } .d.off { background: #c3ccd6; }
.rate { text-align: right; }
.lg { margin-bottom: 2.2mm; }
.lg .nm { font-weight: 700; font-size: 8.3pt; color: #1d2630; }
.lg .lv { font-size: 7.7pt; color: #5a6672; }
.ct { margin-bottom: 0; }
.ct .nm { font-size: 8.2pt; color: #1d2630; }
.ct .dt { font-size: 7.6pt; color: #6a7580; }
/* newest first; the arrow points up the date order */
.up { color: #14365c; font-size: 8.5pt; line-height: 1; margin: .8mm 0 .8mm .6mm; }
.ic { vertical-align: middle; }
.pr { font-size: 7.9pt; }
.pr b { color: #14365c; }
.chip { display: inline-block; background: #dde4ec; color: #22405f; font-size: 7.4pt;
        padding: .5mm 1.6mm; border-radius: 1mm; margin: 0 1mm 1mm 0; }
/* Forces the following sidebar block onto the next sheet. */
.pagebreak { break-before: page; page-break-before: always; height: 0; }
/* Page 2 top spacing lives inside the columns, not in the @page margin, so
   the sidebar's grey background reaches the paper edge. Both columns use the
   same 9mm so their first lines stay level. */
.pagebreak + h2 { margin-top: 9mm; }
.row.page2 { break-before: page; page-break-before: always; margin-top: 9mm; }
"""


def sidebar_sections():
    """(title, html) for each sidebar section, in order."""
    info = [("Phone", P_PHONE, D.CONTACT["phone"]),
            ("E-mail", P_MAIL, D.CONTACT["email"]),
            ("Location", P_PIN, D.CONTACT["location"]),
            ("Work status", P_SHIELD, D.CONTACT["visa"]),
            ("LinkedIn", P_LINK, D.CONTACT["linkedin"]),
            ("GitHub", P_GIT, D.CONTACT["github"]),
            ("Portfolio", P_LINK, D.CONTACT["portfolio"])]
    pi = ''.join(f'<div class="pi"><div class="lbl">{icon(p, "#14365c", 10)}{l}</div>'
                 f'<div class="val">{v}</div></div>' for l, p, v in info)
    sk = ''.join(f'<div class="sk"><div class="nm">{n}</div>'
                 f'<div class="rate">{dots(r)}</div></div>' for n, r in D.SKILL_RATINGS)
    lg = ''.join(f'<div class="lg"><div class="nm">{n}</div><div class="lv">{l}</div></div>'
                 for n, l, _ in D.LANGUAGES)
    ct = '<div class="up">&#8593;</div>'.join(
        f'<div class="ct"><div class="nm">{n}</div><div class="dt">{d}</div></div>'
        for n, d in D.CERTIFICATIONS)
    chips = ''.join(f'<span class="chip">{t}</span>' for t in D.LEARNING)
    return [
        ("Personal Info", pi),
        ("Skills", sk),
        ("Languages", lg),
        ("Learning", f'<div>{chips}</div>'),
        ("Certifications", ct),
    ]


def build(out):
    exp = ''
    for n, j in enumerate(D.EXPERIENCE):
        cls = 'row page2' if n == MAIN_PAGE2_FROM else 'row'
        exp += f'''<div class="{cls}"><div class="when">{j["from"]} -<br>{j["to"]}</div>
<div class="what"><h3>{j["role"]}</h3>
<div class="org">{j["company"]} — {j["location"]}</div>
<div class="proj">{j["projects"]}</div>
{ul(j["bullets"])}
<div class="tech">{j["stack"]}</div></div></div>'''

    ed = D.EDUCATION
    edu = f'''<div class="row"><div class="when">{ed["from"]} -<br>{ed["to"]}</div>
<div class="what"><h3>{ed["school"]}</h3>
<div class="org">{ed["degree"]} — {ed["location"]}</div></div></div>'''

    pr = D.PROJECT
    proj = (f'<div class="pr"><b>{pr["name"]}</b> · {pr["url"]}<br>{pr["blurb"]}'
            + ul(pr["points"]) + '</div>')

    strengths = ''.join(f'<div class="ks"><b>{t}</b> — {d}</div>'
                        for t, d in D.STRENGTHS)

    page1, page2 = [], []
    for title, html in sidebar_sections():
        (page2 if title in SIDEBAR_PAGE2 else page1).append(f'<h2>{title}</h2>{html}')
    side = ''.join(page1)
    if page2:
        side += '<div class="pagebreak"></div>' + ''.join(page2)

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{D.NAME} — Resume</title><style>{CSS}</style></head><body>
<div class="band"><div class="txt"><h1>{D.NAME.title()}</h1>
<div class="role">{D.TITLE} — {D.SUBTITLE}</div></div>
<img src="{D.PHOTO}" alt="{D.NAME.title()}"></div>
<div class="wrap">
 <div class="main">
  <p class="sum">{D.SUMMARY}</p>
  <h2>Key Strengths</h2>{strengths}
  <h2>Experience</h2>{exp}
  <h2>Selected Project</h2>{proj}
  <h2>Education</h2>{edu}
 </div>
 <div class="side">{side}</div>
</div></body></html>'''
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out)


if __name__ == '__main__':
    build(sys.argv[1])
