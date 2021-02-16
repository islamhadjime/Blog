from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.FileField(verbose_name="Аватар",null=True, blank=True)
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"Город")
    


    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return  reverse("view_user",args=[self.user.first_name])

    

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор",related_name="posts")
    title = models.CharField(max_length=250)
    slug  = models.SlugField(max_length=250)
    text  = models.TextField()
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug':self.slug})


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="",verbose_name=u"Пост", related_name="comments")
   
    name = models.CharField(max_length=80,default="")
    email = models.EmailField( default="")
    text = models.TextField(verbose_name=u"Текст", null=True, blank=True)
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["datetime"]
