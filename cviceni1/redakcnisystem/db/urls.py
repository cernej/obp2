from django.urls import path
from . import views

app_name = "db"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("articles/create/", views.ArticleCreateView.as_view(), name="article_create"),
    path("articles/<int:pk>/edit/", views.ArticleEditView.as_view(), name="article_edit"),
    path("articles/<int:pk>/delete/", views.ArticleDeleteView.as_view(), name="article_delete"),
]