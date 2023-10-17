# -*- coding: utf-8 -*-

from dildeolupbiten.api.turkish_verbs.verb import *


def test_turkish_verb_instance():
    verb = TurkishVerb("ol")
    assert "conjugations" in verb
    assert "verb" in verb
    assert verb["verb"] == "ol"


def test_turkish_verb_conjugations():
    verb = TurkishVerb("ol")
    conjugations = verb["conjugations"]
    assert isinstance(conjugations, dict)
    for modality in TurkishVerb.modalities:
        if modality not in ["mastar", "ortaç", "ulaç"]:
            assert modality in conjugations
            if modality == "haber kipi":
                for tense in TurkishVerb.tenses:
                    assert tense in conjugations[modality]
                    for subject in TurkishVerb.subjects:
                        assert subject in conjugations[modality][tense]
            else:
                for subject in TurkishVerb.subjects:
                    assert subject in conjugations[modality]


def test_query():
    args = {"subject": "ben", "modality": ["haber kipi"], "tense": "şimdiki zaman"}
    assert TurkishVerb.query(args, "subject") == ["ben"]
    assert TurkishVerb.query(args, "modality") == ["haber kipi"]
    assert TurkishVerb.query(args, "tense") == ["şimdiki zaman"]


def test_isinstance():
    verb = TurkishVerb("ol")
    assert TurkishVerb.isinstance(verb)


def test_query_invalid():
    args = {"subject": "invalid_subject", "modality": ["invalid_modality"], "tense": "invalid_tense"}
    assert TurkishVerb.query(args, "subject") is None
    assert TurkishVerb.query(args, "modality") is None
    assert TurkishVerb.query(args, "tense") is None
