from rest_framework import serializers
from .tag import TagSerializer
from .author import AuthorSerializer
from apps.book.models import Book

class ReadBookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"
        # depth = 1

class CreateBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"