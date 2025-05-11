# -*- coding: utf-8 -*-


import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_leaflet as dl
import psycopg2
import numpy as np
import json
import pandas as pd
import io
import base64



# Tworzenie aplikacji Dash
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Mapa stacji paliw</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="light-mode">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
def get_station_data():
    connection = psycopg2.connect(
        host="localhost",
        database="stacje_paliw",
        user="postgres",
        password="oeu7mv"
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT DISTINCT CONCAT(nazwa_stacji, ' ', adres) 
        FROM public.stacje_paliw
    """)
    stations = cursor.fetchall()
    cursor.close()
    connection.close()
    return [station[0] for station in stations]

def get_fuel_types():
    return ['diesel', 'lpg', 'pb95', 'pb98']

def fetch_stations_from_db():
    conn = psycopg2.connect(
        host="localhost",
        database="stacje_paliw",
        user="postgres",
        password="oeu7mv"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT lat, lon, nazwa_stacji, diesel, lpg, pb95, pb98, dzielnica, adres
        FROM public.stacje_paliw;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    stations = []
    for lat, lon, nazwa, diesel, lpg, pb95, pb98, dzielnica, adres in rows:
        stations.append({
            "lat": lat,
            "lon": lon,
            "nazwa": nazwa,
            "diesel": diesel,
            "lpg": lpg,
            "pb95": pb95,
            "pb98": pb98,
            "dzielnica": dzielnica,
            "adres": adres
        })
    return stations

stacje_dane = fetch_stations_from_db()

def get_logo_icon(nazwa_stacji):
    name = nazwa_stacji.lower()
    if "mol" in name:
        return "/assets/logos/mol2.png"
    elif "orlen" in name:
        return "/assets/logos/orlen1.png"
    elif "shell" in name:
        return "/assets/logos/shell1.png"
    elif "circle k" in name:
        return "/assets/logos/circlek.png"
    elif "avia" in name:
        return "/assets/logos/avia.png"
    elif "amic energy" in name:
        return "/assets/logos/amic_logo1.png"
    elif "makro" in name:
        return "/assets/logos/makro.png"
    elif "watis" in name:
        return "/assets/logos/watis.png"
    elif "intermarche" in name:
        return "/assets/logos/intermarche.png"
    elif "bp" in name:
        return "/assets/logos/bp1.png"
    elif "moya" in name:
        return "/assets/logos/moya1.png"
    else:
        return "/assets/logos/default.png"

def get_markers_from_db():
    connection = psycopg2.connect(
        host="localhost",
        database="stacje_paliw",
        user="postgres",
        password="oeu7mv"
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT lat, lon, nazwa_stacji, diesel, lpg, pb95, pb98, dzielnica, adres
        FROM public.stacje_paliw
    """)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    markers = []
    for lat, lon, nazwa_stacji, diesel, lpg, pb95, pb98, dzielnica, adres in rows:
        icon_url = get_logo_icon(nazwa_stacji)
        popup_content = html.Div([
            html.B(nazwa_stacji),
            html.Br(),
            html.Table([
                html.Tr([html.Th("Rodzaj"), html.Th("Cena [zł]")]),
                html.Tr([html.Td("Diesel"), html.Td(f"{diesel}")]),
                html.Tr([html.Td("LPG"), html.Td(f"{lpg}")]),
                html.Tr([html.Td("PB95"), html.Td(f"{pb95}")]),
                html.Tr([html.Td("PB98"), html.Td(f"{pb98}")]),
            ], style={"borderCollapse": "collapse", "width": "100%"}, className="fuel-table"),
            html.Br(),
            html.Div(f"Adres: {adres}"),
            html.Div(f"Dzielnica: {dzielnica}")
        ])
        marker = dl.Marker(
            position=[lat, lon],
            icon={
                "iconUrl": icon_url,
                "iconSize": [20, 20],
                "iconAnchor": [20, 40],
                "popupAnchor": [0, -40]
            },
            children=dl.Popup(popup_content),
        )
        markers.append(marker)
    return markers



markers = get_markers_from_db()
markers_layer = dl.LayerGroup(id="markers-layer", children=markers)

geojson_file_path = r"dzielnice.geojson"
with open(geojson_file_path, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)


geojson_children = []
for feature in geojson_data["features"]:
    props = feature["properties"]
    geometry = feature["geometry"]
    name = props.get("JPT_NAZWA_", "Nieznana dzielnica").strip()

    geojson_children.append(
        dl.FeatureGroup([
            dl.GeoJSON(data=feature, options=dict(style=dict(
                color="#3388ff",
                weight=2,
                opacity=1,
                fillOpacity=0.3,
                fillColor="#3388ff"
            )),
            hoverStyle=dict(
                weight=4,
                color="#ff7800",
                fillOpacity=0.5
            )),
            dl.Popup(html.B(f"Dzielnica: {name}"))
        ])
    )

