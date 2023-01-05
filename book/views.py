from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets

from book.models import Book
from book.permissions import IsAdminOrIfAuthenticatedReadOnly
from book.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BookListSerializer

        return BookSerializer

    def get_queryset(self):
        """Retrieve the book with filters"""
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        cover = self.request.query_params.get("cover")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        if cover:
            queryset = queryset.filter(cover__icontains=cover)

        return queryset.distinct()

    # Only for documentation purposes
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by title (ex. ?title=Test)"
            ),
            OpenApiParameter(
                "author",
                type=str,
                description="Filter by author (ex. ?author=Test)"
            ),
            OpenApiParameter(
                "cover",
                type=str,
                description="Filter by cover (ex. ?cover=Hard or Soft)"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
