# Práctica 1: Web scraping

## Descripción
Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante el lenguaje de programación Python para extraer así datos de la web QueLibroLeo para obtener información de un listado de libros recomendados y sus características, para luego usar la REST API de Google Books, cruzar los datos y añadir información adicional para el dataset final.

## Miembros del equipo
La actividad ha sido realizada de manera individual por Jose Manuel Gómez López.

## Ficheros del código fuente

* **src/main.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **src/scraper.py**: contiene la implementación de la clase _AccidentsScraper_ cuyos métodos generan el conjunto de datos a partir de la base de datos online [PlaneCrashInfo](http://www.planecrashinfo.com/database.htm).
* **src/reason_classifier.py**: contiene la implementación de la clase que se encarga de asignar una causa a un resumen de accidente dado. Para ello, utiliza la librería *TextBlob*.

## Recursos

1. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
2. Masip, D. El lenguaje Python. Editorial UOC.
2. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
4. Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
