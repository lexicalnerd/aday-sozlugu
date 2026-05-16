import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const ROOT = process.cwd();
const OUTPUT_DIR = path.join(ROOT, "outputs");
const XLSX_PATH = path.join(OUTPUT_DIR, "turkish_political_discourse_findings.xlsx");

const COLORS = {
  navy: "#17324D",
  paleBlue: "#EAF3FF",
  blue: "#1565C0",
  red: "#C62828",
  green: "#2E7D32",
  gray: "#64748B",
  lightGray: "#F3F6FA",
  border: "#D8DEE9",
  white: "#FFFFFF",
};

const CANDIDATES = [
  { key: "erdogan", name: "Erdoğan", color: COLORS.red },
  { key: "ogan", name: "Oğan", color: COLORS.blue },
  { key: "kilicdaroglu", name: "Kılıçdaroğlu", color: COLORS.green },
];

function csvParse(text) {
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    const n = text[i + 1];
    if (c === '"' && inQuotes && n === '"') {
      field += '"';
      i++;
    } else if (c === '"') {
      inQuotes = !inQuotes;
    } else if (c === "," && !inQuotes) {
      row.push(field);
      field = "";
    } else if ((c === "\n" || c === "\r") && !inQuotes) {
      if (c === "\r" && n === "\n") i++;
      row.push(field);
      if (row.some((v) => v !== "")) rows.push(row);
      row = [];
      field = "";
    } else {
      field += c;
    }
  }
  row.push(field);
  if (row.some((v) => v !== "")) rows.push(row);
  return rows;
}

async function readCsv(relPath) {
  const text = await fs.readFile(path.join(ROOT, relPath), "utf8");
  const rows = csvParse(text);
  const headers = rows[0];
  return rows.slice(1).map((row) =>
    Object.fromEntries(headers.map((header, i) => [header, row[i] ?? ""])),
  );
}

function toNumber(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

function titleCaseSlug(key) {
  return CANDIDATES.find((candidate) => candidate.key === key)?.name ?? key;
}

function candidatePath(key, kind) {
  if (kind === "words") return `corpus/outputs/frequencies/${key}_combined_top_words.csv`;
  if (kind === "bigrams") return `corpus/outputs/ngrams/${key}_combined_top_bigrams.csv`;
  if (kind === "trigrams") return `corpus/outputs/ngrams/${key}_combined_top_trigrams.csv`;
  if (kind === "identity") return `corpus/outputs/frequencies/${key}_combined_identity_counts.csv`;
  if (kind === "clusters") return `corpus/outputs/ngrams/${key}_combined_word_clusters.csv`;
  throw new Error(`Unknown kind ${kind}`);
}

function setColumnWidths(sheet, widths) {
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, 1, 1).format.columnWidthPx = width;
  });
}

function styleTitle(sheet, range, title, subtitle = "") {
  const r = sheet.getRange(range);
  r.merge();
  r.values = [[subtitle ? `${title}\n${subtitle}` : title]];
  r.format = {
    fill: COLORS.navy,
    font: { color: COLORS.white, bold: true, size: 18 },
    wrapText: true,
    horizontalAlignment: "left",
    verticalAlignment: "center",
  };
  r.format.rowHeightPx = subtitle ? 58 : 40;
}

