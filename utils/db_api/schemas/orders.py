from sqlalchemy import Column, Integer, sql, String, Sequence, BigInteger

from utils.db_api.database import db


class Order(db.Model):
    __tablename__ = 'orders'
    query: sql.Select
    user_id = Column(BigInteger, Sequence('user_id_seq'))
    user_name = Column(String)
    name = Column(String)
    quantity = Column(Integer)
    amount = Column(Integer)
