def not_suspended_member(request):
    def wrapper_func(request):
        if request.user:
            pass
        return wrapper_func
