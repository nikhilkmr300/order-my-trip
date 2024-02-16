import os

from flask import Flask, render_template, request

from core.matrices import *
from core.tsp import *

app = Flask(__name__)


def get_ip(request):
    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        return request.environ["REMOTE_ADDR"]
    else:
        return request.environ["HTTP_X_FORWARDED_FOR"]


@app.route("/", methods=["POST", "GET"])
def main():
    app.logger.info(f"Client at {get_ip(request)} accessed endpoint /.")

    if request.method == "GET":
        return render_template(
            "landing.html",
            GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
            origin="Seattle",
            waypoints="Los Angeles|Austin|Atlanta|New York",
            destination="Seattle",
        )
    else:
        locs = request.form.getlist("textbox[]")
        distances, times = build_matrices(locs)

        min_distance, min_time = None, None
        min_distance, min_path = tsp_dp(distances)

        if len(min_path) == 2:
            return render_template(
                "landing.html",
                GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
                origin=f"{min_path[0]}",
                destination=f"{min_path[-1]}",
            )
        else:
            return render_template(
                "landing.html",
                GMAPS_API_KEY=os.environ["GMAPS_API_KEY"],
                origin=f"{min_path[0]}",
                waypoints=format_locs(min_path[1:-1]),
                destination=f"{min_path[-1]}",
                min_path=min_path,
                min_distance=min_distance,
                min_time=min_time
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
