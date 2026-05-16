from __future__ import annotations

import re
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None


# ---------------------------------------------------------------------------
# Sample config
# ---------------------------------------------------------------------------
# Change these three values for the first transcript you want to analyze.
# Put the transcript in corpus/raw/erdogan/ or point INPUT_FILE to any .txt file.
INPUT_FILE = Path("corpus/raw/erdogan/sample_erdogan_transcript.txt")
TARGET_SPEAKER_LABEL = "Erdoğan"
POLITICIAN_NAME = "erdogan"
ANALYZE_ALL_RAW_FILES_FOR_POLITICIAN = True
POLITICIAN_CONFIGS = [
    {"politician_name": "erdogan", "target_speaker_label": "Erdoğan"},
    {"politician_name": "ogan", "target_speaker_label": "Oğan"},
    {"politician_name": "kilicdaroglu", "target_speaker_label": "Kılıçdaroğlu"},
]


BASE_DIR = Path("corpus")
EXTRACTED_DIR = BASE_DIR / "extracted"
CLEANED_DIR = BASE_DIR / "cleaned"
OUTPUTS_DIR = BASE_DIR / "outputs"


# Add new expected labels here as the corpus grows. The parser also has a
# conservative label heuristic, but explicit labels are safer for interviews.
KNOWN_SPEAKER_LABELS = {
    "Erdoğan",
    "Kılıçdaroğlu",
    "Oğan",
    "Speaker 1",
    "Speaker 2",
    "Speaker 3",
    "Moderatör",
    "Moderator",
    "Sunucu",
    "Gazeteci",
}


IDENTITY_TERMS = [
    "biz",
    "bizim",
    "onlar",
    "millet",
    "milletimiz",
    "halk",
    "devlet",
    "türkiye",
    "cumhur",
    "ittifak",
    "terör",
    "genç",
    "aile",
    "vatan",
    "bayrak",
]


CANDIDATE_COMPARISON_TERMS = [
    "ben",
    "benim",
    "siz",
    "türk",
    *IDENTITY_TERMS,
]


CLUSTER_ANCHORS = [
    "biz",
    "ben",
    "türkiye",
    "türk",
    "millet",
    "milletimiz",
    "devlet",
]


CANDIDATE_COLORS = {
    "erdogan": "#c62828",
    "ogan": "#1565c0",
    "kilicdaroglu": "#2e7d32",
}


CANDIDATE_DISPLAY_NAMES = {
    "erdogan": "Erdoğan",
    "ogan": "Oğan",
    "kilicdaroglu": "Kılıçdaroğlu",
}


# Function words are excluded from frequency and ngram outputs because they are
# usually less informative for this discourse analysis. Pronouns are intentionally
# not included here: "biz", "bizim", "onlar", "ben" remain analytically visible.
EXCLUDED_FUNCTION_WORDS = {
    "acaba",
    "ama",
    "ancak",
    "anda",
    "artık",
    "aslında",
    "aynı",
    "az",
    "bazı",
    "belki",
    "bile",
    "bir",
    "biraz",
    "birçok",
    "böyle",
    "bu",
    "buna",
    "bunda",
    "bundan",
    "bunlar",
    "bunların",
    "bunları",
    "bunu",
    "bunun",
    "burada",
    "bütün",
    "çünkü",
    "çok",
    "daha",
    "da",
    "de",
    "defa",
    "diye",
    "dolayı",
    "eğer",
    "en",
    "fakat",
    "falan",
    "filan",
    "gene",
    "gibi",
    "göre",
    "hala",
    "hani",
    "hatta",
    "hem",
    "hep",
    "her",
    "herhangi",
    "hiç",
    "ile",
    "için",
    "içinde",
    "ise",
    "işte",
    "ki",
    "kadar",
    "karşı",
    "kaldı",
    "mı",
    "mi",
    "mu",
    "mü",
    "nasıl",
    "ne",
    "neden",
    "nerede",
    "neyse",
    "niye",
    "olan",
    "olarak",
    "oldu",
    "olduğu",
    "olması",
    "olmaz",
    "olsa",
    "olsun",
    "o",
    "onu",
    "onun",
    "orada",
    "öyle",
    "şayet",
    "şekilde",
    "şey",
    "şeyden",
    "şimdi",
    "şöyle",
    "şu",
    "şuna",
    "şunda",
    "şundan",
    "şunu",
    "sonra",
    "tabi",
    "tabii",
    "tam",
    "tüm",
    "üzere",
    "ve",
    "veya",
    "ya",
    "yani",
    "yine",
    "yok",
    "zaten",
}


