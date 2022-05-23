from django.http import HttpResponse
from django.shortcuts import redirect


def auth_users(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Вы не авторизованы для просмотра этой страницы')
        return wrapper
    return decorators


