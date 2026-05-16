from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).parent
OUTPUTS = ROOT / "corpus" / "outputs"
SITE = ROOT / "site"


CANDIDATES = {
    "Erdoğan": {
        "slug": "erdogan",
        "label": "Erdoğan",
        "color": "#f6b21a",
        "soft": "#fff0bd",
    },
    "Oğan": {
        "slug": "ogan",
        "label": "Oğan",
        "color": "#2f80d8",
        "soft": "#dcebff",
    },
    "Kılıçdaroğlu": {
        "slug": "kilicdaroglu",
        "label": "Kılıçdaroğlu",
        "color": "#e30613",
        "soft": "#ffd9dd",
    },
}


IDENTITY_TERMS = [
    "biz",
    "bizim",
    "ben",
    "benim",
    "onlar",
    "millet",
    "milletimiz",
    "halk",
    "devlet",
    "türkiye",
    "türk",
    "cumhur",
    "ittifak",
    "terör",
    "genç",
    "aile",
    "vatan",
    "bayrak",
]


GLOSS = {
    "biz": "we",
    "bizim": "our",
    "bize": "to us",
    "ben": "i",
    "benim": "my",
    "onlar": "they",
    "onlara": "to them",
    "onları": "them",
    "millet": "nation",
    "milleti": "nation",
    "milletimiz": "our nation",
    "milletimizi": "our nation",
    "milletinin": "of the nation",
    "milletine": "to the nation",
    "halk": "people",
    "devlet": "state",
    "devletin": "of the state",
    "türkiye": "turkey",
    "türkiyeyi": "turkey",
    "türk": "turkish",
    "cumhur": "republic",
    "cumhurbaşkanı": "president",
    "cumhuriyet": "republic",
    "cumhuriyeti": "republic",
    "ittifak": "alliance",
    "ittifakı": "alliance",
    "terör": "terror",
    "genç": "youth",
    "aile": "family",
    "vatan": "homeland",
    "bayrak": "flag",
    "bayrağı": "flag",
    "göç": "migration",
    "kamu": "public",
    "suç": "crime",
    "sandıkta": "at the ballot box",
    "ola": "may it be",
    "kendilerini": "themselves",
    "cumhurbaşkanlığı": "presidency",
    "kararını": "decision",
    "göreve": "to office",
    "kaldırdık": "we removed",
    "tek": "one",
    "diğer": "other",
    "var": "exists",
    "varız": "we exist",
    "değil": "not",
    "sayın": "honorable",
    "bay": "mr",
    "parti": "party",
    "partisi": "party",
    "zaman": "time",
    "lazım": "needed",
    "inşallah": "god willing",
    "kürt": "kurdish",
    "allah": "god",
    "devam": "continue",
    "istanbul": "istanbul",
    "özellikle": "especially",
    "seçim": "election",
    "önemli": "important",
    "kemal": "kemal",
    "güçlü": "strong",
    "rusya": "russia",
    "diyor": "says",
    "söz": "word",
    "aday": "candidate",
    "adayı": "candidate",
    "adayım": "i am a candidate",
    "başkan": "chair",
    "başkanı": "president",
    "genel": "general",
    "ak": "ak",
    "hdp": "hdp",
    "ata": "ata",
    "ikinci": "second",
    "tura": "round",
    "doğru": "correct",
    "ifade": "expression",
    "edeyim": "let me say",
    "yeni": "new",
    "şafak": "şafak",
    "milliyetçisi": "nationalist",
    "milliyetçileri": "nationalists",
    "milliyetçiliği": "nationalism",
    "milliyetçisiyim": "i am a nationalist",
    "biliyor": "knows",
    "musunuz": "do you",
    "profesörlerle": "with professors",
    "profesör": "professor",
    "siyaseti": "politics",
    "siyasetinde": "in politics",
    "siyasetinin": "of politics",
    "lirası": "lira",
    "milleti": "nation",
    "milliyetçilerini": "nationalists",
    "milliyetçilerinin": "of nationalists",
    "genci": "youth",
    "dünyasının": "of the world",
    "kesimleriyle": "with segments",
    "oluşturamazsınız": "you cannot build",
    "sevilmez": "is not loved",
    "meclisi": "assembly",
    "yutmuyor": "does not buy it",
    "mayasının": "of its essence",
    "hakikaten": "truly",
    "aklı": "mind",
    "seçimini": "choice",
    "ittifakından": "from the alliance",
    "adamlığı": "statesmanship",
    "adamları": "statesmen",
    "adamı": "statesman",
    "imkanlarıyla": "with its means",
    "imkanları": "means",
    "imkanıyla": "with its means",
    "demek": "means",
    "anlayışında": "in its understanding",
    "gerçek": "real",
    "kontrol": "control",
    "ödeyecek": "will pay",
    "terbiyesi": "discipline",
    "yönetimi": "administration",
    "hastanesi": "hospital",
    "diyoruz": "we say",
    "yönetmede": "in governing",
    "beyle": "with mr",
    "yaşasın": "long live",
    "kapısında": "at the door",
    "para": "money",
    "asla": "never",
    "buyuz": "this is us",
    "üretmiyoruz": "we do not produce",
    "kendi": "own",
    "iyi": "good",
    "yönetiyoruz": "we govern",
    "demokrasiyi": "democracy",
    "gerçekten": "really",
    "kazanıyoruz": "we are winning",
    "su": "water",
    "ilk": "first",
    "ilkeler": "principles",
    "asgari": "minimum",
    "evimize": "to our home",
    "savunma": "defense",
    "olacağız": "we will be",
    "olmayıp": "rather than being",
    "yaşatmam": "i will not keep alive",
    "pek": "very",
    "bedeli": "cost",
    "genelinde": "across",
    "son": "last",
    "ortak": "joint",
    "değer": "value",
    "yüzyılı": "century",
    "yüzyılını": "century",
    "yüzyılının": "of the century",
    "güvenliğinin": "of security",
    "önüne": "in front of",
    "büyük": "big",
    "üreten": "producing",
    "üretmesi": "production",
    "kökenli": "originating",
    "bitti": "ended",
    "kazanacak": "will win",
    "katma": "added",
    "özgürleşmiş": "liberated",
    "gerçeği": "reality",
    "süratle": "quickly",
    "bulunduğu": "where it is",
    "meselesi": "issue",
    "demiştim": "i had said",
    "olayıdır": "is the matter",
    "olayı": "matter",
    "ekseninden": "from the axis",
    "geleceğe": "to the future",
    "nüfusunun": "of the population",
    "teknoloji": "technology",
    "hakkari": "hakkari",
    "battı": "sank",
    "üzerinden": "through",
    "geleceğiyle": "with its future",
}


