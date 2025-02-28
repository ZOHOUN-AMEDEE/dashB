import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Charger les données
df = pd.read_csv('dataset_imputed.csv')

# Convertir l'année en entier
df['Year'] = df['Year'].astype(int)

# Liste des troubles mentaux pour les filtres et les graphiques
mental_disorders = [
    'Schizophrenia (%)', 'Bipolar disorder (%)', 'Eating disorders (%)',
    'Anxiety disorders (%)', 'Drug use disorders (%)', 'Depression (%)',
    'Alcohol use disorders (%)'
]

# Plage d'années disponibles dans le dataset
years = sorted(df['Year'].unique())
min_year, max_year = min(years), max(years)

# Créer l'application Dash avec un thème bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Définition de la mise en page du dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Tendances mondiales en matière de troubles de santé mentale", 
                   className="text-center my-4 text-primary")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filtres", className="bg-primary text-white"),
                dbc.CardBody([
                    html.Label("Sélectionner une année:"),
                    dcc.Slider(
                        id='year-slider',
                        min=min_year,
                        max=max_year,
                        value=max_year,
                        marks={year: str(year) for year in range(min_year, max_year+1, 5)},
                        step=1
                    ),
                    html.Div(id='slider-output-container', className="mt-2"),
                    
                    html.Label("Sélectionner un trouble mental:", className="mt-3"),
                    dcc.Dropdown(
                        id='disorder-dropdown',
                        options=[{'label': disorder, 'value': disorder} for disorder in mental_disorders],
                        value='Depression (%)',
                        clearable=False,
                        className="mb-3"
                    ),
                    
                    html.Label("Comparer des pays:", className="mt-2"),
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country, 'value': country} for country in sorted(df['Entity'].unique())],
                        value=['France', 'United States', 'China', 'Brazil', 'South Africa'],
                        multi=True,
                        className="mb-3"
                    ),
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=3),
        
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Carte mondiale de la prévalence", className="card-title"), className="bg-primary text-white"),
                        dbc.CardBody([
                            dcc.Graph(id='world-map', style={'height': '60vh'})
                        ])
                    ], className="mb-4 shadow h-100")
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Statistiques globales", className="card-title"), className="bg-primary text-white"),
                        dbc.CardBody(id='stats-container')
                    ], className="mb-4 shadow")
                ], width=12)
            ])
        ], width=12, lg=9)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Évolution temporelle des troubles", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dcc.Graph(id='time-series-plot', style={'height': '50vh'})
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Comparaison des troubles par pays", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dcc.Graph(id='disorder-comparison-plot', style={'height': '50vh'})
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Top 10 des pays les plus touchés", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dcc.Graph(id='top-countries-plot', style={'height': '50vh'})
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Matrice de corrélation entre troubles", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dcc.Graph(id='correlation-heatmap', style={'height': '50vh'})
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Tendances régionales", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dcc.Graph(id='regional-trends-plot', style={'height': '50vh'})
                ])
            ], className="mb-4 shadow")
        ], width=12, lg=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Tableau de données", className="card-title"), className="bg-primary text-white"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{"name": i, "id": i} for i in df.columns if i != 'index'],
                        page_size=10,
                        filter_action="native",
                        sort_action="native",
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'minWidth': '100px', 'maxWidth': '180px',
                            'whiteSpace': 'normal', 'textAlign': 'left'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    )
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    
    html.Footer(
        html.P("Dashboard de Tendances Mondiales en Matière de Troubles de Santé Mentale © 2025", 
               className="text-center text-muted py-3")
    )
], fluid=True)

# Callback pour mettre à jour le texte du slider
@app.callback(
    Output('slider-output-container', 'children'),
    Input('year-slider', 'value')
)
def update_slider_output(year):
    return f"Année sélectionnée: {year}"

