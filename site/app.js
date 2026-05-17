const data = window.ADAY_SOZLUGU_DATA;

const copy = {
  tr: {
    "nav.dictionary": "sözlük",
    "nav.identity": "kimlik",
    "nav.clusters": "kümeler",
    "nav.data": "veri",
    "nav.method": "yöntem",
    "hero.kicker": "türkçe siyasi söylem analizi",
    "hero.title": "aday sözlüğü",
    "hero.byline": "ali, codex ile",
    "hero.network": "kelime ağı",
    "stats.files": "dosya",
    "stats.turns": "aday konuşması",
    "stats.tokens": "temiz token",
    "corpus.eyebrow": "corpus",
    "corpus.title": "önce aynı ölçekte okuyalım.",
    "corpus.body":
      "her aday için sadece hedef konuşmacı blokları analiz edildi. moderatör, gazeteci ve soru metinleri dışarıda bırakıldı; oranlar farklı metin hacimlerini karşılaştırmak için 1.000 temiz token başına hesaplandı.",
    "corpus.insight.title": "corpus dengesi bulguları sınırlar.",
    "corpus.insight.body":
      "oğan ve kılıçdaroğlu için hedef konuşma bloğu sayısı erdoğan’dan daha yüksek. bu yüzden yorumlarda ham sayılardan çok 1.000 token başına oranlara ve tekrarlayan ifade kalıplarına bakmak gerekir.",
    "act.label": "act i",
    "act.title": "kelimeler, kimlikler, kümeler",
    "act.one": "hangi kelimeler adaylara yapışıyor?",
    "act.two": "“biz” ve “ben” ne kadar merkezde?",
    "act.three": "bir çapa kelimeden sonra hangi ifadeler geliyor?",
    "findings.eyebrow": "bulgular",
    "findings.title": "bu veri ne söylüyor?",
    "findings.erdogan.title": "erdoğan: kolektif ve karşıtlık kuran dil",
    "findings.erdogan.body":
      "erdoğan’da “biz” oranı yüksek, “terör” ve “bay kemal / bay bay” gibi karşıtlık kuran ifadeler öne çıkıyor. bu dil, seçmeni ortak bir “biz” içinde toplarken rakibi isimlendiren ve çatışma hattı kuran bir retoriğe yaslanıyor.",
    "findings.ogan.title": "oğan: milliyetçi ve aday-merkezli dil",
    "findings.ogan.body":
      "oğan’da “türk” açık ara en ayırt edici kimlik terimi. aynı zamanda “ben” oranı en yüksek aday; “sinan oğan”, “türk milliyetçisi”, “ata ittifakı” gibi ifadeler söylemi hem kişisel pozisyona hem de milliyetçi kimliğe bağlıyor.",
    "findings.kilicdaroglu.title": "kılıçdaroğlu: kurumlar, parti ve açıklama dili",
    "findings.kilicdaroglu.body":
      "kılıçdaroğlu’nda “parti”, “genel başkan”, “cumhuriyet halk / halk partisi” ve “ifade edeyim” gibi kalıplar daha görünür. “biz” güçlü kalsa da dil, hareket ve kurum üzerinden açıklama yapmaya daha yakın duruyor.",
    "findings.note":
      "not: bu sonuçlar mevcut transcript örneklerine dayanır; corpus büyüdükçe oranlar ve öne çıkan kümeler değişebilir.",
    "frequency.eyebrow": "sıklık",
    "frequency.title": "kimin sözlüğünde hangi kelime öne çıkıyor?",
    "frequency.body":
      "aday seçerek en sık geçen kelimelerin dağılımını inceleyin. işlev kelimeleri ve sayı tokenları çıkarıldı; zamirler özellikle korunuyor.",
    "frequency.limit": "ilk 24 kelime",
    "frequency.insight.title": "sıklıklar üç farklı odak gösteriyor.",
    "frequency.insight.body":
      "erdoğan’ın listesinde “biz”, “bizim”, “türkiye”, “terör” ve “bay” birlik ve karşıtlık eksenini kuruyor. oğan’da “ben”, “türk”, “sayın”, “türkiye” ve “ittifakı” adayın kendisini milliyetçi pazarlık alanına yerleştiriyor. kılıçdaroğlu’nda “biz”, “parti”, “lazım”, “zaman” ve “genel” daha açıklayıcı ve örgütsel bir tona işaret ediyor.",
    "identity.eyebrow": "kimlik dili",
    "identity.title": "“biz”, “ben”, “türkiye” ve diğer işaretler.",
    "identity.body":
      "bu bölüm seçili terimlerde adayların 1.000 token başına kullanımını gösterir. mutlak sayılar yerine oranlara bakmak küçük ve büyük corpus farklarını dengeler.",
    "identity.insight.title": "zamirler ideolojik pozisyonu değil, hitap biçimini gösteriyor.",
    "identity.insight.body":
      "“biz” erdoğan ve kılıçdaroğlu’nda en güçlü kolektif işaretlerden biri. oğan ise “ben” ve “türk” oranlarında ayrışıyor; bu, söylemin hem kişisel konuma hem de milliyetçi kimliğe daha fazla yaslandığını düşündürüyor. “terör” erdoğan ve kılıçdaroğlu’nda görünürken oğan’da daha düşük kalıyor.",
    "clusters.eyebrow": "kelime kümeleri",
    "clusters.title": "bir kelimenin hemen ardından ne geliyor?",
    "clusters.body":
      "“biz x”, “ben x”, “türkiye x”, “millet x” gibi yakın takip örüntüleri, söylemin özne kurma biçimini daha görünür hale getirir.",
    "clusters.anchor": "çapa kelime",
    "clusters.byColor": "aday rengine göre",
    "clusters.insight.title": "kümeler tek kelimeden daha açıklayıcı.",
    "clusters.insight.body":
      "“biz yaptık / biz varız” erdoğan’da icraat ve varlık iddiası kuruyor. oğan’ın “ben türk” ve “türk milliyetçisi” çevresi kimlik ilanı gibi çalışıyor. kılıçdaroğlu’nda “ben adayım”, “biz üretmiyoruz” ve “biz yönetiyoruz” türü kümeler eleştiri ile yönetme iddiasını yan yana getiriyor.",
    "phrases.eyebrow": "ifadeler",
    "phrases.title": "en sık iki ve üçlü ifadeler",
    "phrases.note": "* “bay bay” ifadesi “bye-bye” ses oyunuyla kullanılıyor.",
    "phrases.insight.title": "kalıp ifadeler siyasal rolü görünür kılıyor.",
    "phrases.insight.body":
      "erdoğan’ın kalıplarında rakip isimlendirme ve sloganlaşma belirgin. oğan’ın kalıpları aday adları, ittifaklar ve milliyetçi kimlik etrafında yoğunlaşıyor. kılıçdaroğlu’nun kalıpları parti kurumu, açıklama dili ve politika kapasitesi etrafında toplanıyor.",
    "conclusion.eyebrow": "sonuç",
    "conclusion.title": "aynı seçim, üç farklı özne kurma biçimi.",
    "conclusion.body":
      "bu örneklemde erdoğan söylemi ortak “biz” ve karşıtlık çizgisiyle, oğan söylemi milliyetçi kimlik ve kişisel adaylık konumuyla, kılıçdaroğlu söylemi ise kurum, parti ve açıklama diliyle öne çıkıyor. bu farklar tek başına ideoloji kanıtı değil; ancak politik hizalanmanın konuşma içinde hangi özne, hangi rakip ve hangi kolektif etrafında kurulduğunu gösteren izler sunuyor.",
    "raw.eyebrow": "ham veri",
    "raw.title": "transcript dosyaları",
    "raw.body":
      "analizde kullanılan ham transcript dosyaları aşağıda. site kopyaları doğrudan açılabilir; yöntem kısmında anlatıldığı gibi analiz yalnızca hedef aday bloklarını kullanır.",
    "method.eyebrow": "yöntem notu",
    "method.title": "ne ölçüldü?",
    "method.one": "konuşmacı etiketi satırları yakalandı ve yalnızca hedef aday blokları çıkarıldı.",
    "method.two":
      "türkçe karakterler korundu; apostrof ve seçili siyasi terim varyantları normalize edildi.",
    "method.three": "“ve”, “da”, “de”, “ama” gibi işlev kelimeleri çıkarıldı; zamirler çıkarılmadı.",
    "method.four": "“cumhurbaşkanı” ile “cumhurbaşkanlığı” otomatik birleştirilmedi.",
    files: "dosya",
    targetTurns: "hedef konuşma bloğu",
    cleanedTokens: "temiz token",
    analysisTokens: "analiz tokenı",
    topWords: "en sık kelimeler",
    noCluster: "bu çapa için kayıt yok.",
    clusterSuffix: "kümeleri",
    times: "kez",
  },
  en: {
    "nav.dictionary": "dictionary",
    "nav.identity": "identity",
    "nav.clusters": "clusters",
    "nav.data": "data",
    "nav.method": "method",
    "hero.kicker": "turkish political discourse analysis",
    "hero.title": "candidate lexicon",
    "hero.byline": "by ali, with codex",
    "hero.network": "word network",
    "stats.files": "files",
    "stats.turns": "candidate turns",
    "stats.tokens": "clean tokens",
    "corpus.eyebrow": "corpus",
    "corpus.title": "read everything on the same scale.",
    "corpus.body":
      "only target speaker blocks were analyzed for each candidate. moderator, journalist, and question text were excluded; rates are calculated per 1,000 clean tokens to compare uneven transcript volume.",
    "corpus.insight.title": "corpus balance limits the findings.",
    "corpus.insight.body":
      "oğan and kılıçdaroğlu have more target speaker turns than erdoğan in this sample. for that reason, the interpretation should lean on per-1,000-token rates and repeated phrase patterns rather than raw counts alone.",
    "act.label": "act i",
    "act.title": "words, identities, clusters",
    "act.one": "which words stick to each candidate?",
    "act.two": "how central are “biz” and “ben”?",
    "act.three": "what follows an anchor word?",
    "findings.eyebrow": "findings",
    "findings.title": "what does the data suggest?",
    "findings.erdogan.title": "erdoğan: collective and adversarial language",
    "findings.erdogan.body":
      "erdoğan has a high rate of “biz” and foregrounds adversarial phrases such as “terör” and “bay kemal / bay bay.” the pattern builds a shared “we” while naming opponents and drawing conflict lines.",
    "findings.ogan.title": "oğan: nationalist and candidate-centered language",
    "findings.ogan.body":
      "oğan’s most distinctive identity term is “türk.” he also has the highest rate of “ben”; phrases such as “sinan oğan,” “türk milliyetçisi,” and “ata ittifakı” tie the discourse to personal positioning and nationalist identity.",
    "findings.kilicdaroglu.title": "kılıçdaroğlu: institutional and explanatory language",
    "findings.kilicdaroglu.body":
      "kılıçdaroğlu more visibly uses institutional and party language: “parti,” “genel başkan,” “cumhuriyet halk / halk partisi,” and “ifade edeyim.” “biz” remains strong, but the register leans toward explanation through movement and institution.",
    "findings.note":
      "note: these findings are based on the current transcript sample; rates and clusters may shift as the corpus grows.",
    "frequency.eyebrow": "frequency",
    "frequency.title": "which words stand out for each candidate?",
    "frequency.body":
      "select a candidate to inspect the most frequent words. function words and number-only tokens are removed; pronouns are kept.",
    "frequency.limit": "top 24 words",
    "frequency.insight.title": "frequency points to three different centers of gravity.",
    "frequency.insight.body":
      "erdoğan’s list combines “biz,” “bizim,” “türkiye,” “terör,” and “bay,” building a field of unity and opposition. oğan’s “ben,” “türk,” “sayın,” “türkiye,” and “ittifakı” place him in a nationalist bargaining space. kılıçdaroğlu’s “biz,” “parti,” “lazım,” “zaman,” and “genel” point toward a more explanatory and organizational register.",
    "identity.eyebrow": "identity language",
    "identity.title": "“we”, “i”, “turkey”, and other markers.",
    "identity.body":
      "this section shows selected terms per 1,000 tokens. rates make small and large corpora easier to compare.",
    "identity.insight.title": "pronouns show address, not ideology by themselves.",
    "identity.insight.body":
      "“biz” is a strong collective marker for erdoğan and kılıçdaroğlu. oğan stands apart in the rates for “ben” and “türk,” suggesting a discourse more anchored in personal position and nationalist identity. “terör” is visible for erdoğan and kılıçdaroğlu but remains lower for oğan.",
    "clusters.eyebrow": "word clusters",
    "clusters.title": "what comes right after a word?",
    "clusters.body":
      "near-following patterns such as “biz x”, “ben x”, “türkiye x”, and “millet x” make subject-building in discourse easier to see.",
    "clusters.anchor": "anchor word",
    "clusters.byColor": "by candidate color",
    "clusters.insight.title": "clusters explain more than single words.",
    "clusters.insight.body":
      "“biz yaptık / biz varız” frames erdoğan’s “we” as achievement and presence. oğan’s “ben türk” and “türk milliyetçisi” environment works like an identity declaration. kılıçdaroğlu’s clusters such as “ben adayım,” “biz üretmiyoruz,” and “biz yönetiyoruz” place criticism and governing claims side by side.",
    "phrases.eyebrow": "phrases",
    "phrases.title": "most common two- and three-word phrases",
    "phrases.note": "* “bay bay” is used as a bye-bye wordplay.",
    "phrases.insight.title": "set phrases reveal political role.",
    "phrases.insight.body":
      "erdoğan’s phrases emphasize opponent naming and slogan-like repetition. oğan’s phrases concentrate around candidate names, alliances, and nationalist identity. kılıçdaroğlu’s phrases cluster around party institution, explanatory speech, and policy capacity.",
    "conclusion.eyebrow": "conclusion",
    "conclusion.title": "one election, three ways of building a political subject.",
    "conclusion.body":
      "in this sample, erdoğan’s discourse stands out through a shared “we” and conflict lines; oğan’s through nationalist identity and personal candidacy; kılıçdaroğlu’s through institution, party, and explanation. these patterns are not proof of ideology on their own, but they show how political alignment leaves traces in which subject, opponent, and collective each speaker builds.",
    "raw.eyebrow": "raw data",
    "raw.title": "transcript files",
    "raw.body":
      "the raw transcript files used in the analysis are linked below. these website copies open directly; as described in the method note, the analysis uses only the target candidate blocks.",
    "method.eyebrow": "method note",
    "method.title": "what was measured?",
    "method.one": "speaker-label lines were detected and only target candidate blocks were extracted.",
    "method.two": "turkish characters were preserved; apostrophes and selected political term variants were normalized.",
    "method.three": "function words such as “ve”, “da”, “de”, and “ama” were removed; pronouns were not removed.",
    "method.four": "“cumhurbaşkanı” and “cumhurbaşkanlığı” were not automatically merged.",
    files: "files",
    targetTurns: "target turns",
    cleanedTokens: "clean tokens",
    analysisTokens: "analysis tokens",
    topWords: "top words",
    noCluster: "no records for this anchor.",
    clusterSuffix: "clusters",
    times: "times",
  },
};

