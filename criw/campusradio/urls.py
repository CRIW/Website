from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show/(?P<show_slug>[0-9a-zA-Z-]+)/$',views.show, name='show'),
    url(r'^episode$',views.episodes,name='episodes'),
    url(r'^episode/(?P<episode_slug>[0-9a-zA-Z-]+)/$',views.episode, name='episode')
]
