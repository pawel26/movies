from django.contrib import admin
from .models import Movie, Ratings, Comment, Stuff


class MovieAdmin(admin.ModelAdmin):
    pass


class RatingsAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class StuffAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)
admin.site.register(Ratings, RatingsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Stuff, StuffAdmin)
