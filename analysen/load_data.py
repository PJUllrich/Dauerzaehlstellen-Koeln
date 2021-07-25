import pandas as pd
import datetime


class LoadData:
    MAPPING = {
        1: "01_bonner_straße_rad",
        2: "02_venloer_straße_rad",
        4: "04_hohenzollernbrücke",
        5: "05_deutzer_brücke_kpl.",
        6: "06_neumarkt_kpl",
        7: "07_alfred_schütte_kpl",
        8: "08_vorgebirgspark",
        9: "09_alphons-sibermann-weg",
        10: "10_stadtwald",
        11: "11_niederländer_ufer",
        12: "12_vorgebirgswall",
        13: "universitätsstr._kpl",
        14: "zülpicher_neu_kpl",
    }

    NAMINGS = {
        1: "Bonner Str.",
        2: "Venloer Str.",
        4: "Hohenzollerbrücke",
        5: "Deutzer Brück",
        6: "Neumarkt",
        7: "Alfred-Schütte-Allee",
        8: "Vorgebirgspark",
        9: "Alphons-Sibermann-Weg",
        10: "Stadtwald",
        11: "Niederländer Ufer",
        12: "Vorgebirgswall",
        13: "Universitätsstr.",
        14: "Zülpicher Str.",
    }

    def load(keys):
        files = {}
        for key, value in LoadData.MAPPING.items():
            if key not in keys:
                continue

            fp = LoadData.__filepath(value)
            d = pd.read_csv(fp, parse_dates=["Datum"], date_parser=LoadData.__parsedate)
            files[key] = d

        return files

    def __parsedate(v):
        return datetime.datetime.strptime(v, "%d.%m.%Y")

    def __filepath(name):
        return f"./daten/{name}.csv"
