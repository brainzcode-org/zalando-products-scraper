# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
import sqlite3


class ZalandPipeline:
    def process_item(self, item, spider):
        return item


class StockAvailabilityPipeline:
    def process_item(self, item, spider):
        adaptor = ItemAdapter(item)

        if adaptor.get("availability") == "http://schema.org/InStock":
            adaptor["availability"] = "InStock"

        if adaptor.get("availability") == "http://schema.org/OutOfStock":
            adaptor["availability"] = "OutOfStock"

        return item


class SQLitePipeline:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("products.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
                name,
                colour,
                images,
                manufacturer,
                sku,
                url,
                desc,
                variant_sku,
                availabilty,
                priceUSD
            )
            """
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """SELECT * FROM products WHERE variant_sku = ?""", (item["variant_sku"],)
        )

        result = self.cur.fetchone()

        if result:
            spider.logger.warn(f"item already in DB, {item['variant_sku']}")
        else:
            self.cur.execute(
                """INSERT INTO products(name, colour, images, manufacturer, sku, url, desc, variant_sku, availabilty, priceUSD) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (
                    item["name"],
                    item["colour"],
                    item["images"],
                    item["manufacturer"],
                    item["sku"],
                    item["url"],
                    item["desc"],
                    item["variant_sku"],
                    item["availability"],
                    item["priceUSD"],
                ),
            )
            self.conn.commit()

            return item
