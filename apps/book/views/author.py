from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, RetrieveDestroyAPIView
from apps.book.models import Author
from apps.book.serializers import AuthorSerializer



@api_view(['GET'])
def list_authors(request):
    authors = Author.objects.all()

    data = AuthorSerializer(authors, many=True)

    return Response(data.data, status=status.HTTP_200_OK)


class DetailAuthor(RetrieveDestroyAPIView):

    queryset = Author.objects.all()

    serializer_class = AuthorSerializer


class DeleteAuthor(DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer