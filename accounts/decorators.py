from django.http import HttpResponseForbidden

def vendor_required(view_func):
    """ Restricts access to vendors only """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'vendor':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapper

def admin_required(view_func):
    """ Restricts access to admin users only """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Admins only.")
    return wrapper
