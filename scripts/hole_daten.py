import requests
import json
import csv
from collections.abc import Iterable

ID_KOELN = 677
URL_COUNTER_LIST = 'http://www.eco-public.com/ParcPublic/GetCounterList'
URL_COUNTER_DATA = 'http://www.eco-public.com/ParcPublic/CounterData'
DATEN_FOLDER_PATH = 'Daten/'


# Hole Daten zu allen Dauerzaehlstellen
def hole_zaehler_uebersicht(save=True):
    r = requests.post(URL_COUNTER_LIST, data={'id': ID_KOELN})
    if save:
        with open(DATEN_FOLDER_PATH + 'counter_list.json', 'w') as f:
            json.dump(r.json(), f)
    else:
        return r.json()


# Holt die Zählerstände pro Tag für den Vorgebirgspark
def hole_zaehler_details(idPdc, von, bis, filename, interval=4):
    # interval: 4 = taeglich, 5 = woechentlich, 6 = monatlich
    r = requests.post(URL_COUNTER_DATA, data={
        'idOrganisme': ID_KOELN,
        'idPdc': idPdc,
        'debut': von,
        'fin': bis,
        'interval': interval,
        'pratiques': ''
    })

    with open(DATEN_FOLDER_PATH + filename + '.csv', mode='w') as f:
        writer = csv.writer(
            f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Datum', 'Zaehlerstand'])

        for row in r.json():
            if isinstance(row, Iterable):
                writer.writerow(row)


def hole_alle_zaehler_details():
    von = '01/01/2020'
    bis = '11/04/2020'
    uebersicht = hole_zaehler_uebersicht(save=False)
    for row in uebersicht:
        idPdc = row['idPdc']
        filename = row['nom'].replace(' ', '_').lower()
        hole_zaehler_details(idPdc, von, bis, filename)


if __name__ == "__main__":
    hole_alle_zaehler_details()
