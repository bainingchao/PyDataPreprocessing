# -*- coding: utf-8 -*-
__author__ = 'BaiNingchao'

import sys,os
from scrapy.cmdline import execute


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])  # scrapy crawl jobbole
