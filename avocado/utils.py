from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [
    {'title': 'Breweries', 'url_name': 'breweries'},
    {'title': 'About us', 'url_name': 'about'},
    {'title': 'Add a story', 'url_name': 'add_page'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Map', 'url_name': 'beer_map'}
    # {'title': 'Log in', 'url_name': 'login'}
]


class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('beer'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
