# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from bs4 import BeautifulSoup
import requests
from werkzeug.utils import html
import MisRecetas

class WebScrapping:
    
    
    # Constructor de la clase Receta
    def __init__(self, ingred):
        self.ingrediente = ingred

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

        lista_elem = []
        
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
            
            if elem.find('span', class_="property duracion") is not None:
                receta.set_tiempo(elem.find('span', class_='property duracion').text)
            
            lista_elem.append(receta)
        
        return lista_elem


    def informacion_receta_recetasgratis(self,url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        titulo = soup.find('h1', class_="titulo titulo--articulo").text
        imagen = soup.find('div', class_="imagen lupa").find('img').get('src')

        receta = MisRecetas.MisRecetas(titulo, imagen, "RECETAS GRATIS", url)

        # Este span proporciona la 'dificultad' 'tiempo' y 'comensales', sin embargo
        # en la página solo se muestra el tiempo y los comensales, por lo que nos quedamos con
        # la segunda y tercera posicion del array
        busqueda_tiempo = soup.find('span', class_='property duracion')
        busqueda_comensales = soup.find('span', class_='property comensales')
        busqueda_categoria = soup.find('span', class_='property para')

        if busqueda_tiempo is not None:
            receta.set_tiempo(busqueda_tiempo.text)

        if busqueda_comensales is not None:
            receta.set_comensales(busqueda_comensales.text)
        
        if busqueda_categoria is not None:
            receta.set_categoria(busqueda_categoria.text)


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

        lista_elem = []

        for elem in elementos:
            # Obtenemos los parámetros deseados
            # Como el tag <a href...> donde se aloja el titulo no tiene ningún atributo 'class'
            # no se puede hacer la búsqueda por la clase, de forma que buscamos todos los <a href>
            # dentro del artículo y solo guardamos el atributo 'title'
            titulo = elem.find('a', href=True).find('strong').text
            imagen = elem.find('img', class_='rdr-image wp-post-image').get('src')

            # Obtenemos la URL donde se encuentra la información detallada de la receta para poder
            # hacer el webscrapping de más información (ingredientes, tiempo....)
            infoLaReceta = (elem.find('a', href=True).get('href'))

            # Aniadimos los parámetros obtenidos del webScrapping en una lista de
            # elementos de tipo MisRecetas.
            # Es necesario escribir "MisRecetas.MisRecetas" para llamar a la clase
            # MisRecetas que está dentro del módulo con el mismo nombre
            receta = MisRecetas.MisRecetas(titulo, imagen, "RECETAS DE RECHUPETE", infoLaReceta)
            
            lista_elem.append(receta)

        return lista_elem
  
            
    def informacion_receta_rechupete(self,url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        titulo = soup.find('header').find('h1').text
        imagen_list = soup.find_all('img', attrs={"loading": "lazy"})
        imagen = imagen_list[1].get('src')

        receta = MisRecetas.MisRecetas(titulo, imagen, "RECETAS DE RECHUPETE", url)

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