from django.shortcuts import render

from django.views.generic import TemplateView
from .models import *


class IndexPage(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        article_data = []
        all_article = Article.objects.all()[:9]
        for article in all_article:
            article_data.append({
                'title': article.title,
                'cover': article.content.url,
                'category': article.category.title,
                'created_at': article.created_at,
            })
        context = {
            'article_data': article_data
        }
        return render(request, 'index.html', context)