const gloss = {
  aday: "candidate", adayı: "candidate", adayım: "i am a candidate",
  ahlaki: "moral", ak: "ak", alana: "to the field", allah: "god",
  amerika: "america", anlamıyorum: "i do not understand", anneme: "to my mother",
  arkadaşlarımı: "my friends", asgari: "minimum", asla: "never", ata: "ata",
  ayağının: "of your foot", ayrı: "separate", açtık: "we opened", aşkına: "for the sake of",
  bakın: "look", bana: "to me", batı: "west", bay: "mr", başka: "other",
  başkan: "chair", başkanı: "president", bekir: "bekir", belediye: "municipality",
  ben: "i", benim: "my", beraber: "together", biliyor: "knows",
  biliyorsunuz: "you know", bilmez: "does not know", bin: "thousand", bireysel: "individual",
  birlikte: "together", biz: "we", bize: "to us", bizim: "our", bugün: "today",
  bugünkü: "today's", bunlara: "to these", buradan: "from here", buyuz: "this is us",
  büyük: "big", bırakma: "do not leave", ciddi: "serious", cumhur: "republic",
  cumhurbaşkanı: "president", cumhuriyet: "republic", cumhuriyeti: "republic",
  dedi: "said", demokrasiyi: "democracy", devam: "continue", devlet: "state",
  devletin: "of the state", değeri: "value", değil: "not", diyor: "says",
  diğer: "other", dolar: "dollar", dolayısıyla: "therefore", doğru: "correct",
  edeceğiz: "we will", ederim: "i would", edeyim: "let me say", ediyorum: "i say",
  elbette: "of course", emine: "emine", erdoğan: "erdoğan", evet: "yes",
  evime: "to my home", evimize: "to our home", gelince: "when it comes",
  genel: "general", gerekçe: "reason", gerçekten: "really", gittim: "i went",
  grup: "group", göreve: "to office", gün: "day", günü: "day", güçlü: "strong",
  haliç: "haliç", halk: "people", halkı: "people", hayır: "no", hdp: "hdp",
  hemen: "right away", hesap: "account", hiçbir: "none", ifade: "expression",
  ihraç: "expel", iki: "two", ikinci: "second", ilk: "first", ilkeler: "principles",
  imam: "imam", inanıyorum: "i believe", insanlar: "people", inşallah: "god willing",
  inşası: "construction", istanbul: "istanbul", istediğim: "what i want",
  istiyorum: "i want", ittifak: "alliance", ittifakı: "alliance", iyi: "good",
  içerisinde: "inside", iş: "work", kahraman: "hero", kaldırdık: "we removed",
  kalkıp: "getting up", karar: "decision", kardeşimizin: "of our sibling",
  kardeşlerimizin: "of our siblings", katma: "added", kazanıyoruz: "we are winning",
  kemal: "kemal", kendi: "own", kente: "to the city", kira: "rent", konusu: "matter",
  köyde: "in the village", kürt: "kurdish", kılıçdaroğlu: "kılıçdaroğlu",
  lazım: "needed", malum: "as known", manada: "in meaning", medya: "media",
  mesela: "for example", millet: "nation", milleti: "nation", milletime: "to my nation",
  milletimiz: "our nation", milletimizi: "our nation", milletinin: "of the nation",
  "millet + milletimiz": "nation + our nation", milliyetçileri: "nationalists",
  milliyetçisi: "nationalist", milyar: "billion", milyon: "million",
  muhalefete: "to the opposition", musunuz: "do you", mutabakat: "agreement",
  mümkün: "possible", nedir: "what is", olacak: "will be", olayım: "let me be",
  olur: "happens", onlar: "they", onlara: "to them", onları: "them", orayı: "there",
  ortak: "joint", oy: "vote", oğan: "oğan", parti: "party", partinin: "of the party",
  partisi: "party", pazar: "sunday", rahmet: "mercy", rakka: "raqqa", rusya: "russia",
  sadece: "only", sandıkta: "at the ballot box", saydım: "i counted", sayın: "mr",
  seninle: "with you", severiz: "we love", seçim: "election", seçtim: "i chose",
  sinan: "sinan", siyasal: "political", siyasetçiysem: "if i am a politician",
  siz: "you", size: "to you", sizin: "your", son: "last", soru: "question",
  sorumluluk: "responsibility", su: "water", söz: "word", tek: "single", terör: "terror",
  teşekkür: "thanks", tura: "round", türk: "turkish", türkiye: "turkey", var: "exists",
  varız: "we exist", vatandaşlarıma: "to my citizens", yapmıyorum: "i do not do",
  yaptık: "we did", yaşar: "yaşar", yeni: "new", yerel: "local", yetenek: "talent",
  yönetiyoruz: "we govern", yüksek: "high", yıllardır: "for years", zaman: "time",
  zamanında: "on time", çalışacağım: "i will work", çağrıda: "in a call",
  çocukluğum: "my childhood", önce: "before", önemli: "important",
  örgütleriyle: "with their organizations", örgütü: "organization",
  özdağ: "özdağ", özellikle: "especially", öğrenmeden: "without learning",
  üretmiyoruz: "we do not produce", ürün: "product", ımf: "imf", ısrar: "insistence",
  ığdırlıyım: "i am from iğdır", şafak: "şafak", şahsen: "personally", şen: "şen",
  genç: "youth", aile: "family", vatan: "homeland", bayrak: "flag",
  oluşturamazsınız: "you cannot build", sevilmez: "is not loved", meclisi: "assembly",
  yutmuyor: "does not buy it", mayasının: "of its essence", hakikaten: "truly",
  aklı: "mind", seçimini: "choice", ittifakından: "from the alliance",
  adamlığı: "statesmanship", adamları: "statesmen", adamı: "statesman",
  imkanlarıyla: "with its means", imkanları: "means", imkanıyla: "with its means",
  demek: "means", anlayışında: "in its understanding", gerçek: "real",
  kontrol: "control", ödeyecek: "will pay", terbiyesi: "discipline",
  yönetimi: "administration", hastanesi: "hospital", diyoruz: "we say",
  yönetmede: "in governing", beyle: "with mr", yaşasın: "long live",
  kapısında: "at the door", para: "money", president: "president",
};

