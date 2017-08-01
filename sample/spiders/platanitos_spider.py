import scrapy
import re

from urlparse import urlparse

from sample.items import ProductItem


class PlatanitosCategorySpider(scrapy.Spider):

    name = "platanitos"

    start_urls = [
        'https://platanitos.com/catalogo'
    ]

    cont = 0

    def parse(self, response):
        pparse = urlparse(response.url)
        if pparse.path:
            for href in response.css('a.items::attr(href)').extract():
                yield scrapy.Request(response.urljoin(href), callback=self.parse_detail)
            next_page = response.xpath('//ul[@class="pagination"]//li[not(@class)]/a/@href').extract_first()
            next_page = str(next_page)
            tmp = next_page.split("=", 2)
            if len(tmp) > 2:
                tmp[2] = str(self.cont)
                next_page = ''.join([tmp[0], '=', tmp[1], '=', tmp[2]])
                self.cont += 1
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        else:
            category_menu = response.xpath('//ul[@class="nav wsmenu-list"]').extract()
            categories_list = re.findall('"/catalogo/[a-zA-Z-]+/[a-zA-Z-]+"', category_menu[0])
            categories_set = set(categories_list)
            for url in categories_set:
                yield scrapy.Request(response.urljoin(url.strip('"')), callback=self.parse)

    def parse_detail(self, response):
        for item in response.xpath("//article[@id='producto-box1']"):
            product = ProductItem()
            product['title'] = item.xpath('//div[@id="producto-box1-box1"]/span[@class="item-descrip"]/text()').extract_first()
            product['description'] = item.xpath('//div[@id="producto-box1-box1"]/span[@class="item-descrip"]/text()').extract_first()
            product['sku'] = item.xpath('//div[@class="sku-style"]/text()').re_first(r"SKU:\s*(.*)")
            product['price'] = item.xpath('//div[@id="producto-box1-box3-box4"]/text()').re_first(r"S/\s*(.*)")
            product['image'] = item.xpath('//div[@id="producto-box1-box4-box1"]/img/@src').extract_first()

            yield product
