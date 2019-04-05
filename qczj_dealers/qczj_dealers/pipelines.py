# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import json
import codecs
from qczj_dealers.items import QczjPriceItem
from qczj_dealers.items import QczjDealersItem


class Pipeline(object):
    def __init__(self):
        self.fp = open('dealer_info.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def open_spider(self, spider):
        print('爬虫开始了...')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        print('爬虫结束了...')


class JsonPipeline(object):
    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('dealer_info.json', 'a', encoding='utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    # 处理结束后关闭 文件 IO 流
    def close_spider(self, spider):
        self.file.close()


class TxtPipeline(object):
    def open_spider(self, spider):
        print('爬虫开始了...')

    def process_item(self, item, spider):
        if isinstance(item, QczjDealersItem):
            with open('dealer_info.txt', 'a', encoding='utf-8') as f:
                f.write(item['dealer_name']+'&'+item['dealer_city']+'&'+item['dealer_class']+'&'+item['dealer_phone']+'&'+item['dealer_addr']+'&'+item['dealer_brands']+
                '\n')
            return item
        elif isinstance(item, QczjPriceItem):
            with open('price_info.txt', 'a', encoding='utf-8') as f:
                f.write(item['dealer_name'] + '&' + item['model_name'] + '&' + item['type_name'] + '&' + item[
        'guide_price'] + '&' + item['promotion_price']  + '\n')
            return item

    def close_spider(self, spider):
        print('爬虫结束了...')

