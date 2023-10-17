# -*- coding: utf-8 -*-

from flask import Blueprint

from dildeolupbiten.api.get import get
from dildeolupbiten.api.italian_verbs.verb import ItalianVerb
from dildeolupbiten.api.italian_verbs.models import ItalianVerbModel
from dildeolupbiten.api.italian_verbs.setup import get_conjugations

italian_verbs = Blueprint("italian_verbs", __name__)


@italian_verbs.route("/api/italian_verbs", methods=["GET"])
async def get_verb():
    return await get("italian_verbs", ItalianVerbModel, ItalianVerb, get_conjugations)
