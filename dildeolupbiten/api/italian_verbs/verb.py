# -*- coding: utf-8 -*-

from dildeolupbiten.api.verb import Verb
from dildeolupbiten.utils import create_dict


class ItalianVerb(Verb):
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

    def __init__(self, verb):
        super().__init__({"verb": verb, "conjugations": {}})
        self.add_sub_dicts()

    def add_sub_dicts(self):
        for i in [
            [["indicativo"], self.tenses, self.subjects],
            [["congiuntivo"], ["presente", "imperfetto", "passato", "trapassato"], self.subjects],
            [["condizionale"], ["presente", "passato"], self.subjects],
            [["imperativo"], ["presente"], self.subjects],
            [self.modalities[-3:], ["presente", "passato"]]
        ]:
            self["conjugations"].update(create_dict(*i))
