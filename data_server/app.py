import json
import subprocess

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/data")
def data():
    data = [(1, 2),
            (2, 2.5),
            (3, 2)]
    output = []
    for point in data:
        output.append({"x": point[0], "y": point[1]})
    return json.dumps(output)


@app.route("/temp")
def temp():
    data = subprocess.check_output(["tail", "-n1", "../temp_data_water.csv"]).decode()
    timestamp, greenhouse_temp, porch_temp, water_temp, inside1_temp, inside2_temp = data.strip().split(",")

    greenhouse_f = round(float(greenhouse_temp) * 9 / 5 + 32, 1)
    water_f = round(float(water_temp) * 9 / 5 + 32, 1)
    porch_f = round(float(porch_temp) * 9 / 5 + 32, 1)
    inside_f = round((float(inside1_temp) + float(inside2_temp))/2 * 9 / 5 + 32, 1)

    return json.dumps(
        {"Greenhouse": "{:0.1f}°F".format(greenhouse_f),
         "Greenhouse water": "{:0.1f}°F".format(water_f),
         "Front Porch": "{:0.1f}°F".format(porch_f),
         "Inside": "{:0.1f}°F".format(inside_f)
         })


if __name__ == '__main__':
    app.run()
