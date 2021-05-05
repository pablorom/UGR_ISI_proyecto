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

class MisRecetas:
    
    # Constructor de la clase Receta
    def __init__(self,tit,img, orig):
        self.titulo = tit
        self.urlImagen = img
        self.paginaOriginal = orig
        #yo aniadiria un campo que indique el nombre de la pagina original
        
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
        