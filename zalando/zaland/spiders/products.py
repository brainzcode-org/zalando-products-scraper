import scrapy

from ..items import ZalandItem
import json


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["zalando.co.uk"]

    def start_requests(self):
        start_urls = []
        for page in range(1, 155):
            start_urls.append(
                f"https://www.zalando.co.uk/mens-clothing-t-shirts/?p={page}"
            )

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.css(
            "article.z5x6ht._0xLoFW.JT3_zV.mo6ZnF._78xIQ- > a::attr(href)"
        ).getall()

        for link in links:
            if "https" in link:
                yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        item = ZalandItem()

        products_data = json.loads(
            response.css("script[type='application/ld+json']::text").get()
        )

        for p in products_data["offers"]:
            item["name"] = products_data["name"]
            item["colour"] = products_data["color"]
            item["images"] = json.dumps(products_data["image"])
            item["manufacturer"] = products_data["manufacturer"]
            item["sku"] = products_data["sku"]
            item["url"] = products_data["url"]
            item["desc"] = products_data["description"]
            item["variant_sku"] = p["sku"]
            item["availability"] = p["availability"]
            item["priceUSD"] = p["price"]
            yield item
