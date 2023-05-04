from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Idea(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    validated = models.BooleanField()

    def __str__(self):
        return self.name


class Implementation(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_url = models.CharField(max_length=200)
    demo_url = models.CharField(max_length=200)
    validated = models.BooleanField()

    def __str__(self):
        return "%s'd %s" % (self.author.username, self.idea.name)


# TODO comments
# TODO screenshots
