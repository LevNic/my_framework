import quopri

from views.template_engine import render


def main_view(request):
    """
    Использование шаблонизатора
    :param request:
    :return: HTML страничка
    """
    secret = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    """
    Просто возвращаем текст
    :param request:
    :return:
    """
    return '200 OK', render('about.html')


def decode_value(val):
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
