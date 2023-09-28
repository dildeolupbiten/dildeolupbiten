# -*- coding: utf-8 -*-

import os
import bs4
import requests
import threading

from dildeolupbiten.api.italian_verbs.verb import ItalianVerb
from dildeolupbiten.api.italian_verbs.models import ItalianVerbModel


def get_url(url: str):
    r = None
    while not r:
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            pass
    return r


def get_italian_verbs(url):
    return sorted(get_url(url).json())


def get_section_groups(url):
    soup = bs4.BeautifulSoup(get_url(url).content, "html.parser")
    return [
        section_group
        for section_group in soup.find_all("div", attrs={"class": "section group"})
        if not section_group.find("a")
    ]


def get_conjugations(verb, url, app, db):
    section_groups = get_section_groups(url=url + verb['verb'])
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
    with app.app_context():
        db.session.add(ItalianVerbModel(verb=verb))
        db.session.commit()


def join_threads(threads, total, count):
    for thread in threads:
        thread.join()
        count += 1
        print(f"\rProgress: {round(count / total * 100, 2)} %", end="")
    return [], count


def get_database(app, db):
    gist = (
        "https://gist.githubusercontent.com/dildeolupbiten/"
        "734059b12da83ef3440bd8013efa336c/raw/"
        "0005d47f536943b475632c9be641b4b9a6bff479/italian-verbs.json"
    )
    url = "https://www.italian-verbs.com/italian-verbs/conjugation.php?parola="
    italian_verbs = get_italian_verbs(url=gist)
    with app.app_context():
        data = [str(i[0]) for i in db.session.execute(db.select(ItalianVerbModel)).all()]
    to_be_downloaded = [i for i in italian_verbs if i not in data]
    total = len(italian_verbs)
    count = len(data)
    index = 0
    threads = []
    if to_be_downloaded:
        print("Downloading verbs...")
        for verb in to_be_downloaded:
            if threading.active_count() == os.cpu_count():
                threads, count = join_threads(threads, total, count)
            thread = threading.Thread(
                target=get_conjugations,
                args=(ItalianVerb(verb=verb), url, app, db),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            index += 1
        if count != total:
            join_threads(threads, total, count)
        print("\nDownload completed...")