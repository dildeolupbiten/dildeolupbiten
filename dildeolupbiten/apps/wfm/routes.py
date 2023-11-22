# -*- coding: utf-8 -*-

from flask import render_template, Blueprint

wfm = Blueprint("wfm", __name__)


@wfm.route("/wfm", methods=["GET", "POST"])
def index():
    return render_template("apps/wfm/index.html", title="WFM")
