from django.urls import path
from . import views
# from django.conf.urls import url

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),

]
