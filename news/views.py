from django.shortcuts import render, redirect
from .forms import NewsForm, UserRegisterForm, UserLoginForm, SignalForm
from .models import News, Category
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
import os


def signal(request):
    if request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                subject=form.cleaned_data["subject"],
                message=form.cleaned_data["body"],
                from_email=os.getenv("EMAIL_HOST_USER"),
                recipient_list=[
                    os.getenv("EMAIL_HOST_ADMIN"),
                ],
                fail_silently=False,
            )

            if mail:
                messages.success(request, message="Письмо отправлено")
                return redirect("signal")

            else:
                messages.error(request, message="Ошибка")

    else:
        form = SignalForm()
    return render(request, template_name="news/signal.html", context={"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1"),
            )
            if user is None:
                user = form.save()
                login(request, user)
                messages.success(request, message="Регистрация прошла успешно")
                return redirect("home")
        else:
            messages.error(request, message="Ошибка регистрации")
    else:
        form = UserRegisterForm()
    return render(request, "news/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "User already exists")
    else:
        form = UserLoginForm()
    return render(request, template_name="news/login.html", context={"form": form})


class HomeNews(ListView):
    paginate_by = 3
    model = News
    template_name = "news/index.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related("category")


class GetCategory(ListView):
    model = News
    template_name = "news/category.html"
    context_object_name = "news"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.kwargs["category_id"], is_published=True
        ).select_related("category")


class ViewNews(DetailView):
    model = News
    context_object_name = "news_item"
    template_name = "news/view_news.html"
    pk_url_kwarg = "news_id"


def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, "news/add_news.html", {"form": form})
