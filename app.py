import streamlit as st
import numpy as np
import pandas as pd
import math
#import matplotlib.pyplot as plt

# --- App Konfiguration ---
st.set_page_config(page_title="Satteldach Rechner", layout="wide")

st.title("🏠 Satteldach-Rechner")
st.caption("Inkl. Visualisierung, Materialbedarf und statischer Einschätzung – mit Schneelast Südostbayern")

# --- Ziegelprofile ---
ziegelprofile = {
    "Erlus Großfalzziegel": {"deckbreite": 225, "decklaenge": 340, "ortgang": 200},
    "Braas Harzer Pfanne": {"deckbreite": 235, "decklaenge": 330, "ortgang": 220},
    "Creaton Futura": {"deckbreite": 245, "decklaenge": 345, "ortgang": 210},
}

# --- Eingaben ---
st.sidebar.header("🔧 Eingabewerte")
#st.image("https://images.pexels.com/photos/175709/pexels-photo-175709.jpeg", width=100)
profilwahl = st.sidebar.selectbox("Ziegelprofil", list(ziegelprofile.keys()))
dachbreite_m = st.sidebar.number_input("Dachbreite (m)", 4.0, 20.0, 10.0)
dachlaenge_m = st.sidebar.number_input("Dachlänge (m)", 2.0, 20.0, 4.0)
neigung_deg = st.sidebar.slider("Dachneigung (°)", 10, 45, 18)
lattenstaerke = st.sidebar.radio("Lattenstärke (cm)", ["3×5", "4×6"])
sparrenabstand_m = st.sidebar.select_slider("Sparrenabstand (m)", options=[0.5, 0.6, 0.7], value=0.6)

# --- Ziegelmaße aus Profil ---
deckbreite = ziegelprofile[profilwahl]["deckbreite"]
decklaenge = ziegelprofile[profilwahl]["decklaenge"]
ortgangbreite = ziegelprofile[profilwahl]["ortgang"]
lattabstand_m = decklaenge / 1000

# --- Berechnungen ---
dachbreite_mm = dachbreite_m * 1000
dachlaenge_mm = dachlaenge_m * 1000
anzahl_ziegel_breite = int((dachbreite_mm - 2 * ortgangbreite) // deckbreite)
effektive_breite = anzahl_ziegel_breite * deckbreite + 2 * ortgangbreite
anzahl_ziegel_laenge = int(dachlaenge_mm // decklaenge)
effektive_laenge = anzahl_ziegel_laenge * decklaenge

flaeche_m2 = (effektive_breite * effektive_laenge) / 1_000_000 * 2
gesamt_ziegel = anzahl_ziegel_breite * anzahl_ziegel_laenge * 2
reserve = int(gesamt_ziegel * 0.05)
gesamt_ziegel_mit_reserve = gesamt_ziegel + reserve

neigung_rad = math.radians(neigung_deg)
sparrenlaenge_m = round((dachbreite_m / 2) / math.cos(neigung_rad), 2)
anzahl_sparren = int(dachlaenge_m / sparrenabstand_m) + 1
anzahl_lattten = int(sparrenlaenge_m / lattabstand_m) + 1

# --- Schnürung alle 5 Ziegelbreiten ---
schnuerung_abstand_cm = 5 * deckbreite / 10
anzahl_schnuerungen = int((effektive_breite / 10) // schnuerung_abstand_cm) + 1

# --- Sparrendimension basierend auf Dachlast ---
gesamtlast_kN_m2 = 0.85 + 1.5  # Eigenlast + Schneelast
q = gesamtlast_kN_m2 * sparrenabstand_m
M = q * sparrenlaenge_m**2 / 8  # in kNm
sparrenempf = "≥ 8×18 cm (C24)" if M <= 4.0 else "≥ 8×20 cm (C24)"

# --- Ergebnisanzeige ---
st.subheader("📐 Ergebnisse")
col1, col2 = st.columns(2)
with col1:
    st.metric("Effektive Dachbreite (m)", round(effektive_breite / 1000, 2))
    st.metric("Dachfläche (m²)", round(flaeche_m2, 2))
    st.metric("Sparrenlänge (m)", sparrenlaenge_m)
    st.metric("Empfohlene Sparrendimension", sparrenempf)
with col2:
    st.metric("Ziegelanzahl (inkl. Reserve)", gesamt_ziegel_mit_reserve)
    st.metric("Dachlatten (Stück)", anzahl_lattten)
    st.metric("Schnürungen (alle 5 Deckbreiten)", anzahl_schnuerungen)
    st.metric("Ortgangziegel (gesamt)", 2 * anzahl_ziegel_laenge)
'''
# --- Materialübersicht ---
st.subheader("📦 Materialbedarf")
material_df = pd.DataFrame({
    "Material": [
        "Dachziegel (inkl. Reserve)",
        "Ortgangziegel",
        "Sparren (lfm)",
        "Dachschalung (m²)",
        "Dachpappe (10% Zuschlag)",
        f"Dachlatten ({lattenstaerke})"
    ],
    "Menge": [
        gesamt_ziegel_mit_reserve,
        2 * anzahl_ziegel_laenge,
        round(anzahl_sparren * sparrenlaenge_m, 2),
        round(flaeche_m2, 2),
        round(flaeche_m2 * 1.1, 2),
        round(anzahl_lattten * (dachbreite_m), 2)
    ],
    "Einheit": ["Stk", "Stk", "m", "m²", "m²", "lfm"]
})
st.table(material_df)

# --- Visualisierung ---
st.subheader("📊 Visualisierung: Seitenansicht – Sparren & Latten")
fig, ax = plt.subplots(figsize=(10, 5))
for y in range(anzahl_lattten):
    ax.hlines(y, 0, anzahl_sparren - 1, colors='dodgerblue', linewidth=2)
for x in range(anzahl_sparren):
    ax.vlines(x, 0, anzahl_lattten - 1, colors='darkgreen', linewidth=1.5, linestyles='dashed')
ax.set_title("Sparren (grün) & Latten (blau)")
ax.set_xticks(range(anzahl_sparren))
ax.set_yticks(range(anzahl_lattten))
ax.invert_yaxis()
ax.set_xlabel("Sparren")
ax.set_ylabel("Latten (Ziegelreihen)")
st.pyplot(fig)
'''
