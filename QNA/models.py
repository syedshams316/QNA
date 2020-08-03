from django.conf import settings
from django.db import models


# Create your models here.

class Question(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    up_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_up_vote')
    down_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_down_vote')

    def __str__(self):
        return str(self.question) + str(self.author)


class Comment(models.Model):

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    up_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_up_vote')
    down_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_down_vote')

    def __str__(self):
        return str(self.author) + ' : ' + str(self.text)
