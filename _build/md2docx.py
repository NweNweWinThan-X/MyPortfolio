#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown -> .docx for the CV files.

Modes:
  en  single column, no layout tables (ATS-safe), Calibri, portrait in the header
  ja  real tables for project blocks, Yu Gothic
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv_data as CVD  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.opc.constants import RELATIONSHIP_TYPE as RT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Pt, RGBColor, Cm  # noqa: E402

INLINE = re.compile(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\[[^\]]+?\]\([^)]+?\))')
ACCENT = RGBColor(0x14, 0x36, 0x5C)
SUBTLE = RGBColor(0x30, 0x50, 0x7A)
GREY = RGBColor(0x55, 0x55, 0x55)


def set_fonts(doc, latin, east_asian):
    st = doc.styles['Normal']
    st.font.name = latin
    st.font.size = Pt(10)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    rf.set(qn('w:ascii'), latin)
    rf.set(qn('w:hAnsi'), latin)
    rf.set(qn('w:eastAsia'), east_asian)


def style_run(run, latin, east_asian):
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    rf.set(qn('w:ascii'), latin)
    rf.set(qn('w:hAnsi'), latin)
    rf.set(qn('w:eastAsia'), east_asian)


def add_hyperlink(par, url, text, cfg, size=None):
    """Append a clickable w:hyperlink run; python-docx has no API for this."""
    r_id = par.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), r_id)
    run = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), cfg['latin'])
    rf.set(qn('w:hAnsi'), cfg['latin'])
    rf.set(qn('w:eastAsia'), cfg['ea'])
    rpr.append(rf)
    col = OxmlElement('w:color')
    col.set(qn('w:val'), '1D5F99')
    rpr.append(col)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rpr.append(u)
    if size is not None:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(int(size.pt * 2)))
        rpr.append(sz)
    run.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    run.append(t)
    link.append(run)
    par._p.append(link)          # runs are appended in order, so this stays in place
    return link


def add_inline(par, text, cfg, bold=False, size=None, color=None):
    text = text.replace('<br>', '\n')
    for part in INLINE.split(text):
        if not part:
            continue
        m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)
        if m:
            add_hyperlink(par, m.group(2), m.group(1), cfg, size=size)
            continue
        b, i, mono = bold, False, False
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            part, b = part[2:-2], True
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            part, i = part[1:-1], True
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            part, mono = part[1:-1], True
        for n, chunk in enumerate(part.split('\n')):
            if n:
                par.add_run().add_break()
            if not chunk:
                continue
            run = par.add_run(chunk)
            run.bold = b
            run.italic = i
            if size:
                run.font.size = size
            if color is not None:
                run.font.color.rgb = color
            style_run(run, 'Consolas' if mono else cfg['latin'], cfg['ea'])


def hrule(par):
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:color'), '14365C')
    pbdr.append(bottom)
    par._p.get_or_add_pPr().append(pbdr)


def shade(cell, hex_fill):
    tcpr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear')
    sh.set(qn('w:fill'), hex_fill)
    tcpr.append(sh)


def parse_table(lines, start):
    rows, i = [], start
    while i < len(lines) and lines[i].lstrip().startswith('|'):
        cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
        if not all(re.fullmatch(r':?-{2,}:?', c or '-') and set(c) <= set('-: ') and c
                   for c in cells):
            rows.append(cells)
        i += 1
    return rows, i


