from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers
from api.post.views import PostImageViewset, RelatedPostViewset


router = routers.DefaultRouter()
router.register("image",PostImageViewset,basename='image')
router.register("related_post",RelatedPostViewset,basename='related')

urlpatterns = [
    path('user/', include('api.user.urls')),
    path('post/', include('api.post.urls')),
    path('like/', include('api.like.urls')),
    path('', include(router.urls)),
]
