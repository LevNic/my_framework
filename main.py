from app import Application
from views import views

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contacts/': views.contact_view,
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)

if __name__ == '__main__':
    pass