# These suffixes cover common proper-name, abbreviation, plural, and possessive
# forms used in Turkish political transcripts. The aim is not full stemming;
# it is targeted normalization for terms where surface variation would otherwise
# hide repeated references to the same political object.
TERM_NORMALIZATION_PATTERNS = [
    (r"\bchp['’`´]?(?:ye|ya|nin|nın|nun|nün|de|da|den|dan|li|lı|lu|lü)?\b", "chp"),
    (
        r"\bak\s+parti['’`´]?(?:ye|ya|nin|nın|nun|nün|de|da|den|dan|li|lı|lu|lü)?\b",
        "ak parti",
    ),
    (
        r"\btürkiye['’`´]?(?:ye|ya|nin|nın|nun|nün|de|da|den|dan|li|lı|lu|lü)?\b",
        "türkiye",
    ),
    (
        r"\biha['’`´]?(?:lar|ler|larımız|lerimiz|ları|leri|nın|nin|ya|ye|da|de|dan|den)?\b",
        "iha",
    ),
    (
        r"\bsiha['’`´]?(?:lar|ler|larımız|lerimiz|ları|leri|nın|nin|ya|ye|da|de|dan|den)?\b",
        "siha",
    ),
    (
        r"\btogg['’`´]?(?:lar|ler|larımız|lerimiz|ları|leri|nın|nin|ya|ye|da|de|dan|den)?\b",
        "togg",
    ),
]


def read_transcript(input_file: Path) -> str:
    """Read a UTF-8 transcript file."""
    return input_file.read_text(encoding="utf-8")


def turkish_lower(text: str) -> str:
    """Lowercase while preserving Turkish dotted/dotless I distinctions."""
    return text.replace("I", "ı").replace("İ", "i").lower()


def is_speaker_label(
    line: str,
    target_speaker: str,
    known_speaker_labels: set[str] | None = None,
) -> bool:
    """Return True when a line appears to be a speaker label.

    Methodological note:
    Speaker labels are expected to appear on their own line. Exact known labels
    are preferred. A limited heuristic catches names such as "Ahmet Hakan" while
    avoiding most short utterances inside a speech block.
    """
    label = line.strip()
    if not label:
        return False

    known = set(known_speaker_labels or set())
    known.add(target_speaker)
    if label in known:
        return True

    if re.fullmatch(r"Speaker\s+\d+", label, flags=re.IGNORECASE):
        return True

    if len(label) > 80:
        return False

    words = label.split()
    if not 2 <= len(words) <= 6:
        return False

    # Labels normally do not end with sentence punctuation.
    if re.search(r"[.!?:;]$", label):
        return False

    # Allow Turkish letters, initials, spaces, hyphens, and apostrophes.
    if not re.fullmatch(r"[A-Za-zÇĞİÖŞÜçğıöşü.'’`\-\s]+", label):
        return False

    return any(word[:1].isupper() for word in words)


def parse_speaker_turns(
    transcript: str,
    target_speaker: str,
    known_speaker_labels: set[str] | None = None,
) -> list[tuple[str, str]]:
    """Parse transcript into (speaker_label, speech_text) turns."""
    turns: list[tuple[str, str]] = []
    current_speaker: str | None = None
    current_lines: list[str] = []

    for raw_line in transcript.splitlines():
        line = raw_line.strip()
        if is_speaker_label(line, target_speaker, known_speaker_labels):
            if current_speaker is not None and current_lines:
                turns.append((current_speaker, "\n".join(current_lines).strip()))
            current_speaker = line
            current_lines = []
        elif current_speaker is not None:
            current_lines.append(raw_line)

    if current_speaker is not None and current_lines:
        turns.append((current_speaker, "\n".join(current_lines).strip()))

    return turns


def extract_target_speaker(
    turns: Iterable[tuple[str, str]],
    target_speaker: str,
) -> str:
    """Extract only the target politician's turns, preserving raw text."""
    selected = [text for speaker, text in turns if speaker.strip() == target_speaker]
    return "\n\n".join(text for text in selected if text)


