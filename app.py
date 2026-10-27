import json
import os

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Bruktbilpris-estimator", page_icon="🚗")

MAPPE = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def last_modell():
    modell = joblib.load(os.path.join(MAPPE, "model.joblib"))
    with open(os.path.join(MAPPE, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    return modell, meta


modell, meta = last_modell()

st.title("Bruktbilpris-estimator")
st.write("Fyll inn opplysninger om bilen, så estimerer modellen hva den er verdt.")

kol1, kol2 = st.columns(2)

with kol1:
    merke = st.selectbox("Merke", list(meta["modeller_per_merke"].keys()))
    bilmodell = st.selectbox("Modell", meta["modeller_per_merke"][merke])
    aar = st.slider("Årsmodell", meta["aar"][0], meta["aar"][1], 2017)
    km = st.number_input("Kjørelengde (km)", min_value=0, max_value=500_000,
                         value=30_000, step=1_000)

with kol2:
    girkasse = st.selectbox("Girkasse", meta["girkasser"])
    drivstoff = st.selectbox("Drivstoff", meta["drivstoff"])
    motor = st.number_input("Motorstørrelse (liter)", min_value=0.0, max_value=6.6,
                            value=1.6, step=0.1)
    

if st.button("Estimer pris", type="primary"):
    bil = pd.DataFrame([{
        "brand": merke,
        "model": bilmodell,
        "year": aar,
        "mileage": km / 1.609,
        "transmission": girkasse,
        "fuelType": drivstoff,
        "engineSize": motor,
    }])

    pris = float(modell.predict(bil)[0])
    margin = meta["feil_prosent"] / 100

    st.metric("Estimert pris", f"£{pris:,.0f}")
    st.write(f"Typisk prisområde: **£{pris * (1 - margin):,.0f} – £{pris * (1 + margin):,.0f}**")
    st.caption(f"Modellen bommer i snitt med omtrent {meta['feil_prosent']} % på biler den ikke har sett før.")

with st.expander("Om modellen"):
    st.write(
        "Modellen er en gradient boosting-modell trent på omtrent 97 000 bruktbilannonser "
        "fra Storbritannia (2000–2020). Prisene er derfor i britiske pund og gjenspeiler "
        "det britiske markedet rundt 2020, ikke dagens norske priser."
    )
    st.write(f"Gjennomsnittlig feil på testdata: £{meta['mae']:,} ({meta['feil_prosent']} %).")