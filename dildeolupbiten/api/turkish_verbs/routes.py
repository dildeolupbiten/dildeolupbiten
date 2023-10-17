# -*- coding: utf-8 -*-

from flask import Blueprint

from dildeolupbiten.api.get import get
from dildeolupbiten.api.turkish_verbs.verb import TurkishVerb
from dildeolupbiten.api.turkish_verbs.models import TurkishVerbModel

turkish_verbs = Blueprint("turkish_verbs", __name__)


@turkish_verbs.route("/api/turkish_verbs", methods=["GET"])
async def get_verb():
    return await get("turkish_verbs", TurkishVerbModel, TurkishVerb, None)
