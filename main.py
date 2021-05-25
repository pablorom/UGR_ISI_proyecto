# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from re import search
from flask import Flask, render_template, request
import Busqueda
import random

app = Flask(__name__)
#app.secret_key = "KEY"
busq = Busqueda.Busqueda()
listaReceta = []

# Se carga la pagina principal (index.html)

@app.route("/")
def index():
    global listaReceta

    ingrediente = ""  # muestra recetas por defecto al no indicarle ningún ingrediente
    busq.set_ingrediente(ingrediente)
    listaReceta = busq.buscar()
    random.shuffle(listaReceta) # las muestra de manera aleatoria
    return render_template("index.html", recetas=listaReceta)


# Procesa el fomulario (de tipo get, para poder ver los ingredientes en la url)
@app.route("/procesar", methods=['GET'])
def procesar():
    global listaReceta
    ingrediente = request.args.get("ingrediente")  # request del parametro ingrediente de la URL
    busq.set_ingrediente(ingrediente)
    listaReceta = busq.buscar()
    return render_template("index.html", recetas=listaReceta) # Se carga un html nuevo (mostrar.html) tras la peticion


# Procesa el fomulario (de tipo get, para poder ver los ingredientes en la url)
@app.route("/categorias", methods=['POST'])
def calcula_tiempo():
    global listaReceta

    #tiempo_id = request.data.decode('UTF-8')
    json = request.form
    tiempo_click = json['tiempo_clickado']
  
    recetas_filtradas = busq.filtrar_por_tiempo(tiempo_click, listaReceta)
    
    
    return render_template("filtroTiempo.html", recetas_tiempo=recetas_filtradas)
    

@app.route("/resultado", methods=['POST'])
def informacion_resultado(): 
    resultado = request.form.get("id-image") # Usamos request.form.get porque el valor a recoger vienen de un formulario
    info_receta = busq.buscar_receta(resultado)
    return render_template("resultado.html", informacion=info_receta) # Se carga un html nuevo (mostrar.html) tras la peticion


# No borrar este metodo (por ahora) ... esto deberia cambiarse por el servidor cloud
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


