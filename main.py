from bs4 import BeautifulSoup
import requests

'''
Example of a request to recetasgratis.net with pollo as a parameter
recetas will contain all recipes result listed in the firs page
'''

html_text = requests.get('https://www.recetasgratis.net/busqueda?q=pollo').text
soup = BeautifulSoup(html_text, 'lxml')
recetas = soup.find_all('div', class_ = 'resultado link')
#receta = soup.find('div', class_='resultado link')

for receta in recetas:
    titulo = receta.find('a', class_='titulo').text
    comensales = receta.find('span', class_='property comensales').text
    tiempo = receta.find('span', class_='property duracion').text
    categoria = receta.find('div', class_='etiqueta').text
    imagen = receta.find('img', class_='imagen').get('data-imagen')
    print(titulo)
    print(comensales)
    print(tiempo)
    print(categoria)
    print(imagen)

