from django.urls import path
from . import views

urlpatterns = [
   
    path('place_order/', views.place_order, name='place_order'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('gerar-qrcode/', views.gerar_qrcode, name='gerar_qrcode'),
    
] 