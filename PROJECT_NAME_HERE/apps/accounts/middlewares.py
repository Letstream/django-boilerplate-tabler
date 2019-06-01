def UserActivityMiddleware(get_response):

    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated:
            request.user.update_last_active()
        return response

    return middleware
