from dataclasses import dataclass


@dataclass
class Product:
    name: str
    product_id: int
    price: float
    stock: int

@dataclass
class Category:
    name: str
    category_id: int
    items: list[Product]


class Repo:
    categories= []

    def __init__(self, test_data: dict = None):
        for category in test_data.get('categories', []):
            self.categories.append(Category(**category))

        for product in test_data.get('products', []):
            category_name = product.pop('category_name')
            product = Product(**product)
            for category in self.categories:
                if category.name == category_name:
                    category.items.append(product)
                    break


    async def get_categories(self, session):
        # query = select(Categories.category_name, Categories.category_id)
        # result = await session.execute(query)
        # categories = result.execute().all()
        return self.categories


    async def get_products(self, session, category_id) -> list[Product]:
        # query = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.category_id == category_id)
        # result = await session.execute(query)
        # products = result.execute().all()
        for category in self.categories:
            if category.category_id == category_id:
                return category.items

    async def get_product(self, session, product_id) -> Product:
        # query = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.product_id == product_id)
        # result = await session.execute(query)
        # product = result.execute().all()
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    return product

    async def buy_product(self, session, product_id, amount) -> bool:
        # query = update(Products).where(Products.product_id == product_id).values(
        #   stock=Products.stock - amount
        # )
        # await session.execute(query)
        # await session.commit()
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    product.stock -= amount
                    return True