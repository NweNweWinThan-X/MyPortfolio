# CV build

Generates every CV file in `../cv-form/` from one content source.

| File | Purpose |
|--|--|
| `cv_data.py` | All CV content — the single source of truth for version1 and version2 |
| `build_v1.py` | version1: navy header band, grey sidebar with rated skills |
| `build_v2.py` | version2: blue accents, two columns, tagged skills |
| `md2print.py` | classic layout, from `../cv-form/NWENWE_WINTHAN_Resume_EN.md` |
| `md2docx.py` | Word export, from the same Markdown |
| `profile.jpg` | 440×440 portrait, embedded as a data URI |

The classic layout reads the Markdown in `cv-form/`; version1 and version2 read
`cv_data.py`. Changing a fact in one does not change the other — update both.

## Rebuild everything

```sh
cd _build
python3 build_v1.py v1.html
python3 build_v2.py v2.html
python3 md2print.py ../cv-form/NWENWE_WINTHAN_Resume_EN.md classic.html "Nwe Nwe Win Than — Resume"
for f in v1 v2 classic; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$f.pdf" "file://$PWD/$f.html"
done
python3 md2docx.py ../cv-form/NWENWE_WINTHAN_Resume_EN.md classic.docx en

cp v1.pdf      ../cv-form/NWENWE_WINTHAN_Resume_version1.pdf
cp v2.pdf      ../cv-form/NWENWE_WINTHAN_Resume_version2.pdf
cp classic.pdf ../cv-form/NWENWE_WINTHAN_Resume.pdf
cp classic.pdf ../cv-form/NWENWE_WINTHAN_Resume_English.pdf
cp classic.docx ../cv-form/NWENWE_WINTHAN_Resume_EN.docx
```

Requires `pypdf`, `python-docx`, `Pillow` and Google Chrome. All three PDFs
should come out at 2 pages; check before committing.

## Notes

- `profile.jpg` is cropped from the 履歴書 spreadsheet: square, biased 3.5%
  upward so the face sits centred.
- Bullet characters in CSS must be literal `•`, never a `\2022` escape —
  Python reads `\202` in a non-raw string as an octal escape and the marker
  renders as a stray "2".
- version1 pushes Learning and Certifications to page 2 via `SIDEBAR_PAGE2`;
  `.pagebreak + h2` zeroes the heading margin so the two columns start level.
