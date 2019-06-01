from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, '404.html')

def server_error(request):
    return render(request, '500.html')

def permission_denied(request, exception):
    return render(request, '403.html', {'kwargs': exception})

def bad_request(request, exception):
    return render(request, '400.html')