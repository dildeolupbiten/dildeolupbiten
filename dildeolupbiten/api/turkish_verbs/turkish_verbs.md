This API conjugates Turkish verbs based on the conjugation rules of Turkish. You can make various requests with different query parameters.

The parameters are based on the Turkish Verb model:

[code="python"]

class TurkishVerb(Verb):
    modalities = [
        "haber kipi",                # en: indicative                  it: indicativo
        "istek kipi",                # en: conjunctive                 it: congiuntivo
        "şart kipi",                 # en: conditional                 it: condizionale
        "gereklilik kipi",           # en: necessative                 it: necessativo
        "emir kipi",                 # en: imperative                  it: imperativo
        "mastar kipi",               # en: infinitive                  it: infinitivo
        "ortaç kipi",                # en: participle                  it: participio
        "ulaç kipi"                  # en: gerund                      it: gerundio
        "hikaye birleşik zaman",     # en: story compound tense        it: tempo composto storico
        "rivayet birleşik zaman",    # en: rumor compound tense        it: tempo composto rumoroso
        "şart birleşik zaman"        # en: conditional compound tense  it: tempo composto condizionale
    ]
    tenses = [
        "duyulan geçmiş zaman",      # en: dubitative past tense       it: tempo passato dubitativo
        "görülen geçmiş zaman",      # en: definitive past tense       it: tempo passato definitivo
        "şimdiki zaman",             # en: present progressive tense   it: tempo presente progressivo
        "geniş zaman",               # en: simple aorist tense         it: tempo aoristo semplice
        "gelecek zaman"              # en: future tense                it: tempo futuro
    ]
    subjects = [
        "ben",                       # en: i                           it: io
        "sen",                       # en: you                         it: tu
        "o",                         # en: he/she                      it: lui/lei
        "biz",                       # en: we                          it: noi
        "siz",                       # en: you                         it: voi
        "onlar"                      # en: they                        it: loro
    ]

[/code]

All Turkish verbs have aforementioned attributes. A TurkishVerb object has similar attributes with the following verb model:

[code="json"]

