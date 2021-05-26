# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

import WebScrapping
import Api
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

    
    # Se llama a los metodos que hace petición a la API
    def busqueda_api(self):
        # Si el ingrediente es vacio la API no devolverá nada
        if(self.ingrediente != ''):
            api_busqueda = Api.Api(self.ingrediente)
            lista_recetasEdamam = api_busqueda.api_edamam()
            
            return lista_recetasEdamam
        else:
            return []

           
    # Se llama a los metodos que realizan WebScrapping sobre Recetas Gratis y Recetas de Rechupete
    def busqueda_scrapping(self):
        ws = WebScrapping.WebScrapping(self.ingrediente)  # Se realiza el web scrapping del ingrediente
        self.listaReceta = ws.buscar_recetasGratis()
        self.listaReceta.extend(ws.buscar_rechupete()) # self.listaReceta contiene los ingredientes de ambas paginas

        return self.listaReceta

    def buscar(self):
        # Si el ingrediente está en caché, obtenemos las recetas de la caché
        # De lo contrario, realizamos el webscrapping y busqueda en la API del ingrediente
        if self.cache.esta_en_cache(self.ingrediente):
            self.listaReceta = self.cache.get_recetas(self.ingrediente)
        else:
            self.listaReceta = self.busqueda_scrapping()
            self.listaReceta.extend(self.busqueda_api()) # contiene los ingredientes de las tres fuentes de informacion

        # Las ordenamos por orden alfabético para mezclar las fuentes de información
        self.listaReceta.sort(key=lambda h: (h.get_nombre()))  
     
        # Añadimos el ingrediente buscado y sus recetas obtenidas en la caché
        self.cache.nueva_busqueda(self.ingrediente, self.listaReceta)

        return self.listaReceta

    # Método que muestra la informacion detallada de la receta elegida por el usuario
    def buscar_receta(self, a_buscar, pagina_recibida, ingr_recibido):
        ws = WebScrapping.WebScrapping("")
              
        if pagina_recibida == "RECETAS DE RECHUPETE":
            info_completa_receta = ws.informacion_receta_rechupete(a_buscar)
        elif pagina_recibida == "RECETAS GRATIS":
            info_completa_receta = ws.informacion_receta_recetasgratis(a_buscar)
        elif pagina_recibida == "EDAMAM API":
            # Si la receta se encuentra en la lista de recetas, la buscamos
            info_completa_receta = 0
            for r in self.listaReceta:
                if r.get_urlReceta() == a_buscar:
                    info_completa_receta = r
                    break;

            # Es posible que no se cuentre en la lista de recetas
            # (por ejemplo, cuando el usuario busca varios ingredientes y despues vuelve hacia atrás)
            # por lo que deberemos buscar la receta en la api para obtener su información
            if info_completa_receta == 0:
                api_busqueda = Api.Api(ingr_recibido)
                info_completa_receta = api_busqueda.api_elemen_edamam(a_buscar, ingr_recibido)

        return info_completa_receta


    # Método que filtra las recetas obtenidas tras la búsqueda
    # a razoón del tiempo seleccionado por el usuario
    def filtrar_por_tiempo(self, tiempo_elegido , recetas):
        recetas_filtradas = []

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

                # POCO, MEDIO Y MUCHO son los valores que devuelven los botones
                # que el usuario puede elegir para filtrar sus recetas
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


