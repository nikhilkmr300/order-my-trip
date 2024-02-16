import json
import os

import pandas as pd
import requests


def format_locs(locs):
    return "|".join([loc.replace("|", "") for loc in locs])


def build_matrices(locs):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json",
        params={
            "origins": format_locs(locs),
            "destinations": format_locs(locs),
            "language": "en-US",
            "key": os.environ["GMAPS_API_KEY"],
        },
    )
    response = json.loads(response.text)

    # Standardizing locs names
    locs = response["origin_addresses"]

    distances = pd.DataFrame(index=locs, columns=locs)
    times = pd.DataFrame(index=locs, columns=locs)

    for i, row in enumerate(response["rows"]):
        for j, element in enumerate(row["elements"]):
            distances.iloc[i, j] = element["distance"]["value"]
            times.iloc[i, j] = element["duration"]["value"]

    return distances, times