function styleHeader(range) {
  range.format = {
    fill: COLORS.paleBlue,
    font: { bold: true, color: COLORS.navy },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
}

function styleTable(sheet, rangeAddress) {
  const range = sheet.getRange(rangeAddress);
  range.format = {
    border: { color: COLORS.border, style: "continuous" },
    verticalAlignment: "top",
  };
}

function writeRows(sheet, startCell, rows) {
  if (!rows.length) return;
  const range = sheet.getRange(startCell).resize(rows.length, rows[0].length);
  range.values = rows;
}

function rowFromObject(row, columns) {
  return columns.map((column) => {
    const value = row[column] ?? "";
    const n = Number(value);
    return value !== "" && Number.isFinite(n) ? n : value;
  });
}

function topItemsRows(items, labelCol, countCol, topN = 20) {
  return items.slice(0, topN).map((row, i) => [i + 1, row[labelCol], toNumber(row[countCol])]);
}

function shortTopWords(candidateKey, topN = 5) {
  return topWords[candidateKey]
    .slice(0, topN)
    .map((row) => row.word)
    .join(", ");
}

const workbook = Workbook.create();

const comparison = await readCsv("corpus/outputs/candidate_comparison.csv");
const fileSummary = await readCsv("corpus/outputs/all_candidates_summary.csv");
const topWords = Object.fromEntries(
  await Promise.all(CANDIDATES.map(async (c) => [c.key, await readCsv(candidatePath(c.key, "words"))])),
);
const bigrams = Object.fromEntries(
  await Promise.all(CANDIDATES.map(async (c) => [c.key, await readCsv(candidatePath(c.key, "bigrams"))])),
);
const trigrams = Object.fromEntries(
  await Promise.all(CANDIDATES.map(async (c) => [c.key, await readCsv(candidatePath(c.key, "trigrams"))])),
);
const identityCounts = Object.fromEntries(
  await Promise.all(CANDIDATES.map(async (c) => [c.key, await readCsv(candidatePath(c.key, "identity"))])),
);
const clusters = Object.fromEntries(
  await Promise.all(CANDIDATES.map(async (c) => [c.key, await readCsv(candidatePath(c.key, "clusters"))])),
);

// Dashboard
{
  const sheet = workbook.worksheets.add("Dashboard");
  sheet.showGridLines = false;
  setColumnWidths(sheet, [190, 115, 115, 115, 115, 115, 115, 130, 130, 130, 130, 130]);
  styleTitle(
    sheet,
    "A1:L2",
    "Turkish Political Discourse Analysis",
    "Candidate comparison from politician-only extracted speech blocks",
  );

  const kpiRows = [
    ["Candidate", "Files", "Target turns", "Cleaned tokens", "Analysis tokens", "Top signal words"],
    ...comparison.map((row) => {
      const candidate = CANDIDATES.find((c) => c.name === row.candidate);
      return [
      row.candidate,
      toNumber(row.files),
      toNumber(row.target_turns),
      toNumber(row.cleaned_tokens),
      toNumber(row.analysis_tokens),
      shortTopWords(candidate?.key ?? "erdogan"),
      ];
    }),
  ];
  writeRows(sheet, "A4", kpiRows);
  styleHeader(sheet.getRange("A4:F4"));
  styleTable(sheet, "A4:F7");
  sheet.getRange("B5:E7").format.numberFormat = "#,##0";
  sheet.getRange("F5:F7").format.wrapText = true;
  sheet.getRange("A5:F7").format.rowHeightPx = 34;
  sheet.getRange("A5:A7").format.font = { bold: true };

  const rateHeaders = ["Candidate", "biz / 1k", "ben / 1k", "türkiye / 1k", "türk / 1k", "terör / 1k", "devlet / 1k"];
  const rateRows = [
    rateHeaders,
    ...comparison.map((row) => [
      row.candidate,
      toNumber(row.biz_per_1000),
      toNumber(row.ben_per_1000),
      toNumber(row["türkiye_per_1000"]),
      toNumber(row["türk_per_1000"]),
      toNumber(row["terör_per_1000"]),
      toNumber(row.devlet_per_1000),
    ]),
  ];
  writeRows(sheet, "A10", rateRows);
  styleHeader(sheet.getRange("A10:G10"));
  styleTable(sheet, "A10:G13");
  sheet.getRange("B11:G13").format.numberFormat = "0.00";

  const chart = sheet.charts.add("bar", sheet.getRange("A10:G13"));
  chart.title = "Normalized Identity and Pronoun Terms per 1,000 Tokens";
  chart.hasLegend = true;
  chart.xAxis = { axisType: "textAxis" };
  chart.yAxis = { numberFormatCode: "0.0" };
  chart.setPosition("I4", "L19");

  const insightRows = [
    ["Reading guide"],
    ["Rates normalize by cleaned tokens, making candidates with different transcript volume comparable."],
    ["Top words and clusters are calculated after removing selected function words and number-only tokens."],
    ["Word clouds are available as SVG artifacts in corpus/outputs/charts/."],
  ];
  writeRows(sheet, "A16", insightRows);
  sheet.getRange("A16:G16").merge();
  sheet.getRange("A16:G16").format = { fill: COLORS.lightGray, font: { bold: true, color: COLORS.navy } };
  sheet.getRange("A17:G19").merge(true);
  sheet.getRange("A17:G19").format = { wrapText: true, font: { color: COLORS.gray } };
}

// Candidate Comparison
{
  const sheet = workbook.worksheets.add("Candidate Comparison");
  sheet.showGridLines = false;
  const headers = Object.keys(comparison[0]);
  writeRows(sheet, "A1", [headers, ...comparison.map((row) => rowFromObject(row, headers))]);
  styleHeader(sheet.getRangeByIndexes(0, 0, 1, headers.length));
  styleTable(sheet, `A1:AS${comparison.length + 1}`);
  sheet.freezePanes.freezeRows(1);
  setColumnWidths(sheet, [135, 70, 90, 90, 105, 105, 430, ...Array(headers.length - 7).fill(90)]);
  sheet.getRange("B2:F4").format.numberFormat = "#,##0";
  sheet.getRange("H2:AS4").format.numberFormat = "0.00";
  sheet.getRange("G2:G4").format.wrapText = true;
}

// Top Words
{
  const sheet = workbook.worksheets.add("Top Words");
  sheet.showGridLines = false;
  const rows = [["Rank", "Erdoğan word", "Count", "Oğan word", "Count", "Kılıçdaroğlu word", "Count"]];
  for (let i = 0; i < 30; i++) {
    rows.push([
      i + 1,
      topWords.erdogan[i]?.word ?? "",
      toNumber(topWords.erdogan[i]?.count),
      topWords.ogan[i]?.word ?? "",
      toNumber(topWords.ogan[i]?.count),
      topWords.kilicdaroglu[i]?.word ?? "",
      toNumber(topWords.kilicdaroglu[i]?.count),
    ]);
  }
  writeRows(sheet, "A1", rows);
  styleHeader(sheet.getRange("A1:G1"));
  styleTable(sheet, "A1:G31");
  setColumnWidths(sheet, [60, 150, 80, 150, 80, 170, 80]);
  sheet.freezePanes.freezeRows(1);
}

// Ngrams
{
  const sheet = workbook.worksheets.add("Ngrams");
  sheet.showGridLines = false;
  const rows = [["Rank", "Erdoğan bigram", "Count", "Oğan bigram", "Count", "Kılıçdaroğlu bigram", "Count"]];
  for (let i = 0; i < 25; i++) {
    rows.push([
      i + 1,
      bigrams.erdogan[i]?.bigram ?? "",
      toNumber(bigrams.erdogan[i]?.count),
      bigrams.ogan[i]?.bigram ?? "",
      toNumber(bigrams.ogan[i]?.count),
      bigrams.kilicdaroglu[i]?.bigram ?? "",
      toNumber(bigrams.kilicdaroglu[i]?.count),
    ]);
  }
  rows.push([]);
  rows.push(["Rank", "Erdoğan trigram", "Count", "Oğan trigram", "Count", "Kılıçdaroğlu trigram", "Count"]);
  for (let i = 0; i < 20; i++) {
    rows.push([
      i + 1,
      trigrams.erdogan[i]?.trigram ?? "",
      toNumber(trigrams.erdogan[i]?.count),
      trigrams.ogan[i]?.trigram ?? "",
      toNumber(trigrams.ogan[i]?.count),
      trigrams.kilicdaroglu[i]?.trigram ?? "",
      toNumber(trigrams.kilicdaroglu[i]?.count),
    ]);
  }
  writeRows(sheet, "A1", rows);
  styleHeader(sheet.getRange("A1:G1"));
  styleHeader(sheet.getRange("A28:G28"));
  styleTable(sheet, "A1:G48");
  setColumnWidths(sheet, [60, 190, 80, 190, 80, 210, 80]);
  sheet.freezePanes.freezeRows(1);
}

// Identity Counts
{
  const sheet = workbook.worksheets.add("Identity Counts");
  sheet.showGridLines = false;
  const termSet = identityCounts.erdogan.map((row) => row.term);
  const rows = [["Term", "Erdoğan", "Oğan", "Kılıçdaroğlu", "All candidates"]];
  const allIdentity = await readCsv("corpus/outputs/frequencies/all_candidates_combined_identity_counts.csv");
  for (const term of termSet) {
    const pick = (key) => toNumber(identityCounts[key].find((row) => row.term === term)?.count);
    rows.push([
      term,
      pick("erdogan"),
      pick("ogan"),
      pick("kilicdaroglu"),
      toNumber(allIdentity.find((row) => row.term === term)?.count),
    ]);
  }
  writeRows(sheet, "A1", rows);
  styleHeader(sheet.getRange("A1:E1"));
  styleTable(sheet, `A1:E${rows.length}`);
  setColumnWidths(sheet, [210, 110, 110, 130, 130]);
  sheet.freezePanes.freezeRows(1);
}

// Word Clusters
{
  const sheet = workbook.worksheets.add("Word Clusters");
  sheet.showGridLines = false;
  const headers = ["Candidate", "Anchor", "Cluster", "Following word", "Count"];
  const rows = [headers];
  for (const candidate of CANDIDATES) {
    for (const row of clusters[candidate.key].slice(0, 140)) {
      rows.push([candidate.name, row.anchor, row.cluster, row.following_word, toNumber(row.count)]);
    }
  }
  writeRows(sheet, "A1", rows);
  styleHeader(sheet.getRange("A1:E1"));
  styleTable(sheet, `A1:E${rows.length}`);
  setColumnWidths(sheet, [140, 80, 220, 160, 80]);
  sheet.freezePanes.freezeRows(1);
}

// Corpus Files
{
  const sheet = workbook.worksheets.add("Corpus Files");
  sheet.showGridLines = false;
  const headers = Object.keys(fileSummary[0]);
  writeRows(sheet, "A1", [headers, ...fileSummary.map((row) => rowFromObject(row, headers))]);
  styleHeader(sheet.getRangeByIndexes(0, 0, 1, headers.length));
  styleTable(sheet, `A1:F${fileSummary.length + 1}`);
  setColumnWidths(sheet, [130, 430, 95, 90, 105, 105]);
  sheet.freezePanes.freezeRows(1);
}

// Methodology
{
  const sheet = workbook.worksheets.add("Methodology");
  sheet.showGridLines = false;
  setColumnWidths(sheet, [240, 850]);
  styleTitle(sheet, "A1:B2", "Methodology Notes", "How the workbook was produced");
  const rows = [
    ["Parsing", "Speaker labels on their own line define turns. Only target-politician turns are extracted. Unlabeled files inside a politician folder are treated as politician-only monologues."],
    ["Cleaning", "Turkish characters are preserved; text is lowercased; punctuation, transcription artifacts, and numeric-only analysis tokens are removed."],
    ["Normalization", "Selected political entities and abbreviations are normalized, e.g. CHP’ye -> chp, AK Parti’ye -> ak parti, Türkiye’ye -> türkiye."],
    ["Stop/function words", "Selected Turkish function/filler words are excluded from frequency, ngram, cluster, and word-cloud analysis. Pronouns are retained."],
    ["Rates", "Per-1,000 rates use cleaned tokens as denominator."],
    ["Artifacts", "Word-cloud SVGs and top-word PNG charts are in corpus/outputs/charts/."],
  ];
  writeRows(sheet, "A4", [["Topic", "Note"], ...rows]);
  styleHeader(sheet.getRange("A4:B4"));
  styleTable(sheet, "A4:B10");
  sheet.getRange("B5:B10").format.wrapText = true;
}

for (const sheet of workbook.worksheets.items) {
  const used = sheet.getUsedRange();
  if (used) {
    used.format.font = { name: "Avenir" };
    used.format.verticalAlignment = "top";
  }
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

const dashboardCheck = await workbook.inspect({
  kind: "table",
  range: "Dashboard!A1:G19",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 8,
});
console.log(dashboardCheck.ndjson);

await fs.mkdir(OUTPUT_DIR, { recursive: true });
const previewDir = path.join(OUTPUT_DIR, "workbook_previews");
await fs.mkdir(previewDir, { recursive: true });
for (const sheetName of [
  "Dashboard",
  "Candidate Comparison",
  "Top Words",
  "Ngrams",
  "Identity Counts",
  "Word Clusters",
  "Corpus Files",
  "Methodology",
]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(
    path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(XLSX_PATH);
console.log(`Saved ${XLSX_PATH}`);