def remove_transcription_artifacts(text: str) -> str:
    """Remove common non-speech artifacts before token analysis."""
    text = re.sub(r"\[[^\]]*\]", " ", text)  # [alkış], [gülüşmeler]
    text = re.sub(r"\([^)]*\)", " ", text)  # (alkışlar), (00:01:22)
    text = re.sub(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", " ", text)
    text = re.sub(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b", " ", text)
    return text


def normalize_political_terms(text: str) -> str:
    """Normalize selected political abbreviations and proper-name inflections."""
    normalized = text
    for pattern, replacement in TERM_NORMALIZATION_PATTERNS:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
    return normalized


def clean_turkish_text(raw_text: str) -> str:
    """Create cleaned text while keeping Turkish characters and pronouns."""
    text = turkish_lower(raw_text)
    text = remove_transcription_artifacts(text)
    text = normalize_political_terms(text)

    # Remove apostrophe-marked suffixes that remain after targeted normalization:
    # e.g. "ankara'ya" -> "ankara". This is conservative and only applies when
    # an apostrophe marks the suffix boundary.
    text = re.sub(
        r"\b([a-zçğıöşü]+)['’`´](?:[a-zçğıöşü]+)\b",
        r"\1",
        text,
    )

    # Remove punctuation after apostrophe normalization. Turkish letters remain.
    text = re.sub(r"[^a-zçğıöşü0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(cleaned_text: str) -> list[str]:
    """Tokenize cleaned Turkish text with pronouns retained."""
    return re.findall(r"\b[a-zçğıöşü0-9]+\b", cleaned_text)


def exclude_function_words(tokens: list[str]) -> list[str]:
    """Remove selected function words and number-only tokens for analysis only."""
    return [
        token
        for token in tokens
        if token not in EXCLUDED_FUNCTION_WORDS and not token.isdigit()
    ]


def calculate_word_frequencies(tokens: list[str]) -> Counter:
    return Counter(tokens)


def calculate_ngrams(tokens: list[str], n: int) -> Counter:
    return Counter(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))


def calculate_following_word_clusters(
    tokens: list[str],
    anchors: Iterable[str],
) -> dict[str, Counter]:
    """Count words that immediately follow selected anchors such as 'biz'/'ben'."""
    anchor_set = set(anchors)
    clusters = {anchor: Counter() for anchor in anchor_set}
    for index, token in enumerate(tokens[:-1]):
        if token in anchor_set:
            follower = tokens[index + 1]
            if follower not in EXCLUDED_FUNCTION_WORDS and not follower.isdigit():
                clusters[token][follower] += 1
    return clusters


def save_counter_csv(counter: Counter, output_file: Path, top_n: int, columns: list[str]) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    rows = counter.most_common(top_n)
    data = [
        (" ".join(term) if isinstance(term, tuple) else term, count)
        for term, count in rows
    ]
    write_csv(data, output_file, columns)


def save_word_clusters(
    clusters: dict[str, Counter],
    output_file: Path,
    top_n: int = 30,
) -> None:
    rows = []
    for anchor in sorted(clusters):
        for follower, count in clusters[anchor].most_common(top_n):
            rows.append((anchor, f"{anchor} {follower}", follower, count))
    write_csv(rows, output_file, ["anchor", "cluster", "following_word", "count"])


def save_identity_counts(tokens: list[str], output_file: Path) -> None:
    counts = Counter(tokens)
    rows = [(term, counts[term]) for term in IDENTITY_TERMS]
    rows.append(("millet_plus_milletimiz", counts["millet"] + counts["milletimiz"]))
    write_csv(rows, output_file, ["term", "count"])


def write_csv(rows: list[tuple[str, int]], output_file: Path, columns: list[str]) -> None:
    """Write CSV with pandas when available, falling back to the stdlib csv module."""
    if pd is not None:
        pd.DataFrame(rows, columns=columns).to_csv(output_file, index=False, encoding="utf-8")
        return

    print("pandas is not installed; writing CSV with Python's csv module.")
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)


def save_frequency_chart(counter: Counter, output_file: Path, top_n: int = 20) -> bool:
    if plt is None:
        print("matplotlib is not installed; skipping chart output.")
        return False

    output_file.parent.mkdir(parents=True, exist_ok=True)
    top_words = counter.most_common(top_n)
    if not top_words:
        return False

    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.barh(words[::-1], counts[::-1])
    plt.title(f"Top {top_n} word frequencies")
    plt.xlabel("Count")
    plt.tight_layout()
    plt.savefig(output_file, dpi=200)
    plt.close()
    return True


def save_word_cloud_svg(
    counter: Counter,
    output_file: Path,
    top_n: int = 120,
    title: str | None = None,
    default_color: str = "#374151",
    word_colors: dict[str, str] | None = None,
    legend_items: list[tuple[str, str]] | None = None,
) -> bool:
    """Save a simple dependency-free SVG word cloud.

    This is intentionally lightweight: it avoids external wordcloud packages so
    the pipeline remains runnable in minimal Python environments. The layout is
    deterministic and uses frequency-scaled font sizes.
    """
    top_words = counter.most_common(top_n)
    if not top_words:
        return False

    output_file.parent.mkdir(parents=True, exist_ok=True)
    width = 1500
    height = 950
    center_x = width // 2
    center_y = height // 2 + 10
    max_count = top_words[0][1]
    fallback_colors = ["#1f4e79", "#8a3ffc", "#006d5b", "#b83280", "#b7791f", "#2f855a"]
    word_colors = word_colors or {}

    placed_boxes: list[tuple[int, int, int, int]] = []
    elements = []

    for index, (word, count) in enumerate(top_words):
        # Square-root scaling keeps frequent words dominant without making the
        # cloud unreadable for medium-frequency terms.
        size = int(15 + 48 * ((count / max_count) ** 0.5))
        estimated_width = int(len(word) * size * 0.58)
        estimated_height = int(size * 1.05)

        x = center_x - estimated_width // 2
        y = center_y
        for step in range(850):
            angle = step * 0.56
            radius = 4 + step * 2.35
            candidate_x = int(center_x + radius * math.cos(angle) - estimated_width / 2)
            candidate_y = int(center_y + radius * math.sin(angle))
            box = (
                candidate_x - 10,
                candidate_y - estimated_height - 10,
                candidate_x + estimated_width + 10,
                candidate_y + 10,
            )
            if box[0] < 20 or box[1] < 70 or box[2] > width - 20 or box[3] > height - 40:
                continue
            if any(
                not (
                    box[2] < other[0]
                    or box[0] > other[2]
                    or box[3] < other[1]
                    or box[1] > other[3]
                )
                for other in placed_boxes
            ):
                continue
            x = candidate_x
            y = candidate_y
            placed_boxes.append(box)
            break
        else:
            continue

        color = word_colors.get(word, default_color or fallback_colors[index % len(fallback_colors)])
        safe_word = (
            word.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        elements.append(
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-family="Avenir, Arial, Helvetica, sans-serif" '
            f'font-weight="700">{safe_word}</text>'
        )

    legend_elements = []
    if legend_items:
        legend_x = 34
        legend_y = 34
        for index, (label, color) in enumerate(legend_items):
            x = legend_x + index * 190
            safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            legend_elements.append(f'<circle cx="{x}" cy="{legend_y}" r="7" fill="{color}"/>')
            legend_elements.append(
                f'<text x="{x + 14}" y="{legend_y + 5}" font-size="16" '
                f'fill="#111827" font-family="Avenir, Arial, Helvetica, sans-serif">{safe_label}</text>'
            )

    title_element = ""
    if title:
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        title_element = (
            f'<text x="{width - 34}" y="39" text-anchor="end" font-size="18" '
            f'fill="#111827" font-family="Avenir, Arial, Helvetica, sans-serif" '
            f'font-weight="700">{safe_title}</text>'
        )

    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            *legend_elements,
            title_element,
            *elements,
            "</svg>",
        ]
    )
    output_file.write_text(svg, encoding="utf-8")
    return True


