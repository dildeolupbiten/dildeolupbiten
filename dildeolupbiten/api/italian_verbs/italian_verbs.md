This API conjugates 12322 Italian verbs. You can make various requests with different query parameters.

The parameters are based on the Italian Verb model:

```python
class ItalianVerb(dict):
    modalities = [
        "indicativo",           # en: indicative                tr: haber/bildirme kipi
        "congiuntivo",          # en: conjunctive               tr: istek kipi
        "condizionale",         # en: conditional               tr: dilek-şart kipi
        "imperativo",           # en: imperative                tr: emir kipi
        "infinito",             # en: infinitive                tr: mastar
        "participio",           # en: participle                tr: ortaç (sıfat fiil)
        "gerundio"              # en: gerund                    tr: ulaç (bağ fiil)
    ]
    tenses = [
        "presente",             # en: present tense             tr: şimdiki zaman/geniş zaman
        "imperfetto",           # en: past continuous tense     tr: bir süreliğine devam etmiş geçmiş zaman
        "passato prossimo",     # en: present perfect tense     tr: şimdi ile bağlantılı geçmiş zaman
        "trapassato prossimo",  # en: past perfect tense        tr: geçmiş ile bağlantılı geçmiş zaman
        "passato remoto",       # en: remote past tense         tr: uzak geçmiş zaman
        "trapassato remoto",    # en: preterite perfect tense   tr: uzak geçmiş zaman öncesi
        "futuro semplice",      # en: future tense              tr: gelecek zaman
        "futuro anteriore"      # en: future perfect tense      tr: gelecek zaman öncesi
    ]
    subjects = [
        "io",                   # en: i                         tr: ben
        "tu",                   # en: you                       tr: sen
        "lui/lei",              # en: he/she                    tr: o
        "noi",                  # en: we                        tr: biz
        "voi",                  # en: you                       tr: siz
        "loro"                  # en: they                      tr: onlar
    ]
```

All Italian verbs have aforementioned attributes. An ItalianVerb object has similar attributes with the following verb model:

```json
{
    "conjugations": {
        "condizionale": {
            "passato": {
                "io": "io sarei stato/a",
                "loro": "loro sarebbero stati/e",
                "lui/lei": "lui/lei sarebbe stato/a",
                "noi": "noi saremmo stati/e",
                "tu": "tu saresti stato/a",
                "voi": "voi sareste stati/e"
            },
            "presente": {
                "io": "io sarei",
                "loro": "loro sarebbero",
                "lui/lei": "lui/lei sarebbe",
                "noi": "noi saremmo",
                "tu": "tu saresti",
                "voi": "voi sareste"
            }
        },
        "congiuntivo": {
            "imperfetto": {
                "io": "che io fossi",
                "loro": "che loro fossero",
                "lui/lei": "che lui/lei fosse",
                "noi": "che noi fossimo",
                "tu": "che tu fossi",
                "voi": "che voi foste"
            },
            "passato": {
                "io": "che io sia stato/a",
                "loro": "che loro siano stati/e",
                "lui/lei": "che lui/lei sia stato/a",
                "noi": "che noi siamo stati/e",
                "tu": "che tu sia stato/a",
                "voi": "che voi siate stati/e"
            },
            "presente": {
                "io": "che io sia",
                "loro": "che loro siano",
                "lui/lei": "che lui/lei sia",
                "noi": "che noi siamo",
                "tu": "che tu sia",
                "voi": "che voi siate"
            },
            "trapassato": {
                "io": "che io fossi stato/a",
                "loro": "che loro fossero stati/e",
                "lui/lei": "che lui/lei fosse stato/a",
                "noi": "che noi fossimo stati/e",
                "tu": "che tu fossi stato/a",
                "voi": "che voi foste stati/e"
            }
        },
        "gerundio": {
            "passato": "essendo stato/a/i/e",
            "presente": "essendo"
        },
        "imperativo": {
            "presente": {
                "io": "-",
                "loro": "siano",
                "lui/lei": "sia",
                "noi": "siamo",
                "tu": "sii",
                "voi": "siate"
            }
        },
        "indicativo": {
            "futuro anteriore": {
                "io": "io sar\u00f2 stato/a",
                "loro": "loro saranno stati/e",
                "lui/lei": "lui/lei sar\u00e0 stato/a",
                "noi": "noi saremo stati/e",
                "tu": "tu sarai stato/a",
                "voi": "voi sarete stati/e"
            },
            "futuro semplice": {
                "io": "io sar\u00f2",
                "loro": "loro saranno",
                "lui/lei": "lui/lei sar\u00e0",
                "noi": "noi saremo",
                "tu": "tu sarai",
                "voi": "voi sarete"
            },
            "imperfetto": {
                "io": "io ero",
                "loro": "loro erano",
                "lui/lei": "lui/lei era",
                "noi": "noi eravamo",
                "tu": "tu eri",
                "voi": "voi eravate"
            },
            "passato prossimo": {
                "io": "io sono stato/a",
                "loro": "loro sono stati/e",
                "lui/lei": "lui/lei \u00e8 stato/a",
                "noi": "noi siamo stati/e",
                "tu": "tu sei stato/a",
                "voi": "voi siete stati/e"
            },
            "passato remoto": {
                "io": "io fui",
                "loro": "loro furono",
                "lui/lei": "lui/lei fu",
                "noi": "noi fummo",
                "tu": "tu fosti",
                "voi": "voi foste"
            },
            "presente": {
                "io": "io sono",
                "loro": "loro sono",
                "lui/lei": "lui/lei \u00e8",
                "noi": "noi siamo",
                "tu": "tu sei",
                "voi": "voi siete"
            },
            "trapassato prossimo": {
                "io": "io ero stato/a",
                "loro": "loro erano stati/e",
                "lui/lei": "lui/lei era stato/a",
                "noi": "noi eravamo stati/e",
                "tu": "tu eri stato/a",
                "voi": "voi eravate stati/e"
            },
            "trapassato remoto": {
                "io": "io fui stato/a",
                "loro": "loro furono stati/e",
                "lui/lei": "lui/lei fu stato/a",
                "noi": "noi fummo stati/e",
                "tu": "tu fosti stato/a",
                "voi": "voi foste stati/e"
            }
        },
        "infinito": {
            "passato": "essere stato/a/i/e",
            "presente": "essere"
        },
        "participio": {
            "passato": "stato/a/i/e",
            "presente": "ente"
        }
    },
    "verb": "essere"
}
```

In order to find the conjugations of a verb, we can use the following parameters:

- verb
- modality
- tense
- subject

Query all conjugations of a single verb:

- <a target="_blank" style="color:blue;" href=/api/italian_verbs?data={"verb":"essere"}>/api/italian_verbs?data={"verb": "essere"}</a>

Query all conjugations of some verbs:

- <a target="_blank" style="color:blue;" href=/api/italian_verbs?data={"verb":["essere","avere"]}>/api/italian_verbs?data={"verb": ["essere", "avere"]}</a>

Query a specific mood and a specific subject:

- <a target="_blank" style="color:blue;" href=/api/italian_verbs?data={"verb":"essere","modality":"indicativo","subject":"noi"}>/api/italian_verbs?data={"verb": "essere", "modality": "indicativo", "subject": "noi"}</a>

Query with multiple values:

- <a target="_blank" style="color:blue;" href=/api/italian_verbs?data={"verb":["essere","avere"],"tense":["presente","imperfetto"]}>/api/italian_verbs?data={"verb": ["essere", "avere"], "tense": ["presente", "imperfetto"]}</a>

Basically, as long as you write valid verbs, you can combine endpoints to get more specific conjugations of these verbs.
