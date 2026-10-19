#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render version2 of the CV to print-ready A4 HTML.

Blue accents, portrait top-right, two columns with tagged skills.
Render with: Chrome --headless --print-to-pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_data as D  # noqa: E402
from build_v1 import (P_CAL, P_GIT, P_MAIL, P_PHONE, P_PIN, P_LINK, P_SHIELD,
                      dots, icon, ul)  # noqa: E402

CSS = """
@page { size: A4; margin: 9mm 10mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
       font-size: 8.3pt; line-height: 1.36; color: #1f2328; }
h1 { font-size: 23pt; font-weight: 800; letter-spacing: .3px; line-height: 1; }
.role { font-size: 11pt; font-weight: 700; color: #1a86f0; margin-top: 1.5mm; }
.meta { display: flex; flex-wrap: wrap; gap: 1.5mm 6mm; margin-top: 2.5mm;
        font-size: 8pt; font-weight: 600; }
.meta span { display: inline-flex; align-items: center; gap: 1.4mm; }
.hdr { border-bottom: 1.6pt solid #1f2328; padding-bottom: 3mm; margin-bottom: 3.5mm;
       display: flex; align-items: center; gap: 7mm; }
.hdr .txt { flex: 1; }
.hdr img { width: 25mm; height: 25mm; border-radius: 50%; object-fit: cover;
           flex: 0 0 25mm; border: .7mm solid #dfe5ec; }
.cols { display: flex; gap: 6mm; align-items: flex-start; }
.l { width: 60%; } .r { width: 40%; }
h2 { font-size: 11pt; font-weight: 800; letter-spacing: .4px; text-transform: uppercase;
     border-bottom: 1.4pt solid #1f2328; padding-bottom: .8mm; margin: 4.5mm 0 2.2mm; }
h2:first-child { margin-top: 0; }
h3 { font-size: 10pt; font-weight: 600; }
.co { color: #1a86f0; font-weight: 700; font-size: 8.8pt; margin-top: .3mm; }
.dl { display: flex; gap: 5mm; font-size: 7.8pt; color: #5a6672; margin: .8mm 0 1.2mm; }
.dl span { display: inline-flex; align-items: center; gap: 1.2mm; }
ul { list-style: none; }
li { position: relative; padding-left: 3.2mm; margin-bottom: 1.1mm; }
li::before { content: "•"; position: absolute; left: .5mm; color: #1f2328; }
.job { margin-bottom: 3mm; page-break-inside: avoid; border-bottom: .5pt dashed #cfd5dc;
       padding-bottom: 2.2mm; }
.job:last-child { border-bottom: 0; }
.tech { font-size: 7.5pt; color: #6a7580; font-style: italic; margin-top: 1mm; }
.blk { margin-bottom: 2.6mm; page-break-inside: avoid; }
.blk .t { font-weight: 700; font-size: 8.6pt; }
.blk .s { color: #4e5a66; }
.blk .u { color: #1a86f0; font-size: 7.6pt; }
.tag { display: inline-block; font-weight: 700; font-size: 7.9pt; padding: .4mm 1.8mm .9mm;
       border-bottom: 1.1pt solid #9fb6cc; margin: 0 1.4mm 1.6mm 0; }
.ach { display: flex; gap: 2mm; margin-bottom: 2.4mm; page-break-inside: avoid; }
.ach .bq { flex: 0 0 4.6mm; }
.ach .t { font-weight: 700; font-size: 8.5pt; }
.ach .d { color: #4e5a66; }
.lrow { display: flex; justify-content: space-between; align-items: baseline;
        margin-bottom: .4mm; }
.lrow .n { font-weight: 700; font-size: 8.4pt; }
.d2 { display: inline-block; width: 2.2mm; height: 2.2mm; border-radius: 50%; margin-left: .8mm; }
.d2.on { background: #1a86f0; } .d2.off { background: #ccd4dc; }
.lv { font-size: 7.6pt; color: #5a6672; margin-bottom: 2mm; }
.sum { text-align: justify; }
.stat { display: flex; gap: 4mm; margin: 1.2mm 0; }
.stat b { font-size: 11pt; color: #1a86f0; }
.stat i { font-style: normal; font-size: 7.3pt; color: #6a7580; display: block; }
/* newest first; the arrow points up the date order */
.up { color: #1a86f0; font-size: 8.5pt; line-height: 1; margin: .6mm 0 .6mm .4mm; }
.blk.cert { margin-bottom: 0; }
"""


