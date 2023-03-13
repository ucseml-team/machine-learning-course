# requires: orbit-predictor, requests (pip install orbit-predictor requests)
from datetime import datetime

import requests
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.locations import Location

objects = (
    ("iss", "zarya", 25544),
    ("newsat-3", "milanesat", 42760),
    ("newsat-28", "alice", 52747),
    ("newsat-29", "edith", 52764),
    ("newsat-30", "margherita", 52748),
    ("newsat-31", "ruby", 52752),
)

start = datetime(2023, 1, 1)
end = datetime(2024, 1, 1)

location = Location("UCSE DAR", latitude_deg=-31.266933, longitude_deg=-61.496106, elevation_m=90)

with open("./sate_passes.csv", "w") as passes_file:
    passes_file.write("sate,nickname,norad_id,start,center,end,elevation\n")

    for object_id, object_nick, norad_id in objects:
        print("Getting tle for", object_id)
        response = requests.get(f"https://celestrak.com/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle")
        tle_lines = response.content.decode("utf-8").strip().split("\n")[1:3]

        print("Generating passes for", object_id)
        predictor = get_predictor_from_tle_lines(tle_lines)
        for pass_ in predictor.passes_over(location, start, end, max_elevation_gt=10):
            passes_file.write(
                f"{object_id},{object_nick},{norad_id},"
                f"{pass_.aos.isoformat()},{pass_.max_elevation_date.isoformat()},{pass_.los.isoformat()},"
                f"{pass_.max_elevation_deg}\n"
            )
