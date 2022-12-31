from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# from *ckeditor_uploader.fields* import RichTextUploadingField
import ckeditor
from datetime import datetime


def validate_file_extension(value):
    pass
    # import os
    # from django.core.exceptions import ValidationError
    # if value:
    #     ext = os.path.splitext(value.name)[1]
    #     valid_extension = ['.jpg', '.png', 'jpeg', ]
    #     if not ext.lower() in valid_extension:
    #         raise ValidationError('Unsupported file extension')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to='files/user_avatar/', null=True, blank=True)
    description = models.CharField(
        max_length=512, null=False, blank=True, validators=[validate_file_extension])

    def __str__(self):
        return self.user.get_full_name()
        # return self.user.first_name+" "+self.user.last_name


class Article(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(
        upload_to='files/article_cover/', validators=[validate_file_extension], null=True, blank=True, default='default.jpg')
    content = RichTextField(config_name='non_admin', blank=True, null=True)
    created_at = models.DateTimeField(
        default=datetime.now(), blank=False, null=True)
    category = models.ForeignKey(
        'Category', models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    cover = models.FileField(
        upload_to='files/category_cover/', null=False, blank=False, validators=[validate_file_extension])
    # magic method/dunder

    def __str__(self):
        return self.title
