
import scrapy
import logging
from scrapy.crawler import CrawlerProcess
import requests
import csv

libros = []  

# Definimos clases para hacer scraping
class LibrosSpider(scrapy.Spider):
    name = 'libros'
    allowed_domains = ['quelibroleo.hola.com', 'www.quelibroleo.com']
    start_urls = [
        'https://quelibroleo.hola.com/noticias/libros/los-100-mejores-libros-de-la-literatura-universal-en-espanol']
     
    def parse(self, response):
        
        # Usamos xpaths para encontrar las estructuras html que necesitamos
        libros = response.xpath(
            "//div[@class = 'entry-content']/p[position() >= 4 and not(position() > 104)]/a[1]")
        
        # Recorremos el resultado con un bucle y extraemos los nombres de lso libros y los siguientes enlaces para scrapear
        for libro in libros:
            nombre = libro.xpath(".//text()").get()
            enlace = libro.xpath(".//@href").get()
            url= enlace.replace("http://", "https://")
            yield scrapy.Request(url=url, callback=self.parse_libro, meta={'nombre_libro': nombre})

    #Función para obtner información adicional de cada libro usando su nueva url 
    def parse_libro(self, response):
        global libros
        print('Extrayendo…' + response.url)
        nombre = response.request.meta['nombre_libro']
        
        # Volvemos a usar xpaths para obtener los campos que necesitamos
        linea = {
            'nombre_libro': nombre,
            'genero': response.xpath("//span[text()='Género']/following-sibling::a/text()").get(),
            'editorial': response.xpath("//span[text()='Editorial']/following-sibling::a/text()").get(),
            'año': response.xpath("//span[text()='Año de edición']/following-sibling::text()").get(),
            'isbn': response.xpath("//span[text()='ISBN']/following-sibling::text()").get(),
            'idioma': response.xpath("normalize-space(//span[text()='Idioma']/following-sibling::text())").get()
        }

        # Vamso añadiendo lineas a la lista. Cada linea será un diccionario con todos los campos de cada libro
        libros.append(linea)

# Definimos la clase google_books para hacer uso de su REST API. La autenticación a la la API se realiza con una llave (API Key)
class google_books():
    googleapikey="********************************"

    def search(self, value):
        global libros
        # Definimos lo parametros de busqueda y la llave para la autenticación
        parms = {"q":value, 'key':self.googleapikey}
        # Hacemos uso de la librería requests para la llamada REST
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        print (r.url)
        #Convertimos en json el resultado de la búsqueda
        resultado = r.json()

        numero_paginas='NULL'
        average_rating='NULL'

        #Recogemso los campos que necesitamos cuando esten disponibles para añadirlso al dataset del web scraping y completar la nfomación
        if ("items" in resultado):
            if ("volumeInfo" in resultado['items'][0]):
                if ("pageCount" in resultado['items'][0]["volumeInfo"]):
                    numero_paginas=resultado['items'][0]["volumeInfo"]["pageCount"]
                    
                if ("averageRating" in resultado['items'][0]["volumeInfo"]):
                    average_rating=resultado['items'][0]["volumeInfo"]["averageRating"]
                    
        res = {'numero_paginas': numero_paginas, 'average_rating': average_rating}

        return  res

        


if __name__ == "__main__":
    

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })

    #Llamamos al spider para empezar el scraping
    process.crawl(LibrosSpider)
    process.start()
    print(libros)

    #Inicializamos la conexión con google books creando un objeto de su clase
    book = google_books()
    
    #Buscamos los libros a través de la APi de Google haciendo uso del ISBN de cada libro
    for libro in libros:
        busqueda = "isbn" + libro['isbn']
        print(busqueda)
        info_adicional = book.search(busqueda)
        print(info_adicional)
        #Añadimos la información adicional a la lista de diccionarios
        libro.update(info_adicional)
    
    print(libros)

    #Por último, creamos el dataset con la información recogida de ambos procesos
    csvfile = "dataset_libros.csv"
    keys = libros[0].keys()
    with open(csvfile, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(libros)