geojson_layer = dl.LayerGroup(
    geojson_children,
    id="geojson-dzielnice"
)

# Warstwy mapy
base_layers = [
    dl.BaseLayer(dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"), name="OpenStreetMap", checked=True),
    dl.BaseLayer(dl.TileLayer(url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"), name="OpenTopoMap"),
    dl.BaseLayer(
        dl.WMSTileLayer(
            url="https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution",
            layers="Raster",
            format="image/png",
            transparent=True,
            version="1.3.0",
            attribution="Ortofotomapa Geoportal"
        ),
        name="Ortofotomapa (Geoportal)",
        checked=False
    )
]
overlay_layers = [
    dl.Overlay(
        markers_layer, 
        name="Stacje paliw", 
        checked=True),
    dl.Overlay(
        geojson_layer, 
        name="Granice dzielnic", 
        checked=True)
]



# Komponent mapy
map_component = dl.Map(
    [
        dl.LayersControl(base_layers + overlay_layers),
dl.EasyButton(
    icon='<i class="fa fa-refresh"></i>',
    title="Reset View",
    id="reset-btn",
    position="topleft"
),
        dl.LocateControl(flyTo=True, drawCircle=True, keepCurrentZoomLevel=False, locateOptions={'enableHighAccuracy': True}),
        dl.MeasureControl(
            position="topleft",
            primaryLengthUnit="kilometers",
            primaryAreaUnit="hectares",
            activeColor="#214097",
            completedColor="#972158"
        )
    ],
    center=[52.415, 16.94],
    zoom=11,
    style={'height': '65vh', 'width': '100%', 'borderRadius': '5px'},
    id="map"
)

# Dynamiczny formularz
form_component = html.Div(id="form-container")  

# Przełącznik trybu ciemny/jasny
color_mode_switch = dbc.NavItem(
    html.Div(
        [
            dbc.Label(className="fa fa-sun m-0", html_for="switch"),
            dbc.Switch(id="switch", value=False, className="d-inline-block ms-2", persistence=True),
            dbc.Label(className="fa fa-moon m-0", html_for="switch"),
        ],
        className="d-flex align-items-center",
    ),
)


# Pasek nawigacyjny
navbar = dbc.NavbarSimple(
    children=[
        color_mode_switch,
    ],
    brand="Mapa stacji paliw",
    brand_href="#",
    id="navbar",
    color="primary",  
    dark=True,  
)

# `dcc.Store` do przechowywania stanu trybu
theme_store = dcc.Store(id="theme-store", storage_type="local", data={"dark_mode": False})

stations_data_store = dcc.Store(id='stations-data', data=stacje_dane)

# Layout aplikacji
app.layout = dbc.Container([
    dcc.Store(id="updated-data-store"),
    stations_data_store,
    theme_store,  
    navbar,
    html.Div(id="title-container"), 
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Mapa cen paliw", value="tab-1", className="custom-tab"),
        dcc.Tab(label="Tabela cen paliw", value="tab-2", className="custom-tab"),
    ]),
    html.Div(
    id="sort-container",
    children=[
        html.Label("Sortuj po cenie paliwa:"), 
        dcc.Dropdown(
            id='sort-fuel-dropdown',
            options=[
                {'label': 'Diesel', 'value': 'diesel'},
                {'label': 'LPG', 'value': 'lpg'},
                {'label': 'PB95', 'value': 'pb95'},
                {'label': 'PB98', 'value': 'pb98'},
            ],
            value='diesel',
            style={'width': '200px'}
        )
    ],
    style={'paddingTop': '20px', 'paddingBottom': '20px'}
),
    html.Div(
        id="tabs-content",
        className="container",  
        style={'marginTop': '20px'}  
    ),  
    html.Div(id="footer-container", style={'marginTop': '40px'}),
    html.Div(id="body-class-controller", style={"display": "none"}),
],
fluid=True, id="app-container")

app.clientside_callback(
    """
    function(data) {
        if (data && typeof data.dark_mode !== 'undefined') {
            document.body.classList.remove("light-mode", "dark-mode");
            document.body.classList.add(data.dark_mode ? "dark-mode" : "light-mode");
        }
        return '';
    }
    """,
    Output("body-class-controller", "children"),
    Input("theme-store", "data")
)

# Callback do resetowania widoku
@app.callback(
    [Output("map", "center"), 
     Output("map", "zoom")],    
    Input("reset-btn", "n_clicks")
)
def reset_view(n_clicks):
    if n_clicks:
        return [52.415, 16.94], 11
    return no_update, no_update  

# Callback do dynamicznego tytułu
@app.callback(
    Output("title-container", "children"),
    Input("theme-store", "data")
)
def update_title(theme_store_data):
    dark_mode = theme_store_data["dark_mode"]

    title_style = {
        "color": "white" if dark_mode else "black",
        "textAlign": "center",
        "marginTop": "20px",
        "marginBottom": "20px",
    }

    return html.H1("Ceny paliw w Poznaniu", style=title_style)

# Callback do dynamicznej stopki
@app.callback(
    Output("footer-container", "children"),
    Input("theme-store", "data")
)
def update_footer(theme_store_data):
    dark_mode = theme_store_data["dark_mode"]

    footer_style = {
        "backgroundColor": "#212529" if dark_mode else "#f8f9fa",
        "color": "white" if dark_mode else "black",
        "textAlign": "center",
        "padding": "10px",
        "borderTop": "1px solid #343a40" if dark_mode else "1px solid #dee2e6",
    }

    return html.Div(
        [
            html.P("© Wszelkie prawa zastrzeżone.", style={"margin": 0}),
        ],
        style=footer_style
    )


def get_table_data(sort_by='diesel'):
    connection = psycopg2.connect(
        host="localhost",
        database="stacje_paliw", 
        user="postgres",
        password="password"  
    )
    cursor = connection.cursor()

    query = f"""
        SELECT nazwa_stacji, diesel, lpg, pb95, pb98, dzielnica, adres
        FROM public.stacje_paliw
        ORDER BY {sort_by}  -- Sortowanie po wybranym paliwie
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "value"),
     Input("theme-store", "data"),
     Input("sort-fuel-dropdown", "value")] 
    )
def render_tab_content(tab, theme_store_data, sort_by):
    dark_mode = theme_store_data["dark_mode"]


    table_data = get_table_data(sort_by)  
    
    # Styl formularza
    form_style = {
        'padding': '20px',
        'border': '1px solid #343a40' if dark_mode else '#dee2e6',
        'border-radius': '5px',
        'background-color': 'transparent' if dark_mode else '#f8f9fa',
        'color': 'white' if dark_mode else 'black',
    }

    if tab == "tab-1": 
        # Zawartość zakładki mapa: mapa z formularzem
        return dbc.Row([
            dbc.Col([map_component], md=8, style={'paddingRight': '15px'}),
    
            dbc.Col([
                html.Div([
                    html.Label("Stacja:", className="form-label"),
                    dcc.Dropdown(
                        id="station-dropdown",
                        options=[{"label": station, "value": station} for station in get_station_data()],
                        placeholder="Wybierz stację",
                        className="mb-3"
                    ),
                    html.Label("Rodzaj paliwa:", className="form-label"),
                    dcc.Dropdown(
                        id="fuel-dropdown",
                        options=[{"label": fuel, "value": fuel} for fuel in get_fuel_types()],
                        placeholder="Wybierz rodzaj paliwa",
                        className="mb-3"
                    ),
                    html.Label("Cena:", className="form-label"),
                    dcc.Input(
                        id="price-input",
                        type="number",
                        placeholder="Wprowadź cenę paliwa",
                        min=0,
                        step=0.01,
                        className="form-control mb-3 text-center",
                        style={"textAlign": "center"}  
                    ),
                    dbc.Button("Zaktualizuj dane", id="update-button", n_clicks=0,
                               color="primary", className="mt-2")
                ], className="p-3", style={
                    "backgroundColor": "#f8f9fa",
                    "borderRadius": "8px",
                    "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                    "textAlign": "center"
                })
            ], md=4)
        ], style={'marginTop': '20px'})
    
    elif tab == "tab-2":
        table_data = get_table_data(sort_by)
    
        table_header = [
            html.Thead(html.Tr([
                html.Th("Nazwa stacji"),
                html.Th("Diesel [zł]"),
                html.Th("LPG [zł]"),
                html.Th("PB95 [zł]"),
                html.Th("PB98 [zł]"),
                html.Th("Dzielnica"),
                html.Th("Adres"),
            ]))
        ]
        
        table_body = [html.Tr([html.Td(cell) for cell in row]) for row in table_data]
        
        table = dbc.Table(
            table_header + [html.Tbody(table_body)],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            className="mt-3"
        )
    
        return html.Div([
       html.H3("Tabela cen paliw", className="text-light" if dark_mode else "text-dark"),
       table,
       dcc.Download(id="download-table-data"),
       dbc.Button("Eksportuj do pliku CSV", id="export-button", color="primary", className="mt-4")
   ])
    
    
@app.callback(
    Output("sort-container", "style"),
    Input("tabs", "value")
)
def toggle_sort_dropdown(tab):
    if tab == "tab-2":
        return {'padding-top': '20px', 'paddingBottom': '20px'}
    return {'display': 'none'}
    
@app.callback(
    [Output("update-button", "children"),
     Output("updated-data-store", "data")],  
    Input("update-button", "n_clicks"),
    State("station-dropdown", "value"),
    State("fuel-dropdown", "value"),  
    State("price-input", "value")
)
def update_fuel_price(n_clicks, station, fuel_type, price):
    if n_clicks is not None and station and fuel_type and price:
        try:
            price = float(price)  
        except ValueError:
            return "Wprowadź prawidłową cenę", None  

        try:
            connection = psycopg2.connect(
                host="localhost",
                database="stacje_paliw",
                user="postgres",
                password="password"
            )
            cursor = connection.cursor()

            print(f"Aktualizuję cenę: {price} dla paliwa: {fuel_type} w stacji: {station}")

            if fuel_type == 'diesel':
                update_query = "UPDATE public.stacje_paliw SET diesel = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'lpg':
                update_query = "UPDATE public.stacje_paliw SET lpg = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'pb95':
                update_query = "UPDATE public.stacje_paliw SET pb95 = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'pb98':
                update_query = "UPDATE public.stacje_paliw SET pb98 = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"

            cursor.execute(update_query, (price, station))

            connection.commit()

            cursor.close()
            connection.close()

            return "Dane zaktualizowane", {"station": station, "fuel_type": fuel_type, "price": price}

        except Exception as e:
            print(f"Błąd połączenia z bazą: {e}")
            return "Błąd aktualizacji danych", None

    return "Zaktualizuj dane", None


@app.callback(
    Output("markers-layer", "children"),  
    Input("update-button", "n_clicks"),  
    State("station-dropdown", "value"),  
    State("fuel-dropdown", "value"), 
    State("price-input", "value") 
)
def update_markers(n_clicks, station, fuel_type, price):
    if n_clicks is not None and station and fuel_type and price:
        try:
            price = float(price)  
        except ValueError:
            return "Wprowadź prawidłową cenę", None  

        try:
            connection = psycopg2.connect(
                host="localhost",
                database="stacje_paliw",
                user="postgres",
                password="password"
            )
            cursor = connection.cursor()

            print(f"Aktualizuję cenę: {price} dla paliwa: {fuel_type} w stacji: {station}")

            # Tworzymy zapytanie, które zaktualizuje tylko odpowiedni rodzaj paliwa
            if fuel_type == 'diesel':
                update_query = "UPDATE public.stacje_paliw SET diesel = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'lpg':
                update_query = "UPDATE public.stacje_paliw SET lpg = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'pb95':
                update_query = "UPDATE public.stacje_paliw SET pb95 = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"
            elif fuel_type == 'pb98':
                update_query = "UPDATE public.stacje_paliw SET pb98 = %s WHERE CONCAT(nazwa_stacji, ' ', adres) = %s"

            cursor.execute(update_query, (price, station))

            connection.commit()

            cursor.close()
            connection.close()

            updated_markers = get_markers_from_db()  
            return updated_markers

        except Exception as e:
            print(f"Błąd połączenia z bazą: {e}")
            return "Błąd aktualizacji danych", None

    return no_update  

# Callback do zmiany trybu ciemny/jasny
@app.callback(
    [Output("app-container", "className"),
     Output("theme-store", "data")],
    Input("switch", "value"),
    Input("theme-store", "data")
)
def toggle_theme(switch_value, store_data):
    dark_mode = switch_value

    app_class = "bg-dark text-white" if dark_mode else "bg-light text-dark"

    store_data["dark_mode"] = dark_mode

    return app_class, store_data

from datetime import date

@app.callback(
    Output("download-table-data", "data"),
    Input("export-button", "n_clicks"),
    State("sort-fuel-dropdown", "value"),
    prevent_initial_call=True
)
def export_table_to_csv(n_clicks, sort_by):
    rows = get_table_data(sort_by)
    columns = ["Nazwa stacji", "Diesel [zł]", "LPG [zł]", "PB95 [zł]", "PB98 [zł]", "Dzielnica", "Adres"]
    df = pd.DataFrame(rows, columns=columns)

    today = date.today().isoformat()
    filename = f"ceny_paliw_{today}.csv"

    return dcc.send_data_frame(df.to_csv, filename=filename, index=False, encoding="utf-8-sig")


# Uruchamianie serwera
if __name__ == "__main__":
    app.run_server(debug=True)
