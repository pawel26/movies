from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Movie, Ratings, Comment
from .serializers import MovieSerializer, RatingsSerializer, CommentSerializer
from api.permissions import AllowedToCreate


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowedToCreate]
    filterset_fields = {
        "comments__author__username": ['exact'],
        "title": ["exact", "iexact"],
        "metascore": ["exact", "lte", "gte", "in"],
        "language": ["exact", "iexact"],
        "country": ["exact", "iexact"],
        "year": ["exact", "lte", "gte", "in"],
        "runtime": ["exact", "lte", "gte", "in"],
        "rates__source": ["exact", "iexact"],
    }


class RatingsViewSet(viewsets.ModelViewSet):
    serializer_class = RatingsSerializer
    search_fields = ["source"]
    permission_classes = [AllowedToCreate]

    def get_queryset(self):
        qs = Ratings.objects.all()
        movie = self.request.query_params.get("movie", None)
        if movie is not None:
            qs = qs.filter(movie__title=movie)
        return qs


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowedToCreate]
    filterset_fields = {
        "movie": ['exact'], 
        "movie__title": ['exact'], 
        "author__username": ['exact'],
        "classification": ['exact', 'in']
        }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RaportViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    renderer_classes = [XLSXRenderer]
    permission_classes = [IsAuthenticated]
    filename = "movies.xlsx"
