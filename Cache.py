# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

class Cache:

    #Constructor:
    def __init__(self):
        self.LIMITE_TAM = 10                # Límite del tamaño del diccionario que almacenará la caché
        self.NUMERO_BUSQUEDAS = 3           # Número de búsquedas necesarias para almacenar alguna búsqueda en caché
        self.TAM_REGISTRO_BUSQ = 100        # Número máximo del contador de búsquedas que se almacena en el diccionario de registro
        self.cache = dict()                 # Caché
        self.registro_busquedas = dict()    # Registro de búsquedas que irá contando cuántas veces se hace una búsqueda concreta
        self.historial_cache = list()       # Historial de ANTIGÜEDAD para ver qué se elimina cuando el caché llegue al límite
        self.historial_registro = list()    # Historial de ANTIGÜEDAD para ver qué se elimina si el registro de búsquedas llega al límite


    def nueva_busqueda(self, ingrediente, recetas):
        # Si el ingrediente buscado ya está en el registro de búsquedas actualizamos el historial para ponerlo como el más reciente
        if ingrediente in self.registro_busquedas:
            self.registro_busquedas[ingrediente] = self.registro_busquedas[ingrediente] + 1

            # Actualizamos el historial del registro
            self.historial_registro.remove(ingrediente)
            self.historial_registro.insert(0, ingrediente)

            if self.registro_busquedas[ingrediente] >= self.NUMERO_BUSQUEDAS:
                self.guardar_en_cache(ingrediente, recetas)
        
        else:

            if len(self.historial_registro) == 0:
                self.registro_busquedas[ingrediente] = 1
                self.historial_registro.append(ingrediente)

            elif len(self.historial_registro) < self.TAM_REGISTRO_BUSQ:
                self.registro_busquedas[ingrediente] = 1
                self.historial_registro.insert(0, ingrediente)

            elif len(self.historial_registro) == self.TAM_REGISTRO_BUSQ:
                x = self.historial_registro[self.TAM_REGISTRO_BUSQ - 1]

                self.historial_registro.remove(x)
                self.historial_registro.insert(0, ingrediente)

                del self.registro_busquedas[x]
                self.registro_busquedas[ingrediente] = 1

    
    def guardar_en_cache(self, ingrediente, recetas):

        if ingrediente in self.historial_cache:
            self.historial_cache.remove(ingrediente)
            self.historial_cache.insert(0, ingrediente)

        else:
            if len(self.historial_cache) == 0:
                self.cache[ingrediente] = recetas
                self.historial_cache.append(ingrediente)

            elif len(self.historial_cache) < self.LIMITE_TAM:
                self.cache[ingrediente] = recetas
                self.historial_cache.insert(0, ingrediente)

            elif len(self.historial_cache) == self.LIMITE_TAM:
                x = self.historial_cache[self.LIMITE_TAM - 1]

                self.historial_cache.remove(x)
                self.historial_cache.insert(0, ingrediente)

                del self.cache[x]
                self.cache[ingrediente] = recetas


    def get_recetas(self, ingrediente):
        return self.cache[ingrediente]

    
    def esta_en_cache(self, ingrediente):
        return ingrediente in self.cache.keys()





