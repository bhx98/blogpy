from django.forms   import BaseModelForm
from models import Article

class ArticleForm(BaseModelForm):
    class Meta:
        model=Article
        fields='__all__'