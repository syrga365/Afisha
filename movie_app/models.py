from django.db import models
from django.db.models import Avg


# class User(models.Model):
#     name = models.CharField(max_length=100, required=True)
#     email = models.EmailField(required=True)


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def movies_count(self):
        return 'Movie count:', self.movie.count()


class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    director = models.ForeignKey('movie_app.Director', on_delete=models.CASCADE, related_name='movie')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey('movie_app.Movie', on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text[:20]

    @property
    def rating(self):
        # return Review.objects.filter(movie=self).aggregate(Avg('stars'))
        total_stars = sum(review.stars or 0 for review in self.movie.reviews.all())
        total_reviews = self.movie.reviews.count()

        if total_reviews == 0:
            return 'No reviews yet'
        else:
            average_rating = total_stars / total_reviews
            return f'Average stars: {average_rating:.2f}'
