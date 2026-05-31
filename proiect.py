"""
Echipa: 31-E8
Studenti: GOLUBOV RAUL-IOAN, GODJA ALEXANDRU-MIHAI
Tema proiect: D6-T2 | Procesarea unui flux de date

Surse și documentație reutilizată:
1. Documentație NewsAPI: https://newsapi.org/docs/client-libraries/python
2. Documentație Matplotlib: https://matplotlib.org/stable/gallery/lines_bars_and_markers/fill_between_alpha.html#sphx-glr-gallery-lines-bars-and-markers-fill-between-alpha-py
"""

from newsapi import NewsApiClient
import csv
from collections import Counter
import matplotlib.pyplot as plt

#CONFIGURARE
API_KEY = '197a09165f7d4a4bbd11c82cbe2e8a20'


def preia_stiri(subiect):
    """
    Interoghează News API pentru a obține știrile despre un subiect dat.
    Returnează un dicționar cu numărul de articole publicate în fiecare zi.
    """
    newsapi = NewsApiClient(api_key=API_KEY)
    raspuns = newsapi.get_everything(q=subiect, language='en', sort_by='relevancy', page_size=100)

    date_publicare = []

    for articol in raspuns['articles']:
        data_zi = articol['publishedAt'].split('T')[0]
        date_publicare.append(data_zi)

    numar_pe_zile = Counter(date_publicare)
    return numar_pe_zile


def salveaza_in_csv(date_dict, nume_fisier="flux_stiri.csv"):
    """
    Primește dicționarul cu date și numărul de știri și le stochează într-un fișier CSV.
    """
    date_sortate = sorted(date_dict.items())

    with open(nume_fisier, mode='w', newline='', encoding='utf-8') as fisier_csv:
        scriitor = csv.writer(fisier_csv)
        scriitor.writerow(["Data", "Numar Stiri"])

        for data, numar in date_sortate:
            scriitor.writerow([data, numar])

    print(f"Datele au fost salvate cu succes în fișierul '{nume_fisier}'!")


def afiseaza_grafic(nume_fisier="flux_stiri.csv"):
    """
    Citește datele din fișierul CSV și generează graficul evoluției.
    """
    zile = []
    numar_stiri = []

    with open(nume_fisier, mode='r', encoding='utf-8') as fisier_csv:
        cititor = csv.reader(fisier_csv)
        next(cititor)

        for rand in cititor:
            zile.append(rand[0])
            numar_stiri.append(int(rand[1]))

    """
    Configurarea și afișarea graficului
    """
    plt.figure(figsize=(10, 6))
    plt.plot(zile, numar_stiri, marker='o', color='royalblue', label='Număr articole')


    plt.fill_between(zile, numar_stiri, alpha=0.3, color='royalblue')

    plt.title("Evoluția știrilor în funcție de timp")
    plt.xlabel("Timp (Zile)")
    plt.ylabel("Număr de știri publicate")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    subiect_cautare = "Hormuz"

    print(f"--- Colectare date pentru subiectul: {subiect_cautare} ---")


    date_stiri = preia_stiri(subiect_cautare)
    if len(date_stiri) > 0:
        salveaza_in_csv(date_stiri)
        afiseaza_grafic()
    else:
        print("Nu s-au găsit știri recente pentru acest subiect.")