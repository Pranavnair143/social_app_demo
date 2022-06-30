from urllib import request
from rest_framework import serializers

from api.like.models import Like
from api.user.models import CustomUser
from .models import PostImage,Post,Tag


class PostReadSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()
    like=serializers.SerializerMethodField()
    like_num=serializers.SerializerMethodField()
    dislike_num=serializers.SerializerMethodField()
    liked_users=serializers.SerializerMethodField()
    dislike=serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(many=True,read_only=True,slug_field='name')
    class Meta:
        model=Post
        fields=['id','liked_users','images','tags','like','dislike','like_num','dislike_num']
    
    def get_like_num(self,instance):
        user_id=self.context['request']
        fav=list(Like.objects.filter(user_id=user_id.user,post_id=instance.id,status=1))
        return len(fav)
    
    def get_dislike_num(self,instance):
        user_id=self.context['request']
        fav=list(Like.objects.filter(user_id=user_id.user,post_id=instance.id,status=2))
        return len(fav)

    def get_liked_users(self,instance):
        users=Like.objects.filter(post_id=instance.id,status=1).values_list('user_id',flat=True)
        names=[]
        for i in users:
            names.append(CustomUser.objects.get(id=i).name)
        return list(names)

    def get_images(self,instance):
        img=PostImage.objects.filter(post_id=instance.id).values_list('image',flat=True)
        if (img==None):
            return None
        return list(img)
    
    
    def get_like(self,instance):
        user_id=self.context['request']
        fav=list(Like.objects.filter(user_id=user_id.user,post_id=instance.id,status=1))
        if len(fav)>0:
            return True
        return False
    
    def get_dislike(self,instance):
        user_id=self.context['request']
        fav=list(Like.objects.filter(user_id=user_id.user,post_id=instance.id,status=2))
        if len(fav)>0:
            return True
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'description',
            'tags'
        ]

class PostCreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostImage
        fields='__all__'

class PostReadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostImage
        fields='__all__'

