import omdb

import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import reverse

from .models import Movie, Ratings, Stuff, Comment
from nlp_classifier.classification import load_trained_classifier, classify


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["source", "value"]


class StuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff
        fields = ["director", "writer", "actors", "total_actors", "total_writers"]


class MovieCreateSerializer(serializers.ModelSerializer):
    # remove redundant serializer and extract create logic
    rates = RatingsSerializer(many=True, required=False)
    stuff = StuffSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = [
            "title",
            "year",
            "rated",
            "released",
            "runtime",
            "genre",
            "plot",
            "language",
            "country",
            "awards",
            "metascore",
            "imdb_id",
            "dvd",
            "production",
            "stuff",
            "rates",
        ]


class MovieSerializer(serializers.ModelSerializer):

    rates = RatingsSerializer(many=True, required=False)
    stuff = StuffSerializer(many=True, required=False)
    # comments = serializers.StringRelatedField(many=True)
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = [
            "title",
            "year",
            "rated",
            "released",
            "runtime",
            "genre",
            "plot",
            "language",
            "country",
            "awards",
            "metascore",
            "imdb_id",
            "dvd",
            "production",
            "stuff",
            "rates",
            "total_rates",
            "comments",
        ]

    def get_comments(self, obj):
        #add obj annotations for average
        request = self.context.get('request')
        comments = {
            "positive": request.build_absolute_uri('/api/comments/?movie={}&classification=1'.format(obj.id)),
            "negative": request.build_absolute_uri('/api/comments/?movie={}&classification=0'.format(obj.id)),
            "unclassified": request.build_absolute_uri('/api/comments/?movie={}&classification=-1'.format(obj.id)),
            "total": obj.total_comments,
            "total_positives": obj.positive_comments.count(),
            "total_negatives": obj.negative_comments.count(),
            "total_not_classified": obj.unclassified_comments.count(),
        }
        return comments

    def create(self, validated_data):
        omdb.set_default("apikey", "4a41d844")
        omdb.set_default("tomatoes", True)
        movie_data = omdb.get(title=f"{self.validated_data['title']}")
        ratings = movie_data["ratings"]
        if Movie.objects.filter(title=movie_data["title"]).exists():
            raise ValidationError("Movie already exists in database.")
        movie_serializer = MovieCreateSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie = movie_serializer.save()
            for rating_data in ratings:
                rating = Ratings(movie=movie)
                rating_serializer = RatingsSerializer(rating, data=rating_data)
                if rating_serializer.is_valid():
                    rating_serializer.save()
            stuff = Stuff.objects.create(
                director=movie_data["director"],
                writer=movie_data["writer"],
                actors=movie_data["actors"],
            )
            movie.stuff.add(stuff)

            return movie
        else:
            raise ValidationError(movie_serializer.errors)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["movie", "body"]

    def create(self, validated_data):
        classifier = load_trained_classifier()
        comment = validated_data["body"]
        author = validated_data["author"]
        movie = validated_data["movie"]
        classified_class = classify(comment, classifier)
        if classified_class == "Negative":
            prediction = 0
        else:
            prediction = 1
        comment_obj = Comment.objects.create(
            author=author, movie=movie, body=comment, classification=prediction
        )
        return comment_obj
