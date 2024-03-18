from scrapy import Spider

class FoxtrotSpider(Spider):
    name = "foxtrot"
    start_urls = ["https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_smartfon.html"]

    def parse(self, response) -> None:
        for link in response.css("a.card__title::attr(href)").getall():
            yield response.follow(link, self.parse_page)
        for i in range(2, 10):
            next_page = f"https://www.foxtrot.com.ua/uk/shop/mobilnye_telefony_smartfon.html?page={i}"
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        product_name = response.css("h1.page__title::text").get()
        product_price = response.css("div.product-box__main_price::text").get().strip()
        product_grade = response.css("div.review-total-rating__value::text").get().strip()
        if product_name:
            yield {
                "product_name": product_name.strip(),
                "product_link": response.url,
                "product_price": product_price,
                "product_grade": product_grade,
            }
