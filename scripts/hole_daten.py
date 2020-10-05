import requests
import json
import csv
from datetime import datetime, timedelta
from collections.abc import Iterable

ID_KOELN = 677
URL_COUNTER_LIST = 'http://www.eco-public.com/ParcPublic/GetCounterList'
URL_COUNTER_DATA = 'http://www.eco-public.com/ParcPublic/CounterData'
DATEN_FOLDER_PATH = 'daten/'


def hole_datum_des_letzten_updates():
    try:
        with open(DATEN_FOLDER_PATH + 'letztes_update.txt', "r") as f:
            return datetime.strptime(f.read(), "%d/%m/%Y")
    except IOError:
        return None


def update_datum_des_letzten_updates(datum):
    with open(DATEN_FOLDER_PATH + 'letztes_update.txt', "w") as f:
        f.write(datum.strftime("%d/%m/%Y"))


def hole_daten(von, bis):
    uebersicht = hole_zaehler_uebersicht(save=False)
    for row in uebersicht:
        idPdc = row['idPdc']
        filename = row['nom'].replace(' ', '_').lower()
        hole_zaehler_details(idPdc, von, bis, filename)


# Hole Daten zu allen Dauerzaehlstellen
def hole_zaehler_uebersicht(save=False):
    r = requests.post(URL_COUNTER_LIST, data={'id': ID_KOELN})
    if save:
        with open(DATEN_FOLDER_PATH + 'counter_list.json', 'w') as f:
            json.dump(r.json(), f)
    else:
        return r.json()


# Holt die Zählerstände fuer einen Zaehler und speichert diese
def hole_zaehler_details(idPdc, von, bis, filename, append=True, interval=4):
    # interval: 4 = taeglich, 5 = woechentlich, 6 = monatlich
    r = requests.post(URL_COUNTER_DATA, data={
        'idOrganisme': ID_KOELN,
        'idPdc': idPdc,
        'debut': von,
        'fin': bis,
        'interval': interval,
        'pratiques': ''
    })

    mode = 'a' if append else 'w'

    with open(DATEN_FOLDER_PATH + filename + '.csv', mode=mode) as f:
        writer = csv.writer(
            f, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if not append:
            writer.writerow(['Datum', 'Zaehlerstand'])

        for row in r.json():
            if isinstance(row, Iterable):
                date_german = datetime.strptime(
                    row[0], "%m/%d/%Y").strftime("%d.%m.%Y")
                count = int(float(row[1]))

                writer.writerow([date_german, count])


# Holt alle Zaehlerstaende fuer einen Zeitraum fuer alle Zaehler
def hole_alle_zaehler_details():
    von = '01/06/2016'
    bis = '05/10/2020'

    hole_daten(von, bis)


def hole_daten_fuer_gestern():
    gestern = datetime.today() - timedelta(days=1)
    letztes_update_am = hole_datum_des_letzten_updates()

    str_datum_gestern = gestern.strftime("%d/%m/%Y")

    if letztes_update_am is None or letztes_update_am.date() == gestern.date():
        hole_daten(str_datum_gestern, str_datum_gestern)
    elif letztes_update_am.date() < gestern.date():
        datum_ab_wann_daten_fehlen = letztes_update_am + timedelta(days=1)
        str_datum_fehlend = datum_ab_wann_daten_fehlen.strftime("%d/%m/%Y")
        hole_daten(str_datum_fehlend, str_datum_gestern)

    update_datum_des_letzten_updates(gestern)


if __name__ == "__main__":
    hole_daten_fuer_gestern()