def output_paths(politician_name: str, input_file: Path) -> dict[str, Path]:
    stem = input_file.stem
    return {
        "extracted": EXTRACTED_DIR / politician_name / f"{stem}_extracted.txt",
        "cleaned": CLEANED_DIR / politician_name / f"{stem}_cleaned.txt",
        "words": OUTPUTS_DIR / "frequencies" / f"{politician_name}_{stem}_top_words.csv",
        "identity": OUTPUTS_DIR / "frequencies" / f"{politician_name}_{stem}_identity_counts.csv",
        "bigrams": OUTPUTS_DIR / "ngrams" / f"{politician_name}_{stem}_top_bigrams.csv",
        "trigrams": OUTPUTS_DIR / "ngrams" / f"{politician_name}_{stem}_top_trigrams.csv",
        "clusters": OUTPUTS_DIR / "ngrams" / f"{politician_name}_{stem}_word_clusters.csv",
        "chart": OUTPUTS_DIR / "charts" / f"{politician_name}_{stem}_top_words.png",
        "wordcloud": OUTPUTS_DIR / "charts" / f"{politician_name}_{stem}_wordcloud.svg",
    }


def combined_output_paths(politician_name: str) -> dict[str, Path]:
    return {
        "extracted": EXTRACTED_DIR / politician_name / f"{politician_name}_combined_extracted.txt",
        "cleaned": CLEANED_DIR / politician_name / f"{politician_name}_combined_cleaned.txt",
        "words": OUTPUTS_DIR / "frequencies" / f"{politician_name}_combined_top_words.csv",
        "identity": OUTPUTS_DIR / "frequencies" / f"{politician_name}_combined_identity_counts.csv",
        "bigrams": OUTPUTS_DIR / "ngrams" / f"{politician_name}_combined_top_bigrams.csv",
        "trigrams": OUTPUTS_DIR / "ngrams" / f"{politician_name}_combined_top_trigrams.csv",
        "clusters": OUTPUTS_DIR / "ngrams" / f"{politician_name}_combined_word_clusters.csv",
        "chart": OUTPUTS_DIR / "charts" / f"{politician_name}_combined_top_words.png",
        "wordcloud": OUTPUTS_DIR / "charts" / f"{politician_name}_combined_wordcloud.svg",
    }