const phraseGloss = {
  "biz yaptık": "we did",
  "biz varız": "we exist",
  "biz asla": "we never",
  "biz buyuz": "this is us",
  "biz seçim": "we / election",
  "biz türk": "we / turkish",
  "biz türkiye": "we / turkey",
  "biz hdp": "we / hdp",
  "biz asgari": "we / minimum",
  "biz ilk": "we / first",
  "biz evimize": "we / to our home",
  "biz bize": "we / to us",
  "biz sayın": "we / mr",
  "biz ilkeler": "we / principles",
  "biz milletimizi": "we / our nation",
  "biz diğer": "we / other",
  "biz üretmiyoruz": "we do not produce",
  "biz kendi": "we / our own",
  "biz onları": "we / them",
  "biz iyi": "we / good",
  "biz yönetiyoruz": "we govern",
  "biz demokrasiyi": "we / democracy",
  "biz gerçekten": "we / really",
  "biz kazanıyoruz": "we are winning",
  "biz su": "we / water",
  "ben şahsen": "i personally",
  "ben inanıyorum": "i believe",
  "ben türk": "i / turkish",
  "ben cumhurbaşkanı": "i / president",
  "ben adayım": "i am a candidate",
  "ben genel": "i / general",
  "ben size": "i / to you",
  "türkiye cumhuriyeti": "republic of turkey",
  "türkiye yüzyılı": "century of turkey",
  "türkiye ittifakı": "turkey alliance",
  "türkiye güçlü": "turkey strong",
  "türk milliyetçisi": "turkish nationalist",
  "cumhur ittifakı": "people's alliance",
  "ata ittifakı": "ata alliance",
  "ak parti": "ak party",
  "bay kemal": "mr kemal",
  "sinan oğan": "sinan oğan",
  "sayın erdoğan": "mr erdoğan",
  "sayın kılıçdaroğlu": "mr kılıçdaroğlu",
  "genel başkan": "chairperson",
  "cumhuriyet halk": "republican people's",
  "halk partisi": "people's party",
  "iyi parti": "good party",
  "doğru değil": "not correct",
  "millet ittifakı": "nation alliance",
  "millet tek": "nation / one",
  "millet ittifakından": "from the nation alliance",
  "millet özellikle": "nation / especially",
  "millet oluşturamazsınız": "you cannot build a nation",
  "millet sevilmez": "the nation is not loved",
  "millet meclisi": "national assembly",
  "millet yutmuyor": "the nation does not buy it",
  "millet mayasının": "of the nation's essence",
  "millet hakikaten": "nation / truly",
  "millet aklı": "national mind",
  "millet seçimini": "the nation's choice",
};

