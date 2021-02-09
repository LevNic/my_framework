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
