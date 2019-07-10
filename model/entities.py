from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector
import datetime

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    username = Column(String(12))

class Message(connector.Manager.Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    content = Column(String(500))
    sent_on = Column(default=datetime.datetime.now())
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_to_id = Column(Integer, ForeignKey('users.id'))
    user_from = relationship(User, foreign_keys=[user_from_id])
    user_to = relationship(User, foreign_keys=[user_to_id])

class Learn(connector.Manager.Base):
    __tablename__ = 'learn'
    id = Column(Integer, Sequence('learn_id_seq'), primary_key=True)
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_from_name = Column(String(50), ForeignKey('users.username'))
    Tema  = Column(String(500))
    Curso = Column(String(500))
    Lugar = Column(String(500))
    Hora  = Column(String(500))
    Tiempo= Column(String(500))

class Teach(connector.Manager.Base):
    __tablename__='teach'
    id = Column(Integer, Sequence('teach_id_seq'), primary_key=True)
    user_from_id_t = Column(Integer, ForeignKey('users.id'))
    name_t = Column(String(50), ForeignKey('users.username'))
    HoraEnviado = Column(default=datetime.datetime.now())
    Curso_t = Column(String(50))



