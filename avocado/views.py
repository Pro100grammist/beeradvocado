from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import *
from .utils import *
from .models import *


class BeerHome(DataMixin, ListView):
    model = Beer
    template_name = 'avocado/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Beermania')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Beer.objects.filter(is_published=True).select_related('cat')


class BeerCategory(DataMixin, ListView):
    model = Beer
    template_name = 'avocado/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Beer.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddForm
    template_name = 'avocado/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add a story')
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Beer
    template_name = 'avocado/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='post')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationPageForm
    template_name = 'avocado/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'avocado/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authorization')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'avocado/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Feedback')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned.data)
        return redirect('home')


def logout_func(request):
    logout(request)
    return redirect('login')


def breweries(request):
    return render(request, 'avocado/breweries.html', {'menu': menu, 'title': 'Breweries'})


def about(request):
    return render(request, 'avocado/about.html', {'menu': menu, 'title': 'About us'})


def contact(request):
    return HttpResponse('Feedback')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Archive sorted by years</h1><p>{year}</p>')


# menu = ['About us', 'Add a story', 'Feedback', 'Log in']
#
# def index(request):
#     posts = Beer.objects.all()
#     horizontal_menu = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0,
#     }
#     return render(request, 'avocado/index.html', context=horizontal_menu)
#
#
# def show_category(request, cat_id):
#     posts = Beer.objects.filter(cat_id=cat_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     horizontal_menu = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Beer',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'avocado/index.html', context=horizontal_menu)
#
#
# def show_post(request, post_slug):
#     post = get_object_or_404(Beer, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'avocado/post.html', context=context)
#
# def addpage(request):
#     if request.method == 'POST':
#         form = AddForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Beer.objects.create(**form.cleaned_data)
#             return redirect('home')
#
#     else:
#         form = AddForm()
#     return render(request, 'avocado/addpage.html', {'form': form, 'menu': menu})
#
# def login(request):
#     return HttpResponse('Authorization')