{
    "conjugations": {
        "haber kipi": {
            "duyulan geçmiş zaman": {
                "ben": "olmuşum",
                "sen": "olmuşsun",
                "o": "olmuş",
                "biz": "olmuşuz",
                "siz": "olmuşsunuz",
                "onlar": "olmuşlar"
            },
            "görülen geçmiş zaman": {
                "ben": "oldum",
                "sen": "oldun",
                "o": "oldu",
                "biz": "olduk",
                "siz": "oldunuz",
                "onlar": "oldular"
            },
            "şimdiki zaman": {
                "ben": "oluyorum",
                "sen": "oluyorsun",
                "o": "oluyor",
                "biz": "oluyoruz",
                "siz": "oluyorsunuz",
                "onlar": "oluyorlar"
            },
            "geniş zaman": {
                "ben": "olurum",
                "sen": "olursun",
                "o": "olur",
                "biz": "oluruz",
                "siz": "olursunuz",
                "onlar": "olurlar"
            },
            "gelecek zaman": {
                "ben": "olacağım",
                "sen": "olacaksın",
                "o": "olacak",
                "biz": "olacağız",
                "siz": "olacaksınız",
                "onlar": "olacaklar"
            }
        },
        "istek kipi": {
            "ben": "olayım",
            "sen": "olasın",
            "o": "ola",
            "biz": "olak",
            "siz": "olasınız",
            "onlar": "olalar"
        },
        "şart kipi": {
            "ben": "olsam",
            "sen": "olsan",
            "o": "olsa",
            "biz": "olsak",
            "siz": "olsanız",
            "onlar": "olsalar"
        },
        "gereklilik kipi": {
            "ben": "olmalıyım",
            "sen": "olmalısın",
            "o": "olmalı",
            "biz": "olmalıyız",
            "siz": "olmalısınız",
            "onlar": "olmalılar"
        },
        "emir kipi": {
            "ben": "-",
            "sen": "ol",
            "o": "olsun",
            "biz": "-",
            "siz": "olun",
            "onlar": "olsunlar"
        },
        "hikaye birleşik zaman": {
            "duyulan geçmiş zaman": {
                "ben": "olmuştum",
                "sen": "olmuştun",
                "o": "olmuştu",
                "biz": "olmuştuk",
                "siz": "olmuştunuz",
                "onlar": "olmuştular"
            },
            "görülen geçmiş zaman": {
                "ben": "olduydum",
                "sen": "olduydun",
                "o": "olduydu",
                "biz": "olduyduk",
                "siz": "olduydunuz",
                "onlar": "olduydular"
            },
            "şimdiki zaman": {
                "ben": "oluyordum",
                "sen": "oluyordun",
                "o": "oluyordu",
                "biz": "oluyorduk",
                "siz": "oluyordunuz",
                "onlar": "oluyordular"
            },
            "geniş zaman": {
                "ben": "olurdum",
                "sen": "olurdun",
                "o": "olurdu",
                "biz": "olurduk",
                "siz": "olurdunuz",
                "onlar": "olurdular"
            },
            "gelecek zaman": {
                "ben": "olacaktım",
                "sen": "olacaktın",
                "o": "olacaktı",
                "biz": "olacaktık",
                "siz": "olacaktınız",
                "onlar": "olacaktılar"
            },
            "istek kipi": {
                "ben": "olaydım",
                "sen": "olaydın",
                "o": "olaydı",
                "biz": "olaydık",
                "siz": "olaydınız",
                "onlar": "olaydılar"
            },
            "şart kipi": {
                "ben": "olsaydım",
                "sen": "olsaydın",
                "o": "olsaydı",
                "biz": "olsaydık",
                "siz": "olsaydınız",
                "onlar": "olsaydılar"
            },
            "gereklilik kipi": {
                "ben": "olmalıydım",
                "sen": "olmalıydın",
                "o": "olmalıydı",
                "biz": "olmalıydık",
                "siz": "olmalıydınız",
                "onlar": "olmalıydılar"
            }
        },
        "rivayet birleşik zaman": {
            "duyulan geçmiş zaman": {
                "ben": "olmuşmuşum",
                "sen": "olmuşmuşsun",
                "o": "olmuşmuş",
                "biz": "olmuşmuşuz",
                "siz": "olmuşmuşsunuz",
                "onlar": "olmuşmuşlar"
            },
            "şimdiki zaman": {
                "ben": "oluyormuşum",
                "sen": "oluyormuşsun",
                "o": "oluyormuş",
                "biz": "oluyormuşuz",
                "siz": "oluyormuşsunuz",
                "onlar": "oluyormuşlar"
            },
            "geniş zaman": {
                "ben": "olurmuşum",
                "sen": "olurmuşsun",
                "o": "olurmuş",
                "biz": "olurmuşuz",
                "siz": "olurmuşsunuz",
                "onlar": "olurmuşlar"
            },
            "gelecek zaman": {
                "ben": "olacakmışım",
                "sen": "olacakmışsın",
                "o": "olacakmış",
                "biz": "olacakmışız",
                "siz": "olacakmışsınız",
                "onlar": "olacakmışlar"
            },
            "istek kipi": {
                "ben": "olaymışım",
                "sen": "olaymışsın",
                "o": "olaymış",
                "biz": "olaymışız",
                "siz": "olaymışsınız",
                "onlar": "olaymışlar"
            },
            "şart kipi": {
                "ben": "olsaymışım",
                "sen": "olsaymışsın",
                "o": "olsaymış",
                "biz": "olsaymışız",
                "siz": "olsaymışsınız",
                "onlar": "olsaymışlar"
            },
            "gereklilik kipi": {
                "ben": "olmalıymışım",
                "sen": "olmalıymışsın",
                "o": "olmalıymış",
                "biz": "olmalıymışız",
                "siz": "olmalıymışsınız",
                "onlar": "olmalıymışlar"
            }
        },
        "şart birleşik zaman": {
            "duyulan geçmiş zaman": {
                "ben": "olmuşsam",
                "sen": "olmuşsan",
                "o": "olmuşsa",
                "biz": "olmuşsak",
                "siz": "olmuşsanız",
                "onlar": "olmuşsalar"
            },
            "görülen geçmiş zaman": {
                "ben": "olduysam",
                "sen": "olduysan",
                "o": "olduysa",
                "biz": "olduysak",
                "siz": "olduysanız",
                "onlar": "olduysalar"
            },
            "şimdiki zaman": {
                "ben": "oluyorsam",
                "sen": "oluyorsan",
                "o": "oluyorsa",
                "biz": "oluyorsak",
                "siz": "oluyorsanız",
                "onlar": "oluyorsalar"
            },
            "geniş zaman": {
                "ben": "olursam",
                "sen": "olursan",
                "o": "olursa",
                "biz": "olursak",
                "siz": "olursanız",
                "onlar": "olursalar"
            },
            "gelecek zaman": {
                "ben": "olacaksam",
                "sen": "olacaksan",
                "o": "olacaksa",
                "biz": "olacaksak",
                "siz": "olacaksanız",
                "onlar": "olacaksalar"
            },
            "gereklilik kipi": {
                "ben": "olmalıysam",
                "sen": "olmalıysan",
                "o": "olmalıysa",
                "biz": "olmalıysak",
                "siz": "olmalıysanız",
                "onlar": "olmalıysalar"
            }
        },
        "mastar kipi": "olmak",
        "ortaç kipi": "olmuş",
        "ulaç kipi": "olarak"
    }
}

[/code]

In order to find the conjugations of a verb, we can use the following parameters:

- verb
- modality
- tense
- subject

Query all conjugations of a single verb:

- <a target="_blank" class="btn-outline-secondary" href=/api/turkish_verbs?data={"verb":"olmak"}>/api/turkish_verbs?data={"verb": "olmak"}</a>

Query all conjugations of some verbs:

- <a target="_blank" class="btn-outline-secondary" href=/api/turkish_verbs?data={"verb":["olmak","gelmek"]}>/api/turkish_verbs?data={"verb": ["olmak", "gelmek"]}</a>

Query a specific mood and a specific subject:

- <a target="_blank" class="btn-outline-secondary" href=/api/turkish_verbs?data={"verb":"olmak","modality":"haber%20kipi","subject":"biz"}>/api/turkish_verbs?data={"verb": "olmak", "modality": "haber kipi", "subject": "biz"}</a>

Query with multiple values:

- <a target="_blank" class="btn-outline-secondary" href=/api/turkish_verbs?data={"verb":["olmak","gelmek"],"tense":["şimdiki%20zaman","duyulan%20geçmiş%20zaman"]}>/api/turkish_verbs?data={"verb": ["olmak", "gelmek"], "tense": ["şimdiki zaman", "duyulan geçmiş zaman"]}</a>

Basically, as long as you write valid verbs, you can combine endpoints to get more specific conjugations of these verbs.
