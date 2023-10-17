# -*- coding: utf-8 -*-

import asyncio

from dildeolupbiten.api.verb import Verb
from dildeolupbiten.utils import create_dict
from dildeolupbiten.api.turkish_verbs.setup import TurkishVerbChart


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
    ]
    tenses = [
        "duyulan geçmiş zaman",      # en: dubitative past tense       it: tempo passato dubitativo
        "görülen geçmiş zaman",      # en: definitive past tense       it: tempo passato definitivo
        "şimdiki zaman",             # en: present progressive tense   it: tempo presente progressivo
        "geniş zaman",               # en: simple aorist tense         it: tempo aoristo semplice
        "gelecek zaman"              # en: future tense                it: tempo futuro
    ]
    composite_tenses = [
        "hikaye birleşik zaman",     # en: story compound tense       it: tempo composto storico
        "rivayet birleşik zaman",    # en: rumor compound tense       it: tempo composto rumoroso
        "şart birleşik zaman"        # en: conditional compound tense it: tempo composto condizionale
    ]
    subjects = [
        "ben",                       # en: i                           it: io
        "sen",                       # en: you                         it: tu
        "o",                         # en: he/she                      it: lui/lei
        "biz",                       # en: we                          it: noi
        "siz",                       # en: you                         it: voi
        "onlar"                      # en: they                        it: loro
    ]

    def __init__(self, verb):
        super().__init__({"verb": verb, "conjugations": {}})
        self.add_sub_dicts()

    def add_sub_dicts(self):
        for i in [
            [["haber kipi"], self.tenses, self.subjects],
            [["istek kipi", "şart kipi", "gereklilik kipi", "emir kipi"], self.subjects],
            [["hikaye birleşik zaman"], [*self.tenses, *self.modalities[1:4]], self.subjects],
            [["rivayet birleşik zaman"], [self.tenses[0], *self.tenses[2:], *self.modalities[1:4]], self.subjects],
            [["şart birleşik zaman"], [*self.tenses, self.modalities[3]], self.subjects],
            [["mastar kipi"]],
            [["ortaç kipi"]],
            [["ulaç kipi"]]
        ]:
            self["conjugations"].update(create_dict(*i))

    async def conjugate(self):
        verb = self["verb"][:-3]
        chart = TurkishVerbChart(verb)
        for tenses, suffix, mode in [
            (self.tenses, "", "haber kipi"),
            (["istek kipi"], "", "istek kipi"),
            (["şart kipi"], "", "şart kipi"),
            (["gereklilik kipi"], "", "gereklilik kipi"),
            (["emir kipi"], "", "emir kipi"),
            ([*self.tenses, *self.modalities[1:4]], "di", "hikaye birleşik zaman"),
            ([self.tenses[0], *self.tenses[2:], *self.modalities[1:4]], "miş", "rivayet birleşik zaman"),
            ([*self.tenses, self.modalities[3]], "se", "şart birleşik zaman"),
        ]:
            for tense in tenses:
                chart.add_suffix(chart.MAP[tense])
                for subject in self.subjects:
                    if "kip" not in mode:
                        chart.add_suffix(suffix)
                    chart.add_suffix(chart.MAP[subject])
                    if "kip" in mode and "haber" not in mode:
                        self["conjugations"][mode][subject] = chart.word
                    else:
                        self["conjugations"][mode][tense][subject] = chart.word
                    chart.word = verb
                    chart.suffixes = []
                    chart.add_suffix(chart.MAP[tense])
                chart.word = verb
                chart.suffixes = []
        for mode in ["mastar kipi", "ulaç kipi", "ortaç kipi"]:
            chart.add_suffix(chart.MAP[mode])
            self["conjugations"][mode] = chart.word
            chart.word = verb
            chart.suffixes = []
        await asyncio.sleep(0)
