import os

from sqlalchemy import Column, Integer, String, create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from generative_patterns.prototipes import PrototypeMixin

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


# class Category(Base):
#     __tablename__ = 'Category'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#
#
# class Courses(Base):
#     __tablename__ = 'Courses'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     category = Column(String, ForeignKey('Category.id'))


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class SimpleFactory:
    # Фабричный метод
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_):
        return UserFactory.create(type_)

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    #
    # def get_or_create_category(self, name):
    #     for item in self.categories:
    #         if item.name == name:
    #             return item
    #     return self.create_category(name)

    def create_course(self, type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None
