import requests
import json
import csv
from collections.abc import Iterable

ID_KOELN = 677
URL_COUNTER_LIST = 'http://www.eco-public.com/ParcPublic/GetCounterList'
URL_COUNTER_DATA = 'http://www.eco-public.com/ParcPublic/CounterData'
DATEN_FOLDER_PATH = 'Daten/'


# Hole Daten zu allen Dauerzaehlstellen
def hole_zaehler_uebersicht():
    r = requests.post(URL_COUNTER_LIST, data={'id': ID_KOELN})
    with open(DATEN_FOLDER_PATH + 'counter_list.json', 'w') as f:
        json.dump(r.json(), f)


# Holt die Zählerstände pro Tag für den Vorgebirgspark
def hole_zaehler_details():
    # interval: 4 = taeglich, 5 = woechentlich, 6 = monatlich
    # idPdc: 100019755 scheint die Id fuer den Zaehler im Vorgebirgspark zu sein
    r = requests.post(URL_COUNTER_DATA, data={
        'idOrganisme': ID_KOELN,
        'idPdc': '100019755',
        'fin': '11/04/2020',
        'debut': '01/01/2020',
        'interval': 4,
        'pratiques': ''
    })

    with open(DATEN_FOLDER_PATH + 'vorgebirgspark.csv', mode='w') as f:
        writer = csv.writer(
            f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Datum', 'Zaehlerstand'])

        for row in r.json():
            if isinstance(row, Iterable):
                writer.writerow(row)


if __name__ == "__main__":
    hole_zaehler_details()
