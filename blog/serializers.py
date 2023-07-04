from rest_framework import serializers


class SingleArticleSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=128)
    cover = serializers.ImageField()
    # required=False, allow_null=True, allow_blank=True)
    content = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=2048)
    created_at = serializers.DateTimeField(required=True, allow_null=False)


class SubmitArticleSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=128)
    cover = serializers.ImageField()
    # required=False, allow_empty_file=False)
    content = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=2048)
    category_id = serializers.IntegerField(required=True, allow_null=False)
    author_id = serializers.IntegerField(required=True, allow_null=False)
    promote = serializers.BooleanField(required=True, allow_null=False)


class UpdateArticleCoverSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)
    cover = serializers.ImageField()
    # required=False, allow_empty_file=True)


class DeleteArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True, allow_null=False)

class AddContactUsMessageSerializer(serializers.Serializer):
    subject=serializers.CharField()
    name=serializers.CharField()
    email=serializers.EmailField()
    phone=serializers.CharField()
    message=serializers.CharField()
    