def all_candidates_output_paths() -> dict[str, Path]:
    return {
        "extracted": EXTRACTED_DIR / "all_candidates" / "all_candidates_combined_extracted.txt",
        "cleaned": CLEANED_DIR / "all_candidates" / "all_candidates_combined_cleaned.txt",
        "words": OUTPUTS_DIR / "frequencies" / "all_candidates_combined_top_words.csv",
        "identity": OUTPUTS_DIR / "frequencies" / "all_candidates_combined_identity_counts.csv",
        "bigrams": OUTPUTS_DIR / "ngrams" / "all_candidates_combined_top_bigrams.csv",
        "trigrams": OUTPUTS_DIR / "ngrams" / "all_candidates_combined_top_trigrams.csv",
        "clusters": OUTPUTS_DIR / "ngrams" / "all_candidates_combined_word_clusters.csv",
        "chart": OUTPUTS_DIR / "charts" / "all_candidates_combined_top_words.png",
        "wordcloud": OUTPUTS_DIR / "charts" / "all_candidates_combined_wordcloud.svg",
        "summary": OUTPUTS_DIR / "all_candidates_summary.csv",
    }


def candidate_comparison_output_path() -> Path:
    return OUTPUTS_DIR / "candidate_comparison.csv"


def configured_input_files(politician_name: str) -> list[Path]:
    """Return either one configured file or all raw files for the politician."""
    if not ANALYZE_ALL_RAW_FILES_FOR_POLITICIAN:
        return [INPUT_FILE]

    raw_dir = BASE_DIR / "raw" / politician_name
    return sorted(raw_dir.glob("*.txt"))


def analyze_file(
    input_file: Path,
    target_speaker: str,
    known_speaker_labels: set[str] | None = None,
) -> dict[str, object]:
    transcript = read_transcript(input_file)
    turns = parse_speaker_turns(transcript, target_speaker, known_speaker_labels)
    target_turn_count = sum(1 for speaker, _ in turns if speaker.strip() == target_speaker)
    if turns:
        extracted_text = extract_target_speaker(turns, target_speaker)
    else:
        # Some raw files are already politician-only speeches with no speaker
        # label. Because files are organized by politician, treat the whole file
        # as target speech only when no speaker labels are detected at all.
        extracted_text = transcript.strip()
        target_turn_count = 1 if extracted_text else 0
    cleaned_text = clean_turkish_text(extracted_text)
    tokens = tokenize(cleaned_text)
    analysis_tokens = exclude_function_words(tokens)

    return {
        "input_file": input_file,
        "turn_count": len(turns),
        "target_turn_count": target_turn_count,
        "extracted_text": extracted_text,
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "analysis_tokens": analysis_tokens,
    }