const state = {
  candidate: data.candidates[0].slug,
  identityTerm: "biz",
  anchor: "biz",
  lang: "tr",
};

const bySlug = new Map(data.candidates.map((candidate) => [candidate.slug, candidate]));
const revealedElements = new WeakSet();

function fmt(value) {
  return Number(value).toLocaleString(state.lang === "tr" ? "tr-TR" : "en-US");
}

function tr(key) {
  return copy[state.lang][key] ?? key;
}

function candidateName(candidate) {
  return candidate.label.toLocaleLowerCase("tr-TR");
}

function displayWord(word) {
  if (state.lang === "tr") return word;
  return gloss[word] ?? word;
}

function displayPhrase(phrase) {
  if (state.lang === "tr") return phrase;
  return phraseGloss[phrase] ?? phrase;
}

function translatedPhraseMarkup(phrase, translation) {
  if (state.lang === "tr") return `<span>${phrase}</span>`;
  const translated = translation || phraseGloss[phrase] || phrase;
  if (!translated || translated === phrase) return `<span>${phrase}</span>`;
  return `<span>${translated}<small>${phrase}</small></span>`;
}

function tokenMarkup(word, translation) {
  if (state.lang === "tr") return word;
  const translated = translation || gloss[word];
  if (!translated || translated === word) return word;
  return `${word}<small>${translated}</small>`;
}

