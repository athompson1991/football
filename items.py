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

class ReceivingItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    targets = scrapy.Field()
    rec = scrapy.Field()
    catch_pct = scrapy.Field()
    rec_yds = scrapy.Field()
    rec_yds_per_rec = scrapy.Field()
    rec_td = scrapy.Field()
    rec_long = scrapy.Field()
    rec_yds_per_tgt = scrapy.Field()
    rec_per_g = scrapy.Field()
    rec_yds_per_g = scrapy.Field()
    fumbles = scrapy.Field()

class DefenseItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    def_int = scrapy.Field()
    def_int_yds = scrapy.Field()
    def_int_td = scrapy.Field()
    def_int_long = scrapy.Field()
    pass_defended = scrapy.Field()
    fumbles_forced = scrapy.Field()
    fumbles = scrapy.Field()
    fumbles_rec = scrapy.Field()
    fumbles_rec_yds = scrapy.Field()
    fumbles_rec_td = scrapy.Field()
    sacks = scrapy.Field()
    tackles_combined = scrapy.Field()
    tackles_solo = scrapy.Field()
    tackles_assists = scrapy.Field()
    tackles_loss = scrapy.Field()
    qb_hits = scrapy.Field()
    safety_md = scrapy.Field()


class KickingItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    age = scrapy.Field()
    pos = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    fga1 = scrapy.Field()
    fgm1 = scrapy.Field()
    fga2 = scrapy.Field()
    fgm2 = scrapy.Field()
    fga3 = scrapy.Field()
    fgm3 = scrapy.Field()
    fga4 = scrapy.Field()
    fgm4 = scrapy.Field()
    fga5 = scrapy.Field()
    fgm5 = scrapy.Field()
    fga = scrapy.Field()
    fgm = scrapy.Field()
    fg_perc = scrapy.Field()
    xpa = scrapy.Field()
    xpm = scrapy.Field()
    xp_perc = scrapy.Field()
    punt = scrapy.Field()
    punt_yds = scrapy.Field()
    punt_long = scrapy.Field()
    punt_blocked = scrapy.Field()
    punt_yds_per_punt = scrapy.Field()

class FantasyItem(scrapy.Item):
    season = scrapy.Field()
    player = scrapy.Field()
    player_code = scrapy.Field()
    team = scrapy.Field()
    fantasy_pos = scrapy.Field()
    age = scrapy.Field()
    g = scrapy.Field()
    gs = scrapy.Field()
    pass_cmp = scrapy.Field()
    pass_att = scrapy.Field()
    pass_yds = scrapy.Field()
    pass_td = scrapy.Field()
    pass_int = scrapy.Field()
    rush_att = scrapy.Field()
    rush_yds = scrapy.Field()
    rush_yds_per_att = scrapy.Field()
    rush_td = scrapy.Field()
    targets = scrapy.Field()
    rec = scrapy.Field()
    rec_yds = scrapy.Field()
    rec_yds_per_rec = scrapy.Field()
    rec_td = scrapy.Field()
    fumbles = scrapy.Field()
    fumbles_lost = scrapy.Field()
    all_td = scrapy.Field()
    two_pt_md = scrapy.Field()
    two_pt_pass = scrapy.Field()
    fantasy_points = scrapy.Field()
    fantasy_points_ppr = scrapy.Field()
    draftkings_points = scrapy.Field()
    fanduel_points = scrapy.Field()
    vbd = scrapy.Field()
    fantasy_rank_pos = scrapy.Field()
    fantasy_rank_overall = scrapy.Field()