from utils.db_api.database import db
from utils.db_api.schemas.items import Item


class DBCommands(db.Model):
    # async def show_items(self):
    #     items = await Item.query.gino.all()
    #     return items

    async def show_pizza(type):
        pizza = await Item.query.where(Item.type == "Піца").gino.all()
        return pizza

    async def show_sushi(type):
        sushi = await Item.query.where(Item.type == "Суші").gino.all()
        return sushi

    async def show_burgers(type):
        burgers = await Item.query.where(Item.type == "Бургер").gino.all()
        return burgers
