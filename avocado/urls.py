from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', cache_page(60)(BeerHome.as_view()), name='home'),  # index
    path('breweries/', breweries, name='breweries'),
    path('beer_map/', beer_map, name='beer_map'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_func, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BeerCategory.as_view(), name='category'),  # path('category/<int:cat_id>/', show_category, name='category')
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
