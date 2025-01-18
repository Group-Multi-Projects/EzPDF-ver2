from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'files-api',views.FileViewSet, basename='file')
app_name = "File"
urlpatterns = [
    path('',include(router.urls)),
    path("edit/<int:file_id>/",views.edit_file,name="edit_file"),
    path('upload/', views.upload_file, name='file-upload'),
]
