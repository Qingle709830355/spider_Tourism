from scrapy_redis.spiders import RedisSpider
from scrapy import Selector, spiders

from touristspider.items import TouristspiderItem


class TouristSpider(RedisSpider):
    name = 'tourist'
    redis_key = 'tourist:tuniu'
    # start_urls = ['http://www.tuniu.com/trips/12606533']

    def parse(self, response):
        sel = Selector(response)
        item = TouristspiderItem()
        item['id'] = response.url.split('/')[-1] if response.url[-1] != '/' else response.url.split('/')[-2]
        item['title'] = sel.xpath('/html/body/div[2]/div[1]/div[2]/div/div[1]/h1/text()').extract()[0]
        item['avatar'] = sel.xpath('/html/body/div[2]/div[1]/div[2]/div/a/img/@src').extract()[0]
        item['author'] = sel.xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/div/p[1]/text()').extract()[0]
        item['create_info'] = sel.xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/div/p[2]/text()').extract()[0]
        item['tags'] = sel.xpath('//*[@class="tag-item"]/text()').extract()
        item['content'] = sel.xpath('//*[@class="sdk-trips-container"]').extract()[0]
        yield item
