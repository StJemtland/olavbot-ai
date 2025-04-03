import pandas as pd
import datetime

# Last inn loggene fra bot_v5
try:
    transaksjoner = pd.read_csv("transaksjonslogg_v5.csv")
    beslutninger = pd.read_csv("beslutningslogg_v5.csv")
except FileNotFoundError:
    print("Fant ikke loggfilene. Kjør bot_v5.py først.")
    raise SystemExit

# Hent dagens dato
i_dag = datetime.date.today()

# Filtrer dagens hendelser
dagens_beslutninger = beslutninger[beslutninger["Dato"] == str(i_dag)]
dagens_transaksjoner = transaksjoner[transaksjoner["Transaksjoner"].str.startswith(str(i_dag))]

# Finn potensielle kjøp (lav RSI)
anbefalte_kjop = dagens_beslutninger[
    (dagens_beslutninger["RSI"] < 30) &
    (dagens_beslutninger["Handling"] == "Ingen handling")
]

# Estimert oppside basert på RSI-nivå
anbefalte_kjop["Estimert Oppside (%)"] = (70 - anbefalte_kjop["RSI"]) * 1.2

# Finn potensielle salg
salgs_signaler = dagens_beslutninger[
    (dagens_beslutninger["RSI"] > 70) &
    (dagens_beslutninger["Handling"] == "Ingen handling")
]

# Lag rapporttekst
rapport_tekst = "\n📊 DAGSRAPPORT FRA AI-FORVALTER\n"
rapport_tekst += f"🗓️ Dato: {i_dag}\n\n"

rapport_tekst += "💰 Transaksjoner i dag:\n"
if not dagens_transaksjoner.empty:
    for t in dagens_transaksjoner["Transaksjoner"]:
        rapport_tekst += f"  - {t}\n"
else:
    rapport_tekst += "  Ingen kjøp eller salg i dag.\n"

rapport_tekst += "\n📈 Potensielle kjøp:\n"
if not anbefalte_kjop.empty:
    for _, row in anbefalte_kjop.iterrows():
        rapport_tekst += f"  - {row['Asset']} (RSI: {row['RSI']}), Estimert oppside: {round(row['Estimert Oppside (%)'], 1)}%\n"
else:
    rapport_tekst += "  Ingen anbefalte kjøp nå.\n"

rapport_tekst += "\n📉 Mulige salg:\n"
if not salgs_signaler.empty:
    for _, row in salgs_signaler.iterrows():
        rapport_tekst += f"  - {row['Asset']} (RSI: {row['RSI']}) – vurder å selge.\n"
else:
    rapport_tekst += "  Ingen klare salgssignaler.\n"

rapport_tekst += "\n🧠 AI-kommentar:\n"
if not anbefalte_kjop.empty:
    rapport_tekst += "Markedet gir kjøpsmuligheter. RSI indikerer oversolgt – potensiale for gevinst.\n"
elif not dagens_transaksjoner.empty:
    rapport_tekst += "Boten handlet basert på markedssignalene. Vi følger strategien.\n"
else:
    rapport_tekst += "Rolig marked. Boten avventer sterkere signaler før neste handling.\n"

# Skriv til fil
with open("dagens_ai_rapport.txt", "w") as f:
    f.write(rapport_tekst)

# Vis i terminal
print(rapport_tekst)
