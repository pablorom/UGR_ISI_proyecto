# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

import WebScrapping

class Busqueda:

    # Constructor de la clase Receta
    def __init__(self):
        self.ingrediente = ""
        self.listaReceta = []

    def get_ingrediente(self):
        return self.ingrediente
    
    def set_ingrediente(self, ingr):
        self.ingrediente = ingr
        # Si el usuario introduce los ingredientes separados con comas, las eliminamos
        self.ingrediente = self.ingrediente.replace(",","")
    
    # Se llama a los metodos que realizan WebScrapping sobre Recetas Gratis y No Solo Dulces
    def busqueda_scrapping(self):
        ws = WebScrapping.WebScrapping(self.ingrediente)  # Se realiza el web scrapping del ingrediente
        ws.buscar_recetasGratis()
        # self.listaReceta contiene los ingredientes de ambas paginas
        self.listaReceta = ws.buscar_rechupete()
        print("API EDAMAM")
        ws.api_edamam()

        return self.listaReceta

    # Aqui falta el método que realiza la búsqueda con la API 

    def buscar(self):
        self.listaReceta = self.busqueda_scrapping()
        # Aqui se llamaria al método que hace una busqueda con la API

        return self.listaReceta

    # Método que muestra los resultados (para comprobar que funciona bien)
    def buscar_receta(self, imagen):
        #return next(r for r in self.listaReceta if r.get_urlImagen() == imagen)
        info_basica_receta = next(r for r in self.listaReceta if r.get_urlImagen() == imagen)
        ws = WebScrapping.WebScrapping("")

        if info_basica_receta.get_paginaOriginal() == "RECETAS DE RECHUPETE":
            info_completa_receta = ws.informacion_receta_rechupete(info_basica_receta)
        elif info_basica_receta.get_paginaOriginal() == "RECETAS GRATIS":
            info_completa_receta = ws.informacion_receta_recetasgratis(info_basica_receta)

        return info_completa_receta
