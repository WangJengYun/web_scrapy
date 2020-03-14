# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd
from scrapy_splash import SplashRequest

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://www.cwb.gov.tw/V7/observe/real/NewObs.htm']
    req_url = "http://localhost:8050/render.html"
    def start_requests(self):
        for url in self.start_urls:
            New_url = "http://localhost:8050/render.html?url={}&wait={}".format(url,5)
            yield scrapy.Request(New_url,callback =self.area_parse,dont_filter=True)

    def area_parse(self, response):
        areas = response.xpath('//ul[@role="tablist"]//a/text()').extract()
        href = response.xpath('//ul[@role="tablist"]//a/@href').extract()
        area_urls = ['https://www.cwb.gov.tw'+shorthref for shorthref in href]
        for area,area_url in zip(areas,area_urls):
            New_url = "http://localhost:8050/render.html?url={}&wait={}".format(area_url, 5)
            yield scrapy.Request(New_url, callback=self.data_parse,meta={'area':area},dont_filter=True)

    def data_parse(self, response):
        html_tables = response.xpath("//table[@class='tablesorter']").extract()
        locations = response.xpath('//p[@class="SubTabA"]/span/a/text()').extract()
        for html_table,location in zip(html_tables,locations) :
            data = pd.read_html(html_table)[0]
            dist_data = data.to_dict('records')
            for row in dist_data:
                row['地區'] = response.meta['area']
                row['縣市'] = location
                yield row