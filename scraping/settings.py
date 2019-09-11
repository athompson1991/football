# -*- coding: utf-8 -*-


BOT_NAME = 'football'

SPIDER_MODULES = ['football.scraping.spiders']
NEWSPIDER_MODULE = 'football.scraping.spiders'

ROBOTSTXT_OBEY = True


ITEM_PIPELINES = {
   'football.scraping.pipelines.FootballPipeline': 300,
}

CSV_OUTPUT = "../script/data/"
YEARS = range(1990, 2019)