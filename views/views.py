import quopri

from views.template_engine import render
from models import categories_list, courses_list


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
