from scrapy import Spider


class RozetkaSpider(Spider):
    name = "rozetka"
    start_urls = ["https://rozetka.com.ua/mobile-phones/c80003/"]

    def parse(self, response) -> None:
        for link in response.css("a.goods-tile__heading::attr(href)").getall():
            yield response.follow(link, self.parse_page)
        for i in range(2, 10):
            next_page = f"https://rozetka.com.ua/mobile-phones/c80003/page={i}/"
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        product_url = response.url
        product_name = response.css("h1.product__title-collapsed::text").get()
        product_price = response.css("p.product-price__big::text").get()
        if product_name:
            yield {
                "product_name": product_name,
                "product_link": product_url,
                "product_price": product_price,
            }
