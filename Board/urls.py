from django.conf.urls import url
from . import views

app_name = 'Board'
urlpatterns = [
    url(r'^(?P<section_id>[a-z]+)/$', views.section, name='section'),
    url(r'^$', views.index, name='index'),
]
