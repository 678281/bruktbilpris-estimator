# Bruktbilpris-estimator

En nettside som estimerer markedsverdien til en bruktbil basert på merke, modell,
årsmodell, kjørelengde, girkasse, drivstoff og motorstørrelse.
Laget som prosjektoppgave i DAT158 Maskinlæring.

**Prøv nettsiden:** 

https://bruktbilpris-estimator-5tmcjdappafjcqsblcj8uny.streamlit.app

## Resultater

Den endelige modellen er en tunet gradient boosting-modell.

| Modell | MAE (testsett) | R² |
|---|---|---|
| Baseline (median) | £6 789 | −0,05 |
| Ridge-regresjon | £2 288 | 0,862 |
| Random forest | £1 402 | 0,947 |
| Gradient boosting (tunet) | £1 306 | 0,952 |

Modellen bommer i snitt med omtrent 8 % på biler den ikke har sett før.
Se rapporten for en fullstendig beskrivelse.

## Innhold i repoet

| Fil/mappe | Beskrivelse |
|---|---|
| `analyse.ipynb` | Hele analysen: innlesing, rensing, utforskning, modellering og evaluering |
| `app.py` | Nettsiden (Streamlit) |
| `model.joblib` | Den trente modellen |
| `meta.json` | Informasjon nettsiden bruker (merker, modeller, feilmargin) |
| `data/` | Datasettet |
| `figurer/` | Grafer brukt i rapporten |
| `requirements.txt` | Python-pakker med versjoner |
| `Bruktbilpris-estimator-rapport.pdf` | Rapporten |

## Data

Datasettet er «100,000 UK Used Car Data set» fra Kaggle:
https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes. Lisens: [CC0: Public Domain].
Det inneholder omtrent 100 000 bruktbilannonser fra Storbritannia, fordelt på ni bilmerker.

## Kjøre prosjektet selv

Krever Python 3.9.

**1. Last ned repoet og installer pakkene**

```bash
git clone https://github.com/678281/bruktbilpris-estimator
cd bruktbilpris-estimator
python3 -m venv .venv
source .venv/bin/activate        # På Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install notebook
```

**2. Reprodusere analysen og trene modellen**

```bash
jupyter notebook analyse.ipynb
```

Velg *Run → Run All Cells*. Notebooken leser dataene, renser dem, trener og
evaluerer modellene, og lagrer den beste modellen som `model.joblib` og `meta.json`.
Tuningen (GridSearchCV) tar noen minutter.

**3. Starte nettsiden lokalt**

```bash
streamlit run app.py
```

Nettsiden åpnes på http://localhost:8501.

## Deployment

Nettsiden er publisert med Streamlit Community Cloud:

1. Logg inn på share.streamlit.io med GitHub-kontoen.
2. Velg *Create app*, og velg dette repoet, branch `main` og filen `app.py`.
3. Under *Advanced settings* velger du Python 3.9.
4. Klikk *Deploy*.

## Begrensninger

- Prisene er i britiske pund og gjenspeiler det britiske markedet rundt 2020.
- Modellen dekker bare de ni bilmerkene i datasettet og biler fra 2000–2020.
- Modellen kjenner ikke til bilens tilstand, utstyr eller servicehistorikk.

## Forfattere

Jonas Berdal Holm
Shahoz Shwana
Alexander Dahle

## Kilder og bruk av KI

- Datasett: https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes
- scikit-learn, pandas, matplotlib og Streamlit
- Claude (Anthropic) ble brukt gjennom hele prosjektet: til å skrive og forklare
  store deler av koden, forklare metoder, feilsøke utviklingsmiljøet og skrive
  utkast til store deler av rapporten, som gruppen deretter gikk gjennom og redigerte.