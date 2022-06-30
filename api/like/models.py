from django.db import models
from django.contrib.auth import get_user_model
from django.forms import BooleanField
from api.post.models import Post

User=get_user_model()

class Like(models.Model):
    STATUS = (
        (1, 'Liked'),
        (2, 'Disliked'),
    )
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id= models.ForeignKey(Post,on_delete=models.CASCADE)
    status=models.CharField(choices=STATUS,max_length=50)
    
    def __str__(self):
        return "User: "+str(self.user_id) +" --- Post:"+ str(self.post_id)