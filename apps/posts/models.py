from django.db import models

# Create your models here.
# MVC: MODEL VIEW CONTROLLER

class Post(models.Model):
    title = models.CharField(max_length=120)
    excerpt = models.CharField(max_length=250)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title
    
    # comes from posts.urls 'detail'
    def get_absolute_url(self):
        return "/posts/%s/" %(self.id)

    