function clusterMarkup(row) {
  return translatedPhraseMarkup(row.cluster, row.translation);
}

function renderStaticText() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = tr(element.dataset.i18n);
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === state.lang);
  });
}

function setCandidate(slug) {
  state.candidate = slug;
  renderCandidateTabs();
  renderWordField();
}

function renderMetricCards() {
  const wrap = document.querySelector("#metricCards");
  wrap.innerHTML = data.candidates
    .map(
      (candidate) => `
        <article class="metric-card" style="--candidate-color: ${candidate.color}">
          <h3><span class="dot"></span>${candidateName(candidate)}</h3>
          <div class="stat"><span>${tr("files")}</span><strong>${fmt(candidate.files)}</strong></div>
          <div class="stat"><span>${tr("targetTurns")}</span><strong>${fmt(candidate.targetTurns)}</strong></div>
          <div class="stat"><span>${tr("cleanedTokens")}</span><strong>${fmt(candidate.cleanedTokens)}</strong></div>
          <div class="stat"><span>${tr("analysisTokens")}</span><strong>${fmt(candidate.analysisTokens)}</strong></div>
        </article>
      `
    )
    .join("");
}

function renderCandidateTabs() {
  const tabs = document.querySelector("#candidateTabs");
  tabs.innerHTML = data.candidates
    .map(
      (candidate) => `
        <button class="${candidate.slug === state.candidate ? "active" : ""}"
          style="--candidate-color: ${candidate.color}"
          type="button"
          data-candidate="${candidate.slug}">
          <span class="dot"></span>${candidateName(candidate)}
        </button>
      `
    )
    .join("");

  tabs.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => setCandidate(button.dataset.candidate));
  });
}

