# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from bs4 import BeautifulSoup
import json
import requests
import MisRecetas

class WebScrapping:
    
    
    # Constructor de la clase Receta
    def __init__(self, ingred):
        self.ingrediente = ingred
        self.listaReceta = []
        # Si el usuario introduce los ingredientes separados con comas, las eliminamos
        self.ingrediente = self.ingrediente.replace(",","")

        
    # Metodo que realice el WebScrapping de "Recetas Gratis"    
    def buscar_recetasGratis(self):
        url = 'https://www.recetasgratis.net/busqueda?q='
        # ¡NOTA! Sirve tanto con uno como con más de un ingrediente
        # ya que varios ingredientes se reciben de la forma ingrediente=ing1+ing2
        url_completa = url + self.ingrediente
        html_text = requests.get(url_completa).text
        soup = BeautifulSoup(html_text, 'lxml')
        elementos = soup.find_all('div', class_ = 'resultado link')
        
        for elem in elementos:
            # Obtenemos los parámetros deseados
            titulo = elem.find('a', class_='titulo').text
            imagen = elem.find('img', class_='imagen').get('data-imagen')

            # Obtenemos la URL donde se encuentra la información detallada de la receta para poder
            # hacer el webscrapping de más información (ingredientes, tiempo....)
            infoLaReceta = elem.find('a', href=True).get('href') 
            
            # Aniadimos los parámetros obtenidos del webScrapping en una lista de
            # elementos de tipo MisRecetas.
            # Es necesario escribir "MisRecetas.MisRecetas" para llamar a la clase
            # MisRecetas que está dentro del módulo con el mismo nombre
            receta = MisRecetas.MisRecetas(titulo, imagen, "RECETAS GRATIS", infoLaReceta)
            receta.set_categoria(elem.find('div', class_='etiqueta').text)
            self.listaReceta.append(receta)


    def informacion_receta_recetasgratis(self,receta):
        html_text = requests.get(receta.get_urlReceta()).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Este spam proporciona la 'dificultad' 'tiempo' y 'comensales', sin embargo
        # en la página solo se muestra el tiempo y los comensales, por lo que nos quedamos con
        # la segunda y tercera posicion del array
        if soup.find('div', class_='properties') is not None:
            receta.set_tiempo(soup.find('span', class_='property duracion').text)
            receta.set_comensales(soup.find('span', class_='property comensales').text)

        # Obtención de los ingredientes
        lista_ingredientes = soup.find_all('li', class_="ingrediente")
        # Se debe borrar la lista antes de rellenarla ya que si el usuario recarga la pagina de una receta
        # el objeto sdigue existiendo y multiplica la información
        receta.remove_ingredientes()
        if len(lista_ingredientes) > 0: 
            for lst in lista_ingredientes:
                lst = lst.text
                lst = lst.replace("\n", "")
                receta.add_ingrediente(lst)

        # Obtenemos los pasos de la receta correspondiente
        lista_preparacion = soup.find_all('div', class_='apartado')
        receta.remove_preparacion()

        if len(lista_preparacion) > 0:
            for prep in lista_preparacion:
                # Es necesario este if para recoger exclusivamente los pasos pertenecientes a la receta
                # y omitir información no necesaria de la página
                if prep.find('div', class_='orden') is not None:
                    parrafo = prep.find('p').text   
                    receta.add_preparacion(parrafo)             

        return receta


    # Metodo que realice el WebScrapping de "Recetas de Rechupete"  
    def buscar_rechupete(self):
        url = 'https://www.recetasderechupete.com/?s='
        url_completa = url + self.ingrediente
        html_text = requests.get(url_completa).text
        soup = BeautifulSoup(html_text, 'lxml')
        elementos = soup.find_all('div', class_='pure-u-1-2 pure-u-lg-1-5')

        for elem in elementos:
            # Obtenemos los parámetros deseados
            # Como el tag <a href...> donde se aloja el titulo no tiene ningún atributo 'class'
            # no se puede hacer la búsqueda por la clase, de forma que buscamos todos los <a href>
            # dentro del artículo y solo guardamos el atributo 'title'
            titulo = elem.find('a', href=True).find('strong').text
            imagen = elem.find('img', class_='rdr-image wp-post-image').get('src')

            # Obtenemos la URL donde se encuentra la información detallada de la receta para poder
            # hacer el webscrapping de más información (ingredientes, tiempo....)
            infoLaReceta = elem.find('a', href=True).get('href')          
            

            # Aniadimos los parámetros obtenidos del webScrapping en una lista de
            # elementos de tipo MisRecetas.
            # Es necesario escribir "MisRecetas.MisRecetas" para llamar a la clase
            # MisRecetas que está dentro del módulo con el mismo nombre
            receta = MisRecetas.MisRecetas(titulo, imagen, "RECETAS DE RECHUPETE", infoLaReceta)
            self.listaReceta.append(receta)

        return self.listaReceta
  
            
    def informacion_receta_rechupete(self,receta):
        html_text = requests.get(receta.get_urlReceta()).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Este spam proporciona la 'dificultad' 'tiempo' y 'comensales', sin embargo
        # en la página solo se muestra el tiempo y los comensales, por lo que nos quedamos con
        # la segunda y tercera posicion del array
        info_aux = soup.find_all('span', class_='rdr-tag')
        if len(info_aux) > 0:
            receta.set_tiempo(info_aux[1].text)
            receta.set_comensales(info_aux[2].text)

        # Nos quedamos con la primera categoria indicada por la página
        categoria_div = soup.find('div', {'id':'extrainfo'})
        if categoria_div is not None:
            categorias = categoria_div.find_all('a', href=True)
            receta.set_categoria(categorias[0].text)

        # Obtención de los ingredientes
        ingredientes_div = soup.find('div', {'id':'ingredients'})

        # Se debe borrar la lista antes de rellenarla ya que si el usuario recarga la pagina de una receta
        # el objeto sdigue existiendo y multiplica la información
        receta.remove_ingredientes()

        if ingredientes_div is not None:
            lista_ingredientes = ingredientes_div.find('ul').find_all('li')
          
            for lst in lista_ingredientes:
                receta.add_ingrediente(lst.text)
        
        # Obtenemos los pasos de la receta correspondiente
        preparacion_div = soup.find('div', {'id':'description'})
        receta.remove_preparacion()

        if preparacion_div is not None:
            lista_preparacion = preparacion_div.find_all('ol')
            for prep in lista_preparacion:
                lista_parrafos = prep.find_all('li')
                for p in lista_parrafos:
                    receta.add_preparacion(p.text)


        return receta


    # Peticion a la API edamam
    def api_edamam(self):
        app_id = '583703c0'
        app_key = '1c2dbf65b7d182baa76c867f0a0bea10'
        url = 'https://api.edamam.com'
        url_completa = 'https://api.edamam.com/search?q='+self.ingrediente+'&app_id='+app_id+'&app_key='+app_key+'&from=0&to=3'
        response = requests.get(url_completa)
        json_data = response.json()
        recipes = json_data['hits']
        #We iterate through all recipes
        for rec in recipes:
            print(rec['recipe']['image'])
  
            
    def informacion_receta_edamam(self,receta):
        return receta
            
            
    
