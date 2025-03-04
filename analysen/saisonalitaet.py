from load_data import LoadData

import matplotlib.pyplot as plt
import holidays
import pandas as pd

h = holidays.Germany()


def plot_df(df, **kwargs):
    dfy = df[df["Datum"].dt.year.between(2018, 2019)]
    # dfy = dfy[dfy["Datum"].dt.weekday < 5]
    # dfy = dfy[dfy.apply(lambda x: x["Datum"] not in h, axis=1)]
    dfy = dfy[dfy.apply(lambda x: x["Datum"] in h or x["Datum"].weekday() > 4, axis=1)]
    dg = dfy.groupby(dfy["Datum"].dt.month).mean()
    plt.plot(dg, **kwargs)


pendlerstrecken = [1, 2, 4, 5, 6, 13]
freizeitstrecken = [7, 9, 10, 11, 12]
files = LoadData.load(freizeitstrecken)
avg_df = pd.DataFrame({"Datum": [], "Zaehlerstand": []})


for key, data in files.items():
    avg_df = avg_df.append(data)
    plot_df(data, label=LoadData.NAMINGS[key], linestyle="dotted", linewidth=1.5)

plot_df(avg_df, label="Durchschnitt", linestyle="solid", linewidth=3.0, c="k")

plt.ylim(0)
plt.xlim(1, 12)
plt.grid(True)
plt.legend()
plt.title(
    'Durchschnittliche Radzahlen auf "Freizeitstrecken". Nur Feiertage und Wochenenden. Zeitraum 2018 und 2019'
)
plt.show()
