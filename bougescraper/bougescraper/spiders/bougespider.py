import scrapy
from bougescraper.items import BougescraperItem, BougeGoogleScraperItem
from scrapy.loader import ItemLoader
import re
import requests
import json
from bougescraper.config import KEY


#https://www.commune-mairie.fr/equipements/treillieres-44209/


class BougeSpider(scrapy.Spider):
    name = "bouge"

    start_urls = ["http://www.treillieres.fr/mes-loisirs/equipements-sportifs-et-salles-municipales/equipements-sportifs-2459.html"]

    def parse(self, response):
        
        for link in response.css("div.list-type-3__wrapper a.link-bloc::attr(href)").getall():

            yield scrapy.Request(response.urljoin(link), callback=self.parse_detail)

    def parse_detail(self, response):
        
        for equips in response.css("article.section-main"):
            l = ItemLoader(item=BougescraperItem(), selector=equips)
            l.add_css('address', 'p.list-infos__item.list-infos__address a')
            l.add_css('name', 'h1.heading__title::text')
            l.add_css("details", "p.list-infos__item.list-infos__infos")

            yield l.load_item()


class BougeSpiderGoogle(scrapy.Spider):
    name = "googlebouge"

    start_urls = [f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=salle+de+sport&location=47.32715,-1.621485&radius=2000&key={KEY}"]
    # custom_settings = {
    #     "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
    # }

    def parse(self, response):
        json_response = json.loads(response.text)
        listings = json_response["results"]
        for item in listings:
            l = ItemLoader(item=BougeGoogleScraperItem(), selector=item)
            l.add_value('name', item["name"])
            l.add_value('address', item["formatted_address"])
            l.add_value('gps_latitude', item["geometry"]["location"]["lat"])
            l.add_value('gps_longitude', item["geometry"]["location"]["lng"])
            l.add_value('general_type', "{0}, {1}".format(item["types"][0], item["types"][1]))

            yield l.load_item()