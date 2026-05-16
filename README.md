# aday sözlüğü / candidate lexicon

A small research pipeline and static website for comparing how Turkish political candidates use language in interview transcripts.

The project extracts only target candidate speech blocks from labeled transcript files, cleans and normalizes Turkish text, calculates word and phrase frequencies, and presents the results in a bilingual interactive site.

## Corpus

Raw transcripts live in:

```text
corpus/raw/erdogan/
corpus/raw/ogan/
corpus/raw/kilicdaroglu/
```

The website also includes static copies under `site/raw-data/` so readers can open the source transcript files directly from the page.

## Method

- Speaker labels are detected on their own line.
- Text after a label is treated as that speaker's turn until the next label.
- Only the configured target speaker blocks are analyzed.
- Moderator, journalist, interviewer, and question text is excluded.
- Turkish characters are preserved.
- Apostrophe forms and selected political term variants are normalized.
- Function words such as `ve`, `da`, `de`, and `ama` are removed from frequency analysis.
- Pronouns are not removed, because pronouns are methodologically important for political discourse analysis.
- Terms such as `cumhurbaşkanı` and `cumhurbaşkanlığı` are not automatically merged.

## Run The Analysis

Create a Python environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the full transcript workflow:

```bash
.venv/bin/python analyze_speeches.py
```

Rebuild the static website data:

```bash
.venv/bin/python build_site_data.py
```

Build the Excel findings workbook:

```bash
node build_findings_workbook.mjs
```

Serve the website locally:

```bash
cd site
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/`.

## Outputs

The pipeline writes extracted text, cleaned text, CSVs, charts, and workbook outputs:

```text
corpus/extracted/
corpus/cleaned/
corpus/outputs/frequencies/
corpus/outputs/ngrams/
corpus/outputs/charts/
outputs/turkish_political_discourse_findings.xlsx
site/
```

## Notes

These findings describe the current transcript sample, not the full universe of each politician's language. As the corpus grows, rates and clusters may shift.

Icon assets are attributed in the site footer: icons created by juicy_fish - Flaticon.
