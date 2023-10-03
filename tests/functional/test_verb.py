# -*- coding: utf-8 -*-

from dildeolupbiten.api.italian_verbs.verb import *


def test_italian_verb_instance():
    verb = ItalianVerb("parlare")
    assert "conjugations" in verb
    assert "verb" in verb
    assert verb["verb"] == "parlare"


def test_italian_verb_conjugations():
    verb = ItalianVerb("parlare")
    conjugations = verb["conjugations"]
    assert isinstance(conjugations, dict)
    for modality in ItalianVerb.modalities:
        assert modality in conjugations
        if modality == "indicativo":
            tenses = ItalianVerb.tenses
            subjects = ItalianVerb.subjects
        elif modality == "congiuntivo":
            tenses = ["presente", "imperfetto", "passato", "trapassato"]
            subjects = ItalianVerb.subjects
        elif modality == "imperativo":
            tenses = ["presente"]
            subjects = ItalianVerb.subjects
        else:
            tenses = ["presente", "passato"]
            subjects = []
        for tense in tenses:
            assert tense in conjugations[modality]
            for subject in subjects:
                assert subject in conjugations[modality][tense]


def test_create_sub_dicts():
    sub_dicts = ItalianVerb.create_sub_dicts(["indicativo"], ["presente"], ItalianVerb.subjects)
    assert isinstance(sub_dicts, dict)
    assert "indicativo" in sub_dicts
    assert "presente" in sub_dicts["indicativo"]
    for subject in ItalianVerb.subjects:
        assert subject in sub_dicts["indicativo"]["presente"]


def test_query():
    args = {"subject": "io", "modality": ["indicativo"], "tense": "presente"}
    assert ItalianVerb.query(args, "subject") == ["io"]
    assert ItalianVerb.query(args, "modality") == ["indicativo"]
    assert ItalianVerb.query(args, "tense") == ["presente"]


def test_isinstance():
    verb = ItalianVerb("parlare")
    assert ItalianVerb.isinstance(verb)


def test_query_invalid():
    args = {"subject": "invalid_subject", "modality": ["invalid_modality"], "tense": "invalid_tense"}
    assert ItalianVerb.query(args, "subject") is None
    assert ItalianVerb.query(args, "modality") is None
    assert ItalianVerb.query(args, "tense") is None

