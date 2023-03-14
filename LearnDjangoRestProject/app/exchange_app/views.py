from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
import requests as req
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from rest_framework import generics
from rest_framework.permissions import *
from .forms import *
from .serializers import WomenSerializer
from django.views.generic import ListView, DetailView, CreateView
from .utils import *
from .management.commands.bot import send_message


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'exchange_app/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context(title="Главная страница").items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'exchange_app/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context(title="Добавление статьи").items()))


def contact(request):
    return HttpResponse('Обратная связь')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'exchange_app/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        return dict(list(context.items()) +
                    list(self.get_user_context(title='Категория - ' + str(c.name),
                                               cat_selected=c.pk).items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'exchange_app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context(title=context['post']).items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'exchange_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context(title="Регистрация").items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'exchange_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context(title="Авторизация").items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def send_message_request(request, post_slug):
    send_message(post_slug)
    return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticated,)


class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminUser, )

