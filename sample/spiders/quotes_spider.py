import scrapy
import psycopg2
import logging


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"

#     def start_requests(self):
#         urls = [
#             'http://quotes.toscrape.com/page/1/',
#             'http://quotes.toscrape.com/page/2/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)

# another way to execute the same spider
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'https://platanitos.com/catalogo/hombres/zapatillas'
#     ]

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = 'quotes-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)

# All the results save into json
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.rudll.pw'
    ]
    cont = 2

    conn = None
    id = None
    url = None
    title = None
    body = None

    query_result = []

    def __init__(self, **kwargs):
        try:
            self.conn = psycopg2.connect(host="172.17.0.4",
                                 database="postgres",
                                 user="postgres",
                                 password="postgres")
            self.cursor = self.conn.cursor()
            # super(QuotesSpider, self).__init__(**kwargs)
            self.conn.commit()
            self.query_result = self.cursor.fetchall()

        except Exception, e:
            logging.warning(e.message)

    def parse(self, response):
        id = self.query_result[0]
        url = self.query_result[1]
        body = self.query_result[2]
        title = self.query_result[3]
        css_body = self.query_result[4]
        css_title = self.query_result[5]
        # follow links to author pages
        for href in response.css('a.items::attr(href)').extract():
            # print('response : ',response)
            # print('sith urljoin: ',response.urljoin(href))
            yield scrapy.Request(response.urljoin(href), callback=self.parse_detail)
        # follow pagination links
        # for next_page in response.xpath('//ul[@class="pagination"]//li[not(@class)]/a/@href').extract():
        #     # next_page = response.css('a.items::attr(href)').extract_first()
        #     if next_page is not None:
        #         next_page = response.urljoin(next_page)
        #         yield scrapy.Request(next_page, callback=self.parse)
        next_page = response.xpath('//ul[@class="pagination"]//li[not(@class)]/a/@href').extract_first()
        next_page = str(next_page)
        # print(next_page)
        tmp = next_page.split("=",2)
        # print(self.cont)
        # print('cont = ',tmp)
        tmp[2] = str(self.cont)
        # print('cont = ',tmp)
        print('----------------------------------------------------------'),
        # print(tmp),
        next_page = ''.join([tmp[0],'=',tmp[1],'=',tmp[2]])
        self.cont += 1
        print(next_page)
        if next_page is not None:
            if self.cont < 15:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                return

    def parse_detail(self, response):
        # print('---------------')
        # print(response)
        # print('---------------')
        for quote in response.xpath("//div[@id='producto-box1']"):
            yield {
                # 'sku': quote.xpath('//div[@class="sku-style"]/text()').re_first(r"SKU:\s*(.*)"),
                'title': quote.xpath('//div[@id="producto-box1-box1"]/span[@class="item-descrip"]/text()').extract_first(),
                'description': quote.xpath('//div[@id="producto-box1-box1"]/span[@class="item-descrip"]/text()').extract_first(),
                # 'price': quote.xpath('//div[@id="producto-box1-box3-box4"]/text()').re_first(r"S/\s*(.*)"),
                # 'img': quote.xpath('//div[@id="producto-box1-box4-box1"]/img/@src').extract_first(),
            }

    # example with pagination webs
    # def parse(self, response):
    #     # follow links to author pages
    #     for href in response.css('.author + a::attr(href)').extract():
    #         yield scrapy.Request(response.urljoin(href),
    #                              callback=self.parse_author)

    #     # follow pagination links
    #     next_page = response.css('li.next a::attr(href)').extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)

    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()

    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }