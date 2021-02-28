import os

from sqlalchemy import Column, Integer, String, create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from generative_patterns.observer import Subject, Observer
import jsonpickle
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





# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# преподаватель
class Teacher(User):
    pass


class Student(User):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# Фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Категория
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


# Курс
class Course(PrototypeMixin, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class SmsNotifier(Observer):

    def update(self, subject: Course):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject: Course):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    def load(self, data):
        return jsonpickle.loads(data)


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# Фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной класс - интерфейс проекта
class TrainingSite:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
