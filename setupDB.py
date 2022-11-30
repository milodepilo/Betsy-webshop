from models import (db, Tag, Product, User, ProductTag,  Transactions, UserProduct)
import os
import pdb

def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsy.db")
    if os.path.exists(database_path):
        os.remove(database_path)


def populate_test_DB():
    db.connect()

    db.create_tables(
        
        [
            Tag,
            Product,
            User,
            UserProduct,
            ProductTag,            
            Transactions
        ]
    )

    tags = [
        "painting",
        "oilpaint",
        "nature",
        "portrait",
        "poem",
        "abstract"
        ]
    products = [
        (["the scream", "screaming person on canvas", 15000],[1, 2, 4]),
        (["sunflowers", "yellow sunflowers on canvas", 20000],[1, 2, 3]),
        (["The Raven", "Poem by Edgar Allen Poe", 50000,],[5]),
        ]
    users = [
        (["bob", "somestreet 1, Whatcity", "cc info bob"], [1]),
        (["henk", "anotherstreet 1, Thiscity", "cc info henk"], [2]),
        (["piet", "differentstreet 2, Alsocity", "cc info piet"], [3])
        ]  
  

    for tag_name in tags:
        Tag.create(
            name = tag_name.lower()
            )
   
    for product, product_tags in products:
        Product.create(
            name = product[0].lower(),
            description = product[1],
            price_in_cents = product[2],            
            )

        for tag in product_tags:            
            ProductTag.create(
                product_id = Product.select(Product.id).where(Product.name == product[0].lower()).get(),
                tag_id = tag
            )            

    for user, product_ids in users:
        User.create(
            name = user[0].lower(),
            adress = user[1],
            billing_info = user[2]
            )

        for product_id in product_ids:
            UserProduct.create(
                user_id = User.select(User.id).where(User.name == user[0]).get(),
                product_id = product_id                                
            )
        

    
    
    db.close()