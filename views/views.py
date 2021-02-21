import quopri

from logging_mod import debug, Logger
from views.template_engine import render
from models import categories_list, courses_list, TrainingSite

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    """
    Использование шаблонизатора
    :param request: запрос
    :return: HTML страничка
    """
    return '200 OK', render('course_list.html', objects_list=courses_list)


def category_list(request):
    """
    Рендеринг странички категории
    :param request: запрос
    :return: страничка
    """
    return '200 OK', render('category_list.html', objects_list=categories_list)


def about_view(request):
    """
    Просто возвращаем текст
    :param request:
    :return:
    """
    return '200 OK', render('about.html')


def decode_value(val):
    """
    Декодирует кодовые точки в текст
    :param val: кодовые точки
    :return: текст
    """
    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    val_decode_str = quopri.decodestring(val_b)
    return val_decode_str.decode('UTF-8')


def contact_view(request):
    """
    Проверка метода запроса
    :param request: запрос
    :return: страница с контактами
    """
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {decode_value(email)} с темой {decode_value(title)}'
              f' и текстом {decode_value(text)}')
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


@debug
def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        # print(data)
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


# @application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)
