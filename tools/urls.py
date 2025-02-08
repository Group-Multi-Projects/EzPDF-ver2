from django.urls import path
from . import views
app_name = "tools"
urlpatterns = [
    # path("draw/",views.draw_save_data,name="draw"),
    # path("addtext/",views.add_text_save_data,name="add_text"),
    path("getalldatas/",views.get_obj_all_changes_event,name="getalldatas"),

    path('test_celery/',views.test_celery),

]