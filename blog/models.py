from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import ckeditor
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField
from django.utils.html import mark_safe


class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name="عنوان پست")
    # body = models.TextField()
    body = RichTextUploadingField()  # CKEditor Rich Text Field

    def __str__(self):
        return self.title


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    if value:
        ext = os.path.splitext(value.name)[1]
        valid_extension = ['.jpg', '.png', 'jpeg', ]
        if not ext.lower() in valid_extension:
            raise ValidationError('Unsupported file extension')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="نام کاربری")
    avatar = models.ImageField(
        upload_to='files/user_avatar/', null=True, blank=True,verbose_name="تصویر پروفایل")
    description = models.CharField(
        max_length=512, null=False, blank=True,verbose_name="توضیحات")

    def img_preview(self):
        return mark_safe(f'<img src="{self.avatar.url}" width="300"/>')

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
        # return self.user.username

        # return self.user.get_full_name()


class Article(models.Model):
    title = models.CharField(max_length=128, null=False,
                             blank=False, verbose_name="عنوان مقاله")
    cover = models.ImageField(
        upload_to='files/article_cover/',  null=True, blank=True, default='default.jpg', verbose_name="تصویر مقاله")

    content = RichTextField(null=True, blank=True)
    created_at = models.DateTimeField(
        default=datetime.now(), blank=False, null=True, verbose_name="تاریخ ایجاد")
    category = models.ForeignKey(
        'Category', models.CASCADE, null=True, blank=True, verbose_name="عنوان دسته بندی")
    author = models.ForeignKey(
        UserProfile, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="نویسنده مقاله")
    promote = models.BooleanField(
        default=False, verbose_name="مقاله ویژه")

    def img_preview(self):
        return mark_safe(f'<img src="{self.cover.url}" width="300"/>')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128, null=False,
                             blank=False, verbose_name="عنوان دسته بندی")
    cover = models.ImageField(
        upload_to='files/category_cover/', null=False, blank=False, verbose_name="تصویر")
    # magic method/dunder

    def category_image(self):
        return mark_safe(f'<img src="{self.cover.url}" width="300"/>'
                         )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class ContactUsMessage:
    subject = models.CharField(max_length=150)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = RichTextField(null=True, blank=True)
    insert_date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.subject