def save_analysis_outputs(
    paths: dict[str, Path],
    extracted_text: str,
    cleaned_text: str,
    tokens: list[str],
    analysis_tokens: list[str],
    wordcloud_title: str | None = None,
    wordcloud_color: str = "#374151",
    wordcloud_word_colors: dict[str, str] | None = None,
    wordcloud_legend: list[tuple[str, str]] | None = None,
    wordcloud_counter: Counter | None = None,
) -> bool:
    for key, path in paths.items():
        if key == "summary":
            continue
        path.parent.mkdir(parents=True, exist_ok=True)

    paths["extracted"].write_text(extracted_text, encoding="utf-8")
    paths["cleaned"].write_text(cleaned_text, encoding="utf-8")

    word_counts = calculate_word_frequencies(analysis_tokens)
    bigram_counts = calculate_ngrams(analysis_tokens, 2)
    trigram_counts = calculate_ngrams(analysis_tokens, 3)
    clusters = calculate_following_word_clusters(tokens, CLUSTER_ANCHORS)

    save_counter_csv(word_counts, paths["words"], 50, ["word", "count"])
    save_counter_csv(bigram_counts, paths["bigrams"], 20, ["bigram", "count"])
    save_counter_csv(trigram_counts, paths["trigrams"], 20, ["trigram", "count"])
    save_word_clusters(clusters, paths["clusters"])
    save_identity_counts(tokens, paths["identity"])
    save_word_cloud_svg(
        wordcloud_counter or word_counts,
        paths["wordcloud"],
        title=wordcloud_title,
        default_color=wordcloud_color,
        word_colors=wordcloud_word_colors,
        legend_items=wordcloud_legend,
    )
    return save_frequency_chart(word_counts, paths["chart"])


def run_analysis(
    input_file: Path,
    target_speaker: str,
    politician_name: str,
    known_speaker_labels: set[str] | None = None,
) -> None:
    paths = output_paths(politician_name, input_file)
    analysis = analyze_file(input_file, target_speaker, known_speaker_labels)
    chart_created = save_analysis_outputs(
        paths=paths,
        extracted_text=analysis["extracted_text"],
        cleaned_text=analysis["cleaned_text"],
        tokens=analysis["tokens"],
        analysis_tokens=analysis["analysis_tokens"],
        wordcloud_title=f"{politician_name} | {input_file.stem}",
        wordcloud_color=CANDIDATE_COLORS.get(politician_name, "#374151"),
        wordcloud_legend=[
            (
                CANDIDATE_DISPLAY_NAMES.get(politician_name, politician_name),
                CANDIDATE_COLORS.get(politician_name, "#374151"),
            )
        ],
    )

    print(f"Analyzed: {input_file}")
    print(f"Parsed turns: {analysis['turn_count']}")
    print(f"Target speaker turns: {analysis['target_turn_count']}")
    print(f"Extracted turns: {paths['extracted']}")
    print(f"Cleaned text: {paths['cleaned']}")
    print(f"Top word frequencies: {paths['words']}")
    print(f"Identity counts: {paths['identity']}")
    print(f"Top bigrams: {paths['bigrams']}")
    print(f"Top trigrams: {paths['trigrams']}")
    print(f"Word clusters: {paths['clusters']}")
    print(f"Word cloud: {paths['wordcloud']}")
    if chart_created:
        print(f"Chart: {paths['chart']}")


def run_combined_analysis(
    input_files: list[Path],
    target_speaker: str,
    politician_name: str,
    known_speaker_labels: set[str] | None = None,
) -> None:
    analyses = [
        analyze_file(input_file, target_speaker, known_speaker_labels)
        for input_file in input_files
    ]

    extracted_parts = [
        f"===== {analysis['input_file']} =====\n{analysis['extracted_text']}"
        for analysis in analyses
        if analysis["extracted_text"]
    ]
    cleaned_parts = [
        f"===== {analysis['input_file']} =====\n{analysis['cleaned_text']}"
        for analysis in analyses
        if analysis["cleaned_text"]
    ]
    combined_tokens = [
        token
        for analysis in analyses
        for token in analysis["tokens"]
    ]
    combined_analysis_tokens = [
        token
        for analysis in analyses
        for token in analysis["analysis_tokens"]
    ]

    paths = combined_output_paths(politician_name)
    chart_created = save_analysis_outputs(
        paths=paths,
        extracted_text="\n\n".join(extracted_parts),
        cleaned_text="\n\n".join(cleaned_parts),
        tokens=combined_tokens,
        analysis_tokens=combined_analysis_tokens,
        wordcloud_title=f"{CANDIDATE_DISPLAY_NAMES.get(politician_name, politician_name)} combined",
        wordcloud_color=CANDIDATE_COLORS.get(politician_name, "#374151"),
        wordcloud_legend=[
            (
                CANDIDATE_DISPLAY_NAMES.get(politician_name, politician_name),
                CANDIDATE_COLORS.get(politician_name, "#374151"),
            )
        ],
    )

    print(f"Combined analysis: {politician_name}")
    print(f"Files combined: {len(input_files)}")
    print(f"Parsed turns: {sum(int(analysis['turn_count']) for analysis in analyses)}")
    print(f"Target speaker turns: {sum(int(analysis['target_turn_count']) for analysis in analyses)}")
    print(f"Extracted combined text: {paths['extracted']}")
    print(f"Cleaned combined text: {paths['cleaned']}")
    print(f"Combined top word frequencies: {paths['words']}")
    print(f"Combined identity counts: {paths['identity']}")
    print(f"Combined top bigrams: {paths['bigrams']}")
    print(f"Combined top trigrams: {paths['trigrams']}")
    print(f"Combined word clusters: {paths['clusters']}")
    print(f"Combined word cloud: {paths['wordcloud']}")
    if chart_created:
        print(f"Combined chart: {paths['chart']}")


