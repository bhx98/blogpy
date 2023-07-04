from django.shortcuts import render

from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import CommentForm
from . import serializers
from jalali_date import datetime2jalali, date2jalali
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def handler_404(request, exception):
    template = loader.get_tempalte('article_404.html')
    return HttpResponse(template.render({'exception': exception}, request), status=404)


class IndexPage(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        article_data = []
        paginator = Paginator(all_article, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for article in all_article:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'author': article.author.user.username,
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
        }
        return render(request, 'index.html', context)


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
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.username,
                    'promote': article.promote,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, we'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            article_title = request.GET('article_title')
            article = Article.objects.filter(title__contains=article_title)
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


class UpdateArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(
                data=request.data)
            if serializers.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad Request'}, status=status.HTTP_400_OK)
            Article.objects.filter(id=article_id).update(cover=cover)
            return Response({'status': 'OK'}, staus=status.HTTP_200_OK)
        except:
            return Response({"status':'Internal Server Error, we'll check it later"},
                            stauts=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):
    def post(self, request, format=None):

        try:
            pass
        except:
            pass


class AddArticleAPIView(APIView):
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

