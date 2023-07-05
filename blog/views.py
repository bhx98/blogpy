from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template import loader
from .forms import CommentForm, ContactForm, LoginForm, UserCreateForm
from . import serializers
from django.contrib import messages
from django.contrib.auth import login, authenticate
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.decorators.vary import vary_on_cookie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


def handler_404(request, exception):
    template = loader.get_tempalte('article_404.html')
    return HttpResponse(template.render({'exception': exception}, request), status=404)


class IndexPage(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        article_data = []
        all_article = Article.objects.all().order_by('-created_at')[:9]
        paginator = Paginator(all_article, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for article in all_article:
            article_data.append({
                'id': article.id,
                'title': article.title,
                'cover': article.cover.url,
                'author': article.author.user.first_name+' '+article.author.user.last_name,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })
        promote_data = []
        all_promote_article = Article.objects.filter(promote=True)
        for promote_article in all_promote_article:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'author': promote_article.author.user.first_name+' '+promote_article.author.user.last_name,
                'avatar': promote_article.author.avatar.url if promote_article.author.avatar else None,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'created_at': promote_article.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promote_article_data': promote_data,
            'page_obj': page_obj,
        }
        return render(request, 'blog/index.html', context)


class ArticleList(ListView):
    model = Article
    paginate_by = 3
    context_object_name = "Article_list"
    template_name = "article_pagination.html"


class ContactPage(TemplateView):
    template_name = 'contact.html'


class CategoryPage(ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category_data'


class AboutPage(TemplateView):
    template_name = 'about.html'


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            authenticate.user(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


class LoginPage(TemplateView):
    template_name = 'registeration/login.html'


class AllArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            all_article = Article.objects.all().order_by('-created_at')[:10]
            data = []
            for article in all_article:
                data.append({
                    'id': article.id,
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.username,
                    'promote': article.promote,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except article.DoesNotExist:

            return HttpResponseNotFound()
        except:
            return Response({'status': "Internal Server Error, we'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):
    def get(request, article_id):
        try:
            # article = get_object_or_404(Article, pk=article_id)
            # article_id = request.GET(id=pk)
            # article = get_object_or_404(article, id=article_id)
            article = Article.objects.filter(pk=article_id)
            serialized_data = serializers.SingleArticleSerializer(
                article, many=True)
            data = serialized_data.data
            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, we'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            from django.db.models import Q
            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []
            for article in articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name+' '+article.user.last_name,
                    "promote": article.promote,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, we'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitArticleAPIView(APIView):
    @login_required
    def post(self, request, format=None):
        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_400_OK)
            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)
            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()
            return Response({'status': status.HTTP_200_OK})
        except:
            return Response({'status': "Internal Server Error, we'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# update article's cover


class UpdateArticleAPIView(APIView):

    @login_required
    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(
                data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            Article.objects.filter(id=article_id).update(cover=cover)
            return Response({'status': 'OK'}, staus=status.HTTP_200_OK)
        except:
            return Response({"status':'Internal Server Error, we'll check it later"},
                            stauts=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):

    @login_required
    def post(self, request, format=None):

        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            Article.objects.filter(id=article_id).delete()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddArticleAPIView(APIView):
    @login_required
    def get(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('aricle_id')
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            Article.objects.filter(id=article_id).delete()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except:
            pass


class AllActiveCommentPost(APIView):
    def get(self, request):
        posts = Post.objects

class ContactUs(APIView):
    # template_name = 'contact.html'

    def post(self, request, format=None):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = ContactUsMessage.subject
            name: ContactUsMessage.name
            email: ContactUsMessage.email
            phone: ContactUsMessage.phone
            message: ContactUsMessage.message
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        else:
            # if a GET (or any other method) we'll create a blank form
            form = ContactForm()
            return render(request, "contact.html", {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
        return render(request, 'registeration/signup.html', {'form': form})
