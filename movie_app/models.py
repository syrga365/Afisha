from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    director = models.ForeignKey('movie_app.Director', on_delete=models.CASCADE, related_name='director')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey('movie_app.Movie', on_delete=models.CASCADE, related_name='movie')

    def __str__(self):
        return self.text[:20]