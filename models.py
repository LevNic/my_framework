import os

from sqlalchemy import Column, Integer, String, create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
DATABASE_NAME = 'base.db3'

ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_URL = os.path.join(ROOT, DATABASE_NAME)

categories_list = ['Development', 'Architect', 'Programming']
courses_list = ['Python', 'Django', 'Flask']


class DataBase:
    """
    Класс - база данных
    """

    media_path = os.path.join(ROOT, 'demo-media')

    def __init__(self):
        self.path = DATABASE_URL
        print('PATH IN DB', self.path)

        self.engine = create_engine(f'sqlite:///{self.path}', echo=False, pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        # Создаём объект MetaData
        self.metadata = MetaData()

        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)
        self.session = Session()
        print('DB CREATED')


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Courses(Base):
    __tablename__ = 'Courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    category = Column(String, ForeignKey('Category.id'))
