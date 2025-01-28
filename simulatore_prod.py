import numpy as np
import pandas as pd


# Definizione delle variabili
anni = [2022, 2023, 2024]  
varieta = ["Chianti Classico DOCG", "Brunello di Montalcino DOCG", "Vino Nobile di Montepulciano DOCG"]  
num_records = len(anni) * len(varieta)  

# Generazione dei dati simulati
data = {
    "Anno": np.tile(anni, len(varieta)),
    "Varietà": np.repeat(varieta, len(anni)),
    "Superficie coltivata (ha)": np.round(np.random.uniform(50, 80, size=num_records), 1),
}

# Calcolo della resa per ettaro (kg) e della produzione totale (kg)
data["Resa per ettaro (kg)"] = np.round(np.random.uniform(6000, 8000, size=num_records), 0)
data["Produzione totale (kg)"] = np.round(data["Resa per ettaro (kg)"] * data["Superficie coltivata (ha)"], 0)

# Generazione dei dati sui costi
data["Costo per ettaro (€)"] = np.round(np.random.uniform(10000, 20000, size=num_records), 2)
data["Costo totale (€)"] = np.round(data["Costo per ettaro (€)"] * data["Superficie coltivata (ha)"], 2)

# Aggiunta del costo per bottiglia e calcolo delle bottiglie prodotte
data["Costo per bottiglia (€)"] = np.round(np.random.uniform(3, 5, size=num_records), 2)
data["Bottiglie prodotte"] = np.round(data["Produzione totale (kg)"] / 1.2)  # 1.2 kg per bottiglia

# Calcolo del costo totale includendo anche il costo per bottiglia
data["Costo totale (€)"] = np.round(data["Costo totale (€)"] + (data["Costo per bottiglia (€)"] * data["Bottiglie prodotte"]), 2)

# Prezzo di vendita e calcolo del ricavo
data["Prezzo vendita per bottiglia (€)"] = np.round(np.random.uniform(6, 9, size=num_records), 2)
data["Ricavo totale (€)"] = np.round(data["Prezzo vendita per bottiglia (€)"] * data["Bottiglie prodotte"], 2)

# Calcolo del guadagno netto
data["Guadagno netto (€)"] = np.round(data["Ricavo totale (€)"] - data["Costo totale (€)"], 2)

# Creazione del DataFrame
df = pd.DataFrame(data)

# Funzione per formattare i valori nel DataFrame
def valori_formattati(df):
    df_formattato = df.copy()
    columns_to_format = [
        "Superficie coltivata (ha)", "Resa per ettaro (kg)", "Produzione totale (kg)", 
        "Costo per ettaro (€)", "Costo totale (€)", "Costo per bottiglia (€)",
        "Bottiglie prodotte", "Prezzo vendita per bottiglia (€)", 
        "Ricavo totale (€)", "Guadagno netto (€)"
    ]
    
    currency_columns = ["Costo per ettaro (€)", "Costo totale (€)", "Costo per bottiglia (€)", 
                        "Prezzo vendita per bottiglia (€)", "Ricavo totale (€)", "Guadagno netto (€)"]

    for col in columns_to_format:
        if col in currency_columns:
            df_formattato[col] = df_formattato[col].apply(lambda x: f'€{x:,.2f}')
        else:
            df_formattato[col] = df_formattato[col].apply(lambda x: f'{x:,.0f}')
    
    return df_formattato

# Formattazione e salvataggio del file
df_formattato = valori_formattati(df)
df_formattato.to_csv("dati_produzione.csv", index=False)


