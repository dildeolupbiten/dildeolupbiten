# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, json, Response
from dildeolupbiten.apps.wfm.shift_plan import ShiftPlan

wfm = Blueprint("wfm", __name__)


@wfm.route("/wfm", methods=["GET", "POST"])
def index():
    if "shift_plan" in request.form:
        hc = int(request.form["Total HC"])
        shift = list(map(int, request.form["Shift"].split(",")))
        days = int(request.form["Days"])
        off = int(request.form["Off Day"])
        shift_plan = ShiftPlan(hc=hc, shifts=shift, days=days, off=off)
        if shift_plan.error:
            return Response(json.dumps([]), 200)
        dist = shift_plan.dist(1, days + 1)
        data = [shift_plan.values.tolist(), dist.values.tolist()]
        return Response(json.dumps(data), 200)
    return render_template("apps/wfm/index.html", title="WFM")
