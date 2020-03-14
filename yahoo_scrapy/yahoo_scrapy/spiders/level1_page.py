# -*- coding: utf-8 -*-
import scrapy
from yahoo_scrapy .items import YahooScrapyItem

class Level1PageSpider(scrapy.Spider):
    name = 'level1_page'
    allowed_domains = ['web']
    start_urls = ['https://tw.buy.yahoo.com/help/helper.asp?p=sitemap&hpp=sitemap']

    def parse(self, response):
        item = YahooScrapyItem()
        category_cells = response.xpath('//div[@class="module  yui3-g"]//li[@class="zone yui3-g"]')
        for category_cell in category_cells:
            title_name = category_cell.xpath('.//h3/a/text()').extract()
            brand_paths = category_cell.xpath('.//li[@class="site-list"]//a')
            brand_names = []
            level2_page_dict = dict()
            for brand_path in brand_paths :
                brand_name_temp = brand_path.xpath('./text()').extract()[0]
                if brand_name_temp in ['電競主機 / 週邊']:
                    level2_page_dict['url'] = 'https://tw.buy.yahoo.com/' + brand_path.xpath('./@href').extract()[0]
                    yield scrapy.Request(level2_page_dict['url'],
                                         meta={'category_name': brand_name_temp,
                                               'item':item},
                                         callback=self.level2_parse,dont_filter=True)
                else :
                    brand_names.append(brand_name_temp)

            for brand_name in brand_names :
                item['category_name'] = title_name[0]
                item['brand_name'] = brand_name
                yield (item)

    def level2_parse(self,response):
        item = response.meta['item']
        category_cells = response.xpath('//li[@class="sitelist "]')
        for category_cell in category_cells :
            title = category_cell.xpath('./h3/a/text()').extract()[0]
            if title in ['電競品牌週邊']:
                brand_names = category_cell.xpath('.//li/a/text()').extract()
                for brand_name in brand_names:
                    item['category_name'] = response.meta['category_name']
                    item['brand_name'] = brand_name
                    yield (item)



