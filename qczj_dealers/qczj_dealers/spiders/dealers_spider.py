# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qczj_dealers.items import QczjDealersItem
from scrapy.http import Request, HtmlResponse
from qczj_dealers.items import QczjPriceItem


class DealersSpider(CrawlSpider):
    name = 'dealers_spider'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['https://dealer.autohome.com.cn/china/0/0/0/0/1/1/0/0.html']

    rules = (
        # 列表页"https://dealer.autohome.com.cn/china/0/36/0/0/1/0/0/0.html#pvareaid=2113614"
        Rule(LinkExtractor(allow=r'.*/china/0/\d+/0/0/\d+/1/0/0.html.*'), follow=True),
        # 详情页"https://dealer.autohome.com.cn/2062577/#pvareaid=2113601"
        Rule(LinkExtractor(allow=r'.*/\d+/#pvareaid=2113601'), callback='parse_detail', follow=False),
        Rule(LinkExtractor(allow=r'.*/\d+/price.html.*'), callback='parse_price', follow=False),
    )


    def parse_detail(self, response):
        # 爬取品牌
        brand_list = []
        brand_dls = response.xpath('//dl[@class="tree-dl"]')
        for brand_dl in brand_dls:
            brand = brand_dl.xpath('.//dt//text()').get()
            brand_list.append(brand)
        dealer_brands = ','.join(brand_list)
        # 爬取经销商信息
        dealer_info = response.xpath('//div[@class="allagency-cont"]')
        dealer_class = dealer_info.xpath('./p/text()').get()
        dealer_phone = dealer_info.xpath('.//span[@class="dealer-api-phone"]/text()').get()
        dealer_addr = dealer_info.xpath('./p[@class="address"]/@title').get()
        # 爬取经销商名称、城市
        dealer_info1 = response.xpath('//div[@class="breadnav"]')
        dealer_city = dealer_info1.xpath('.//a/text()').get()
        dealer_name = dealer_info1.xpath('.//span/text()').getall()[1]
        item = QczjDealersItem(dealer_name=dealer_name, dealer_city=dealer_city, dealer_class=dealer_class,
                               dealer_phone=dealer_phone, dealer_addr= dealer_addr,dealer_brands=dealer_brands)
        yield item

    def parse_price(self,response):
        price_item = {}
        dealer_info = response.xpath('//div[@class="breadnav"]')
        dealer_name = dealer_info.xpath('.//a/text()').getall()[1]
        price_item['dealer_name'] = dealer_name
        price_dls = response.xpath('//div[@class="carprice-cont"]/dl')
        for price_dl in price_dls:
            model_name_tag = price_dl.xpath('./dt//div')[1]
            model_name = model_name_tag.xpath('.//a/text()').get()
            price_item['model_name'] = model_name
            trs = price_dl.xpath('./dd//tr')
            for tr in trs:
                if tr.xpath('./th'):
                    continue
                else:
                    type_name = tr.xpath('./td[1]//text()').getall()[1]
                    price_item['type_name'] = type_name
                    guide_price = tr.xpath('./td[2]//text()').getall()[1]
                    price_item['guide_price'] = guide_price
                    promotion_price_list = tr.xpath('./td[3]//a[@target="_blank"]/text()').getall()
                    if promotion_price_list:
                        promotion_price = promotion_price_list[0]
                    else:
                        promotion_price = guide_price
                    price_item['promotion_price'] = promotion_price
                item = QczjPriceItem(dealer_name = price_item['dealer_name'], model_name = price_item['model_name'], type_name =price_item['type_name'],
                                     guide_price = price_item['guide_price'], promotion_price = price_item['promotion_price'] )
                yield item
