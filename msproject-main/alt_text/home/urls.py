from django.urls import path

from . import views


urlpatterns = [
    path('', views.main, name='home'),
    path('<int:goods_id>/', views.detail, name='detail'),
    path('upload/', views.upload, name='upload'),
    path('review/<int:goods_id>/', views.review, name='review'),
]