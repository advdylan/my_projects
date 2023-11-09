from django.urls import path
from hello import views

urlpatterns = [
    path("", views.index, name="index"),
    path("brian", views.brian, name="brian")
]