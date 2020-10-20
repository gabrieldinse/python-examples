# Author: gabri
# File: cliente_python
# Date: 25/11/2019
# Made with PyCharm

# Standard Library
import datetime
import time
import json

# Third party modules
import requests

# Local application imports


ufsc_latlon = "-26.920941113761874,-49.09862995147705"
locals_latlon = {
    "Vila Germanica": ["-26.914024,-49.085023", "vila_germanica"],
    "Prefeitura Blumenau": ["-26.916379,-49.071185", "pref_blumenau"],
    "Centro Indaial": ["-26.894313,-49.232925", "centro_indaial"],
    "Centro Gaspar": ["-26.932149,-48.954884", "centro_gaspar"],
    "Pomerode": ["-26.751159,-49.173394", "pomerode"]
}


def main():
    while True:
        date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print(f"\nData: {date_time}:")
        for key in locals_latlon:
            url = str(
                f"https://dev.virtualearth.net/REST/v1/Routes/Distanc"
                f"eMatrix?origins={ufsc_latlon}&destinations="
                f"{locals_latlon[key][0]}&travelMode=driving&startTime="
                f"{date_time}-03:00&key=Aq38tkwcBxQIMx4cNwEjgLZ6psiLklV"
                f"ZiUBTmEvXfeUkftkEre2unPQG0ISdUq7b"
            )
            response = requests.get(url).json()
            travel_duration = response[
                "resourceSets"][0][
                "resources"][0]["results"][0]["travelDuration"]
            print(f"UFSC ate {key}: {travel_duration} minutos")
            requests.get("http://192.168.56.106:8080/ScadaBR/httpds?"
                         f"{locals_latlon[key][1]}={travel_duration}")
        time.sleep(1.0)


if __name__ == "__main__":
    main()