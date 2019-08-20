# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PassingItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    qb_rec = scrapy.Field()
    pass_cmp = scrapy.Field()
    pass_att = scrapy.Field()
    pass_cmp_perc = scrapy.Field()
    pass_yds = scrapy.Field()
    pass_td = scrapy.Field()
    pass_td_perc = scrapy.Field()
    pass_int = scrapy.Field()
    pass_int_perc = scrapy.Field()
    pass_long = scrapy.Field()
    pass_yds_per_att = scrapy.Field()
    pass_adj_yds_per_att = scrapy.Field()
    pass_yds_per_cmp = scrapy.Field()
    pass_yds_per_g = scrapy.Field()
    pass_rating = scrapy.Field()
    qbr = scrapy.Field()
    pass_sacked = scrapy.Field()
    pass_sacked_yds = scrapy.Field()
    pass_net_yds_per_att = scrapy.Field()
    pass_adj_net_yds_per_att = scrapy.Field()
    pass_sacked_perc = scrapy.Field()
    comebacks = scrapy.Field()
    gwd = scrapy.Field()

class RushingItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    rush_att = scrapy.Field()
    rush_yds = scrapy.Field()
    rush_td = scrapy.Field()
    rush_long = scrapy.Field()
    rush_yds_per_att = scrapy.Field()
    rush_yds_per_g = scrapy.Field()
    fumbles = scrapy.Field()

