# -*- coding: utf-8 -*-


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

    map = {
        "subject": "subjects",
        "modality": "modalities",
        "tense": "tenses"
    }

    def __init__(self, verb):
        super().__init__({"verb": verb, "conjugations": {}})
        self.add_sub_dicts()

    @classmethod
    def isinstance(cls, instance: 'ItalianVerb'):
        def inner(self, other):
            if len(other) != len(self):
                return False
            for k1, k2 in zip(self, other):
                if k1 != k2:
                    return False
                if isinstance(self[k1], dict):
                    if isinstance(other[k2], dict):
                        return inner(self[k1], other[k1])
                    else:
                        return False
            return True
        return inner(cls.__call__(verb=""), instance)

    @staticmethod
    def create_sub_dicts(modalities, tenses, subjects=None):
        return {
            modality: {
                tense: ("" if not subjects else {subject: "" for subject in subjects})
                for tense in tenses
            } for modality in modalities
        }

    def add_sub_dicts(self):
        for i in [
            [["indicativo"], self.tenses, self.subjects],
            [["congiuntivo"], ["presente", "imperfetto", "passato", "trapassato"], self.subjects],
            [["condizionale"], ["presente", "passato"], self.subjects],
            [["imperativo"], ["presente"], self.subjects],
            [self.modalities[-3:], ["presente", "passato"], None]
        ]:
            self["conjugations"].update(self.create_sub_dicts(*i))

    @classmethod
    def query(cls, args, key):
        if (
            (isinstance(args[key], list) or isinstance(args[key], tuple))
            and
            (data := list(filter(lambda i: i in getattr(cls, cls.map[key]), args[key])))
        ):
            return data
        elif isinstance(args[key], str) and args[key] in getattr(cls, cls.map[key]):
            return [args[key]]
