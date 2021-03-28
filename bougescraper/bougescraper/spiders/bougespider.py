import scrapy
from bougescraper.items import BougescraperItem, BougeGoogleScraperItem
from scrapy.loader import ItemLoader
import requests
import json
from bougescraper.config import KEY # importing google API key



class BougeSpider(scrapy.Spider):
    """
    Spider to get data from Treillières website 
    """
    name = "bouge"

    start_urls = ["http://www.treillieres.fr/mes-loisirs/equipements-sportifs-et-salles-municipales/equipements-sportifs-2459.html"]

    def parse(self, response):
        """
        We parse the first page to get each link to each equipment detail
        """
        
        for link in response.css("div.list-type-3__wrapper a.link-bloc::attr(href)").getall():

            yield scrapy.Request(response.urljoin(link), callback=self.parse_detail)

    def parse_detail(self, response):
        """
        We parse every equipement detail page to get the data we need
        """
        
        for equips in response.css("article.section-main"):
            l = ItemLoader(item=BougescraperItem(), selector=equips)
            l.add_css('address', 'p.list-infos__item.list-infos__address a')
            l.add_css('name', 'h1.heading__title::text')
            l.add_css("sports", "p.list-infos__item.list-infos__infos")

            yield l.load_item()


class BougeSpiderGoogle(scrapy.Spider):
    """
    Spider to get data from Google API with a query ('salle de sport') and a latitude/longitude location
    """
    name = "googlebouge"

    start_urls = [f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=salle+de+sport&location=47.32715,-1.621485&radius=2000&key={KEY}"]
    # custom_settings = {
    #     "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
    # }

    def parse(self, response):
        """
        We parse json item returned by Google API to get the data we need
        """
        json_response = json.loads(response.text)
        listings = json_response["results"]
        for items in listings:
            l = ItemLoader(item=BougeGoogleScraperItem(), selector=items)
            l.add_value('name', items["name"])
            l.add_value('address', items["formatted_address"])
            l.add_value('gps_latitude', items["geometry"]["location"]["lat"])
            l.add_value('gps_longitude', items["geometry"]["location"]["lng"])
            l.add_value('general_type', "{0}, {1}".format(items["types"][0], items["types"][1]))

            yield l.load_item()