def run_all_candidates_analysis(
    politician_configs: list[dict[str, str]],
    known_speaker_labels: set[str] | None = None,
) -> None:
    all_analyses: list[dict[str, object]] = []

    for config in politician_configs:
        politician_name = config["politician_name"]
        target_speaker = config["target_speaker_label"]
        for input_file in configured_input_files(politician_name):
            analysis = analyze_file(input_file, target_speaker, known_speaker_labels)
            analysis["politician_name"] = politician_name
            all_analyses.append(analysis)

    if not all_analyses:
        print("No candidate files found for all-candidates combined analysis.")
        return

    extracted_parts = [
        (
            f"===== {analysis['politician_name']} | {analysis['input_file']} =====\n"
            f"{analysis['extracted_text']}"
        )
        for analysis in all_analyses
        if analysis["extracted_text"]
    ]
    cleaned_parts = [
        (
            f"===== {analysis['politician_name']} | {analysis['input_file']} =====\n"
            f"{analysis['cleaned_text']}"
        )
        for analysis in all_analyses
        if analysis["cleaned_text"]
    ]
    combined_tokens = [
        token
        for analysis in all_analyses
        for token in analysis["tokens"]
    ]
    combined_analysis_tokens = [
        token
        for analysis in all_analyses
        for token in analysis["analysis_tokens"]
    ]
    candidate_word_counts = {
        config["politician_name"]: Counter(
            token
            for analysis in all_analyses
            if analysis["politician_name"] == config["politician_name"]
            for token in analysis["analysis_tokens"]
        )
        for config in politician_configs
    }
    all_word_counts = Counter(combined_analysis_tokens)
    balanced_wordcloud_counts: Counter = Counter()
    for politician, counts in candidate_word_counts.items():
        for word, count in counts.most_common(38):
            balanced_wordcloud_counts[word] = max(balanced_wordcloud_counts[word], count)

    word_colors = {}
    for word in balanced_wordcloud_counts:
        owner = max(
            candidate_word_counts,
            key=lambda politician: candidate_word_counts[politician][word],
        )
        word_colors[word] = CANDIDATE_COLORS.get(owner, "#374151")
    legend = [
        (
            CANDIDATE_DISPLAY_NAMES.get(config["politician_name"], config["politician_name"]),
            CANDIDATE_COLORS.get(config["politician_name"], "#374151"),
        )
        for config in politician_configs
    ]

    paths = all_candidates_output_paths()
    chart_created = save_analysis_outputs(
        paths=paths,
        extracted_text="\n\n".join(extracted_parts),
        cleaned_text="\n\n".join(cleaned_parts),
        tokens=combined_tokens,
        analysis_tokens=combined_analysis_tokens,
        wordcloud_title="all candidates",
        wordcloud_word_colors=word_colors,
        wordcloud_legend=legend,
        wordcloud_counter=balanced_wordcloud_counts,
    )

    summary_rows = [
        (
            analysis["politician_name"],
            str(analysis["input_file"]),
            analysis["turn_count"],
            analysis["target_turn_count"],
            len(analysis["tokens"]),
            len(analysis["analysis_tokens"]),
        )
        for analysis in all_analyses
    ]
    write_csv(
        summary_rows,
        paths["summary"],
        [
            "politician",
            "input_file",
            "parsed_turns",
            "target_turns",
            "cleaned_tokens",
            "analysis_tokens",
        ],
    )

    print("All-candidates combined analysis")
    print(f"Files combined: {len(all_analyses)}")
    print(f"Parsed turns: {sum(int(analysis['turn_count']) for analysis in all_analyses)}")
    print(f"Target speaker turns: {sum(int(analysis['target_turn_count']) for analysis in all_analyses)}")
    print(f"Combined extracted text: {paths['extracted']}")
    print(f"Combined cleaned text: {paths['cleaned']}")
    print(f"Combined top word frequencies: {paths['words']}")
    print(f"Combined identity counts: {paths['identity']}")
    print(f"Combined top bigrams: {paths['bigrams']}")
    print(f"Combined top trigrams: {paths['trigrams']}")
    print(f"Combined word clusters: {paths['clusters']}")
    print(f"Combined word cloud: {paths['wordcloud']}")
    print(f"Candidate/file summary: {paths['summary']}")
    if chart_created:
        print(f"Combined chart: {paths['chart']}")


