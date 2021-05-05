# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

import WebScrapping

class Busqueda:

    # Constructor de la clase Receta
    def __init__(self, ingred):
        self.ingrediente = ingred
        self.listaReceta = []
        # Si el usuario introduce los ingredientes separados con comas, las eliminamos
        self.ingrediente = self.ingrediente.replace(",","")

    # Se llama a los metodos que realizan WebScrapping sobre Recetas Gratis y No Solo Dulces
    def busqueda_scrapping(self):
        ws = WebScrapping.WebScrapping(self.ingrediente)  # Se realiza el web scrapping del ingrediente
        ws.buscar_recetasGratis()
        # self.listaReceta contiene los ingredientes de ambas paginas
        self.listaReceta = ws.buscar_nosolodulces()

        return self.listaReceta

    # Aqui falta el método que realiza la búsqueda con la API 

    def buscar(self):
        self.listaReceta = self.busqueda_scrapping()
        # Aqui se llamaria al método que hace una busqueda conn la API

        return self.listaReceta

    # Método que muestra los resultados (para comprobar que funciona bien)
    def mostrar_receta(self):
        if len(self.listaReceta) != 0:
            for lr in self.listaReceta:
                print(lr.get_nombre())
                print(lr.get_urlImagen())
                print(lr.get_paginaOriginal())
                print("")
        else:
            print("No se ha obtenido ningún resultado para: " + self.ingrediente)