# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

fieldnames = {
    'passing': ['season', 'player', 'player_code', 'team', 'age', 'pos', 'g', 'gs', 'qb_rec', 'pass_cmp', 'pass_att', 'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_td_perc', 'pass_int', 'pass_int_perc', 'pass_long', 'pass_yds_per_att', 'pass_adj_yds_per_att', 'pass_yds_per_cmp', 'pass_yds_per_g', 'pass_rating', 'qbr', 'pass_sacked', 'pass_sacked_yds', 'pass_net_yds_per_att', 'pass_adj_net_yds_per_att', 'pass_sacked_perc', 'comebacks', 'gwd'],
    'rushing': ['season', 'player', 'player_code', 'team', 'age', 'pos', 'g', 'gs', 'rush_att', 'rush_yds', 'rush_td', 'rush_long', 'rush_yds_per_att', 'rush_yds_per_g', 'fumbles']
}

class FootballPipeline(object):

    def open_spider(self, spider):
        spider_name = spider.name
        target_dir = "data/"
        filename = target_dir + spider_name + ".csv"
        self.file = open(filename, 'w')
        self.writer = csv.DictWriter(
           self.file,
           fieldnames=fieldnames[spider_name],
           lineterminator='\n'
        )
        self.writer.writeheader()

    def process_item(self, item, spider):
            self.writer.writerow(dict(item))

    def close_spider(self, spider):
        self.file.close()
