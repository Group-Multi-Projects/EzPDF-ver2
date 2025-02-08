
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'account-api',views.AccountViewset, basename='account')
app_name = "Account"
urlpatterns = [
    path('',include(router.urls)),
    path("signup/",views.SignupView.as_view(),name="signup"),
    path('signin/', views.SignInAPIView.as_view(), name='signin'),
    path("signout/",views.signout,name="signout"),
]
