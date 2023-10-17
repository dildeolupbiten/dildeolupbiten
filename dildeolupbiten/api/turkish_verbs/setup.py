# -*- coding: utf-8 -*-

class TurkishVerbChart:
    VOWELS = "aeıioöuü"
    CONSONANTS = "bcçdfgğhjklmnprsştvyz"
    STRONG = "fstkçşhp"
    BACK = "aıou"
    FRONT = "eiöü"
    ROUNDED = "oöuü"
    UNROUNDED = "aeıi"
    SOFT = "bcdğ"
    HARD = "pçtk"
    MAP = {
        "duyulan geçmiş zaman": "miş",
        "görülen geçmiş zaman": "di",
        "şimdiki zaman": "yor",
        "geniş zaman": "r",
        "gelecek zaman": "ecek",
        "istek kipi": "e",
        "şart kipi": "se",
        "gereklilik kipi": "meli",
        "mastar kipi": "mek",
        "ortaç kipi": "miş",
        "ulaç kipi": "erek",
        "emir kipi": "-",
        "ben": "m",
        "sen": "n",
        "o": "",
        "biz": "z",
        "siz": "niz",
        "onlar": "ler"
    }

    def __init__(self, word):
        self.root = word
        self.word = word
        self.suffixes = []

    def add_suffix(self, suffix: str):
        self.suffixes += [suffix]
        if len(self.suffixes) >= 2 and self.suffixes[-2] == "-":
            self.word = self.word[:-1]
            if suffix == "m" or suffix == "z":
                self.word = "-"
                return
            elif suffix == "n":
                return
            elif suffix == "":
                vowel = self.vowel_harmony("i", [self.BACK, self.FRONT])
                vowel = self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED])
                self.word += "s" + self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED]) + "n"
                return
            elif suffix == "niz":
                exceptions = ["et", "git"]
                if self.word in exceptions or self.word.endswith("et"):
                    self.word = self.word[:-1] + "din"
                    return
                vowel = self.vowel_harmony("i", [self.BACK, self.FRONT])
                vowel = self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED])
                self.word += self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED]) + "n"
                return
            elif suffix == "ler":
                vowel = self.vowel_harmony("i", [self.BACK, self.FRONT])
                vowel = self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED])
                eora = self.vowel_harmony("e", [self.BACK, self.FRONT])
                self.word += "s" + self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED]) + "nl" + eora + "r"
                return
        suffix = self.vowel_derivation(suffix)
        suffix = self.vowel_harmony(suffix, rule=[self.ROUNDED, self.UNROUNDED])
        suffix = self.vowel_harmony(suffix, rule=[self.BACK, self.FRONT])
        suffix = self.consonant_softening(suffix)
        suffix = self.fusion_letter(suffix)
        suffix = self.consonant_fortening(suffix)
        self.word += suffix

    def vowel_harmony(self, suffix: str, rule: list):
        vowel = list(filter(lambda v: v in self.VOWELS, self.word))[-1]
        if suffix in ["ler", "lar"]:
            if vowel in self.BACK:
                return "lar"
            else:
                return "ler"
        if suffix in ["se", "sa"]:
            if vowel in self.BACK:
                return "sa"
            else:
                return "se"
        if suffix in ["yor", "üyor", "iyor", "ıyor", "uyor", "r", "er", "ar"]:
            return suffix
        if suffix in ["ecek", "acak"]:
            if vowel in self.BACK:
                return "acak"
            else:
                return "ecek"
        if suffix in ["e", "a"]:
            if vowel in self.BACK:
                return "a"
            else:
                return "e"
        if suffix in ["meli", "malı"]:
            if vowel in self.BACK:
                return "malı"
            else:
                return "meli"
        if suffix in ["mek", "mak"]:
            if vowel in self.BACK:
                return "mak"
            else:
                return "mek"
        if suffix in ["erek", "arak"]:
            if vowel in self.BACK:
                return "arak"
            else:
                return "erek"
        old, new = (rule[0], rule[1]) if vowel in rule[1] else (rule[1], rule[0])
        for i, j in zip(old, new):
            suffix = suffix.replace(i, j)
        return suffix

    def vowel_derivation(self, suffix: str):
        vowel = list(filter(lambda i: i in self.VOWELS, self.word))[-1]
        exceptional_suffixes = ["ecek", "se", "di", "miş", "meli", "mek"]
        suffixes_1 = ["r", "ecek", "acak", "e", "a", "miş", "mış", "muş", "müş"]
        if suffix == "r":
            if len(self.word) >= 4 and (self.word.endswith("er") or self.word.endswith("ar")):
                suffix = self.vowel_harmony("i", [self.BACK, self.FRONT]) + suffix
                return self.vowel_harmony(suffix, [self.ROUNDED, self.UNROUNDED])
            if self.word == "gül":
                return "er"
        if suffix == "ler":
            if vowel in self.BACK:
                return "lar"
            else:
                return "ler"
        if suffix == "yor":
            mapping = {"e": "i", "a": "ı"}
            if self.word[-1] in mapping:
                self.word = self.word[:-1] + mapping[self.word[-1]]
                return "yor"
            vowel = self.vowel_harmony("i", [self.BACK, self.FRONT])
            return self.vowel_harmony(vowel, [self.ROUNDED, self.UNROUNDED]) + "yor"
        if (
            suffix == "m"
            and
            any(self.word.endswith(i) for i in suffixes_1)
            and
            self.suffixes[-2] not in ["se", "sa"]
        ):
            suffix = self.vowel_harmony("i", [self.ROUNDED, self.UNROUNDED]) + "m"
            return suffix
        if (
            suffix == "n"
            and
            any(self.word.endswith(i) for i in suffixes_1)
            and
            self.suffixes[-2] not in ["se", "sa"]
        ):
            suffix = "s" + self.vowel_harmony("i", [self.ROUNDED, self.UNROUNDED]) + "n"
            return suffix
        if (
            suffix == "niz"
            and
            any(self.word.endswith(i) for i in suffixes_1)
            and self.suffixes[-2] not in ["se", "sa"]
        ):
            vowel = self.vowel_harmony("i", [self.ROUNDED, self.UNROUNDED])
            suffix = "s" + vowel + "n" + vowel + "z"
            return suffix
        if suffix in ["ler", "lar"]:
            return suffix
        if suffix == "z":
            exceptions = ["se", "sa", "dı", "di", "du", "dü", "tı", "ti", "tu", "tü", "e", "a"]
            if self.suffixes[-2] in exceptions:
                return "k"
            else:
                vowel = self.vowel_harmony("i", [self.ROUNDED, self.UNROUNDED])
                return vowel + "z"
        if (
            suffix
            and
            all(i in self.CONSONANTS for i in [suffix[0], self.word[-1]])
            and
            (suffix not in exceptional_suffixes)
        ):
            if len(self.word) == 2:
                mapping = {"al": "ı", "ol": "u", "öl": "ü"}
                if self.word in mapping:
                    suffix = mapping[self.word] + suffix
                else:
                    if suffix == "yor":
                        suffix = self.vowel_harmony("i", [self.BACK, self.FRONT]) + suffix
                        suffix = self.vowel_harmony(suffix, [self.ROUNDED, self.UNROUNDED])
                    else:
                        suffix = ("e" if vowel in self.FRONT else "a") + suffix
            elif len(self.word) == 3:
                mapping = {
                    "bil": "i", "gel": "i", "gör": "ü", "bul": "u", "kal": "ı",
                    "ver": "i", "vur": "u", "var": "ı", "dur": "u", "san": "ı"
                }
                if self.word in mapping:
                    suffix = mapping[self.word] + suffix
                else:
                    suffix = ("e" if vowel in self.FRONT else "a") + suffix
            else:
                suffix = vowel + suffix
        return suffix

    def consonant_softening(self, suffix):
        if suffix in ["sınız", "siniz", "sunuz", "sünüz"]:
            suffixes = ["ecek", "acak"]
            if self.suffixes[-2] in suffixes:
                return suffix
        if suffix and suffix[0] in self.VOWELS and self.word[-1] in self.HARD:
            exceptions = ["et", "git"]
            suffixes = ["ecek", "acak", "iyor", "ıyor", "uyor", "üyor", "e", "a", "er", "erek", "arak"]
            if suffix in suffixes and (self.word in exceptions or self.word.endswith("et")):
                self.word = self.word[:-1] + self.SOFT[self.HARD.index(self.word[-1])]
        if suffix and suffix[-1] in "mz":
            suffixes = ["ecek", "acak"]
            if self.suffixes[-2] in suffixes:
                self.word = self.word[:-1] + self.SOFT[self.HARD.index(self.word[-1])]
        return suffix

    def fusion_letter(self, suffix):
        exceptional_suffixes = ["se", "sa", "miş", "mış", "di", "dı", "meli", "malı", "m", "n", "niz", "nız"]
        hikaye_birlesik = ["dı", "di", "du", "dü", "tı", "ti", "tu", "tü"]
        rivayet_birlesik = ["mış", "miş", "muş", "müş"]
        sart_birlesik = ["se", "sa"]
        if (
            len(self.suffixes) >= 2
            and
            (suffix in hikaye_birlesik or suffix in rivayet_birlesik or suffix in sart_birlesik)
            and
            (self.suffixes[-2] in hikaye_birlesik or self.suffixes[-2] in ["a", "e", "se", "sa"])
        ):
            return "y" + suffix
        if suffix and suffix[-1] == "k" and self.word[-1] not in self.VOWELS:
            return suffix
        if suffix and all(i in self.VOWELS for i in [suffix[0], self.word[-1]]):
            suffix = "y" + suffix
        if (
            (self.word[-1] in self.VOWELS)
            and
            (suffix in exceptional_suffixes)
            and
            (self.root != self.word)
        ):
            suffixes = ["meli", "malı"]
            if self.suffixes[-2] in suffixes:
                if suffix == "m":
                    suffix = "y" + self.word[-1] + suffix
                elif suffix in ["n", "nız", "niz"]:
                    suffix = "s" + self.word[-1] + suffix
                else:
                    suffix = "y" + suffix
        return suffix

    def consonant_fortening(self, suffix):
        if suffix and self.word[-1] in self.STRONG and suffix[0] in self.SOFT:
            suffix = self.HARD[self.SOFT.index(suffix[0])] + suffix[1:]
        return suffix
