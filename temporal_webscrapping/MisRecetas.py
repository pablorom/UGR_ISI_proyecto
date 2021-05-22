# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

"""
    En esta clase se define los parámetros comunes de 
    la información obtenida al usar WebScrapping y la API
"""

class MisRecetas(object):
    
    # Constructor de la clase Receta
    def __init__(self,tit,img,orig,url):
        self.titulo = tit
        self.urlImagen = img
        self.paginaOriginal = orig
        self.urlReceta = url
        self.tiempo = "No disponible"
        self.comensales = "No disponible"
        self.categoria = "No disponible"
        self.ingredientes = []
        
        
    # Definimos los get y set de las variables   
    def get_nombre(self):
        return self.titulo
    
    def set_nombre(self, tit):
        self.titulo = tit
        
    def get_urlImagen(self):
        return self.urlImagen
    
    def set_urlImagen(self, imagen):
        self.urlImagen = imagen

    def get_paginaOriginal(self):
        return self.paginaOriginal
    
    def set_paginaOriginal(self, orig):
        self.paginaOriginal = orig

    def get_urlReceta(self):
        return self.urlReceta
    
    def set_urlReceta(self, url):
        self.urlReceta = url    

    def get_tiempo(self):
        return self.tiempo
    
    def set_tiempo(self, tmp):
        self.tiempo = tmp

    def get_comensales(self):
        return self.comensales
    
    def set_comensales(self, px):
        self.comensales = px

    def get_categoria(self):
        return self.categoria
    
    def set_categoria(self, cat):
        self.categoria = cat
        
    def get_ingredientes(self):
        return self.ingredientes
    
    def add_ingrediente(self, ingr):
        self.ingredientes.append(ingr)

    def remove_ingredientes(self):
        self.ingredientes.clear()

    