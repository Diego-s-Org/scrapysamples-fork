# -*- coding: utf-8 -*-

BOT_NAME = 'sample'

SPIDER_MODULES = ['sample.spiders']
NEWSPIDER_MODULE = 'sample.spiders'

LOG_LEVEL = 'INFO'

DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