def run_candidate_comparison(
    politician_configs: list[dict[str, str]],
    known_speaker_labels: set[str] | None = None,
) -> None:
    """Create a candidate-level comparison table.

    Counts are raw counts from the cleaned politician-only corpus. Rates are
    normalized per 1,000 cleaned tokens, which makes comparisons fairer when
    candidates have different amounts of transcript data.
    """
    rows = []
    columns = [
        "candidate",
        "files",
        "parsed_turns",
        "target_turns",
        "cleaned_tokens",
        "analysis_tokens",
        "top_10_analysis_words",
    ]

    for term in CANDIDATE_COMPARISON_TERMS:
        columns.extend([term, f"{term}_per_1000"])
    columns.extend(["millet_plus_milletimiz", "millet_plus_milletimiz_per_1000"])

    for config in politician_configs:
        politician_name = config["politician_name"]
        target_speaker = config["target_speaker_label"]
        input_files = configured_input_files(politician_name)
        analyses = [
            analyze_file(input_file, target_speaker, known_speaker_labels)
            for input_file in input_files
        ]
        tokens = [
            token
            for analysis in analyses
            for token in analysis["tokens"]
        ]
        analysis_tokens = [
            token
            for analysis in analyses
            for token in analysis["analysis_tokens"]
        ]
        token_counts = Counter(tokens)
        top_words = "; ".join(
            f"{word}:{count}"
            for word, count in Counter(analysis_tokens).most_common(10)
        )
        cleaned_total = len(tokens)

        row = [
            CANDIDATE_DISPLAY_NAMES.get(politician_name, politician_name),
            len(input_files),
            sum(int(analysis["turn_count"]) for analysis in analyses),
            sum(int(analysis["target_turn_count"]) for analysis in analyses),
            cleaned_total,
            len(analysis_tokens),
            top_words,
        ]

        for term in CANDIDATE_COMPARISON_TERMS:
            count = token_counts[term]
            rate = round((count / cleaned_total) * 1000, 2) if cleaned_total else 0
            row.extend([count, rate])

        millet_combined = token_counts["millet"] + token_counts["milletimiz"]
        millet_combined_rate = (
            round((millet_combined / cleaned_total) * 1000, 2)
            if cleaned_total
            else 0
        )
        row.extend([millet_combined, millet_combined_rate])
        rows.append(tuple(row))

    output_file = candidate_comparison_output_path()
    write_csv(rows, output_file, columns)
    print(f"Candidate comparison table: {output_file}")


if __name__ == "__main__":
    for config in POLITICIAN_CONFIGS:
        politician_name = config["politician_name"]
        target_speaker_label = config["target_speaker_label"]
        input_files = configured_input_files(politician_name)
        if not input_files:
            print(f"No input files found for {politician_name}; skipping.")
            print()
            continue

        print(f"===== Running {politician_name} corpus =====")
        for input_file in input_files:
            if not input_file.exists():
                raise FileNotFoundError(
                    f"Input file not found: {input_file}\n"
                    "Update INPUT_FILE in the config section or place a transcript at that path."
                )

            run_analysis(
                input_file=input_file,
                target_speaker=target_speaker_label,
                politician_name=politician_name,
                known_speaker_labels=KNOWN_SPEAKER_LABELS,
            )
            print()

        if len(input_files) > 1:
            run_combined_analysis(
                input_files=input_files,
                target_speaker=target_speaker_label,
                politician_name=politician_name,
                known_speaker_labels=KNOWN_SPEAKER_LABELS,
            )
            print()

    print("===== Running all candidates combined corpus =====")
    run_all_candidates_analysis(
        politician_configs=POLITICIAN_CONFIGS,
        known_speaker_labels=KNOWN_SPEAKER_LABELS,
    )
    print()
    print("===== Running candidate comparison table =====")
    run_candidate_comparison(
        politician_configs=POLITICIAN_CONFIGS,
        known_speaker_labels=KNOWN_SPEAKER_LABELS,
    )
