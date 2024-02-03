# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, json, Response, jsonify
from dildeolupbiten.apps.wfm.shift_plan import ShiftPlan
from dildeolupbiten.apps.wfm.break_plan import create_break_plans

wfm = Blueprint("wfm", __name__)
export = {}


@wfm.route("/wfm", methods=["GET", "POST"])
async def index():
    global export
    if "shift_plan" in request.args and export:
        copy = export.copy()
        export = {}
        return copy
    if "shift" in request.form:
        hc = int(request.form["Total HC"])
        shift = list(map(int, request.form["Shift"].split(",")))
        days = int(request.form["Days"])
        off = int(request.form["Off"])
        shift_plan = ShiftPlan(hc=hc, shifts=shift, days=days, off=off)
        await shift_plan.build()
        if shift_plan.error:
            return Response(json.dumps([]), 200)
        dist = await shift_plan.dist(1, days + 1)
        data = [shift_plan.values.tolist(), dist.values.tolist()]
        return Response(json.dumps(data), 200)
    elif "break" in request.form:
        shift_plan = json.loads(request.form["shift_plan"])
        needs = json.loads(request.form["needs"])
        activities = json.loads(request.form["activities"])
        work_hour = json.loads(request.form["work_hour"])
        data = await create_break_plans(shift_plan, needs, activities, work_hour)
        return Response(json.dumps(data), 200)
    elif "export" in request.form:
        export = json.loads(request.form["export"])
        return Response(json.dumps({}), 200)
    return render_template("apps/wfm/index.html", title="WFM")
