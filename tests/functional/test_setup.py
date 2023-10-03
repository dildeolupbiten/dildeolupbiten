# -*- coding: utf-8 -*-

from dildeolupbiten.api.italian_verbs.setup import *


def test_get_url():
    # Test an invalid url
    assert get_url("a") == []
    # Test a valid url
    assert get_url("https://www.google.com")


def test_get_section_groups():
    # Test an invalid url
    assert get_section_groups("a") == []
    # Assert that links that have no section group return empty lists.
    assert get_section_groups("https://www.google.com") == []
    # Test a valid url
    assert get_section_groups("https://www.italian-verbs.com/italian-verbs/conjugation.php?parola=essere") != []


def test_get_conjugations():
    import asyncio
    loop = asyncio.new_event_loop()

    async def test_invalid_argument():
        conjugations = await get_conjugations("essere")
        assert conjugations is None

    async def test_valid_argument():
        conjugations = await get_conjugations(ItalianVerb("essere"))
        assert conjugations

    # Test an invalid argument
    loop.run_until_complete(test_invalid_argument())
    # Test a valid argument
    loop.run_until_complete(test_valid_argument())
