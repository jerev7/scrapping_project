import scrapy
from bougescraper.items import BougescraperItem
from scrapy.loader import ItemLoader
import re


#https://www.commune-mairie.fr/equipements/treillieres-44209/
sport_word_list = ["TENNIS", "BASCKETBALL", "FOOTBALL", "BOXE", "TENNIS DE TABLE", "RUGBY", "COURSES", "LANCERS"]


class BougeSpider(scrapy.Spider):
    name = "bouge"

    start_urls = ["http://www.treillieres.fr/mes-loisirs/equipements-sportifs-et-salles-municipales/equipements-sportifs-2459.html"]

    def parse(self, response):
        
        for link in response.css("div.list-type-3__wrapper a.link-bloc::attr(href)").getall():

            yield scrapy.Request(response.urljoin(link), callback=self.parse_detail)

    def parse_detail(self, response):
        
        for equips in response.css("article.section-main"):
            sports_list = []
            l = ItemLoader(item=BougescraperItem(), selector=equips)
            
            l.add_css('address', 'p.list-infos__item.list-infos__address a')
            l.add_css('name', 'h1.heading__title::text')

            l.add_css("sports", "p.list-infos__item.list-infos__infos")
            
            # paragraph2 = paragraph.replace(',', ' , ').replace(".", " . ")
            # paragraph2_in_list = paragraph2.split(' ')
            # sport_list = [i for i in paragraph2_in_list if i in stop_words]



            yield l.load_item()





