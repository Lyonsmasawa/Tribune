from distutils.command.upload import upload
from django.db import models
import datetime as dt

# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length=30) 
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.first_name
    
    def save_editor(self):
        self.save()

    class Meta:
        ordering = ['first_name']

class tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=30)
    post = models.TextField()
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE)
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now_add=True) #auto_now_add will automatically save the exact time and date to db as soon as we save that model
    article_image = models.ImageField(upload_to = 'articles/')

    def __str__(self):
        return self.title

    @classmethod
    def today_news(cls):
        today = dt.date.today()
        news = cls.objects.filter(pub_date__date = today) #Django provides a query filter date that allows us to convert out datetimefield to a date. Query filters allow us to customize our queries to fit our needs. They are defined using two underscores before the field.
        return news

    @classmethod
    def days_news(cls, date):
        news = cls.objects.filter(pub_date__date = date)
        return news

    @classmethod
    def search_by_title(cls,search_term):
        news = cls.objects.filter(title__icontains=search_term)
        return news