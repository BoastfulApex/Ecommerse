from django.http import HttpResponse
from django.shortcuts import redirect


def un_authintificated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            groups = None
            if request.user.groups.exists():
                print(request.user.groups.all())
                groups = request.user.groups.all()[0].name
            if groups in roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("<h2>Bu sahifaga kirish uchun sizda ruhsat yo'q</h2>")

        return wrapper

    return decorator
