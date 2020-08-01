from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Stuff(models.Model):

    director = models.CharField(max_length=50, null=True)
    writer = models.CharField(max_length=150, null=True)
    actors = models.TextField(null=True)

    @property
    def total_actors(self):
        actors_list = self.actors.split(",")
        return len(actors_list)

    @property
    def total_writers(self):
        writers_list = self.writer.split(",")
        return len(writers_list)

    def __str__(self):
        return str(self.pk)


class Movie(models.Model):

    title = models.CharField(max_length=50, unique=True)
    year = models.CharField(max_length=9, null=True)
    rated = models.CharField(max_length=10, null=True)
    released = models.CharField(max_length=20, null=True)
    runtime = models.CharField(max_length=10, null=True)
    genre = models.CharField(max_length=50, null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=25, null=True)
    country = models.CharField(max_length=35, null=True)
    awards = models.TextField(null=True)
    metascore = models.CharField(max_length=4, null=True)
    imdb_id = models.CharField(max_length=25, null=True)
    dvd = models.CharField(max_length=30, null=True)
    production = models.CharField(max_length=50, null=True)
    stuff = models.ManyToManyField(Stuff)

    @property
    def comments(self):
        self.comments.all()

    @property
    def total_comments(self):
        return self.comments.count()
    
    @property
    def positive_comments(self):
        return Comment.classified_as.positive().filter(movie=self)

    @property
    def negative_comments(self):
        return Comment.classified_as.negative().filter(movie=self)
    
    @property
    def unclassified_comments(self):
        return Comment.classified_as.unclassified().filter(movie=self)

    @property
    def total_rates(self):
        return self.rates.count()

    def __str__(self):
        return self.title


class Ratings(models.Model):

    source = models.CharField(max_length=50, null=True)
    value = models.CharField(max_length=6, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rates")

    def __str__(self):
        return "{}: {}".format(self.movie.title, self.value)


class ClassifiedCommentsQuerySet(models.QuerySet):

    def positive(self):
        return self.filter(classification=1)

    def negative(self):
        return self.filter(classification=0)
    
    def unclassified(self):
        return self.filter(classification=-1)

class Comment(models.Model):

    CLASSIFICATION_OPTIONS = [(-1, "not classified"), (0, "negative"), (1, "positive")]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(null=True)
    classification = models.CharField(
        max_length=1, choices=CLASSIFICATION_OPTIONS, default=-1,
    )
    objects = models.Manager()
    classified_as = ClassifiedCommentsQuerySet.as_manager()

    def __str__(self):
        return "author: {}, body: {}".format(self.author, self.body)
