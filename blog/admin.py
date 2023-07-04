from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin

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
    list_display = ['user', 'img_preview', 'description']
    readonly_fields = ['img_preview']


class ArticleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    content = forms.CharField(widget=CKEditorWidget())
    search_fields = ['title', 'content']
    list_display = ['title', 'category', 'Created_at', 'author', 'img_preview']
    readonly_fields = ['img_preview']

    def Created_at(self, obj):
        return datetime2jalali(obj.created_at).strftime('%Y/%m/%d %H:%M:%S')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    readonly_fields = ['category_image']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
