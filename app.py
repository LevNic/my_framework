import quopri


class Application:

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def add_route(self, url):
        """
        паттерн декоратор
        добавляет url и его представление в словарь
        :param url:
        :return: функция добавляющая словарь
        """

        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        """
        Разберем данные из url строки
        :param data: строка url запроса
        :return: словарь с данными
        """
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            # записываем данные в словарь
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        """
        Разбираем строку байт
        :param data: строка байт
        :return: декодированные данные в виде словаря
        """
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        """
        Разбипаем данные из get запроса
        :param env: словарь с данными
        :return: данные в виде байтов
        """
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        # Получаем все данные запроса
        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)

        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            # получаем view по url
            view = self.urlpatterns[path]
            # добавляем параметры запросов
            request = {'method': method, 'data': data, 'request_params': request_params}
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)
            # вызываем view, получаем результат
            code, text = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [text.encode('utf-8')]
        else:
            # Если url нет в urlpatterns - то страница не найдена
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]


class DebugApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
