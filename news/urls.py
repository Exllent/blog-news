from django.urls import path
from news.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', index, name='home'),
    path('register/', register, name='register'),
    path('signal/', signal, name='signal'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    # path('', cache_page(60 * 15)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', GetCategory.as_view(), name='category'),
    path('news/<int:news_id>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', AddNews.as_view(), name='add_news')
    path('news/add-news/', add_news, name='add_news')
]
