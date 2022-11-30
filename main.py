__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from setupDB import populate_test_DB, delete_database
from models import (Product, User, UserProduct, ProductTag, Tag, Transactions)
from autocorrect import Speller


delete_database()
populate_test_DB()


def search(term):
    check = Speller(lang="en")

    query = (Product.select(Product)
             .where((Product.name.contains(check(term.lower()))) |
             (Product.description.contains(check(term.lower())))))

    for item in query:
        print(item.name)


def list_user_products(user_id):
    query = (
        Product.select(Product, UserProduct, User)
        .join(UserProduct)
        .join(User)
        .where(User.id == user_id)
    )
    return query


def list_products_per_tag(tag_id):
    query = (
        Product.select(Product, ProductTag, Tag)
        .join(ProductTag)
        .join(Tag)
        .where(Tag.id == tag_id)
    )

    return query


def add_product_to_catalog(user_id, product):
    new_product = Product.create(
        name=product["name"],
        description=product["description"],
        price_in_cents=product["price"],
    )
    UserProduct.create(
        user_id=user_id,
        product_id=Product.select(Product.id)
        .where(Product.name == product["name"]),
        stock=product["stock"]
    )


def remove_product(product_id, user_id):
    remove = UserProduct.delete().where((UserProduct.product_id == product_id)
                                        & (UserProduct.user_id == user_id))
    remove.execute()


def update_stock(product_id, user_id, new_quantity):
    query = (UserProduct
             .update(stock=new_quantity)
             .where((UserProduct.product_id == product_id) &
                    (UserProduct.user_id == user_id)))
    query.execute()


def purchase_product(product_id, buyer_id, seller_id, quantity):
    new_stock = 0
    old_stock = (UserProduct.select()
                 .where((UserProduct.product_id == product_id) &
                        (UserProduct.user_id == seller_id)))

    for stock in old_stock:
        new_stock = stock.stock - quantity
        old_id = stock.id
    if new_stock <= 0:
        remove_product(product_id, buyer_id)

    update_stock(product_id, seller_id, new_stock)
    update_stock(product_id, buyer_id, quantity)

    up, created = UserProduct.get_or_create(
        user_id=buyer_id,
        product_id=product_id,
        defaults={"stock": 1}
    )

    transaction = Transactions.create(
        from_seller=seller_id,
        to_buyer=buyer_id,
        product=product_id,
        billing_info=User.select(User.billing_info).where(User.id == buyer_id),
        ammount=quantity
    )


# drawing_hands = {
#     "name": "drawing hands",
#     "description": "2 hands drawing each other",
#     "price": 600000,
#     "stock": 1
# }


# add_product_to_catalog(1, drawing_hands)
print(search("screaim"))
# update_stock(1,1,2)
# purchase_product(1, 2, 1, 1)
# remove_product(2, 2)
