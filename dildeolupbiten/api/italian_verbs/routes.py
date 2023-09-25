# -*- coding: utf-8 -*-

from json.decoder import JSONDecodeError
from flask import request, Blueprint, json, Response, render_template, current_app

from dildeolupbiten.utils import query, render, api_info, pygmentize
from dildeolupbiten.api.italian_verbs.models import ItalianVerbModel

italian_verbs = Blueprint("italian_verbs", __name__)


@italian_verbs.route("/api/italian_verbs", methods=["GET"])
def get():
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
            elif isinstance(args["verb"], str):
                verbs = ItalianVerbModel.query.filter(ItalianVerbModel.verb["verb"].astext == args["verb"]).all()
            else:
                return {}
        else:
            return {}
        verbs = [verb.verb for verb in verbs]
        for arg in allowed_args[:-1]:
            if arg in args:
                verbs = [
                    {
                        "verb": verb["verb"],
                        "conjugations": query(
                            verb["conjugations"],
                            [args[arg]] if isinstance(args[arg], str) else args[arg]
                        )
                    }
                    for verb in verbs
                ]
        return verbs
    return Response("Bad request", 400)
