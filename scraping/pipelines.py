# -*- coding: utf-8 -*-

import csv
from .settings import CSV_OUTPUT
from .fieldnames import fieldnames

class FootballPipeline(object):

    def open_spider(self, spider):
        spider_name = spider.name
        target_dir = CSV_OUTPUT
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
