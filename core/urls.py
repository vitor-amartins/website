from django.urls import path
from core import views


urlpatterns = [
    path('tree/', views.tree, name="tree"),
    path('links/', views.LinkList.as_view(), name="links-list"),
    path('react/', views.react, name="react")
]
