# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from flask import Flask, render_template, request
import Busqueda
import random

# Variables globales
app = Flask(__name__)
busq = Busqueda.Busqueda()
listaReceta = []
recetas_filtradas = []
ingrediente = "" # muestra recetas por defecto al no indicarle ningún ingrediente

# Se carga la pagina principal (index.html)
@app.route("/")
def index():
    global listaReceta
    global ingrediente

    busq.set_ingrediente(ingrediente)
    listaReceta = busq.buscar()
    random.shuffle(listaReceta) # las muestra de manera aleatoria

    return render_template("index.html", recetas=listaReceta, recetasf=listaReceta, ingred=ingrediente)


# Procesa el fomulario (de tipo get, para poder ver los ingredientes en la url)
@app.route("/procesar", methods=['GET'])
def procesar():
    global listaReceta
    global recetas_filtradas
    global ingrediente
    
    ingrediente_introducido = request.args.get("ingrediente")  # request del parametro ingrediente de la URL


    # Solo se hara la búsqueda si el ingrediente introducido por el usuario es un ingrediente nuevo
    if ingrediente_introducido != ingrediente:
        ingrediente = ingrediente_introducido
        busq.set_ingrediente(ingrediente)
        listaReceta = busq.buscar()
        recetas_filtradas = listaReceta

    return render_template("index.html", recetas=listaReceta, recetasf =recetas_filtradas, ingred=ingrediente)


# En footer.html se encuentra un script (JavaScript) que ejecuta AJAX para llamar a esta funcion
# el cual devuelve un objeto JSON con el que podremos obtener el valor del boton pulsado
# por el usuario, el cual se correspondera a uno de los tres valores que usaremos para
# filtrar el tiempo.
# Las recetas modificadas (recetas_filtradas) se renderizan a filtroTiempo.html, template que
# la funcion Javascript sustituirá en index.html para mostrar las recetas filtradas.
@app.route("/categorias", methods=['POST'])
def calcula_tiempo():
    global listaReceta
    global recetas_filtradas

    json = request.form
    tiempo_click = json['tiempo_clickado'] 
  
    recetas_filtradas = busq.filtrar_por_tiempo(tiempo_click, listaReceta) # Funcion que categoriza las recetas por tiempo
        
    return render_template("filtroTiempo.html", recetas_tiempo=recetas_filtradas)



# Funcion que muestra la informacion de la receta seleccionada por el usuario
# El parámetro para reconocer qué receta ha sido pulsada es la imagen, ya que es el único
# parámetro que sabemos con seguridad que siempre será distinto.
# Incluso si dos recetas tuviesen la misma imagen, al venir de fuentes de información distintas
# la URL obtenida ya no será la misma.
@app.route("/resultado", methods=['POST'])
def informacion_resultado(): 
    resultado = request.form.get("id-url-receta") # Usamos request.form.get porque el valor a recoger vienen de un formulario
    pagina = request.form.get("id-pag-original")
    ingr_obtenido = request.form.get("id-ingrediente")
    info_receta = busq.buscar_receta(resultado, pagina, ingr_obtenido)
    return render_template("resultado.html", informacion=info_receta) # Se carga un html nuevo (mostrar.html) tras la peticion


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


