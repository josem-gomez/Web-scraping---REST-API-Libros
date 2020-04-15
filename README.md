# Práctica 1: Web scraping

## Descripción
Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante el lenguaje de programación Python para extraer así datos de la web QueLibroLeo para obtener información de un listado de libros recomendados y sus características, para luego usar la REST API de Google Books, cruzar los datos y añadir información adicional para el dataset final.

Para el web scraping, ya que en anteriores ocasiones había usado la librería BeautifulSoap, he utilizado la librería Scrapy en conjunción con xpaths. Se obtiene un listado de libros recomendados para su lectura con los atributos Nombre, Género, Editorial, Año, ISBN e Idioma. A continuación se hace uso de la REST API de Google Books. La autenticación se realiza con un API key y se realizan busquedas basadas en los ISBNs de los libros ya capturados en la web QueLibroLeo. Desde Google Books obtenemos el número de páginas del libro y la valoración media de los usuarios (ambas cuando estan disponibles) y se añade al dataset creado desde el scraping.

## Miembros del equipo
La actividad ha sido realizada de manera individual por Jose Manuel Gómez López.

## Ficheros del código fuente

* **ListaLibros/spiders/libros.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **ListaLibros**: Directorio con ficheros de configuración de Scrapy
* **ListaLibros/spiders/ejemplo_output.txt**: Ejemplo de salida del scraper
## Recursos

1. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
2. Masip, D. El lenguaje Python. Editorial UOC.
2. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
4. Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
