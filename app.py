import streamlit as st
import numpy as np
import pandas as pd
import math

# --- Seitenlayout ---
st.set_page_config(page_title="Satteldach Rechner", layout="wide")
st.title("🏠 Satteldach-Berechnung mit Erlus Großfalzziegel")
st.markdown("Berechne Ziegelbedarf, Sparrenlänge, Lattung und zeige eine schematische Seitenansicht des Daches.")

# --- Eingabebereich ---
st.sidebar.header("🔧 Eingabewerte")
dachbreite_m = st.sidebar.number_input("Dachbreite (m)", min_value=1.0, value=10.0)
dachlaenge_m = st.sidebar.number_input("Dachlänge (m)", min_value=1.0, value=4.0)
neigung_deg = st.sidebar.number_input("Dachneigung (°)", min_value=5.0, max_value=45.0, value=18.0)

deckbreite = st.sidebar.number_input("Ziegel Deckbreite (mm)", value=225)
decklaenge = st.sidebar.number_input("Ziegel Decklänge (mm)", value=340)
ortgangbreite = st.sidebar.number_input("Ortgangziegel Deckbreite (mm)", value=200)

sparrenabstand_m = st.sidebar.number_input("Sparrenabstand (m)", value=0.6)
lattabstand_m = decklaenge / 1000  # m

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

# --- Ergebnisdarstellung ---
st.subheader("📐 Berechnete Werte")
col1, col2 = st.columns(2)

with col1:
    st.metric("Effektive Dachbreite (m)", effektive_breite / 1000)
    st.metric("Effektive Dachlänge (m)", effektive_laenge / 1000)
    st.metric("Dachfläche (m²)", round(flaeche_m2, 2))
    st.metric("Sparrenlänge (m)", sparrenlaenge_m)

with col2:
    st.metric("Ziegelanzahl (gesamt)", gesamt_ziegel)
    st.metric("Reserve (5%)", reserve)
    st.metric("Ziegel inkl. Reserve", gesamt_ziegel_mit_reserve)
    st.metric("Anzahl Sparren", anzahl_sparren)

# --- Materialübersicht ---
st.subheader("📦 Materialbedarf")

material_df = pd.DataFrame({
    "Material": [
        "Dachziegel (inkl. Reserve)",
        "Ortgangziegel",
        "Sparren (lfm)",
        "Dachschalung (m²)",
        "Dachpappe (m², mit 10% Überlappung)",
        "Dachlatten (lfm)"
    ],
    "Menge": [
        gesamt_ziegel_mit_reserve,
        2 * anzahl_ziegel_laenge,
        round(anzahl_sparren * sparrenlaenge_m, 2),
        round(flaeche_m2, 2),
        round(flaeche_m2 * 1.1, 2),
        round(anzahl_ziegel_laenge * (dachbreite_m / 0.4) * 2)
    ],
    "Einheit": ["Stk", "Stk", "m", "m²", "m²", "lfm"]
})
st.table(material_df)

# --- Visualisierung ---
st.subheader("📊 Visualisierung: Seitenansicht der Sparren- & Lattungseinteilung")

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))
for y in range(anzahl_lattten):
    ax.hlines(y, 0, anzahl_sparren - 1, colors='dodgerblue', linewidth=2)

for x in range(anzahl_sparren):
    ax.vlines(x, 0, anzahl_lattten - 1, colors='darkgreen', linewidth=1.5, linestyles='dashed')

ax.set_title("Sparren (grün, vertikal) & Latten (blau, horizontal)")
ax.set_xticks(range(anzahl_sparren))
ax.set_yticks(range(anzahl_lattten))
ax.set_xlabel("Sparren")
ax.set_ylabel("Dachlatten (Reihen)")
ax.invert_yaxis()
st.pyplot(fig)