function positions(count) {
  const layout = [
    [56, 46],
    [28, 22],
    [78, 20],
    [22, 54],
    [78, 55],
    [48, 76],
    [46, 16],
    [90, 36],
    [12, 38],
    [62, 25],
    [30, 82],
    [72, 82],
    [10, 72],
    [90, 72],
    [18, 12],
    [84, 10],
    [42, 56],
    [64, 62],
    [36, 36],
    [54, 91],
    [8, 88],
    [93, 88],
    [24, 68],
    [72, 40],
  ];
  return layout.slice(0, count);
}

function renderWords(container, words, candidate, maxWords = 24) {
  const chosen = words.slice(0, maxWords);
  const max = Math.max(...chosen.map((word) => Number(word.count)));
  if (window.matchMedia("(max-width: 560px)").matches) {
    container.classList.add("word-list");
    container.innerHTML = chosen
      .map(
        (word, index) => `
          <div class="word-list-row" style="--candidate-color: ${candidate.color}; --bar-width: ${(Number(word.count) / max) * 100}%; --row-delay: ${index * 34}ms">
            <span class="rank">${index + 1}</span>
            <span class="word">${word.word}</span>
            <span class="count">${word.count}</span>
          </div>
        `
      )
      .join("");
    return;
  }
  container.classList.remove("word-list");
  container.innerHTML = chosen
    .map((word, index) => {
      const [left, top] = positions(chosen.length)[index];
      const size = 18 + (Number(word.count) / max) * 46;
      const mobileSize = 15 + (Number(word.count) / max) * 23;
      return `
        <span class="floating-word"
          title="${word.word}: ${word.count}"
          style="--word-color: ${candidate.color}; --mobile-word-size: ${mobileSize}px; --word-delay: ${index * 32}ms; left: ${left}%; top: ${top}%; font-size: ${size}px;">
          ${tokenMarkup(word.word, word.translation)}
        </span>
      `;
    })
    .join("");
}

