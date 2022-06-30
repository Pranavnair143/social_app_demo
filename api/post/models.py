from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Tag(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag,blank=True)

class PostImage(models.Model):
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    image=models.ImageField(upload_to="post/post_images")