PHRASE_GLOSS = {
    "bay bay": "bye-bye*",
    "bay bay kemal": "bye-bye kemal*",
    "bırakma allah": "do not leave us, god",
    "müslümansız bırakma allah": "do not leave it without muslims, god",
    "yurdu müslümansız bırakma": "do not leave the homeland without muslims",
    "söz konusu": "in question",
    "söz konusu değil": "out of the question",
    "milyar dolar": "billion dollars",
    "biliyor musunuz": "do you know?",
    "biliyor musunuz ben": "do you know, i...",
    "ifade edeyim": "let me say",
    "yüksek yetenek": "high talent",
    "yeni şafak": "yeni şafak",
    "teşekkür ederim": "thank you",
    "teşekkür ediyorum": "thank you",
    "allah aşkına": "for god's sake",
    "allah rahmet": "god have mercy",
    "devam edeceğiz": "we will continue",
    "pazar günü": "sunday",
    "ciddi manada": "seriously",
    "konusu değil": "not the case",
    "mümkün değil": "not possible",
    "nedir bilmez": "does not know what it is",
    "ortak mutabakat": "joint agreement",
    "belediye başkanı": "mayor",
    "yetenek inşası": "talent building",
    "bana oy": "vote for me",
    "milyar milyon": "billions and millions",
    "katma değeri": "added value",
    "değeri yüksek": "high value",
    "yüksek ürün": "high-value product",
    "emine şen": "emine şen",
    "şen yaşar": "şen yaşar",
    "türk profesörlerle": "with turkish professors",
    "turkish profesörlerle": "with turkish professors",
    "türk bayrağı": "turkish flag",
    "türk milliyetçisi": "turkish nationalist",
    "türk milliyetçileri": "turkish nationalists",
    "türk milliyetçilerini": "turkish nationalists",
    "türk milliyetçilerinin": "of turkish nationalists",
    "türk milleti": "turkish nation",
    "türk milletinin": "of the turkish nation",
    "türk milletine": "to the turkish nation",
    "türk siyaseti": "turkish politics",
    "türk siyasetinde": "in turkish politics",
    "türk siyasetinin": "of turkish politics",
    "türk lirası": "turkish lira",
    "türk genci": "turkish youth",
    "türk dünyasının": "of the turkic world",
    "türk milliyetçisiyim": "i am a turkish nationalist",
    "türk milliyetçiliği": "turkish nationalism",
    "türkiye cumhuriyeti": "republic of turkey",
    "türkiye yüzyılı": "century of turkey",
    "türkiye yüzyılını": "the century of turkey",
    "türkiye yüzyılının": "of the century of turkey",
    "türkiye genelinde": "across turkey",
    "türkiye olacağız": "we will be turkey",
    "türkiye savunma": "turkey defense",
    "türkiye son": "turkey + last",
    "türkiye büyük": "turkey + big",
    "türkiye güçlü": "turkey + strong",
    "türkiye kökenli": "turkey-origin",
    "türkiye buradan": "turkey + from here",
    "türkiye bitti": "turkey ended",
    "türkiye üreten": "turkey producing",
    "türkiye kazanacak": "turkey will win",
    "türkiye göç": "turkey + migration",
    "türkiye kamu": "turkey + public",
    "türkiye suç": "turkey + crime",
    "türkiye türkiye": "turkey + turkey",
    "millet ittifakı": "nation alliance",
    "millet oluşturamazsınız": "you cannot build a nation",
    "millet sevilmez": "the nation is not loved",
    "millet meclisi": "national assembly",
    "millet yutmuyor": "the nation does not buy it",
    "millet hakikaten": "nation + truly",
    "millet aklı": "national mind",
    "millet seçimini": "the nation's choice",
    "millet tek": "nation + one",
    "millet özellikle": "nation + especially",
    "millet mayasının": "of the nation's essence",
    "milletimiz sandıkta": "our nation at the ballot box",
    "milletimiz ola": "may our nation be",
    "milletimiz kendilerini": "our nation + themselves",
    "milletimiz cumhurbaşkanlığı": "our nation + presidency",
    "milletimiz kararını": "our nation + decision",
    "milletimiz türkiye": "our nation + turkey",
    "milletimiz var": "our nation exists",
    "biz yaptık": "we did",
    "biz varız": "we exist",
    "biz asla": "we never",
    "biz buyuz": "this is us",
    "biz ımf": "we + imf",
    "biz seçim": "we + election",
    "biz haliç": "we + haliç",
    "biz göreve": "we + to office",
    "biz kaldırdık": "we removed",
    "biz tek": "we + one",
    "biz değil": "we + not",
    "biz açtık": "we opened",
    "biz severiz": "we love",
    "biz hdp": "we + hdp",
    "biz asgari": "we + minimum",
    "biz ilk": "we + first",
    "biz türkiye": "we + turkey",
    "biz evimize": "we + to our home",
    "biz türk": "we + turkish",
    "biz bize": "we + to us",
    "biz sayın": "we + honorable",
    "biz ilkeler": "we + principles",
    "biz milletimizi": "we + our nation",
    "biz diğer": "we + other",
    "biz üretmiyoruz": "we do not produce",
    "biz kendi": "we + own",
    "biz onları": "we + them",
    "biz iyi": "we + good",
    "biz yönetiyoruz": "we govern",
    "biz demokrasiyi": "we + democracy",
    "biz gerçekten": "we + really",
    "biz kazanıyoruz": "we are winning",
    "biz su": "we + water",
    "ben şahsen": "i personally",
    "ben inanıyorum": "i believe",
    "ben adayım": "i am a candidate",
    "ak parti": "ak party",
    "cumhur ittifakı": "people's alliance",
    "ata ittifakı": "ata alliance",
    "bay kemal": "mr kemal",
    "sayın erdoğan": "mr erdoğan",
    "sayın kılıçdaroğlu": "mr kılıçdaroğlu",
    "sinan oğan": "sinan oğan",
    "genel başkan": "chairperson",
    "cumhuriyet halk": "republican people's",
    "halk partisi": "people's party",
    "iyi parti": "good party",
    "doğru değil": "not correct",
}


