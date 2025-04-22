from flask import Flask, render_template # Importar Flask y render_template para crear la aplicación web

import json # Importar el módulo json para manejar archivos JSON

import plotly # Importar la biblioteca Plotly para crear gráficos interactivos

import plotly.express as px # Importar Plotly Express para crear gráficos de manera sencilla

import pandas as pd # Importar pandas para manejar datos en forma de DataFrame

from collections import Counter # Importar Counter para contar elementos en listas

app = Flask(__name__)



def cargar_datos():
    with open("clubes_deportivos.geojson.txt", "r", encoding="utf-8") as f: # Abrir el archivo GeoJSON. "clubes_deportivos.geojson.txt" es el archivo que contiene los datos de los clubes deportivos en formato GeoJSON.
        
        data = json.load(f)
    clubs = [feature["properties"] for feature in data["features"]] # Extraer propiedades de cada club
    # Extraer comunas, barrios y tipos de clubes
    comunas = [str(club.get("com")).strip() for club in clubs if club.get("com")] # "com" es la clave para la comuna en el GeoJSON
    barrios = [str(club.get("bar")).strip() for club in clubs if club.get("bar")] 
    tipos = [str(club.get("tip")).strip() for club in clubs if club.get("tip")]
    
    return comunas, barrios, tipos # Listas de comunas, barrios y tipos de clubes

def generar_graficos():

    comunas, barrios, tipos = cargar_datos() # Cargar datos desde el archivo GeoJSON
    
    # Contar la cantidad de clubes por comuna, tipo y barrio
    conteo_comunas = Counter(comunas)
    df_comunas = pd.DataFrame(conteo_comunas.items(), columns=["Comuna", "Cantidad"]) # Crear DataFrame para las comunas
    fig_comunas = px.bar(df_comunas, x="Comuna", y="Cantidad", title="Cantidad de Clubes por Comuna") # Gráfico de barras para comunas

    conteo_tipos = Counter(tipos)
    df_tipos = pd.DataFrame(conteo_tipos.items(), columns=["Tipo", "Cantidad"])
    fig_tipos = px.pie(df_tipos, names="Tipo", values="Cantidad", title="Distribución por Tipo de Club")

    conteo_barrios = Counter(barrios).most_common(10)
    df_barrios = pd.DataFrame(conteo_barrios, columns=["Barrio", "Cantidad"])
    fig_barrios = px.bar(df_barrios, x="Cantidad", y="Barrio", orientation="h", title="Top 10 Barrios con Más Clubes")

    graficos = { # Crear un diccionario para almacenar los gráficos
        "comunas": json.dumps(fig_comunas, cls=plotly.utils.PlotlyJSONEncoder), # Convierte la figura de Plotly a JSON para su uso
        "tipos": json.dumps(fig_tipos, cls=plotly.utils.PlotlyJSONEncoder),
        "barrios": json.dumps(fig_barrios, cls=plotly.utils.PlotlyJSONEncoder)
    }

    return graficos

@app.route("/")
def index():
    graficos = generar_graficos()
    return render_template("index.html", graficos=graficos)

if __name__ == "__main__":
    app.run()
