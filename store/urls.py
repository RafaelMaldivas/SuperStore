from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.store, name='store'),
    path('categoria/<slug:categoria_slug>/', views.store, name='produtos_por_categoria'),
    path('categoria/<slug:categoria_slug>/<slug:produto_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

] 
