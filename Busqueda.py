# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

import WebScrapping
import Cache


class Busqueda:

    # Constructor de la clase Receta
    def __init__(self):
        self.ingrediente = ""
        self.listaReceta = []
        self.cache = Cache.Cache()

    def get_ingrediente(self):
        return self.ingrediente
    
    def set_ingrediente(self, ingr):
        self.ingrediente = ingr
        # Si el usuario introduce los ingredientes separados con comas, las eliminamos
        self.ingrediente = self.ingrediente.replace(",","")

    
    # Aqui falta el método que realiza la búsqueda con la API 
    # Se llama a los metodos que hace petición a la API
    def busqueda_api(self):
        # Si el ingrediente es vacio la API no devolverá nada
        if(self.ingrediente != ''):
                ws = WebScrapping.WebScrapping(self.ingrediente)
                lista_recetasEdamam = ws.api_edamam()
                return lista_recetasEdamam
        else:
            return []

        
    
    # Se llama a los metodos que realizan WebScrapping sobre Recetas Gratis y No Solo Dulces
    def busqueda_scrapping(self):
        if self.cache.esta_en_cache(self.ingrediente):
            self.listaReceta = self.cache.get_recetas(self.ingrediente)

        else:
            ws = WebScrapping.WebScrapping(self.ingrediente)  # Se realiza el web scrapping del ingrediente
            lista_recetasgratis = ws.buscar_recetasGratis()
            # self.listaReceta contiene los ingredientes de ambas paginas
            lista_rechupete = ws.buscar_rechupete()
            lista_api = self.busqueda_api()

            self.listaReceta = []

            if len(lista_recetasgratis) < len(lista_rechupete):
                for i in range(len(lista_recetasgratis)):
                    self.listaReceta.append(lista_recetasgratis[i])
                    self.listaReceta.append(lista_rechupete[i])
                    

                for i in range(len(lista_recetasgratis), len(lista_rechupete)):
                    self.listaReceta.append(lista_rechupete[i]) 
            else:
                for i in range(len(lista_rechupete)):
                    self.listaReceta.append(lista_recetasgratis[i])
                    self.listaReceta.append(lista_rechupete[i])

                for i in range(len(lista_rechupete), len(lista_recetasgratis)):
                    self.listaReceta.append(lista_recetasgratis[i])


            for receta in lista_api:
                self.listaReceta.append(receta)

            self.cache.nueva_busqueda(self.ingrediente, self.listaReceta)

        return self.listaReceta

    

    def buscar(self):
        self.listaReceta = self.busqueda_scrapping()

        return self.listaReceta

    # Método que muestra los resultados (para comprobar que funciona bien)
    def buscar_receta(self, imagen):
        ws = WebScrapping.WebScrapping("")

        info_basica_receta = next(r for r in self.listaReceta if r.get_urlImagen() == imagen)
        
        if info_basica_receta.get_paginaOriginal() == "RECETAS DE RECHUPETE":
            info_completa_receta = ws.informacion_receta_rechupete(info_basica_receta)
        elif info_basica_receta.get_paginaOriginal() == "RECETAS GRATIS":
            info_completa_receta = ws.informacion_receta_recetasgratis(info_basica_receta)
        elif info_basica_receta.get_paginaOriginal() == "EDAMAM API":
            info_completa_receta = info_basica_receta

        return info_completa_receta


    # Método que filtra las recetas obtenidas tras la búsqueda
    # a razoón del tiempo seleccionado por el usuario
    # Valores de tiempo: poco | medio | mucho !!!! :)
    def filtrar_por_tiempo(self, tiempo_elegido , recetas):
        recetas_filtradas = []

        # ¡NOTA! Este metodo lo he hecho para probar que funciona...
        # Si entrais en la pagina y pulsais uno de los botones para filtrar
        # la lista de recetas que aparece debera de cambiar y solamente aparecerán
        # las recetas que tienen el atributo tiempo a "No disponible" :)
        # Cuando se haga la filtracion por tiempo esto ya no debera estar aquí jeje
        for receta in recetas:
            tiempo = receta.get_tiempo()
            minutos_totales = -1

            if tiempo != "No disponible":

                if receta.get_paginaOriginal() == "RECETAS GRATIS":


                    if " " in tiempo:
                        horas,minutos = tiempo.split(" ")

                        indice = horas.find("h")
                        horas = horas[0:indice]

                        minutos_totales = int(horas) * 60

                        indice = minutos.find("m")
                        minutos = minutos[0:indice]

                        minutos_totales = minutos_totales + int(minutos)

                    elif "h" in tiempo:
                        horas = tiempo
                        
                        indice = horas.find("h")
                        horas = horas[0:indice]

                        minutos_totales = int(horas) * 60
                        
                
                    elif "m" in tiempo:
                        minutos = tiempo

                        indice = minutos.find("m")
                        minutos = minutos[0:indice]

                        minutos_totales = int(minutos)

                elif receta.get_paginaOriginal() == "EDAMAM API":

                     minutos_totales = tiempo

                
                if tiempo_elegido == "poco":
                    if minutos_totales > 0 and minutos_totales <= 30:
                        recetas_filtradas.append(receta)
                elif tiempo_elegido == "medio":
                    if minutos_totales > 30 and minutos_totales <= 60:
                        recetas_filtradas.append(receta)
                elif tiempo_elegido == "mucho":
                    if minutos_totales > 60:
                        recetas_filtradas.append(receta)

        return recetas_filtradas
            



        # Para la filtracion... 
        # No incluir ninguna que tenga valor "No disponible"
        # Las recetas de la API solo contienen un numero
        # Las recetas de RecetasGratis tienen los valores: 10m, 15m, ..., 45m , 1h 30m, 2h 30m, 3h, ... 24h
        # Las recetas de RecetasRechupete tienen los valores: 35 min 55 min, 90 min...
        # Se que en python existen funciones como is_numeric(), replace('min', '')...

        return recetas_filtradas


