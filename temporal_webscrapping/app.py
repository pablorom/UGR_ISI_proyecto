# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from flask import Flask, render_template, request
import WebScrapping

app = Flask(__name__)

# Se carga la pagina principal (index.html)
@app.route("/")
def index():
    return render_template("index.html")

# Procesa el fomulario (de tipo get, para poder ver los ingredientes en la url)
@app.route("/procesar", methods=['GET'])
def procesar():
    ingrediente = request.args.get("ingrediente")  # request del parametro ingrediente del formulario
    ws = WebScrapping.WebScrapping(ingrediente)  # Se realiza el web scrapping del ingrediente
    ws.buscar_recetasGratis()
    ws.buscar_nosolodulces()
    ws.mostrar_receta()
    return render_template("mostrar.html", ingrediente=ingrediente) # Se carega un html nuevo (mostrar.html) tras la peticion

# No borrar este metodo (por ahora) ... esto deberia cambiarse por el servidor cloud
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5500, debug=True)