def translate_phrase(text):
    text = str(text).strip()
    if not text:
        return ""
    lowered = text.lower()
    if lowered in PHRASE_GLOSS:
        return PHRASE_GLOSS[lowered]
    translated = [GLOSS.get(word, word) for word in lowered.split()]
    return " ".join(translated)


def translated_records(path, phrase_columns, limit=None):
    df = read_csv(path)
    if limit:
        df = df.head(limit)
    for column in phrase_columns:
        if column in df.columns:
            df["translation"] = df[column].apply(translate_phrase)
            break
    if "word" in df.columns:
        df["translation"] = df["word"].apply(translate_phrase)
    return df.to_dict(orient="records")


def read_csv(path):
    return pd.read_csv(path).fillna("")


def records(path, limit=None):
    df = read_csv(path)
    if limit:
        df = df.head(limit)
    return df.to_dict(orient="records")


def build():
    comparison = read_csv(OUTPUTS / "candidate_comparison.csv")
    corpus_files = read_csv(OUTPUTS / "all_candidates_summary.csv")

    candidates = []
    for _, row in comparison.iterrows():
        meta = CANDIDATES[row["candidate"]]
        slug = meta["slug"]

        identity = {
            term: {
                "count": int(row.get(term, 0) or 0),
                "per1000": float(row.get(f"{term}_per_1000", 0) or 0),
            }
            for term in IDENTITY_TERMS
            if term in comparison.columns
        }
        identity["millet + milletimiz"] = {
            "count": int(row.get("millet_plus_milletimiz", 0) or 0),
            "per1000": float(row.get("millet_plus_milletimiz_per_1000", 0) or 0),
        }

        candidates.append(
            {
                **meta,
                "files": int(row["files"]),
                "parsedTurns": int(row["parsed_turns"]),
                "targetTurns": int(row["target_turns"]),
                "cleanedTokens": int(row["cleaned_tokens"]),
                "analysisTokens": int(row["analysis_tokens"]),
                "topWordsSummary": row["top_10_analysis_words"],
                "identity": identity,
                "topWords": translated_records(
                    OUTPUTS / "frequencies" / f"{slug}_combined_top_words.csv",
                    ["word"],
                    40,
                ),
                "bigrams": translated_records(
                    OUTPUTS / "ngrams" / f"{slug}_combined_top_bigrams.csv",
                    ["bigram"],
                    20,
                ),
                "trigrams": translated_records(
                    OUTPUTS / "ngrams" / f"{slug}_combined_top_trigrams.csv",
                    ["trigram"],
                    20,
                ),
                "clusters": translated_records(
                    OUTPUTS / "ngrams" / f"{slug}_combined_word_clusters.csv",
                    ["cluster"],
                    120,
                ),
            }
        )

    payload = {
        "title": "aday sözlüğü",
        "updated": "2026-05-16",
        "candidates": candidates,
        "corpusFiles": corpus_files.to_dict(orient="records"),
        "identityTerms": IDENTITY_TERMS + ["millet + milletimiz"],
        "allCandidates": {
            "topWords": translated_records(
                OUTPUTS / "frequencies" / "all_candidates_combined_top_words.csv",
                ["word"],
                60,
            ),
            "bigrams": translated_records(
                OUTPUTS / "ngrams" / "all_candidates_combined_top_bigrams.csv",
                ["bigram"],
                30,
            ),
            "trigrams": translated_records(
                OUTPUTS / "ngrams" / "all_candidates_combined_top_trigrams.csv",
                ["trigram"],
                30,
            ),
        },
    }

    SITE.mkdir(exist_ok=True)
    data_js = "window.ADAY_SOZLUGU_DATA = "
    data_js += json.dumps(payload, ensure_ascii=False, indent=2)
    data_js += ";\n"
    (SITE / "data.js").write_text(data_js, encoding="utf-8")


if __name__ == "__main__":
    build()
