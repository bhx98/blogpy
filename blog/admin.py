from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
# Register your models here.

# admin.site.register(UserProfile)
# admin.site.register(Article)
# admin.site.register(Category)


class textEditorAdmin(admin.ModelAdmin):
    list_display = ["title"]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar', 'description']


class ArticleAdmin(admin.ModelAdmin):
    content = forms.CharField(widget=CKEditorWidget())
    search_fields = ['title', 'content']
    list_display = ['title', 'category', 'created_at', 'author']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
