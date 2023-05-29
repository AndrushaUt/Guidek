from django.db import models

# Create your models here.

class Guide(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField(max_length=200)
    photo = models.ImageField(null=True, upload_to="photos/", blank=True)
    date = models.DateField()
    username = models.CharField(max_length=150, null=False)
    likes_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"author: {self.username}   title:{self.title}"


class Comment(models.Model):
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    to_post = models.IntegerField()

    def __str__(self):
        return f"author: {self.author} num_post: {self.to_post}"


class Like(models.Model):
    username = models.CharField(max_length=100)
    to_post = models.IntegerField()

    def __str__(self):
        return f"username: {self.username} num_post: {self.to_post}"