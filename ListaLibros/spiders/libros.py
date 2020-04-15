
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
        for libro in libros:
            nombre = libro.xpath(".//text()").get()
            enlace = libro.xpath(".//@href").get()
            url= enlace.replace("http://", "https://")
            yield scrapy.Request(url=url, callback=self.parse_libro, meta={'nombre_libro': nombre})
     
    def parse_libro(self, response):
        global libros
        print('Extrayendo…' + response.url)
        nombre = response.request.meta['nombre_libro']
        
        linea = {
            'nombre_libro': nombre,
            'genero': response.xpath("//span[text()='Género']/following-sibling::a/text()").get(),
            'editorial': response.xpath("//span[text()='Editorial']/following-sibling::a/text()").get(),
            'año': response.xpath("//span[text()='Año de edición']/following-sibling::text()").get(),
            'isbn': response.xpath("//span[text()='ISBN']/following-sibling::text()").get(),
            'idioma': response.xpath("normalize-space(//span[text()='Idioma']/following-sibling::text())").get()
        }
        libros.append(linea)

class google_books():
    googleapikey="AIzaSyBOgE2gyUgiNoznN40_eQ0rzg0Hw0TciPI"

    def search(self, value):
        global libros
        parms = {"q":value, 'key':self.googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        print (r.url)
        resultado = r.json()

        numero_paginas='NULL'
        average_rating='NULL'

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

    process.crawl(LibrosSpider)
    process.start()
    print(libros)
    book = google_books()
    
    for libro in libros:
        busqueda = "isbn" + libro['isbn']
        print(busqueda)
        info_adicional = book.search(busqueda)
        print(info_adicional)
        libro.update(info_adicional)
    
    print(libros)

    csvfile = "dataset_libros.csv"
    keys = libros[0].keys()
    with open(csvfile, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(libros)
