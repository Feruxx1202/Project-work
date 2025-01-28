import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Inizializzazione dell'app Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Interattiva"

# Layout principale dell'app
app.layout = html.Div(
    children=[
        # Barra del menu in alto (Tabs)
        html.Div(
            children=[
                dcc.Tabs(
                    id="menu-tabs",
                    value="analisi",
                    children=[
                        dcc.Tab(label="Analisi Guadagni 2025", value="analisi"),
                        dcc.Tab(label="Produttività", value="produttivita"),
                        dcc.Tab(label="Meteo", value="meteo"),
                        dcc.Tab(label="Tabelle", value="tabelle"),
                    ],
                ),
            ],
        ),
        # Area di contenuto che cambia in base alla selezione
        html.Div(id="content")
    ],
)

# Callback per aggiornare il contenuto principale 
@app.callback(
    Output("content", "children"),
    Input("menu-tabs", "value")
)
def update_content(selected_item):
    if selected_item == "analisi":
        return analisi()
    elif selected_item == "produttivita":
        return produttivita()
    elif selected_item == "meteo":
         return meteo()
    elif selected_item == "tabelle":
        return tabelle()
    
# FUNZIONI PER PAGINE TABS
# Funzione per creare il layout della pagina
def analisi():
    return html.Div(
        # Stile principale della pagina
        style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#f9f9f9'},
        
        children=[

            # Titolo principale
            html.H1(
                "Calcolo Produzione di Uva, Ricavi e Costi Totali",
                style={'text-align': 'center', 'color': '#4A90E2'}), 
            
            # Linea di separazione sotto il titolo
            html.Hr(style={'border-top': '2px solid #4A90E2'}),

            # Box che contiene tutto il contenuto della pagina
            html.Div([   
            
                # Box per il calcolatore
                html.Div([
                    # Intestazione del calcolatore
                    html.H3("Calcolatore", style={'textAlign': 'center', 'color': '#34495E', 'marginBottom': '30px', 'fontWeight': 'bold'}), 
                    
                    # Gruppo di input per il calcolatore
                    html.Div([
                        # Input per la superficie del vigneto
                        html.Div([
                            html.Label("Superficie vigneto (ha):", style={'fontSize': '16px', 'color': '#34495E'}),
                            dcc.Input(id="superficie-vigneto", type="number", value=2.0, step=0.1, style={'width': '65px', 'textAlign': 'center'})
                        ], style={'marginRight': '30px'}),

                        # Input per la resa per ettaro
                        html.Div([
                            html.Label("Resa per ettaro (kg):", style={'fontSize': '16px', 'color': '#34495E'}),
                            dcc.Input(id="resa-ettaro", type="number", value=8000,max=8000, style={'width': '65px', 'textAlign': 'center'})
                        ])
                    ], style={'display': 'flex', 'justifyContent': 'center'}),

                    # Spazio vuoto per separare le sezioni
                    html.Br(),

                    # Input per i Kg necessari per una bottiglia
                    html.Div([
                        html.Label("Kg necessari per una bottiglia:", style={'fontSize': '16px', 'color': '#34495E'}),
                        dcc.Input(id="kg-per-bottiglia", type="number", value=1.3, step=0.1, style={'width': '65px', 'textAlign': 'center'})
                    ], style={'marginBottom': '20px'}),

                    # Slider per il prezzo per bottiglia
                    html.Div([
                        html.Label("Prezzo per bottiglia (€):", style={'fontSize': '16px', 'color': '#34495E'}),
                        dcc.Slider(id="prezzo-bottiglia", min=8, max=18, step=1, value=10, 
                                   marks={i: f"{i}€" for i in range(8, 19, 1)}, 
                                   tooltip={"placement": "bottom", "always_visible": True}),
                    ], style={'marginBottom': '20px'}),

                    # Input per il costo per ettaro e per bottiglia
                    html.Div([
                        html.Div([
                            html.Label("Costo per ettaro (€):", style={'fontSize': '16px', 'color': '#34495E'}),
                            dcc.Input(id="costo-ettaro", type="number", value=10000, style={'width': '65px', 'textAlign': 'center'})
                        ], style={'marginRight': '30px'}),

                        html.Div([
                            html.Label("Costo per bottiglia (€):", style={'fontSize': '16px', 'color': '#34495E'}),
                            dcc.Input(id="costo-bottiglia", type="number", value=7, style={'width': '65px', 'textAlign': 'center'})
                        ])
                    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '30px'}),

                    # Bottone per calcolare i ricavi e i costi
                    html.Div([
                        html.Button(
                            "Calcola Ricavi e Costi", id="calcola-dati",
                            style={'backgroundColor': '#2980B9', 'color': 'white', 'border': 'none', 'padding': '12px 25px',
                                   'cursor': 'pointer', 'borderRadius': '5px', 'width': '100%'}
                        ),
                    ], style={'marginBottom': '30px', 'textAlign': 'center'}),

                    # Sezione che mostrerà i risultati
                    html.Div(id="output-dati", style={'padding': '20px', 'backgroundColor': '#ECF0F1', 'borderRadius': '10px',
                                                       'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'textAlign': 'center', 'fontSize': '18px', 'color': '#2C3E50'}),
                
                ], style={'background-color': '#fff', 'padding': '15px', 'border-radius': '10px', 
                          'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'margin-top': '20px'}),

                # Sezione grafico per visualizzare i dati
                html.Div([
                    dcc.Graph(id="grafico-dati", style={'height': '450px', 'width': '100%'})
                ], style={'flex': '1', 'minHeight': '500px', 'background-color': '#fff', 'padding': '15px', 
                          'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'margin-top': '20px'})
        
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'gap': '2%'})
        ]) 

# Stile comune da riutilizzare in produttività per i box
common_style = {
    'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
    'border-radius': '10px',
    'background-color': '#fff',
    'padding': '15px'
}

def produttivita():
    return html.Div(
        style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#f9f9f9'},
        children=[
            # Titolo principale
            html.H1(
                "Visualizzazione Produzione Vini per Anno e Varietà",
                style={'text-align': 'center', 'color': '#4A90E2', 'margin-bottom': '30px'}
            ),
            # Linea orizzontale
            html.Hr(style={'border-top': '2px solid #4A90E2', 'margin-bottom': '30px'}),
            
            # Contenitore principale per le sezioni (grafico e statistiche)
            html.Div([
                # Sezione per selezione variabile e grafico
                html.Div(
                    style={'width': '65%', 'padding': '15px'},
                    children=[
                        # Dropdown per la selezione della variabile
                        dcc.Dropdown(
                            id='variable-dropdown',
                            options=[
                                {'label': 'Superficie coltivata (ha)', 'value': 'Superficie coltivata (ha)'},
                                {'label': 'Produzione totale (kg)', 'value': 'Produzione totale (kg)'},
                                {'label': 'Costo totale (€)', 'value': 'Costo totale (€)'},
                                {'label': 'Guadagno netto (€)', 'value': 'Guadagno netto (€)'},
                                {'label': 'Bottiglie prodotte', 'value': 'Bottiglie prodotte'},
                                {'label': 'Resa per ettaro (kg)', 'value': 'Resa per ettaro (kg)'},
                            ],
                            value='Produzione totale (kg)',
                            style={'width': '80%', 'margin': '0 auto'}
                        ),
                        # Grafico
                        dcc.Graph(
                            id='bar-chart',
                            style={**common_style, 'marginTop': '20px'}
                        ),
                        # Spiegazione dei calcoli
                        html.Div([
                            html.H3("Spiegazione dei Calcoli 📊", style={'text-align': 'center', 'margin-bottom': '15px', 'color': '#4A90E2'}),
                            html.P("Le statistiche visualizzate per ogni varietà sono calcolate come segue:", style={'font-weight': 'bold'}),
                            html.Ul([
                                html.Li("🔢 Totale: La somma dei valori della variabile selezionata per la varietà di vino."),
                                html.Li("📊 Media: La media aritmetica dei valori per la varietà di vino in tutti gli anni."),
                                html.Li("⬇️ Minimo: Il valore minimo della variabile per la varietà di vino durante gli anni."),
                                html.Li("⬆️ Massimo: Il valore massimo della variabile per la varietà di vino durante gli anni."),
                                html.Li("📉 Deviazione Standard: Misura della dispersione dei dati attorno alla media."),
                                html.Li("⚖️ Mediana: Il valore centrale della variabile per la varietà di vino quando i dati sono ordinati."),
                            ], style={'padding-left': '20px'}),
                            html.P("Queste statistiche ti permettono di ottenere un'idea chiara sulla distribuzione e l'andamento della variabile selezionata per ogni varietà di vino.", style={'margin-top': '15px'})
                        ], style={**common_style, 'border': '1px solid #ddd', 'marginTop': '17px'})
                    ]
                ),
                # Sezione per le statistiche 
                html.Div(
                    style={'width': '30%', 'padding': '15px'},
                    children=[
                        html.Div(
                            style={**common_style, 'border': '1px solid #ddd'},
                            id='stats-box',
                            children=[html.H3("Statistiche per ogni Vino", style={'text-align': 'center', 'margin-bottom': '20px'})]
                        ),
                    ]
                ),
            ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '30px', 'align-items': 'flex-start'}),
        ]
    )


def meteo():
    return html.Div(
        style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#f9f9f9'},
        children=[
            html.H1("Dashboard Meteo", style={'text-align': 'center', 'color': '#4A90E2', 'margin-bottom': '30px'}),
            html.Hr(style={'border-top': '2px solid #4A90E2', 'margin-bottom': '30px'}),
            
            html.Div([ 
                dcc.Dropdown(
                    id='variabile_dropdown',
                    options=[
                        {'label': 'Temperatura (°C)', 'value': 'Temperatura (°C)'},
                        {'label': 'Nuvolosità (%)', 'value': 'Nuvolosità (%)'},
                        {'label': 'Esposizione Solare (ore)', 'value': 'Esposizione Solare (ore)'},
                        {'label': 'Umidità (%)', 'value': 'Umidità (%)'},
                        {'label': 'Precipitazioni (mm)', 'value': 'Precipitazioni (mm)'}
                    ],
                    value= 'Precipitazioni (mm)', 
                    style={'width': '50%', 'margin': '0 auto'}
                )
            ], style={'textAlign': 'center', 'padding': '20px'}),

            # Grafico sotto il dropdown
            html.Div([dcc.Graph(id='grafico_meteo')], style={'padding': '20px'}),

            html.Div([
                html.Div(id='stats_mese', style={'width': '45%', 'textAlign': 'center', 'fontSize': '14px', 'height': '110px',  'marginTop': '20px','background-color': '#fff', 'padding': '10px', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border': '1px solid #ddd'}),
                html.Div(id='analisi_sezione', style={'width': '45%', 'marginTop': '20px','background-color': '#fff', 'padding': '15px', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border': '1px solid #ddd'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '20px'}),

            html.Div(id='tabella_confronto', style={'width': '45%', 'textAlign': 'center', 'marginTop': '-320px','background-color': '#fff', 'padding': '10px', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'border': '1px solid #ddd'})
        ]
    )

def tabelle():
    return html.Div(
        style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#f9f9f9'},
        children=[
        html.H1("Tabelle Grezze", style={'text-align': 'center', 'color': '#4A90E2', 'background-color': '#f9f9f9'}),
        html.Hr(style={'border-top': '2px solid #4A90E2'}),

        html.Div([
            html.Div([
                html.H3("Seleziona Tabella da Visualizzare:"),
                dcc.RadioItems(
                    id='table-switch',
                    options=[
                        {'label': 'Meteo', 'value': 'table-1'},
                        {'label': 'Produttività', 'value': 'table-2'}
                    ],
                    value='table-1',
                    inline=True,
                )
            ], style={'width': '50%', 'padding': '10px'}),

            html.Div([
                html.H3("Filtra per periodo:"),
                dcc.DatePickerRange(
                    id='date-picker',
                    start_date=start_date,
                    end_date=end_date,
                    min_date_allowed=start_date,
                    max_date_allowed=end_date,
                    display_format='YYYY-MM-DD',
                ),
                html.Button("X", id='reset-date', n_clicks=0, style={"cursor": "pointer"})
            ], id='date-picker-div', style={'width': '50%', 'padding': '10px', 'text-align': 'center'})
        ], style={'display': 'flex', 'background-color': '#fff', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'padding': '10px'}),

        html.Div([
            html.H3("Dataframe Meteo"),
            dash_table.DataTable(
                id='table-1',
                columns=[{"name": col, "id": col} for col in df_meteo.columns],
                data=df_meteo.to_dict('records'),
                page_size=31,
                style_header={'backgroundColor': '#e1e1e1', 'fontWeight': 'bold', 'textAlign': 'center', 'whiteSpace': 'normal', 
                    'height': 'auto', },
                style_data={'border': '1px solid #ddd', 'padding': '8px', 'textAlign': 'center'},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f2f2f2'}],
                fixed_rows={'headers': True}
            )
        ], id='table-1-div'),

        html.Div([
            html.H3("Dataframe Produttività"),
            dash_table.DataTable(
                id='table-2',
                columns=[{"name": col, "id": col} for col in df_prod.columns],
                data=df_prod.to_dict('records'),
                page_size=len(df_prod),  
                style_table={'width': '100%', 'height': 'auto', 'overflowY': 'auto'}, 
                style_header={'backgroundColor': '#e1e1e1', 'fontWeight': 'bold', 'textAlign': 'center', 'whiteSpace': 'normal', 
                    'height': 'auto', },
                style_data={'border': '1px solid #ddd', 'padding': '8px', 'textAlign': 'center'},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f2f2f2'}]
            )
        ], id='table-2-div'),

    ])
    
# Callback per calcolare ricavi, costi, profitto ed aggiornare il grafico
@app.callback(
    [Output("output-dati", "children"),  # Output del risultato testuale
     Output("grafico-dati", "figure")],  # Output del grafico
    [Input("superficie-vigneto", "value"),  # Input per la superficie del vigneto
     Input("resa-ettaro", "value"),  # Input per la resa per ettaro
     Input("kg-per-bottiglia", "value"),  # Input per i kg per bottiglia
     Input("prezzo-bottiglia", "value"),  # Input per il prezzo per bottiglia
     Input("costo-ettaro", "value"),  # Input per il costo per ettaro
     Input("costo-bottiglia", "value"),  # Input per il costo per bottiglia
     Input("calcola-dati", "n_clicks")]  # Input per il numero di click sul pulsante di calcolo
)

# INIZIO FUNZIONE PAGINA ANALISI 2025
def calcola_dati(superficie, resa, kg_bottiglia, prezzo_bottiglia, costo_ettaro, costo_bottiglia, n_clicks):
    if n_clicks is None:
        return "", go.Figure()  # Se non sono stati effettuati click, ritorna vuoto

    # Assicurati che tutti i valori siano validi 
    if superficie is None or resa is None or kg_bottiglia is None or prezzo_bottiglia is None or costo_ettaro is None or costo_bottiglia is None:
        return "Errore: Tutti i campi devono essere riempiti correttamente.", go.Figure()  # Messaggio di errore se ci sono valori nulli

    # Verifica che i valori siano positivi
    if superficie <= 0 or resa <= 0 or kg_bottiglia <= 0 or prezzo_bottiglia <= 0 or costo_ettaro <= 0 or costo_bottiglia <= 0:
        return "Errore: I valori devono essere positivi.", go.Figure()  # Messaggio di errore se uno dei valori è negativo o zero

    # Calcola la produzione totale in kg
    produzione_totale_kg = superficie * resa

    # Calcola il numero di bottiglie prodotte
    if kg_bottiglia > 1.1:
        bottiglie_prodotte = produzione_totale_kg / kg_bottiglia  # Calcolo delle bottiglie prodotte
    else:
        return "Errore: i kg per bottiglia devono essere maggiori di 1.1", go.Figure()  # Messaggio di errore se kg per bottiglia è troppo basso

    # Calcola i ricavi totali
    ricavi_totali = bottiglie_prodotte * prezzo_bottiglia

    # Calcola i costi totali
    costi_totali = (superficie * costo_ettaro) + (bottiglie_prodotte * costo_bottiglia)

    # Calcola il profitto netto
    profitto_netto = ricavi_totali - costi_totali

    # Risultato testuale con formattazione dei numeri e separazione in righe
    risultato = [
        html.Div(f"Produzione totale: {produzione_totale_kg:,.2f} kg"),  # Mostra la produzione totale in kg
        html.Div(f"Bottiglie prodotte: {bottiglie_prodotte:,.0f} "),  # Mostra il numero di bottiglie prodotte
        html.Div(f"Profitto netto: {profitto_netto:,.2f} €")  # Mostra il profitto netto
    ]

    # Creazione del grafico 
    figure = go.Figure()
    figure.add_trace(go.Bar(  # Crea un grafico a barre
        x=["Ricavi Totali", "Costi Totali", "Profitto Netto"],  # Etichette per le barre
        y=[ricavi_totali, costi_totali, profitto_netto],  # Dati per le barre
        marker_color=['green', 'red', 'blue'],  # Colori delle barre
        text=[f"€{ricavi_totali:,.2f}", f"€{costi_totali:,.2f}", f"€{profitto_netto:,.2f}"],  # Testo sulle barre
        textposition='auto'  # Posizione automatica del testo sulle barre
    ))
    figure.update_layout(  # Impostazioni del layout del grafico
        title="Analisi Economica",  # Titolo del grafico
        xaxis_title="Categorie",  # Titolo dell'asse x
        yaxis_title="Valore (€)",  # Titolo dell'asse y
    )

    return risultato, figure  # Ritorna i risultati testuali e il grafico
# FINE FUNZIONE CALCOLI PAGINA ANALISI 2025

#Carica e pulisce i dati in base al tipo (produzione o meteo).
def carica_e_pulisci_dati(percorso_file, tipo_dati):
    try:
        # Carica il file CSV
        df = pd.read_csv(percorso_file, encoding="utf-8")
        
        if tipo_dati == "produzione":
            # Lista delle colonne da pulire per i dati di produzione
            colonne_da_pulire = ['Produzione totale (kg)', 'Costo totale (€)', 'Guadagno netto (€)', 
                                 'Superficie coltivata (ha)', 'Bottiglie prodotte', 'Resa per ettaro (kg)']
            for col in colonne_da_pulire:
                if col in df.columns:
                    df[col] = df[col].replace({'€': '', ',': '', ' ': ''}, regex=True)
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        elif tipo_dati == "meteo" and 'Data' in df.columns:
            # Pulisce i dati meteo
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df['Anno'] = df['Data'].dt.year
            df['Mese'] = df['Data'].dt.month
            df['Data'] = df['Data'].dt.date  
        
        return df  # Restituisce il DataFrame pulito
    except FileNotFoundError:
        print(f"Errore: Il file {percorso_file} non è stato trovato.")
        return None
    except Exception as e:
        print(f"Errore durante il caricamento o la pulizia di {percorso_file}: {e}")
        return None

# Caricamento e pulizia dei dati di produzione e meteo
df_prod = carica_e_pulisci_dati("dati_produzione.csv", "produzione")
df_meteo = carica_e_pulisci_dati("dati_meteo.csv", "meteo")

# Imposta la data di inizio e fine in base ai dati meteo
if df_meteo is not None:
    start_date = df_meteo['Data'].min()
    end_date = df_meteo['Data'].max()
    

# FUNZIONI PAGINA PRODUTTIVITA
@app.callback(
    [Output('bar-chart', 'figure'),  # Output per il grafico a barre
     Output('stats-box', 'children')],  # Output per la sezione delle statistiche
    Input('variable-dropdown', 'value')  # Input: valore selezionato dal dropdown
)
def aggiorna_grafico_e_statistiche(variabile_selezionata):
    # Creazione di un grafico a barre utilizzando Plotly Express
    fig_bar = px.bar(df_prod, x='Anno', y=variabile_selezionata, color='Varietà',
                     title=f'{variabile_selezionata} per Anno e Varietà',  # Titolo dinamico
                     labels={'Anno': 'Anno', variabile_selezionata: variabile_selezionata})  # Etichette asse

    # Modifica dell'aspetto del grafico
    fig_bar.update_layout(
        barmode='group',  # Le barre vengono raggruppate per categoria
        xaxis_title="Anno",  # Titolo asse X
        yaxis_title=variabile_selezionata,  # Titolo asse Y basato sulla variabile selezionata
        xaxis_tickangle=-45,  # Ruota le etichette dell'asse X per una migliore leggibilità
        yaxis_tickformat=',.2f'  # Formatta i numeri con due decimali e separatori di migliaia
    )

    # Raggruppamento dei dati per 'Varietà' e calcolo delle statistiche
    grouped = df_prod.groupby('Varietà')[variabile_selezionata].agg(['sum', 'mean', 'min', 'max', 'std', 'median'])

    # Mappatura delle statistiche con nomi più leggibili e relative emoji
    nomi_statistiche = {
        'sum': ('Somma', '🔢'), 
        'mean': ('Media', '📊'), 
        'min': ('Minimo', '⬇️'), 
        'max': ('Massimo', '⬆️'), 
        'std': ('Deviazione Standard', '📉'), 
        'median': ('Mediana', '⚖️')
    }

    # Creazione della sezione delle statistiche come lista di div HTML
    stats_content = [
        html.Div([
            html.H4(f"{varieta} 🍇", style={'color': '#4A90E2'}),  # Nome della varietà con emoji
            *[html.P(f"{nomi_statistiche[stat][0]}: {grouped.loc[varieta, stat]:,.2f} {nomi_statistiche[stat][1]}", 
                     style={'font-weight': 'bold'})  
              for stat in ['sum', 'mean', 'min', 'max', 'std', 'median']]  # Usa i nomi mappati e le emoji
        ], style={'margin-bottom': '15px'})  # Spaziatura tra i blocchi
        for varieta in grouped.index  # Itera sulle varietà presenti nel dataset
    ]

    return fig_bar, stats_content  # Restituisce il grafico e le statistiche per l'interfaccia


# INIZIO FUNZIONI PAGINA METEO

# Funzione per calcolare i mesi ideali per coltivare l'uva
def mesi_ideali(df):
    df_medi = df.groupby('Mese').mean(numeric_only=True).reset_index() 
    
    # Filtra i mesi che soddisfano i criteri ideali per la coltivazione dell'uva
    mesi_ideali_list = df_medi[
        (df_medi['Temperatura (°C)'] >= 14) & (df_medi['Temperatura (°C)'] <= 28) & 
        (df_medi['Esposizione Solare (ore)'] >= 6) & 
        (df_medi['Precipitazioni (mm)'] <= 100) & 
        (df_medi['Umidità (%)'] >= 40) & (df_medi['Umidità (%)'] <= 75)
    ]['Mese'].tolist()  
    
    # Converte i numeri dei mesi in nomi abbreviati
    mesi_ideali_nomi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
                         "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    mesi_ideali_nomi = [mesi_ideali_nomi[m-1] for m in mesi_ideali_list]  
    
    return mesi_ideali_nomi, df_medi  # Restituisce i mesi ideali e i dati medi mensili



# Funzione per creare il grafico meteo
def crea_grafico_meteo(df, variabile_selezionata):
    # Filtra il DataFrame per includere solo gli anni di interesse
    df_anno = df[df['Anno'].isin([2022, 2023, 2024, 2025])]  
    
    if variabile_selezionata == 'Precipitazioni (mm)':
        df_anno_mese = df_anno.groupby(['Anno', 'Mese'])[variabile_selezionata].sum().reset_index()
    else:
        df_anno_mese = df_anno.groupby(['Anno', 'Mese'])[variabile_selezionata].mean().reset_index()
    
    # Crea un grafico a linee con Plotly
    fig = px.line(
        df_anno_mese,
        x='Mese',
        y=variabile_selezionata,
        color='Anno',
        title=f"Andamento di {variabile_selezionata} (2022-2025)",
        labels={'Mese': 'Mese', variabile_selezionata: 'Valore Medio'},
        line_group="Anno",
    )

    # Personalizza l'aspetto del grafico
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Mesi come valori sull'asse X
            ticktext=["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]  # Mesi come etichette
        ),
        hovermode='x unified',  # Modalità di visualizzazione dei tooltip
        template="plotly"  # Imposta il tema del grafico
    )

    return fig  # Restituisce il grafico


# Funzione per creare la tabella meteo
def crea_tabella_meteo(df, variabile_selezionata):
    # Filtra i dati per gli anni selezionati
    anni_selezionati = [2022, 2023, 2024, 2025]
    df_anno = df[df['Anno'].isin(anni_selezionati)]
    
    # Se la variabile selezionata è 'Precipitazioni (mm)', sommiamo per ogni mese e anno
    if variabile_selezionata == 'Precipitazioni (mm)':
        df_anno_mese = df_anno.groupby(['Anno', 'Mese'])[variabile_selezionata].sum().reset_index()  # Somma
    else:
        # Per altre variabili, calcoliamo la media mensile
        df_anno_mese = df_anno.groupby(['Anno', 'Mese'])[variabile_selezionata].mean().reset_index()  # Media
    
    # Intestazione della tabella HTML (anni come intestazioni delle colonne)
    intestazione = html.Thead(html.Tr(
        [html.Th("Mese", style={'padding': '4px', 'fontSize': '12px'})] +
        [html.Th(str(anno), style={'padding': '4px', 'fontSize': '12px'}) for anno in anni_selezionati],
        style={'border': '1px solid #ddd', 'textAlign': 'center'}
    ))

    # Corpo della tabella con i dati aggregati
    mesi_labels = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", 
                   "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    
    righe = []
    for mese in range(1, 13):
        # Estraiamo i valori per ogni anno del mese corrente
        valori_mese = [
            f"{df_anno_mese[(df_anno_mese['Anno'] == anno) & (df_anno_mese['Mese'] == mese)][variabile_selezionata].sum():.2f}"
            if variabile_selezionata == 'Precipitazioni (mm)' and not df_anno_mese[(df_anno_mese['Anno'] == anno) & (df_anno_mese['Mese'] == mese)].empty else
            f"{df_anno_mese[(df_anno_mese['Anno'] == anno) & (df_anno_mese['Mese'] == mese)][variabile_selezionata].mean():.2f}"
            if not df_anno_mese[(df_anno_mese['Anno'] == anno) & (df_anno_mese['Mese'] == mese)].empty else '-'
            for anno in anni_selezionati
        ]
        
        # Aggiungiamo la riga per il mese corrente
        righe.append(html.Tr(
            [html.Td(mesi_labels[mese-1], style={'border': '1px solid #ddd', 'padding': '4px', 'fontSize': '12px'})] +
            [html.Td(valore, style={'border': '1px solid #ddd', 'padding': '4px', 'fontSize': '12px'}) for valore in valori_mese]
        ))

    # Costruzione della tabella completa con le righe per i mesi e le colonne per gli anni
    tabella_html = html.Table(
        [intestazione, html.Tbody(righe)],
        style={'borderCollapse': 'collapse', 'width': '100%', 'border': '1px solid #ddd', 'margin': '0 auto'}
    )

    return tabella_html


# Callback per aggiornare grafico, analisi e tabelle nella sezione meteo
@app.callback(
    [Output('grafico_meteo', 'figure'),
     Output('analisi_sezione', 'children'),
     Output('stats_mese', 'children'),
     Output('tabella_confronto', 'children')],
    Input('variabile_dropdown', 'value')
)
def aggiorna_contenuto_meteo(variabile_selezionata):
    # Creazione del grafico per la variabile selezionata
    fig = crea_grafico_meteo(df_meteo, variabile_selezionata)

    # Calcolo dei mesi ideali e dei dati medi mensili
    mesi_ideali_nomi, df_medi = mesi_ideali(df_meteo)

    # Determinazione del mese migliore e peggiore per la variabile selezionata
    mese_migliore = df_medi.loc[df_medi[variabile_selezionata].idxmax(), 'Mese']
    mese_peggiore = df_medi.loc[df_medi[variabile_selezionata].idxmin(), 'Mese']
    mesi_italiani = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    mese_migliore_nome = mesi_italiani[mese_migliore - 1]
    mese_peggiore_nome = mesi_italiani[mese_peggiore - 1]

    # Box di statistica mese migliore e peggiore
    stats_mese = html.Div([ 
        html.H3(f"🌟 Statistica Mesi: ", style={'color': '#007bff', 'fontWeight': 'bold'}),
        html.P(f"Il mese con il valore medio più alto di '{variabile_selezionata}' è {mese_migliore_nome}."),
        html.P(f"Il mese con il valore medio più basso di '{variabile_selezionata}' è {mese_peggiore_nome}.")
    ])

    # Analisi per i mesi ideali per coltivare l'uva
    analisi_html = html.Div([ 
        html.H3("🔍 Analisi per i Mesi Ideali per Coltivare l'Uva", style={'textAlign': 'center'}),
        html.P(f"I mesi ideali per coltivare l'uva 🍇 sono: {', '.join(mesi_ideali_nomi)}.", style={'fontWeight': 'bold', 'color': 'green', 'textAlign': 'center'}),
        html.H4("🌡️ Analisi della Temperatura Media:"),
        html.P(f"✅ La temperatura media ideale per la coltivazione è tra 14°C e 28°C."),
        html.H4("☀️ Analisi Esposizione Solare:"),
        html.P(f"✅ Almeno 6 ore di sole al giorno sono ottimali."),
        html.H4("🌧️ Analisi delle Precipitazioni:"),
        html.P(f"✅ Precipitazioni sotto i 100mm al mese sono ideali per evitare danni."),
        html.H4("💧 Analisi Umidità:"),
        html.P(f"✅ Umidità compresa tra il 40% e il 75% garantisce una crescita sana.")
    ])

    # Tabella di confronto dei dati meteo
    tabella_html = crea_tabella_meteo(df_meteo, variabile_selezionata)

    return fig, analisi_html, stats_mese, tabella_html  # Restituisce il grafico, analisi e tabella

# FINE FUNZIONI PAGINA METEO

# FUNZIONI PAGINA TABELLE
@app.callback(
    [Output('table-1', 'data'),
     Output('date-picker-div', 'style')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('table-switch', 'value')]
)
def aggiorna_tabella_1(start_date, end_date, tabella):
    if tabella == 'table-1':
        filtro = (df_meteo['Data'] >= 
                  pd.to_datetime(start_date).date()) & (df_meteo['Data'] <=
                                                         pd.to_datetime(end_date).date()) if start_date and end_date else True
        return df_meteo[filtro].to_dict('records'), {'display': 'block'}
    return dash.no_update, {'display': 'none'}

@app.callback(
    [Output('table-1-div', 'style'),
     Output('table-2-div', 'style')],
    Input('table-switch', 'value')
)
def mostra_tabella_selezionata(tabella):
    return ({"display": "block"}, {"display": "none"}) if tabella == 'table-1' else ({"display": "none"}, {"display": "block"})

@app.callback(
    [Output('date-picker', 'start_date'),
     Output('date-picker', 'end_date')],
    Input('reset-date', 'n_clicks')
)
def reset_date_picker(n_clicks):
    return (start_date, end_date) if n_clicks > 0 else (dash.no_update, dash.no_update)


if __name__ == '__main__':
    app.run_server(debug=True)