
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# 1. Configuration de l'application (Forçage Dark Mode et Port HF)
app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "color-scheme", "content": "dark"}]
)
server = app.server

# 2. Chargement des données
try:
    df = pd.read_csv('co2_data_clean.csv', sep=';').sort_values('Year')
except FileNotFoundError:
    print("Erreur : co2_data_clean.csv introuvable.")
    exit()

ue_members = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland",
              "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
              "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"]

# 3. Classification des données
def classify_co2(val):
    if pd.isna(val): return None
    if val < 100000: return "< 100 kt / an"
    elif 100000 <= val < 200000: return "< 200 kt / an"
    elif 200000 <= val < 300000: return "200-300 kt / an"
    elif 300000 <= val < 500000: return "300-500 kt / an"
    elif 500000 <= val < 1000000: return "500 kt - 1 Mt / an"
    elif 1000000 <= val < 2000000: return "1 Mt - 2 Mt / an"
    elif 2000000 <= val < 4000000: return "2 Mt - 4 Mt / an"
    elif 4000000 <= val < 5000000: return "4 Mt - 5 Mt / an"
    else: return "> 5 Mt / an"

df['Niveau'] = df['CO2'].apply(classify_co2)

color_map = {
    "< 100 kt / an": "#FFFFFF", "< 200 kt / an": "#B2E699", "200-300 kt / an": "#3F51B5",
    "300-500 kt / an": "#CCCCCC", "500 kt - 1 Mt / an": "#F4D03F", "1 Mt - 2 Mt / an": "#EB984E",
    "2 Mt - 4 Mt / an": "#E67E22", "4 Mt - 5 Mt / an": "#922B21", "> 5 Mt / an": "#FF0000"
}

category_orders = ["< 100 kt / an", "< 200 kt / an", "200-300 kt / an", "300-500 kt / an",
                   "500 kt - 1 Mt / an", "1 Mt - 2 Mt / an", "2 Mt - 4 Mt / an", "4 Mt - 5 Mt / an", "> 5 Mt / an"]

# 4. Préparation du Top 10
df_top = df[~df['Name'].isin(ue_members)].copy()
df_avg = df_top.groupby('Name')['CO2'].mean().reset_index()
top_10_avg = df_avg.sort_values(by='CO2', ascending=True).tail(10)
top_10_avg['Niveau'] = top_10_avg['CO2'].apply(classify_co2)

# --- GRAPHIQUES ---

# Carte
fig_map = px.choropleth(
    df, locations="Name", locationmode="country names", color="Niveau",
    animation_frame="Year", color_discrete_map=color_map,
    category_orders={"Niveau": category_orders}, template="plotly_dark"
)
fig_map.update_geos(showcountries=True, countrycolor="white", showland=True, landcolor="white",
                    oceancolor="#111111", showocean=True, projection_type='natural earth')

fig_map.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend=dict(title="<b>SEUILS D'ÉMISSIONS</b>", x=0.02, y=0.5, font=dict(size=18), bgcolor="rgba(0,0,0,0.8)"),
    sliders=[dict(
        currentvalue={"prefix": "ANNÉE : ", "font": {"size": 55, "color": "white", "family": "Arial Black"}, "xanchor": "center"},
        x=0.5, xanchor="center", len=0.9, pad={"t": 50}
    )]
)

# Barres
fig_bar = px.bar(top_10_avg, x='CO2', y='Name', orientation='h', color='Niveau', 
                 color_discrete_map=color_map, text='CO2', template="plotly_dark")

fig_bar.update_traces(texttemplate='%{text:.2s}t / an', textposition='outside', textfont=dict(size=20), width=0.5)

fig_bar.update_layout(
    showlegend=False,
    xaxis=dict(visible=False, range=[0, top_10_avg['CO2'].max() * 1.8]),
    yaxis=dict(tickfont=dict(size=20, color="white"), title=""),
    margin=dict(l=10, r=120, t=10, b=10),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)

# --- LAYOUT ---

app.layout = html.Div(style={'backgroundColor': '#111111', 'minHeight': '100vh', 'padding': '20px', 'display': 'flex', 'flexDirection': 'column'}, children=[
    
    # TITRE
    html.Div([
        html.H1("Émissions mondiales de CO₂ par pays et par an (période 1970–2024)",
                style={'textAlign': 'center', 'color': 'white', 'fontFamily': 'Arial Black', 'fontSize': '42px', 'marginBottom': '30px'})
    ], style={'width': '100%'}),

    # GRAPHIQUES
    html.Div(style={'display': 'flex', 'height': '75vh', 'gap': '20px', 'flex': '1'}, children=[
        html.Div([
            dcc.Graph(figure=fig_map, style={'height': '100%'})
        ], style={'width': '72%', 'borderRadius': '15px', 'border': '1px solid #333', 'overflow': 'hidden'}),

        html.Div([
            html.H3("Top 10 des pays les plus émetteurs de CO₂ par an",
                    style={'textAlign': 'center', 'color': 'white', 'fontFamily': 'Arial Black', 'fontSize': '24px', 'marginBottom': '20px'}),
            dcc.Graph(figure=fig_bar, style={'height': '85%'})
        ], style={'width': '28%', 'backgroundColor': '#1a1a1a', 'padding': '20px', 'borderRadius': '15px', 'border': '1px solid #333'})
    ]),
    
    # PIED DE PAGE CENTRÉ
    html.Footer(style={
        'marginTop': '40px', 
        'padding': '20px', 
        'borderTop': '1px solid #333', 
        'display': 'flex', 
        'flexDirection': 'column', 
        'alignItems': 'center', 
        'justifyContent': 'center'
    }, children=[
        
        html.P("Source : EDGAR - Emissions Database for Global Atmospheric Research", 
               style={'color': 'white', 'fontSize': '13px', 'opacity': '0.6', 'marginBottom': '15px'}),
        
        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '35px', 'flexWrap': 'wrap'}, children=[
            
            html.Span("Dashboard developed by Mahmoud TOURKI", 
                      style={'color': 'white', 'fontFamily': 'Arial', 'fontSize': '16px', 'fontWeight': 'bold'}),
            
            # Gmail
            html.A([
                html.Img(src="https://cdn-icons-png.flaticon.com/512/732/732200.png", style={'height': '22px', 'marginRight': '10px'}),
                "mahmoud.tourki24@gmail.com"
            ], href="mailto:mahmoud.tourki24@gmail.com", style={'color': '#bbb', 'textDecoration': 'none', 'fontSize': '14px', 'display': 'flex', 'alignItems': 'center'}),

            # LinkedIn
            html.A([
                html.Img(src="https://cdn-icons-png.flaticon.com/512/174/174857.png", style={'height': '22px', 'marginRight': '10px'}),
                "LinkedIn Profile"
            ], href="https://www.linkedin.com/in/mahmoud-tourki-b228b9147/", target="_blank", style={'color': '#bbb', 'textDecoration': 'none', 'fontSize': '14px', 'display': 'flex', 'alignItems': 'center'})
        ])
    ])
])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
