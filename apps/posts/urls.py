from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list),
    path('create/', views.post_create),
    path(r'^detail/(?P<id>\d+)$', views.post_detail),
    path('update/', views.post_update),
    path('delete/', views.post_delete),
]
