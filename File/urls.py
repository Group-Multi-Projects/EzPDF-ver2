from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "File"
urlpatterns = [
    path("edit/<int:file_id>/",views.edit_file,name="edit_file"),
    path('upload/', views.upload_file, name='file-upload'),
    path('file_api/<int:id>/',views.get_put_delete_file_api,name="get_put_delete_api"),
    path("get_list_files/<str:page_type>/",views.get_list_files,name="get_list_files"),
    path('trash/<int:id>/',views.add_to_trash,name="add_to_trash"),
]
