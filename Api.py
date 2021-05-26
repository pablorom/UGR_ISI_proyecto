# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

import json
import requests
from werkzeug.utils import html
import MisRecetas

class Api:
      
    # Constructor de la clase Receta
    def __init__(self, ingred):
        self.app_id = '583703c0'
        self.app_key = '1c2dbf65b7d182baa76c867f0a0bea10'
        self.ingrediente = ingred
        # Si el usuario introduce los ingredientes separados con comas, las eliminamos
        self.ingrediente = self.ingrediente.replace(",","")

    # Método que inicializa el json a partir de la api de edaman   
    def inicializar_json(self, ingred):
        url_completa = 'https://api.edamam.com/search?q='+ingred+ \
            '&app_id='+self.app_id+'&app_key='+self.app_key+'&from=0&to=3'
        response = requests.get(url_completa)
        json_data = response.json()
        recipes = json_data['hits']

        return recipes

    # Obtención de la información del JSON
    def api_edamam(self):
        recipes = self.inicializar_json(self.ingrediente)

        lista_elem = []
        # Iteramos por todas las recetas
        for recipe in recipes:
            recipe = recipe['recipe']
            titulo = recipe['label']
            imagen = recipe['image']

            # La API ya nos devuelve toda la info en el JSON
            # Llamamos a los setters para dar valores a cada instancia de MiReceta
            receta = MisRecetas.MisRecetas(titulo, imagen, "EDAMAM API", ' ')

            receta.set_tiempo(int(recipe['totalTime']))
            receta.set_comensales(recipe['yield'])
            receta.set_urlReceta(recipe['url'])
            receta.set_source(recipe['source'])

            for ingredient in recipe['ingredients']:
                receta.add_ingrediente(ingredient["text"])

            lista_elem.append(receta)
        
        return lista_elem

    # Utilizamos este método para mostrar la información de una detallada 
    # de la receta que clickee el usuario. Sabremos qué receta es la que ha 
    # elegido a partir de la URL que recive 'recipe'
    def api_elemen_edamam(self, a_buscar, ingred):
        recipes = self.inicializar_json(ingred)

        # Iteramos por todas las recetas
        for recipe in recipes:
            recipe = recipe['recipe']
            if a_buscar == recipe['url']:
                titulo = recipe['label']
                imagen = recipe['image']
                
                receta = MisRecetas.MisRecetas(titulo, imagen, "EDAMAM API", ' ')

                receta.set_tiempo(int(recipe['totalTime']))
                receta.set_comensales(recipe['yield'])
                receta.set_urlReceta(recipe['url'])
                receta.set_source(recipe['source'])

                for ingredient in recipe['ingredients']:
                    receta.add_ingrediente(ingredient["text"])

                return receta

        return False  # Hacemos el return aunque si entramos a este metodo es porque la receta existe    
        

