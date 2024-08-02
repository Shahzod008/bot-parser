from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = 'sqlite:///telegram_parser.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String, nullable=False, unique=True)


class MinusWord(Base):
    __tablename__ = 'minus_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    minus_word = Column(String, nullable=False, unique=True)


class Spammer(Base):
    __tablename__ = 'spammers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spammer = Column(String, nullable=False, unique=True)


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel = Column(Integer, nullable=False, unique=True)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat = Column(Integer, nullable=False, unique=True)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, nullable=False, unique=True)
    content = Column(String, nullable=False)
    channel_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now())


Base.metadata.create_all(engine)
