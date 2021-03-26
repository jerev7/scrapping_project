import scrapy
from bougescraper.items import BougescraperItem, BougescraperItem2
from scrapy.loader import ItemLoader
import regex


#https://www.commune-mairie.fr/equipements/treillieres-44209/
sport_word_list = ["tennis", "basketball", "football", "boxe", "tennis de table", "rugby"]

class BougeSpider(scrapy.Spider):
    name = "bouge"

    start_urls = ["http://www.treillieres.fr/mes-loisirs/equipements-sportifs-et-salles-municipales/equipements-sportifs-2459.html"]

    def parse(self, response):
        
        for equips in response.css("article.list__item.list-type-3__item"):
            l = ItemLoader(item=BougescraperItem(), selector=equips)
            
            l.add_css('link', 'a.link-bloc::attr(href)')
            l.add_css('address', 'p.list-infos__item.list-infos__address')
            l.add_css('name', 'a.link-bloc')
            # item['name'] = equips.css('a.link-bloc::text').get()
            # item['link'] = "http://www.treillieres.fr" + equips.css('a.link-bloc').attrib["href"]

            yield l.load_item()

        # for equips in response.css("div.list-type-3__wrapper"):
        #     l = ItemLoader(item=BougescraperItem(), selector=equips)
        #     l.add_css('name', 'a.link-bloc')
        #     l.add_css('link', 'a.link-bloc::attr(href)')
        #     # l.add_css('address', )
        #     # item['name'] = equips.css('a.link-bloc::text').get()
        #     # item['link'] = "http://www.treillieres.fr" + equips.css('a.link-bloc').attrib["href"]

        #     yield l.load_item()

class BougeSpider2(scrapy.Spider):
    name = "bouge2"

    start_urls = ["http://www.treillieres.fr/mes-loisirs/equipements-sportifs-et-salles-municipales/equipements-sportifs-2459.html"]

    def parse(self, response):
        
        for link in response.css("div.list-type-3__wrapper a.link-bloc::attr(href)").getall():

            yield scrapy.Request(response.urljoin(link), callback=self.parse_detail)

    def parse_detail(self, response):

        for equips in response.css("article.section-main"):
            sports_list = []
            l = ItemLoader(item=BougescraperItem2(), selector=equips)
            
            l.add_css('address', 'p.list-infos__item.list-infos__address a')
            l.add_css('name', 'h1.heading__title::text')

            for sport in sport_word_list:
                if equips.css("p.list-infos__item.list-infos__infos::text").re(sport) is not None:
                    sports_list.append(sport)
            sports = ' '.join(sports_list)
            l.add_value('sports', sports)


            yield l.load_item()





