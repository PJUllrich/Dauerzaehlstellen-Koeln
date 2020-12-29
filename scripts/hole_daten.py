import requests
import json
import csv
import os
from datetime import datetime, timedelta
from collections.abc import Iterable


ID_KOELN = 677
URL_COUNTER_LIST = f'https://www.eco-visio.net/api/aladdin/1.0.0/pbl/publicwebpageplus/{ID_KOELN}?withNull=true'
URL_COUNTER_DATA = 'https://www.eco-visio.net/api/aladdin/1.0.0/pbl/publicwebpageplus/data'
DATEN_FOLDER_PATH = 'daten/'

PROXY_URL = os.environ['PROXY_URL']
PROXIES = {'http': PROXY_URL, 'https': PROXY_URL}


def get(url, params=None):
    return requests.get(url, params=params, proxies=PROXIES)


def hole_datum_des_letzten_updates():
    try:
        with open(DATEN_FOLDER_PATH + 'letztes_update.txt', "r") as f:
            return f.read()
    except IOError:
        return None


def update_datum_des_letzten_updates(datum):
    with open(DATEN_FOLDER_PATH + 'letztes_update.txt', "w") as f:
        f.write(datum.strftime("%d/%m/%Y"))


def hole_daten(von, bis):
    uebersicht = hole_zaehler_uebersicht(save=False)
    for row in uebersicht:
        idPdc = row['idPdc']
        flowIds = ";".join([str(flowId['id']) for flowId in row['pratique']])
        filename = row['nom'].replace(' ', '_').lower()
        hole_zaehler_details(idPdc, flowIds, von, bis, filename)


# Hole Daten zu allen Dauerzaehlstellen
def hole_zaehler_uebersicht(save=False):
    r = get(URL_COUNTER_LIST)
    if save:
        with open(DATEN_FOLDER_PATH + 'counter_list.json', 'w') as f:
            json.dump(r.json(), f)
    else:
        return r.json()


# Holt die Zählerstände fuer einen Zaehler und speichert diese
def hole_zaehler_details(idPdc, flowIds, von, bis, filename, append=True, interval=4):
    # interval: 4 = taeglich, 5 = woechentlich, 6 = monatlich
    params = {
        'idOrganisme': ID_KOELN,
        'idPdc': idPdc,
        'debut': von,
        'fin': bis,
        'interval': interval,
        'flowIds': flowIds
    }
    url = f'{URL_COUNTER_DATA}/{idPdc}'
    r = get(url, params)

    mode = 'a' if append else 'w'

    with open(DATEN_FOLDER_PATH + filename + '.csv', mode=mode) as f:
        writer = csv.writer(
            f, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not append:
            writer.writerow(['Datum', 'Zaehlerstand'])

        try:
            for row in r.json():
                if isinstance(row, Iterable):
                    date = datetime.strptime(row[0], "%m/%d/%Y")
                    date_german = date.strftime("%d.%m.%Y")
                    count = int(float(row[1]))

                    writer.writerow([date_german, count])
        except json.decoder.JSONDecodeError:
            print(f'{idPdc}: {r.text}')


# Holt alle Zaehlerstaende fuer einen Zeitraum fuer alle Zaehler
def hole_alle_zaehler_details():
    von = '01/06/2016'
    bis = '05/10/2020'

    hole_daten(von, bis)


def hole_neue_daten():
    heute = datetime.today()
    str_datum_heute = heute.strftime("%d/%m/%Y")
    str_datum_letztes = hole_datum_des_letzten_updates()

    hole_daten(str_datum_letztes, str_datum_heute)

    update_datum_des_letzten_updates(heute)


if __name__ == "__main__":
    hole_neue_daten()