function renderHeroOrbit() {
  const words = [];
  data.candidates.forEach((candidate) => {
    candidate.topWords.slice(0, 7).forEach((word) => words.push({ ...word, candidate }));
  });
  const max = Math.max(...words.map((word) => Number(word.count)));
  const container = document.querySelector("#heroOrbit");
  container.innerHTML = words
    .slice(0, 21)
    .map((word, index) => {
      const [left, top] = positions(21)[index];
      const size = 17 + (Number(word.count) / max) * 43;
      return `
        <span class="floating-word"
          title="${candidateName(word.candidate)}: ${word.word} (${word.count})"
          style="--word-color: ${word.candidate.color}; --word-delay: ${index * 36}ms; left: ${left}%; top: ${top}%; font-size: ${size}px;">
          ${tokenMarkup(word.word, word.translation)}
        </span>
      `;
    })
    .join("");
}

function renderWordField() {
  const candidate = bySlug.get(state.candidate);
  document.querySelector("#wordsTitle").textContent = `${candidateName(candidate)}: ${tr("topWords")}`;
  const maxWords = window.matchMedia("(max-width: 560px)").matches ? 12 : 24;
  renderWords(document.querySelector("#wordField"), candidate.topWords, candidate, maxWords);
}

function renderIdentityButtons() {
  const wrap = document.querySelector("#identityButtons");
  wrap.innerHTML = data.identityTerms
    .map(
      (term) => `
        <button class="${term === state.identityTerm ? "active" : ""}" type="button" data-term="${term}">
          ${displayWord(term)}
        </button>
      `
    )
    .join("");

  wrap.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      state.identityTerm = button.dataset.term;
      renderIdentityButtons();
      renderIdentityChart();
    });
  });
}

