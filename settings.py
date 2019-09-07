# -*- coding: utf-8 -*-


BOT_NAME = 'football'

SPIDER_MODULES = ['football.spiders']
NEWSPIDER_MODULE = 'football.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'football.pipelines.FootballPipeline': 300,
}
