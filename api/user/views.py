from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    username = request.POST['email']
    password = request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'status':False,'error': 'Enter a valid email'})

    if len(password) < 6:
        return JsonResponse({'status':False,'error': 'Password length should be at least 6'})

    UserModel = get_user_model()
    user = authenticate(username=username, password=password)

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(
                email=username).values().first()
            usr_dict.pop('password')
            if not user:
                return JsonResponse({'status':False,'error': 'Invalid Credentials'})
            token,_ = Token.objects.get_or_create(user=user)
            user.save()
            #login(request, user)
            return JsonResponse({'token': token.key, 'user': usr_dict})
        else:
            return JsonResponse({'status':False,'error': 'Invalid password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'status':False,'error': 'Invalid Email'})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def signout(request):
    request.user.auth_token.delete()
    logout(request)
    return JsonResponse({'status':True,'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]
