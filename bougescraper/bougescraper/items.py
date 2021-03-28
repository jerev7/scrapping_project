# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re

def make_url_absolute(url):
	return "http://www.treillieres.fr" + url

def render_address(address):
	return address.replace(" Adresse :  ", "")

def find_sports(paragraph):
	sport_word_list = ["tennis", "basketball", "football", "boxe", "tennis de table", "rugby", "course", "lancers"]
	new_sport_list = [""]

	paragraph2 = paragraph.replace(",", " , ").replace(".", " . ")
	for word in sport_word_list:
		les_match = re.findall(r"(?:^|\W)({})(?:$|\W)".format(word), paragraph2)
		new_sport_list.append(les_match)
	sports = " ".join(new_sport_list)
	return sports


class BougescraperItem(scrapy.Item):

	name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
	address = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
	sports = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
