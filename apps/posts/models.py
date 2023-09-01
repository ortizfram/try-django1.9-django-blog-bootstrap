from django.db import models

from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.
# MVC: MODEL VIEW CONTROLLER

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.PROTECT) #superadmin default
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True, 
                              height_field="height_field", 
                              width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=250)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title
    
    # comes from posts.urls 'detail'
    def get_absolute_url(self):
        return "/posts/%s/" %(self.slug)

    class Meta:
        ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None): # recursive function
    #=> slugify title if new. but if slug exists return it (when update)
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    #=> use create_slug() if slug field is empty
    if not instance.slug :
        instance.slug = create_slug(instance) 

pre_save.connect(pre_save_post_receiver, sender=Post)

    