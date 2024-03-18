from scrapy import Spider

class AlloSpider(Spider):
    name = "allo"
    start_urls = ["https://allo.ua/ua/products/mobile/klass-kommunikator_smartfon/"]

    def parse(self, response) -> None:
        for link in response.css("a.product-card__title::attr(href)").getall():
            yield response.follow(link, self.parse_page)
        for i in range(2, 10):
            next_page = f"https://allo.ua/ua/products/mobile/klass-kommunikator_smartfon/p-{i}/"
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        product_name = response.css("h1.p-view__header-title::text").get().strip()
        product_price = response.css("span.sum::text").get().strip()
        product_grade = response.css("span.rating-block__stars-count::text").get().strip()
        if product_name:
            yield {
                "product_name": product_name.strip(),
                "product_link": response.url,
                "product_price": product_price,
                "product_grade": product_grade,
            }
