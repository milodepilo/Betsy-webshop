from peewee import Model,CharField,AutoField,ForeignKeyField,TextField,IntegerField,SqliteDatabase,ManyToManyField
import os

cwd = os.getcwd()
db_path = os.path.join(cwd, "betsy.db")
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):       
    name = CharField()
    description = CharField()
    price_in_cents = IntegerField()
    

    
class Tag(BaseModel):
    name = CharField()
    

class User(BaseModel):    
    name = CharField()
    adress = CharField()
    billing_info = CharField()  
    

class UserProduct(BaseModel):
    user_id = ForeignKeyField(User, backref="products")
    product_id = ForeignKeyField(Product, backref="owner")
    stock = IntegerField(default=1)
    


class ProductTag(BaseModel):
    product_id = ForeignKeyField(Product, backref="tags")
    tag_id = ForeignKeyField(Tag)  


class Transactions(BaseModel):    
    from_seller = ForeignKeyField(User, backref="Sold")
    to_buyer = ForeignKeyField(User, backref='Bought')
    product = ForeignKeyField(Product)
    billing_info = TextField(null=True)
    ammount = IntegerField()
    
    class Meta:
        indexes =(
            (("from_seller", "to_buyer"), False),
        )


