# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re
from bougescraper.config import sport_word_list

def update_address(address):
    return address.replace(",", "")

def find_sports(paragraph):
    """
    We use a regular expression to find sports from the list in the paragraph and we return only the sports found to the scrapy item.
    """
    sports_found = []
    paragraph2 = paragraph.replace(",", " , ").replace(".", " . ")
    for word in sport_word_list:
        sport_match = re.search("(?:^|\W)({0})(?:$|\W)".format(word), paragraph2, re.IGNORECASE)
        if sport_match is not None:
            sports_found.append(sport_match[0])
        else:
            pass
    sports = " ".join(sports_found)
    return sports


class BougescraperItem(scrapy.Item):
    """
    item class for Treillières website spider
    """

    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    address = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    sports = scrapy.Field(input_processor = MapCompose(remove_tags, find_sports), output_processor = TakeFirst())


class BougeGoogleScraperItem(scrapy.Item):
    """
    item class for Google API spider
    """
    name = scrapy.Field()
    address = scrapy.Field(input_processor=MapCompose(update_address))
    gps_longitude = scrapy.Field()
    gps_latitude = scrapy.Field()
    general_type = scrapy.Field()
