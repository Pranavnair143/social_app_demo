
from rest_framework import  viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.like import serializers

from api.like.serializers import LikeSerializer
from .models import Like

class LikeViewset(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer

    @action(methods=['POST'], detail=True,url_path="action")
    def like_action(self, request,pk=None):
        data={
            "post_id":pk,
            "user_id":request.user.id,
            "status":request.data['action']
        }
        if data['status']==0:
            try:
                instance=Like.objects.filter(post_id=pk,user_id=request.user).first()
            except Like.DoesNotExist:
                return Response({"status":False,"errorMsg":"Error"})    
            instance.delete()
            return Response({"status":True,"message":"Removed reaction successfully"})
        else:
            like_list=Like.objects.filter(post_id=pk,user_id=request.user)
            if len(like_list)>0:
                a=like_list.first()
                a.status=data['status']
                a.save()
                return Response({"status":True,"message":f"{dict(Like.STATUS).get(data['status'])} successfully"})
            else:
                instance=self.get_serializer(data=data)
                if instance.is_valid():
                    instance.save()
                    return Response({"status":True,"message":f"{dict(Like.STATUS).get(data['status'])} successfully"})
                return Response({"status":False,"message":instance.errors})