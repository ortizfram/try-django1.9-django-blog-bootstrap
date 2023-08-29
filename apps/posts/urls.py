from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/', views.post_detail, name='detail'),
    path('<int:id>/edit/', views.post_update, name='update'),
    path('delete/', views.post_delete, name='post_delete'),
]
