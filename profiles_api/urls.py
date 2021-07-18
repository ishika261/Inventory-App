from django.urls import path, include
from rest_framework import routers, viewsets
from rest_framework.routers import DefaultRouter
from profiles_api import views


router = DefaultRouter()
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewset)
router.register('inventory', views.InventoryItemViewSet)
router.register('event', views.EventViewSet)
router.register('eventInventory', views.EventInventoryViewSet)
# router.register('feed', views.UserProfileFeedViewsSet)

urlpatterns = [
    # path('hello/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
