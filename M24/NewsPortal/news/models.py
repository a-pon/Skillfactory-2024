from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0

        posts = Post.objects.filter(author=self).values('rating')
        comments = Comment.objects.filter(user=self.user).values('rating')
        posts_comments = Comment.objects.filter(post__author=self).values('rating')

        for post in posts:
            self.rating += post['rating']*3

        for comment in comments:
            self.rating += comment['rating']

        for posts_comment in posts_comments:
            self.rating += posts_comment['rating']

        self.save()


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    news = 'N'
    post = 'P'
    TYPES = [
        (news, 'Новость'),
        (post, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPES, default=post)
    time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header.title()}: {self.preview()}'

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
