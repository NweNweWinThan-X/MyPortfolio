#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown -> print-ready A4 HTML for the classic resume layout.

Single text column so the PDF stays ATS-parseable; tables render as
label/value lines rather than layout tables. Placeholders are highlighted so
they cannot ship by accident. Render with Chrome --headless --print-to-pdf.
"""
import html as H
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_data as D  # noqa: E402

INLINE = re.compile(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\[[^\]]+?\]\([^)]+?\))')
PLACEHOLDER = re.compile(r'(\[(?:ADD METRIC|CONFIRM)[^\]]*\]|【要記入[^】]*】|【要確認[^】]*】)')

CSS = """
@page { size: A4; margin: 8mm 10mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Helvetica, Arial, "Hiragino Sans", "Yu Gothic", sans-serif;
       font-size: 8.05pt; line-height: 1.19; color: #1a1a1a; margin: 0; }
h1 { font-size: 21pt; letter-spacing: .4px; color: #14365c; margin: 0 0 1pt;
     text-align: left; font-weight: 800; }
.head { display: flex; align-items: center; gap: 7mm; border-bottom: 1.6pt solid #14365c;
        padding-bottom: 3mm; margin-bottom: 2mm; }
.head .txt { flex: 1; }
.head img { width: 25mm; height: 25mm; border-radius: 50%; object-fit: cover;
            flex: 0 0 25mm; border: .8mm solid #e2e8ef; }
h2 { font-size: 9.2pt; color: #14365c; margin: 5.5pt 0 2pt; padding-bottom: 1.5pt;
     border-bottom: .9pt solid #c3ccd6; text-transform: uppercase;
     letter-spacing: 1.1px; font-weight: 800; }
h3 { font-size: 8.9pt; color: #14365c; margin: 5pt 0 0; font-weight: 700;
     page-break-after: avoid; }
h4 { font-size: 9.1pt; margin: 4.5pt 0 0; font-weight: 700; page-break-after: avoid; }
p  { margin: 0 0 1.9pt; }
ul { margin: 1.5pt 0 3pt; padding-left: 10pt; list-style: disc outside; }
li::marker { color: #14365c; }
li { margin: 0 0 1pt; page-break-inside: avoid; }
a  { color: #1d5f99; text-decoration: none; }
em { color: #555; font-style: italic; font-size: 8.3pt; }
hr { display: none; }
.subtitle { text-align: left; font-size: 10.2pt; color: #30507a;
            font-weight: 700; margin: 1.5pt 0 3pt; letter-spacing: .2px; }
.contact { text-align: left; font-size: 8.3pt; color: #4a5560; margin: 0 0 1pt; }
ul.contactlist { display: flex; flex-wrap: wrap; gap: 1pt 14pt; margin: 3pt 0 0;
                 padding: 0; list-style: none; }
ul.contactlist li { font-size: 8.3pt; color: #3c4854; margin: 0; padding-left: 7pt;
                    position: relative; }
ul.contactlist li::before { content: "•"; position: absolute; left: 0;
                            color: #14365c; font-weight: 700; }
.kv { margin: 0 0 1.1pt; padding-left: 2pt; }
.kv b { color: #14365c; }
.note { background: #fff6d6; border-left: 2.5pt solid #e0a800; padding: 3pt 5pt;
        font-size: 7.9pt; color: #5a4500; margin: 3pt 0; }
.flag { background: #ffe0e0; color: #a01010; font-weight: 700;
        padding: 0 2pt; border-radius: 2pt; }
.arrow { color: #2f7ec4; font-size: 10pt; line-height: 1; margin: 1pt 0 1pt 3pt; }
.job { page-break-inside: avoid; }
.skills p { margin-bottom: 2pt; }
"""


def inline(text):
    text = text.replace('<br>', '\x00BR\x00')
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)
        if m:
            out.append(f'<a href="{H.escape(m.group(2))}">{H.escape(m.group(1))}</a>')
        elif part.startswith('**') and part.endswith('**') and len(part) > 4:
            out.append(f'<b>{H.escape(part[2:-2])}</b>')
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            out.append(f'<em>{H.escape(part[1:-1])}</em>')
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            out.append(f'<code>{H.escape(part[1:-1])}</code>')
        else:
            out.append(H.escape(part))
    s = ''.join(out)
    s = PLACEHOLDER.sub(lambda m: f'<span class="flag">{m.group(1)}</span>', s)
    return s.replace('\x00BR\x00', '<br>')


def convert(src, dst, title):
    lines = open(src, encoding='utf-8').read().split('\n')
    body, i, first_h1, in_skills = [], 0, True, False
    header_lines = []

    while i < len(lines):
        s = lines[i].strip()

        if not s:
            i += 1
            continue

        if s in ('---', '***', '___'):
            body.append('<hr>')
            i += 1
            continue

        if s in ('↑', '^'):
            body.append('<div class="arrow">&#8593;</div>')
            i += 1
            continue

        if s.startswith('> '):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip())
                i += 1
            body.append(f'<div class="note">{inline(" ".join(buf))}</div>')
            continue

        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(c and set(c) <= set('-: ') for c in cells):
                    rows.append(cells)
                i += 1
            for r in rows:
                cells = [c for c in r if c]
                if not cells:
                    continue
                if len(cells) >= 2:
                    body.append(f'<p class="kv"><b>{inline(cells[0])}</b> &nbsp;—&nbsp; '
                                f'{inline("  ·  ".join(cells[1:]))}</p>')
                else:
                    body.append(f'<p class="kv">{inline(cells[0])}</p>')
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            lvl, text = len(m.group(1)), m.group(2)
            if lvl == 1 and first_h1:
                first_h1 = False
                header_lines.append(f'<h1>{inline(text)}</h1>')
                i += 1
                continue
            in_skills = (lvl == 2 and 'skill' in text.lower())
            body.append(f'<h{lvl}>{inline(text)}</h{lvl}>')
            if lvl == 2:
                body.append('<div class="%s">' % ('skills' if in_skills else 'sec'))
            i += 1
            continue

        m = re.match(r'^[-*]\s+(.*)$', s)
        if m:
            items = []
            while i < len(lines):
                mm = re.match(r'^[-*]\s+(.*)$', lines[i].strip())
                if not mm:
                    break
                txt = mm.group(1)
                i += 1
                while (i < len(lines) and lines[i].startswith('  ')
                       and lines[i].strip()
                       and not re.match(r'^\s*[-*]\s', lines[i])):
                    txt += ' ' + lines[i].strip()
                    i += 1
                items.append(f'<li>{inline(txt)}</li>')
            if not body:                       # still inside the header block
                header_lines.append('<ul class="contactlist">' + ''.join(items) + '</ul>')
            else:
                body.append('<ul>' + ''.join(items) + '</ul>')
            continue

        para = s
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not re.match(r'^(#{1,4}\s|[-*]\s|\||>\s)', lines[i].strip())
               and lines[i].strip() not in ('---', '***', '___', '↑', '^')):
            para += ' ' + lines[i].strip()
            i += 1
        if len(header_lines) and len(header_lines) < 3:
            cls = 'subtitle' if len(header_lines) == 1 else 'contact'
            header_lines.append(f'<p class="{cls}">{inline(para)}</p>')
            continue
        body.append(f'<p>{inline(para)}</p>')

    head = ('<div class="head"><div class="txt">' + ''.join(header_lines)
            + f'</div><img src="{D.PHOTO}" alt="{H.escape(title)}"></div>')
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
           f'<title>{H.escape(title)}</title><style>{CSS}</style></head><body>'
           + head + ''.join(body) + '</body></html>')
    open(dst, 'w', encoding='utf-8').write(doc)
    print('wrote', dst)


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
