from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    content_html = models.TextField()
    url = models.URLField(unique=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
