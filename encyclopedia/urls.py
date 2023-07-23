from django.urls import path

from . import views
app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("create_save", views.create_save, name="create_save"),
    path("random", views.random, name="random"),
    path("edit-save", views.edit_save, name="edit_save"),
    path("edit", views.edit, name="edit"),
    path("search", views.get_searched_entry, name="get_searched_entry"),
    path("<str:title>", views.get_entry, name="get_entry"),
    path("error/<str:error>", views.error, name="error"),
]
