from django.shortcuts import redirect

#checks isf user not authenticating

def user_not_authenticated(function=None, redirect_url='index'):
    '''

    '''
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return wrapped_view

    if function:
        return decorator(function)

    return decorator()