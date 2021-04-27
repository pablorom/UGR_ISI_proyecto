# -*- coding: utf-8 -*-
"""
@author: Alba Casillas Rodríguez
@author: Pablo Robles Molina
@author: Tomás Ruíz Fernández
"""

from bs4 import BeautifulSoup
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
            #Obtenemos los parámetros deseados
            titulo = elem.find('a', class_='titulo').text
            imagen = elem.find('img', class_='imagen').get('data-imagen')
            
            # Aniadimos los parámetros obtenidos del webScrapping en una lista de
            # elementos de tipo MisRecetas.
            # Es necesario escribir "MisRecetas.MisRecetas" para llamar a la clase
            # MisRecetas que está dentro del módulo con el mismo nombre
            receta = MisRecetas.MisRecetas(titulo, imagen)
            self.listaReceta.append(receta)
            
    
    # Metodo que realice el WebScrapping de "No Solo Dulces"
    def buscar_nosolodulces(self):
         url = 'https://nosolodulces.es/?s='
         url_completa = url + self.ingrediente
         html_text = requests.get(url_completa).text
         soup = BeautifulSoup(html_text, 'lxml')
         elementos = soup.find_all('article', class_ = 'col-md-4 receta-categoria')
         
         for elem in elementos:
            # Obtenemos los parámetros deseados
            # Como el tag <a href...> donde se aloja el titulo no tiene ningún atributo 'class'
            # no se puede hacer la búsqueda por la clase, de forma que buscamos todos los <a href>
            # dentro del artículo y solo guardamos el atributo 'title'
            titulo = elem.find('a', href=True).get('title')
            imagen = elem.find('img', class_='img-destacada').get('src')

            # Aniadimos los parámetros obtenidos del webScrapping en una lista de
            # elementos de tipo MisRecetas.
            # Es necesario escribir "MisRecetas.MisRecetas" para llamar a la clase
            # MisRecetas que está dentro del módulo con el mismo nombre
            receta = MisRecetas.MisRecetas(titulo, imagen)
            self.listaReceta.append(receta)
         
             
    # Método que muestra los resultados (para comprobar que funciona bien)
    def mostrar_receta(self):
        for lr in self.listaReceta:
            print(lr.get_nombre())
            print(lr.get_urlImagen())
            print("")
            
    
            
            
    
