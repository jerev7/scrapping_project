# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re

def update_address(address):
    return address.replace(",", "")

def find_sports(paragraph):
    """
    We use a regular expression to find sports from the list in the paragraph and we return only the sports found to the scrapy item.
    """
    sport_word_list = ["Accrobranche", "Acrosport", "Aerobic", "Aéromodélisme", "Aérostation", "Agility", "Aikido", "Airsoft", "Alpinisme", "Apnée", "Aquabike", "Aquagym", "Arts du cirque", "Athlétisme", "Aviation", "Aviron", "Babyfoot", "Badminton", "Ball-Trap", "Basejump", "Baseball", "Basketball","Beachsoccer", "Beachtennis", "Beachvolley", "Béhourd", "Biathlon", "Billard", "BMX", "Bobsleigh", "Boccia", "Bodyboard", "Bodybuilding", "Boomerang", "Bouzkachi", "Bowling", "Boxe", "Boxe anglaise", "Boxe chinoise", "Boxe française", "Boxe thaïlandaise", "Canoë", "Canoë-kayak", "Canyoning", "Canyonisme", "Capoeira", "Catch", "Char à voile", "Claquettes", "Corde à sauter", "Course", "Course à pied", "Course aérienne", "Course camarguaise", "Course d'obstacles", "Course d'orientation", "Course de cote", "Cricket", "Croquet", "Cross training", "Cross-country", "Crosse", "Crossfit", "Curling", "Cyclisme", "Cyclisme sur piste", "Cyclisme sur route", "Cyclo cross", "Cyclotourisme", "Danse", "Danse africaine", "Danse classique", "Danse contemporaine", "Danse country", "Danse indienne", "Danse orientale", "Danse rock", "Danse sportive", "Danse sur glace", "Deltaplane", "Echecs", "Enduro", "Equitation", "Escalade", "Escrime", "Fitness", "Flamenco", "Fléchettes", "Floorball", "Football", "Football américain", "Football australien", "Footgolf", "Footing", "Full contact", "Funboard", "Futsal", "Giraviation", "Golf", "Gymnastique", "Gymnastique artistique", "Gymnastique rythmique", "Haltérophilie", "Handball", "Handisport", "Haïkido", "Hip hop", "Hockey", "Hockey subaquatique", "Hockey sur gazon", "Hockey sur glace", "Horse ball", "Hurling", "Iaïdo", "Jetski", "Jorkyball", "Joutes", "Ju-Jitsu", "Judo", "Karaté", "Karting", "Kempo", "Kendo", "Kenjutsu", "Kick boxing", "Kin ball", "Kitesurf", "Krav-maga", "Kung fu", "Kyokushinkai", "Kyudo", "Lancer du javelot", "Lancer du marteau", "Lancer du poids", "Luge", "Lutte", "Marche", "Marche aquatique", "Marche athlétique", "Marche nordique", "Marche sportive", "Monocycle", "Moto", "Moto cross", "Moto-ball", "Motoneige", "Mountainboard", "Musculation", "Natation", "Natation synchronisée", "Ninjitsu", "Nunchaku", "Omnikin", "Padel", "Paintball", "Pancrace", "Parachutisme", "Paramoteur", "Parapente", "Parkour", "Patinage", "Patinage artistique", "Patinage de vitesse", "Pêche", "Pelote basque", "Pentathlon", "Pétanque", "Ping pong", "Planche à voile", "Plongée", "Plongeon", "Pole dance", "Polo", "Qi gong", "Quad", "Quilles", "Rafting", "Ragga", "Rallycross", "Rallye", "Randonnée", "Rink hockey", "Roller", "Rugby", "Rugby subaquatique", "Salsa", "Samba", "Sambo", "Saut à la perche", "Saut en longueur", "Self défense", "Skateboard", "Ski", "Ski acrobatique", "Ski alpin", "Ski de fond", "Ski nautique", "Skicross", "Snowboard", "Snowkite", "Softball", "Speed riding", "Spéléologie", "Spinning", "Squash", "Sumo", "Surf", "Taekwondo", "Taï chi", "Tambourin", "Tango", "Tchoukball", "Tennis", "Tennis de table", "Teqball", "Tir", "Tir à l'arc", "Tractor pulling", "Trail", "Traîneaux", "Trampoline", "Triathlon", "Tricking", "Trottinette", "Vélo", "Voile", "Volleyball", "Voltige", "Viet Vo Dao", "VTT", "Wakeboard", "Waterpolo", "Wing chun", "Wingsuit", "Yoga", "Zumba"]
    
    new_sport_list = []
    paragraph2 = paragraph.replace(",", " , ").replace(".", " . ")
    for word in sport_word_list:
        les_match = re.search("(?:^|\W)({0})(?:$|\W)".format(word), paragraph2, re.IGNORECASE)
        if les_match is not None:
            new_sport_list.append(les_match[0])
        else:
            pass
    sports = " ".join(new_sport_list)
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
