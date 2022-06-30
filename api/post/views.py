
from rest_framework import  viewsets
from rest_framework.response import Response
from api.post.models import Post, PostImage
from api.post.serializers import PostCreateImageSerializer, PostCreateSerializer, PostReadImageSerializer, PostReadSerializer
from rest_framework.decorators import action
from api.like.models import Like
from .pagination import PostPagination

class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class = PostReadSerializer
    serializer_classes = {
        'list': PostReadSerializer,
        'create_post':PostCreateSerializer
    }
    ordering=('-liked_tags')
    pagination_class = PostPagination

    def get_serializer_class(self): 
        return self.serializer_classes[self.action]
    



    @action(methods=['POST'], detail=False, url_path='create_post')
    def create_post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)
            return Response({"status":True,"message":"Created successfully","data":serializer.data})
        else:
            return Response({"status":False,"errorMsg":serializer.errors})

class PostImageViewset(viewsets.ModelViewSet):
    queryset=PostImage.objects.all()
    serializer_class = PostReadImageSerializer
    serializer_classes = {
        'list': PostReadImageSerializer,
        'create_post_image':PostCreateImageSerializer
    }

    def get_serializer_class(self): 
        return self.serializer_classes[self.action]
    
    @action(methods=['POST'], detail=False, url_path='create_post_image')
    def create_post_image(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True,"message":"Created successfully","data":serializer.data})
        else:
            return Response({"status":False,"errorMsg":serializer.errors})

class RelatedPostViewset(viewsets.ReadOnlyModelViewSet):
    queryset=Post.objects.all()
    serializer_class = PostReadSerializer
    pagination_class = PostPagination
    
    def get_queryset(self):
        like_list=Like.objects.filter(user_id=self.request.user)
        tags_list=[i.post_id.tags.all() for i in like_list]
        tags_id_list=[]
        for i in tags_list:
            for j in i:
                tags_id_list.append(j.id)
        return self.queryset.filter(tags__in=set(tags_id_list)).distinct()