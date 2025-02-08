from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'files-api',FileViewSet, basename='file')
app_name = "File"
urlpatterns = [
    path('',include(router.urls)),
    path("edit/<int:file_id>/",edit_file,name="edit_file"),
    path('upload/', UploadFileView.as_view(), name='upload_file'),
]
