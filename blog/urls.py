from django.urls import path
from . import views
# from django.conf.urls import url

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('category/', views.CategoryPage.as_view(), name='category'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('article/all/', views.AllArticleAPIView.as_view(), name='all_articles'),
    path('article/<int:pk>/', views.SingleArticleAPIView.as_view(),
         name='single_article'),
    path('article/search/', views.SearchArticleAPIView.as_view(),
         name='search_article'),
    path('article/add/', views.SubmitArticleAPIView.as_view(),
         name='submit_article'),
    path('article/update-cover/',
         views.UpdateArticleAPIView.as_view(), name='update_article'),
    path('article/delete/',
         views.DeleteArticleAPIView.as_view(), name='delete_article'),
    #     path('article/add',
    #          views.AddArticleAPIView.as_view(), name='add_article'),
    path('login/',
         views.LoginPage.as_view(), name='login_blog'),
    path('signup/',
         views.signup, name='signup'),
]
