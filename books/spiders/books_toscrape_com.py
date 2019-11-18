from datetime import datetime
import re

import scrapy

from books.items import BooksItem

class BooksToscrapeComSpider(scrapy.Spider):
    name = 'books.toscrape.com'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for page in response.css('.product_pod h3 a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(page), self.parse_item)

        url = response.css('.pager .next a::attr(href)').get()

        #if url is not None:
        if url:
            yield response.follow(url)

    def parse_item(self, response):
        ratings = {'One' : 1, 'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5}
        book = response.css('.product_page .product_main')

        stock = book.css('.instock').get()
        breabcumb = response.css('.breadcrumb li')

        name = book.css('h1::text').get()
        price = float(re.search(r'\d+\.\d+', book.css('.price_color::text').get())[0])
        available = book.css('.instock .icon-ok') is not None
        quantity = int(re.search(r'\d+', stock)[0])
        rating = ratings[book.css('.star-rating::attr(class)').get().replace('star-rating ', '')]
        category = breabcumb[2].css('a::text').get()
        upc = response.css('.product_page table tr')[0].css('td::text').get()
        
        return BooksItem(name=name, price=price, quantity=quantity, available=available, 
                                rating=rating, category=category,url=response.url, 
                                scrape_date=datetime.today().isoformat(), upc=upc)