# Callback pour mettre à jour la carte mondiale
@app.callback(
    Output('world-map', 'figure'),
    [Input('disorder-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_world_map(disorder, year):
    filtered_df = df[df['Year'] == year]
    
    # Créer la carte avec Plotly Express
    fig = px.choropleth(
        filtered_df,
        locations="Code",
        color=disorder,
        hover_name="Entity",
        hover_data=[disorder],
        projection="natural earth",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Prévalence mondiale de {disorder} en {year}"
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=disorder
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    return fig

# Callback pour mettre à jour le graphique d'évolution temporelle
@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('disorder-dropdown', 'value')]
)
def update_time_series(countries, disorder):
    if not countries:
        return go.Figure()
    
    filtered_df = df[df['Entity'].isin(countries)]
    
    fig = px.line(
        filtered_df, 
        x='Year', 
        y=disorder, 
        color='Entity',
        title=f"Évolution de {disorder} au fil du temps"
    )
    
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Prévalence (%)",
        legend_title="Pays",
        hovermode="x unified"
    )
    
    return fig

# Callback pour mettre à jour le graphique de comparaison des troubles
@app.callback(
    Output('disorder-comparison-plot', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_disorder_comparison(countries, year):
    if not countries:
        return go.Figure()
    
    filtered_df = df[(df['Entity'].isin(countries)) & (df['Year'] == year)]
    
    # Obtenir les données pour le graphique radar
    fig = go.Figure()
    
    for country in countries:
        country_data = filtered_df[filtered_df['Entity'] == country]
        if not country_data.empty:
            fig.add_trace(go.Scatterpolar(
                r=country_data[mental_disorders].values.flatten().tolist(),
                theta=mental_disorders,
                fill='toself',
                name=country
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, filtered_df[mental_disorders].max().max() * 1.1]
            )
        ),
        title=f"Comparaison des troubles mentaux par pays en {year}",
        showlegend=True
    )
    
    return fig

# Callback pour mettre à jour le graphique des pays les plus touchés
@app.callback(
    Output('top-countries-plot', 'figure'),
    [Input('disorder-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_top_countries(disorder, year):
    filtered_df = df[df['Year'] == year]
    
    # Obtenir le top 10 des pays pour le trouble sélectionné
    top_countries = filtered_df.sort_values(by=disorder, ascending=False).head(10)
    
    fig = px.bar(
        top_countries,
        x='Entity',
        y=disorder,
        title=f"Top 10 des pays les plus touchés par {disorder} en {year}",
        color=disorder,
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        xaxis_title="Pays",
        yaxis_title="Prévalence (%)",
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig

# Callback pour mettre à jour la matrice de corrélation
@app.callback(
    Output('correlation-heatmap', 'figure'),
    [Input('year-slider', 'value')]
)
def update_correlation_heatmap(year):
    filtered_df = df[df['Year'] == year]
    
    # Calculer la matrice de corrélation
    corr_matrix = filtered_df[mental_disorders].corr()
    
    # Créer la heatmap
    fig = px.imshow(
        corr_matrix,
        x=mental_disorders,
        y=mental_disorders,
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Corrélation entre les troubles mentaux en {year}"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_tickangle=0
    )
    
    return fig

# Callback pour mettre à jour les tendances régionales
@app.callback(
    Output('regional-trends-plot', 'figure'),
    [Input('disorder-dropdown', 'value')]
)
def update_regional_trends(disorder):
    # Simplification: on utilise les trois premières lettres du code comme région
    # Dans un cas réel, il faudrait utiliser une vraie table de correspondance des régions
    
    # Créer une copie du dataframe pour ne pas modifier l'original
    regions_df = df.copy()
    
    # Définir une fonction pour extraire la région
    def get_region(code):
        if pd.isna(code) or len(str(code)) < 3:
            return "Autres"
        
        # Mappage simple des codes de pays aux régions
        first_letter = str(code)[0]
        if first_letter in ['A', 'B']:
            return "Afrique"
        elif first_letter in ['C', 'D', 'E', 'F', 'G']:
            return "Amériques"
        elif first_letter in ['H', 'I', 'J', 'K', 'L', 'M']:
            return "Asie"
        elif first_letter in ['N', 'O', 'P', 'Q', 'R', 'S']:
            return "Europe"
        else:
            return "Océanie"
    
    # Appliquer la fonction pour obtenir les régions
    regions_df['Region'] = regions_df['Code'].apply(get_region)
    
    # Calculer la moyenne par région et par année
    regional_data = regions_df.groupby(['Region', 'Year'])[disorder].mean().reset_index()
    
    # Créer le graphique
    fig = px.line(
        regional_data,
        x='Year',
        y=disorder,
        color='Region',
        title=f"Tendances régionales pour {disorder} au fil du temps",
        line_shape='spline'
    )
    
    fig.update_layout(
        xaxis_title="Année",
        yaxis_title="Prévalence moyenne (%)",
        legend_title="Région",
        hovermode="x unified"
    )
    
    return fig

# Callback pour mettre à jour les statistiques globales
@app.callback(
    Output('stats-container', 'children'),
    [Input('disorder-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_stats(disorder, year):
    filtered_df = df[df['Year'] == year]
    
    # Calculer les statistiques
    global_avg = filtered_df[disorder].mean()
    global_max = filtered_df[disorder].max()
    max_country = filtered_df.loc[filtered_df[disorder].idxmax(), 'Entity']
    global_min = filtered_df[disorder].min()
    min_country = filtered_df.loc[filtered_df[disorder].idxmin(), 'Entity']
    
    # Créer les cartes de statistiques
    stats_cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Moyenne mondiale", className="bg-info text-white"),
                dbc.CardBody([
                    html.H3(f"{global_avg:.2f}%"),
                    html.P(f"Prévalence moyenne de {disorder} en {year}")
                ])
            ], className="text-center mb-3")
        ], width=12, md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Prévalence maximale", className="bg-danger text-white"),
                dbc.CardBody([
                    html.H3(f"{global_max:.2f}%"),
                    html.P(f"{max_country}")
                ])
            ], className="text-center mb-3")
        ], width=12, md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Prévalence minimale", className="bg-success text-white"),
                dbc.CardBody([
                    html.H3(f"{global_min:.2f}%"),
                    html.P(f"{min_country}")
                ])
            ], className="text-center mb-3")
        ], width=12, md=4)
    ])
    
    return stats_cards

# Callback pour mettre à jour la table de données
@app.callback(
    Output('data-table', 'data'),
    [Input('year-slider', 'value'),
     Input('country-dropdown', 'value')]
)
def update_table(year, countries):
    filtered_df = df[df['Year'] == year]
    
    if countries:
        filtered_df = filtered_df[filtered_df['Entity'].isin(countries)]
    
    return filtered_df.to_dict('records')

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)