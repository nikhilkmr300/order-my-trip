import os

from flask import Flask, render_template, request

from core.matrices import *
from core.tsp import *

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "GET":
        return render_template(
            "landing.html", GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
            origin="Seattle",
            waypoints="Los Angeles|Austin|Atlanta|New York",
            destination="Seattle"
        )
    else:
        locs = request.form.getlist("textbox[]")
        distances, times = build_matrices(locs)
        _, path = tsp_dp(distances)

        if len(path) == 2:
            return render_template(
                "landing.html", GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
                origin=f"{path[0]}",
                destination=f"{path[-1]}"
            )
        else:
            print(path)
            return render_template(
                "landing.html",
                GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
                origin=f"{path[0]}",
                waypoints=format_locs(path[1:-1]),
                destination=f"{path[-1]}"
            )
