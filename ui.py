import os

from flask import Flask, render_template, request

from core.tsp import *

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "GET":
        return render_template("landing.html", GMAPS_API_KEY=os.environ["GMAPS_API_KEY"])
    else:
        locs = request.form.getlist("textbox[]")
        print(locs)
        return "Hello"
