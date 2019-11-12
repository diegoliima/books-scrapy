import scrapy


class BooksItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    available = scrapy.Field()
    quantity = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    scrape_date = scrapy.Field()
    url = scrapy.Field()
