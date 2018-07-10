import json

from scrapy import spiders, Request

from touristspidet_master.items import TouristspidetMasterItem


class TouristSpider(spiders.Spider):
    name = 'tourist'

    start_urls = ['http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page=1&limit=10']
    api = 'http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page={page}&limit=10'

    def parse(self, response):
        msg = json.loads(response.text)
        if msg.get('success'):
            data = msg.get('data')
            pageCount = data.get('pageCount')
            for i in range(pageCount):
                yield Request(url=self.api.format(page=i),
                              callback=self.parse_all)

    def parse_all(self, response):
        msg = json.loads(response.text)
        if msg.get('success'):
            data = msg.get('data')
            rows = data.get('rows')
            urls = ['http://www.tuniu.com/trips/' + str(row.get('id')) for row in rows]
            for url in urls:
                item = TouristspidetMasterItem()
                item['url'] = url
                yield item