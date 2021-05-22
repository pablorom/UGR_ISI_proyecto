# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from flask import Flask, render_template, request
import Busqueda

app = Flask(__name__)
busq = Busqueda.Busqueda()

# Se carga la pagina principal (index.html)

@app.route("/")
def index():
    ingrediente = ""  # muestra recetas por defecto al no indicarle ningún ingrediente
    busq.set_ingrediente(ingrediente)
    listaReceta = busq.buscar()
    return render_template("index.html", recetas=listaReceta)

# Procesa el fomulario (de tipo get, para poder ver los ingredientes en la url)
@app.route("/procesar", methods=['GET'])
def procesar():
    ingrediente = request.args.get("ingrediente")  # request del parametro ingrediente de la URL
    busq.set_ingrediente(ingrediente)
    listaReceta = busq.buscar()
    return render_template("index.html", recetas=listaReceta) # Se carega un html nuevo (mostrar.html) tras la peticion

@app.route("/resultado", methods=['POST'])
def informacion_resultado(): 
    resultado = request.form.get("id-image") # Usamos request.form.get porque el valor a recoger vienen de un formulario
    info_receta = busq.buscar_receta(resultado)
    return render_template("resultado.html", informacion=info_receta) # Se carega un html nuevo (mostrar.html) tras la peticion

# No borrar este metodo (por ahora) ... esto deberia cambiarse por el servidor cloud
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5500, debug=True)