function renderIdentityChart() {
  const rows = data.candidates.map((candidate) => ({
    candidate,
    value: candidate.identity[state.identityTerm]?.per1000 ?? 0,
    count: candidate.identity[state.identityTerm]?.count ?? 0,
  }));
  const max = Math.max(...rows.map((row) => row.value), 1);
  document.querySelector("#identityChart").innerHTML = rows
    .map(
      ({ candidate, value, count }) => `
        <div class="identity-row" style="--candidate-color: ${candidate.color}">
          <strong><span class="dot"></span>${candidateName(candidate)}</strong>
          <div class="bar-track" aria-label="${candidateName(candidate)} ${state.identityTerm}: ${value.toFixed(2)} per 1000, count ${count}">
            <div class="bar" style="width: ${(value / max) * 100}%"></div>
          </div>
          <span><strong>${value.toFixed(2)}</strong><small>${fmt(count)} ${tr("times")}</small></span>
        </div>
      `
    )
    .join("");
}

function availableAnchors() {
  const anchors = new Set();
  data.candidates.forEach((candidate) => {
    candidate.clusters.forEach((row) => anchors.add(row.anchor));
  });
  return [...anchors].sort((a, b) => a.localeCompare(b, "tr"));
}

function renderAnchorSelect() {
  const select = document.querySelector("#anchorSelect");
  select.innerHTML = availableAnchors()
    .map((anchor) => `<option value="${anchor}">${displayWord(anchor)} x</option>`)
    .join("");
  select.value = state.anchor;
  select.onchange = () => {
    state.anchor = select.value;
    renderClusters();
  };
}

function renderClusters() {
  document.querySelector("#clusterTitle").textContent = `"${displayWord(state.anchor)} ..." ${tr("clusterSuffix")}`;
  document.querySelector("#clusterGrid").innerHTML = data.candidates
    .map((candidate) => {
      const clusters = candidate.clusters
        .filter((row) => row.anchor === state.anchor)
        .slice(0, 10);
      return `
        <article class="cluster-card" style="--candidate-color: ${candidate.color}">
          <h3>${candidateName(candidate)}</h3>
          ${
            clusters.length
              ? clusters
                  .map(
                    (row) => `
                      <div class="cluster-item">
                        ${clusterMarkup(row)}
                        <span>${row.count}</span>
                      </div>
                    `
                  )
                  .join("")
              : `<p class="muted">${tr("noCluster")}</p>`
          }
        </article>
      `;
    })
    .join("");
}

function renderPhrases() {
  document.querySelector("#phraseColumns").innerHTML = data.candidates
    .map(
      (candidate) => `
        <article class="phrase-card" style="--candidate-color: ${candidate.color}">
          <h3><span class="dot"></span> ${candidateName(candidate)}</h3>
          ${candidate.bigrams
            .slice(0, 8)
            .map(
              (row) => `
                <div class="phrase-pill">
                  ${translatedPhraseMarkup(row.bigram, row.translation)}
                  <strong>${row.count}</strong>
                </div>
              `
            )
            .join("")}
        </article>
      `
    )
    .join("");
}

function initScrollReveals() {
  const elements = document.querySelectorAll(`
    .section,
    .act-card,
    .findings,
    .finding-grid article,
    .metrics,
    .metric-card,
    .story-block,
    .panel,
    .identity-tool,
    .section-insight,
    .phrases,
    .phrase-card,
    .conclusion,
    .raw-data,
    .raw-data-grid article,
    .method
  `);

  if (!("IntersectionObserver" in window)) {
    elements.forEach((element) => element.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );

  elements.forEach((element) => {
    if (revealedElements.has(element)) return;
    revealedElements.add(element);
    element.classList.add("reveal");
    observer.observe(element);
  });
}

function renderAll() {
  renderStaticText();
  renderMetricCards();
  renderCandidateTabs();
  renderHeroOrbit();
  renderWordField();
  renderIdentityButtons();
  renderIdentityChart();
  renderAnchorSelect();
  renderClusters();
  renderPhrases();
  initScrollReveals();
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => {
    state.lang = button.dataset.lang;
    renderAll();
  });
});

renderAll();
