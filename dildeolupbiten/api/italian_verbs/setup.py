# -*- coding: utf-8 -*-

import bs4
import requests
from dildeolupbiten.api.italian_verbs.verb import ItalianVerb


def get_url(url: str):
    r = None
    while not r:
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.MissingSchema:
            return []
    return r


def get_section_groups(url):
    if url := get_url(url):
        soup = bs4.BeautifulSoup(url.content, "html.parser")
        return [
            section_group
            for section_group in soup.find_all("div", attrs={"class": "section group"})
            if not section_group.find("a")
        ]
    else:
        return []


async def get_conjugations(verb):
    if not isinstance(verb, ItalianVerb):
        return
    url = "https://www.italian-verbs.com/italian-verbs/conjugation.php?parola="
    section_groups = get_section_groups(url=url + verb['verb'])
    if not section_groups:
        return
    modality, tense = "", ""
    iter_modalities = iter(verb.modalities)
    index = 0
    for section_group in section_groups:
        for td in section_group.find_all("td"):
            text = td.text.lower().split(":")
            if len(text) > 1:
                text, value = text
            else:
                text, value = text[0], ""
            if text in verb.tenses or text in ["passato", "trapassato"]:
                tense = text
                if tense == "presente":
                    modality = next(iter_modalities)
                if value:
                    verb["conjugations"][modality][tense] = value.strip()
                    index += 1
                continue
            elif text in verb.modalities:
                continue
            verb["conjugations"][modality][tense][verb.subjects[index % len(verb.subjects)]] = text.replace("—", "-")
            index += 1
    return verb
