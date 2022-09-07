from sqlalchemy import sql, Column, String

from utils.db_api.database import db


class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select
    # id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    type = Column(String(25))
    name = Column(String(100), primary_key=True)
    photo = Column(String(250))
    description = Column(String(250))
    price = Column(String(25))
