# -*- coding: utf-8 -*-

from json.decoder import JSONDecodeError
from flask import request, Blueprint, json, Response, render_template, current_app

from dildeolupbiten import db
from dildeolupbiten.utils import render, query, api_info, pygmentize
from dildeolupbiten.api.italian_verbs.models import ItalianVerbModel
from dildeolupbiten.api.italian_verbs.setup import get_conjugations
from dildeolupbiten.api.italian_verbs.verb import ItalianVerb

italian_verbs = Blueprint("italian_verbs", __name__)


@italian_verbs.route("/api/italian_verbs", methods=["GET"])
async def get():
    if "data" in request.args:
        args = json.loads(request.args["data"])
    else:
        try:
            args = json.loads(request.data.decode("utf-8"))
        except JSONDecodeError:
            info = api_info(filename=current_app.root_path + "/api/italian_verbs/italian_verbs.md", url=request.url)
            if "python" in request.headers["User-Agent"]:
                return json.dumps(pygmentize(info))
            return render_template(
                "api/italian_verbs/get.html",
                title="API - Italian Verbs",
                api_main=lambda: render(info)
            )
    allowed_args = ["modality", "subject", "tense", "verb"]
    if all(arg in allowed_args for arg in args):
        if "verb" in args:
            if isinstance(args["verb"], list) or isinstance(args["verb"], tuple):
                verbs = ItalianVerbModel.query.filter(ItalianVerbModel.verb["verb"].astext.in_(args["verb"])).all()
                verbs = [verb.verb for verb in verbs]
                missings = [verb for verb in args["verb"] if verb not in [v["verb"] for v in verbs]]
                if missings:
                    for missing in missings:
                        verb = await get_conjugations(ItalianVerb(verb=missing))
                        if verb:
                            verb = ItalianVerbModel(verb=verb)
                            db.session.add(verb)
                            db.session.commit()
                            verbs += [verb.verb]
                    if not verbs:
                        return {}
            elif isinstance(args["verb"], str):
                verbs = ItalianVerbModel.query.filter(ItalianVerbModel.verb["verb"].astext == args["verb"]).all()
                verbs = [verb.verb for verb in verbs]
                if not verbs:
                    verb = await get_conjugations(ItalianVerb(verb=args["verb"]))
                    if verb:
                        verb = ItalianVerbModel(verb=verb)
                        db.session.add(verb)
                        db.session.commit()
                        verbs += [verb.verb]
                    else:
                        return {}
            else:
                return {}
        else:
            return {}
        for arg in allowed_args[:-1]:
            if arg in args:
                verbs = [
                    {
                        "verb": v["verb"],
                        "conjugations": query(
                            v["conjugations"],
                            [args[arg]] if isinstance(args[arg], str) else args[arg]
                        )
                    }
                    for v in verbs
                ]
        return verbs
    return Response("Bad request", 400)