def convert(src, dst, mode):
    cfg = ({'latin': 'Calibri', 'ea': 'Calibri'} if mode == 'en'
           else {'latin': 'Yu Gothic', 'ea': 'Yu Gothic'})
    doc = Document()
    set_fonts(doc, cfg['latin'], cfg['ea'])
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.4)
        s.left_margin = s.right_margin = Cm(1.6)

    lines = open(src, encoding='utf-8').read().split('\n')
    header_cell = [None]
    header_used = [0]
    i = 0
    first_h1 = True

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped in ('---', '***', '___'):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            hrule(p)
            i += 1
            continue

        # Standalone timeline connector between dated entries.
        if stripped in ('↑', '^'):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.left_indent = Cm(0.25)
            add_inline(p, '↑', cfg, size=Pt(9), color=RGBColor(0x2F, 0x7E, 0xC4))
            i += 1
            continue

        if stripped.startswith('|'):
            rows, i = parse_table(lines, i)
            if not rows:
                continue
            if mode == 'en':
                # ATS-safe: label — value paragraphs, never a layout table
                for r in rows:
                    cells = [c for c in r if c]
                    if not cells:
                        continue
                    p = doc.add_paragraph()
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.left_indent = Cm(0.4)
                    if len(cells) >= 2:
                        add_inline(p, cells[0], cfg, bold=True)
                        p.add_run('  —  ')
                        add_inline(p, '  ·  '.join(cells[1:]), cfg)
                    else:
                        add_inline(p, cells[0], cfg)
            else:
                width = max(len(r) for r in rows)
                t = doc.add_table(rows=0, cols=width)
                t.style = 'Table Grid'
                t.alignment = WD_TABLE_ALIGNMENT.LEFT
                header = rows[0]
                looks_header = all(len(c) < 24 for c in header if c)
                for ri, r in enumerate(rows):
                    row = t.add_row()
                    for ci in range(width):
                        cell = row.cells[ci]
                        cell.paragraphs[0].text = ''
                        txt = r[ci] if ci < len(r) else ''
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_after = Pt(1)
                        bold = ri == 0 and looks_header
                        add_inline(p, txt, cfg, bold=bold, size=Pt(9))
                        if bold:
                            shade(cell, 'EDF1F7')
                        elif ci == 0 and width > 1:
                            shade(cell, 'F7F9FB')
                doc.add_paragraph().paragraph_format.space_after = Pt(4)
            continue

        if stripped.startswith('> '):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip())
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.space_after = Pt(6)
            add_inline(p, ' '.join(buf), cfg, size=Pt(9), color=GREY)
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', stripped)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if level == 1 and first_h1:
                first_h1 = False
                if mode == 'en' and os.path.exists(CVD.PHOTO_PATH):
                    # one borderless table so the portrait sits beside the name;
                    # everything after this stays a single column for ATS parsing
                    t = doc.add_table(rows=1, cols=2)
                    t.autofit = False
                    t.columns[0].width = Cm(13.4)
                    t.columns[1].width = Cm(3.3)
                    cell = t.cell(0, 0)
                    cell.width = Cm(13.4)
                    hp = cell.paragraphs[0]
                    hp.paragraph_format.space_after = Pt(1)
                    add_inline(hp, text, cfg, bold=True, size=Pt(21), color=ACCENT)
                    pic = t.cell(0, 1)
                    pic.width = Cm(3.3)
                    pp = pic.paragraphs[0]
                    pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    pp.add_run().add_picture(CVD.PHOTO_PATH, width=Cm(3.0))
                    header_cell[0] = cell
                else:
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p.paragraph_format.space_after = Pt(2)
                    add_inline(p, text, cfg, bold=True, size=Pt(21), color=ACCENT)
                i += 1
                continue
            sizes = {1: 15, 2: 13, 3: 11, 4: 10}
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10 if level <= 2 else 7)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            add_inline(p, text, cfg, bold=True, size=Pt(sizes[level]),
                       color=ACCENT if level <= 3 else None)
            if level == 2:
                hrule(p)
            i += 1
            continue

        m = re.match(r'^[-*]\s+(.*)$', stripped)
        if m:
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.left_indent = Cm(0.7)
            body = m.group(1)
            i += 1
            while (i < len(lines) and lines[i].startswith('  ')
                   and lines[i].strip()
                   and not re.match(r'^\s*[-*]\s', lines[i])
                   and not lines[i].strip().startswith('|')):
                body += ' ' + lines[i].strip()
                i += 1
            add_inline(p, body, cfg)
            continue

        # paragraph: join soft-wrapped continuation lines
        body = stripped
        i += 1
        while (i < len(lines) and lines[i].strip()
               and not re.match(r'^(#{1,4}\s|[-*]\s|\||>\s)', lines[i].strip())
               and lines[i].strip() not in ('---', '***', '___', '↑', '^')):
            body += ' ' + lines[i].strip()
            i += 1
        if header_cell[0] is not None and header_used[0] < 2:
            p = header_cell[0].add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            add_inline(p, body, cfg,
                       bold=header_used[0] == 0,
                       size=Pt(10.5) if header_used[0] == 0 else Pt(8.5),
                       color=SUBTLE if header_used[0] == 0 else GREY)
            header_used[0] += 1
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        add_inline(p, body, cfg)

    doc.save(dst)
    print('wrote', dst)


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
