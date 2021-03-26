# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def make_url_absolute(url):
	return "http://www.treillieres.fr" + url

def render_address(address):
	return address.replace(" Adresse :  ", "")

class BougescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())    
    link = scrapy.Field(input_processor = MapCompose(remove_tags, make_url_absolute), output_processor = TakeFirst())
    address = scrapy.Field(input_processor = MapCompose(remove_tags, render_address), output_processor = TakeFirst())

class BougescraperItem2(scrapy.Item):

	name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
	address = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
	sports = scrapy.Field()
