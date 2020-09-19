from django.http import HttpResponse
from django.shortcuts import redirect, render
# from .view import unauthorized_access

# decorator to prevent user from accessing restricted pages
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


# to allow only specific user of certain roles access to functions
def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'not_authorized.html')
        return wrapper_func
    return decorator