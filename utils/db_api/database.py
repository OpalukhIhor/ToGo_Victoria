from gino import Gino
from gino.schema import GinoSchemaVisitor

from data import config

db = Gino()


async def create_db():
    await db.set_bind(config.POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    #await db.gino.drop_all()
    await db.gino.create_all()
