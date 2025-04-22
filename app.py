from flask import Flask, render_template  # Importar Flask y render_template para crear la aplicación web
import json  # Importar el módulo json para manejar archivos JSON
import plotly  # Importar la biblioteca Plotly para crear gráficos interactivos
import plotly.express as px  # Importar Plotly Express para crear gráficos de manera sencilla
import pandas as pd  # Importar pandas para manejar datos en forma de DataFrame
from collections import Counter  # Importar Counter para contar elementos en listas
import os  # Importar os para manejar variables de entorno 

app = Flask(__name__, template_folder='templates')


# Función para cargar los datos del archivo GeoJSON
def cargar_datos():
    with open("clubes_deportivos.geojson.txt", "r", encoding="utf-8") as f:  # Abrir el archivo GeoJSON
        data = json.load(f)
    clubs = [feature["properties"] for feature in data["features"]]  # Extraer propiedades de cada club
    
    # Extraer comunas, barrios y tipos de clubes
    comunas = [str(club.get("com")).strip() for club in clubs if club.get("com")]
    barrios = [str(club.get("bar")).strip() for club in clubs if club.get("bar")]
    tipos = [str(club.get("tip")).strip() for club in clubs if club.get("tip")]
    
    return comunas, barrios, tipos  # Listas de comunas, barrios y tipos de clubes

# Función para generar los gráficos
def generar_graficos():
    comunas, barrios, tipos = cargar_datos()  # Cargar datos desde el archivo GeoJSON
    
    # Contar la cantidad de clubes por comuna, tipo y barrio
    conteo_comunas = Counter(comunas)
    df_comunas = pd.DataFrame(conteo_comunas.items(), columns=["Comuna", "Cantidad"])
    fig_comunas = px.bar(df_comunas, x="Comuna", y="Cantidad", title="Cantidad de Clubes por Comuna")

    conteo_tipos = Counter(tipos)
    df_tipos = pd.DataFrame(conteo_tipos.items(), columns=["Tipo", "Cantidad"])
    fig_tipos = px.pie(df_tipos, names="Tipo", values="Cantidad", title="Distribución por Tipo de Club")

    conteo_barrios = Counter(barrios).most_common(10)
    df_barrios = pd.DataFrame(conteo_barrios, columns=["Barrio", "Cantidad"])
    fig_barrios = px.bar(df_barrios, x="Cantidad", y="Barrio", orientation="h", title="Top 10 Barrios con Más Clubes")

    # Convertir las figuras de Plotly a formato JSON para ser insertadas en la plantilla
    graficos = {
        "comunas": json.dumps(fig_comunas, cls=plotly.utils.PlotlyJSONEncoder),
        "tipos": json.dumps(fig_tipos, cls=plotly.utils.PlotlyJSONEncoder),
        "barrios": json.dumps(fig_barrios, cls=plotly.utils.PlotlyJSONEncoder)
    }

    return graficos

# Ruta principal
@app.route("/")
def index():
    graficos = generar_graficos()  # Obtener los gráficos generados
    return render_template("index.html", graficos=graficos)  # Renderizar la plantilla y pasar los gráficos

if __name__ == "__main__":
    # Obtener el puerto de la variable de entorno o usar el puerto 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Escuchar en todas las interfaces disponibles
