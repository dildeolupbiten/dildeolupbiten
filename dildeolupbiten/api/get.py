# -*- coding: utf-8 -*-

from json.decoder import JSONDecodeError
from flask import request, json, Response, render_template, current_app

from dildeolupbiten import db
from dildeolupbiten.utils import query, api_info, pygmentize, HTMLCodeFormat


async def get(title, verb_model, verb_class, get_conjugations):
    if "data" in request.args:
        args = json.loads(request.args["data"])
    else:
        try:
            args = json.loads(request.data.decode("utf-8"))
        except JSONDecodeError:
            info = api_info(
                filename=current_app.root_path + f"/api/{title}/{title}.md",
                url=request.url,
                title=title
            )
            if "python" in request.headers["User-Agent"]:
                return json.dumps(pygmentize(info))
            return render_template(
                f"api/{title}/get.html",
                title=f"API - {title.replace('_', ' ').title()}",
                api_main=lambda: HTMLCodeFormat(info).highlight()
            )
    allowed_args = ["modality", "subject", "tense", "verb"]
    if all(arg in allowed_args for arg in args):
        if "verb" in args:
            if isinstance(args["verb"], list) or isinstance(args["verb"], tuple):
                delete = []
                for v in args["verb"]:
                    if not any(v.endswith(i) for i in ["ire", "are", "ere", "mek", "mak"]):
                        delete += [v]
                for i in delete:
                    args["verb"].remove(i)
                verbs = verb_model.query.filter(verb_model.verb["verb"].astext.in_(args["verb"])).all()
                verbs = [verb.verb for verb in verbs]
                missings = [verb for verb in args["verb"] if verb not in [v["verb"] for v in verbs]]
                if missings:
                    for missing in missings:
                        if any(missing.endswith(i) for i in ["ire", "are", "ere", "mek", "mak"]):
                            if get_conjugations:
                                verb = await get_conjugations(verb_class(verb=missing))
                            else:
                                verb = verb_class(verb=missing[:-3])
                                await verb.conjugate()
                            if verb:
                                verb = verb_model(verb=verb)
                                db.session.add(verb)
                                db.session.commit()
                                verbs += [verb.verb]
                        else:
                            return {}
                    if not verbs:
                        return {}
            elif isinstance(args["verb"], str):
                if not any(args["verb"].endswith(i) for i in ["ire", "are", "ere", "mek", "mak"]):
                    return {}
                verbs = verb_model.query.filter(verb_model.verb["verb"].astext == args["verb"]).all()
                verbs = [verb.verb for verb in verbs]
                if not verbs:
                    if get_conjugations:
                        verb = await get_conjugations(verb_class(verb=args["verb"]))
                    else:
                        verb = verb_class(verb=args["verb"][:-3])
                        await verb.conjugate()
                    if verb:
                        verb = verb_model(verb=verb)
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
