from django.shortcuts import render


def homepage_with_auth(request):
    return render(request, 'common/homepage-with-profile.html')


def homepage_without_auth(request):
    return render(request, 'common/homepage-without-profile.html')


def index(request):
    if not request.user.is_authenticated:
        return homepage_without_auth(request)
    return homepage_with_auth(request)
