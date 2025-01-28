import numpy as np
import pandas as pd

# Funzione per il calcolo della variazione sinusoidale
def variazione_sinusoidale(mese, media, ampiezza, sfasamento):
    return media + ampiezza * np.sin((2 * np.pi * (mese - sfasamento)) / 12)

# Funzione per calcolare il dato meteo con fluttuazioni realistiche
def calcola_meteo_realistico(giorno, media_mensile, ampiezza, sfasamento, fluttuazione_range, clip_min, clip_max):
    mese = giorno.month
    base = variazione_sinusoidale(mese, media_mensile[mese], ampiezza, sfasamento)
    
    # Fluttuazione realistica con una distribuzione normale
    fluttuazione = np.random.normal(0, (fluttuazione_range[1] - fluttuazione_range[0]) / 3)
    
    return round(np.clip(base + fluttuazione, clip_min, clip_max), 1)

# Funzione per calcolare la temperatura
def temperatura_realistica(giorno):
    T_media_mensile = {1: 5, 2: 9, 3: 14, 4: 17, 5: 20, 6: 22, 7: 24, 8: 24, 9: 20, 10: 15, 11: 10, 12: 6}
    return calcola_meteo_realistico(giorno, T_media_mensile, ampiezza=3, sfasamento=6, fluttuazione_range=(-3, 3), clip_min=-5, clip_max=35)

# Funzione per calcolare la nuvolosità
def nuvolosita_realistica(giorno):
    N_media_mensile = {1: 65, 2: 60, 3: 55, 4: 40, 5: 40, 6: 20, 7: 20, 8: 20, 9: 40, 10: 60, 11: 70, 12: 75}
    return calcola_meteo_realistico(giorno, N_media_mensile, ampiezza=10, sfasamento=-2, fluttuazione_range=(-20, 20), clip_min=0, clip_max=100)

# Funzione per calcolare l'esposizione solare
def esposizione_sol_realistica(giorno):
    E_media_mensile = {1: 5, 2: 5, 3: 6, 4: 8, 5: 10, 6: 12, 7: 13, 8: 12, 9: 10, 10: 8, 11: 5, 12: 5}
    return calcola_meteo_realistico(giorno, E_media_mensile, ampiezza=1, sfasamento=6, fluttuazione_range=(0, 1), clip_min=0, clip_max=12)

# Funzione per calcolare l'umidità
def umidita_realistica(giorno):
    U_media_mensile = {1: 76, 2: 70, 3: 69, 4: 66, 5: 66, 6: 68, 7: 65, 8: 66, 9: 69, 10: 73, 11: 76, 12: 78}
    return calcola_meteo_realistico(giorno, U_media_mensile, ampiezza=10, sfasamento=12, fluttuazione_range=(-5, 5), clip_min=30, clip_max=100)

# Funzione per calcolare le precipitazioni con giorni senza pioggia
def precipitazioni_realistiche(giorno):
    P_media_mensile = {1: 2, 2: 2, 3: 1.9, 4: 2.1, 5: 2, 6: 1.7, 7: 1.3, 8: 1.5, 9: 2.3, 10: 2.7, 11: 2.8, 12: 2.4}
    probabilita_pioggia = {1: 0.3, 2: 0.5, 3: 0.4, 4: 0.4, 5: 0.4, 6: 0.3, 7: 0.3, 8: 0.3, 9: 0.4, 10: 0.5, 11: 0.5, 12: 0.4}
    if np.random.rand() > probabilita_pioggia[giorno.month]:
        return calcola_meteo_realistico(giorno, P_media_mensile, ampiezza=5, sfasamento=-2, fluttuazione_range=(-5, 15), clip_min=0, clip_max=90)

# Funzione per generare il DataFrame con i dati meteo
def genera_meteo_df(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    
    dati = {
        "Data": [],
        "Temperatura (°C)": [],
        "Nuvolosità (%)": [],
        "Esposizione Solare (ore)": [],
        "Umidità (%)": [],
        "Precipitazioni (mm)": []
    }
    
    for giorno in date_range:
        dati["Data"].append(giorno.strftime('%Y-%m-%d'))
        dati["Temperatura (°C)"].append(temperatura_realistica(giorno))
        dati["Nuvolosità (%)"].append(nuvolosita_realistica(giorno))
        dati["Esposizione Solare (ore)"].append(esposizione_sol_realistica(giorno))
        dati["Umidità (%)"].append(umidita_realistica(giorno))
        dati["Precipitazioni (mm)"].append(precipitazioni_realistiche(giorno))
    
    return pd.DataFrame(dati)

# Genera i dati meteo
start_date = "2022-01-01"
end_date = "2025-12-31"
df = genera_meteo_df(start_date, end_date)

# Salva il DataFrame in un file CSV
df.to_csv('dati_meteo.csv', index=False)
