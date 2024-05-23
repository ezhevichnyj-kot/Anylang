from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=255, default="unnamed")
    file = models.FileField(upload_to='upldfile/')
    lang = models.CharField(max_length=10, default='RU')

class TranslateArticle(models.Model):
    file = models.FileField(upload_to='upldfile/')
    lang = models.CharField(max_length=255, default='EN')
    orig = models.ForeignKey(to=Article, null=False, on_delete=models.CASCADE)
