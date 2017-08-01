import scrapy

from sample.items import ProductItem


class RipleyCategorySpider(scrapy.Spider):

    name = "ripleycategory"

    start_urls = [
        'http://simple.ripley.com.pe/calzado/calzado-mujer/sandalias'
    ]
    cont = 0

    def parse(self, response):
        for href in response.css('a.catalog-product::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_detail)
        # next_page = response.xpath('//ul[@class="pagination"]//li[not(@class)]/a/@href').extract_first()
        # next_page = str(next_page)
        # tmp = next_page.split("=", 2)
        # if len(tmp) > 2:
        #     tmp[2] = str(self.cont)
        #     next_page = ''.join([tmp[0], '=', tmp[1], '=', tmp[2]])
        #     self.cont += 1
        # if next_page is not None:
        #     if self.cont < 15:
        #         next_page = response.urljoin(next_page)
        #         yield scrapy.Request(next_page, callback=self.parse)
        #     else:
        #         return

    def parse_detail(self, response):
        for item in response.xpath("//section[contains(@class,'product-item')]"):
            product = ProductItem()
            product['title'] = item.xpath('//section[contains(@class,"hidden-xs")]/h1/text()').extract_first()
            product['description'] = item.xpath('//section[contains(@id,"descripcion")]//div[contains(@class,"col-xs-12")]//p').extract_first()
            product['sku'] = item.xpath('//section[contains(@class,"hidden-xs")]/small/span[contains(@class,sku)]/text()').extract_first()
            price = item.xpath("//section[@class='product-info']/ul/li[contains(@class,'product-internet-price')]/span[contains(@class,'product-price')][2]/text()").extract_first()
            product['price'] = price.strip()
            product['image'] = item.xpath("//section[@class='product-images js-product-images-container']/ul[@class='product-image-previews']/li/img/@data-src").extract()

            yield product