def build(out):
    C = D.CONTACT
    meta = ''.join(f'<span>{icon(p, "#1a86f0", 10)}{v}</span>' for p, v in [
        (P_PHONE, C["phone"]), (P_MAIL, C["email"]), (P_PIN, C["location"]),
        (P_LINK, C["linkedin"]), (P_GIT, C["github"]), (P_SHIELD, C["visa"])])

    jobs = ''
    for j in D.EXPERIENCE:
        jobs += f'''<div class="job"><h3>{j["role"]}</h3><div class="co">{j["company"]}</div>
<div class="dl"><span>{icon(P_CAL, "#5a6672", 9)}{j["dates"]}</span>
<span>{icon(P_PIN, "#5a6672", 9)}{j["location"]}</span></div>
{ul(j["bullets"])}<div class="tech">{j["stack"]}</div></div>'''

    ed = D.EDUCATION
    edu = f'''<div class="blk"><h3>{ed["degree"]}</h3><div class="co">{ed["school"]}</div>
<div class="dl"><span>{icon(P_CAL, "#5a6672", 9)}{ed["dates"]}</span>
<span>{icon(P_PIN, "#5a6672", 9)}{ed["location"]}</span></div></div>'''

    pr = D.PROJECT
    stats = ''.join(f'<div><b>{v}</b><i>{l}</i></div>' for v, l in pr["stats"])
    proj = (f'<div class="blk"><div class="t">{pr["name"]}</div>'
            f'<div class="s">{pr["blurb"]}</div>'
            f'<div class="stat">{stats}</div>'
            + ul(pr["points"]) + f'<div class="u">{pr["url"]}</div></div>')

    ach = ''.join(f'<div class="ach"><div class="bq">{icon(P_SHIELD, "#1a86f0", 13)}</div>'
                  f'<div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
                  for t, d in D.STRENGTHS)
    tags = ''.join(f'<span class="tag">{t}</span>' for t in D.SKILL_TAGS)
    learn = ''.join(f'<span class="tag">{t}</span>' for t in D.LEARNING)
    cert = '<div class="up">&#8593;</div>'.join(
        f'<div class="blk cert"><div class="t">{n}</div><div class="s">{d}</div></div>'
        for n, d in D.CERTIFICATIONS)

    langs = ''
    for n, l, r in D.LANGUAGES:
        langs += (f'<div class="lrow"><span class="n">{n}</span>'
                  f'<span>{dots(r, 5, "d2")}</span></div><div class="lv">{l}</div>')

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{D.NAME} — Resume</title><style>{CSS}</style></head><body>
<div class="hdr"><div class="txt"><h1>{D.NAME}</h1>
<div class="role">{D.TITLE_V2}</div>
<div class="meta">{meta}</div></div>
<img src="{D.PHOTO}" alt="{D.NAME}"></div>
<div class="cols">
 <div class="l">
  <h2>Summary</h2><p class="sum">{D.SUMMARY_SHORT}</p>
  <h2>Experience</h2>{jobs}
  <h2>Education</h2>{edu}
 </div>
 <div class="r">
  <h2>Key Strengths</h2>{ach}
  <h2>Skills</h2><div>{tags}</div>
  <h2>Learning Now</h2><div>{learn}</div>
  <h2>Project</h2>{proj}
  <h2>Certifications</h2>{cert}
  <h2>Languages</h2>{langs}
 </div>
</div></body></html>'''
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out)


if __name__ == '__main__':
    build(sys.argv[1])
