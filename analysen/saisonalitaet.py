from load_data import LoadData

import matplotlib.pyplot as plt
import holidays
import pandas as pd

h = holidays.Germany()


def plot_df(df, name, linestyle="dotted", **kwargs):
    dfy = df[df["Datum"].dt.year.between(2018, 2019)]
    dfy = dfy[dfy["Datum"].dt.weekday < 5]
    dfy = dfy[dfy.apply(lambda x: x["Datum"] not in h, axis=1)]
    dg = dfy.groupby(dfy["Datum"].dt.month).mean()
    plt.plot(dg, label=name, linestyle=linestyle, **kwargs)


pendlerstrecken = [1, 2, 4, 5, 6, 13]
freizeitstrecken = [7, 9, 10, 11, 12]
files = LoadData.load(freizeitstrecken)
avg_df = pd.DataFrame({"Datum": [], "Zaehlerstand": []})


for key, data in files.items():
    avg_df = avg_df.append(data)
    plot_df(data, LoadData.NAMINGS[key], linewidth=1.0)

plot_df(avg_df, "Durchschnitt", linestyle="solid", linewidth=3.0, c="k")

plt.ylim(0)
plt.xlim(1, 12)
plt.grid(True)
plt.legend()
plt.title(
    'Durchschnittliche Radzahlen auf "Freizeitstrecken" pro Monat und Messstelle (Zeitraum 2018 und 2019)'
)
plt.show()
