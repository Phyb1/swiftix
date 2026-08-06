from django.urls import path

from . import views

app_name = "posters"

urlpatterns = [
    path("promotions/", views.PosterListView.as_view(), name="poster_list"),
]
