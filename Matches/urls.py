from django.urls import path, include
from rest_framework import routers

from Matches import views

router = routers.DefaultRouter()
router.register(r'matches', views.MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
