# -*- coding: utf-8 -*-


BOT_NAME = 'football'

SPIDER_MODULES = ['football.scraping.spiders']
NEWSPIDER_MODULE = 'football.scraping.spiders'

ROBOTSTXT_OBEY = True

CSV_OUTPUT = "/Users/alex/google_drive/python_projects/football/football/script/data/"

ITEM_PIPELINES = {
   'football.scraping.pipelines.FootballPipeline': 300,
}
