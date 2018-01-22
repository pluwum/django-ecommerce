from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def home_page(request):
    context = {"title": "test view", "content": "my contentx"}
    if request.method == "POST":
        return HttpResponse("Form was submited {}".format(
            request.POST.get('email')))
    return render(request, "home.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form,
        "title": "Not logged in",
        "content": "User not logged in"
    }
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Successfull login")
        else:
            return HttpResponse("Failed login")
    if not request.user.is_authenticated:
        return render(request, "authentication/login.html", context)

    return HttpResponse("Logged in user")