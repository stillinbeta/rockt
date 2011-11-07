from django.db import models


class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    post = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
