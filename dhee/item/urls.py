from django.urls import path
from . import views
from .views import add_to_cart, cart_detail, consolidate_cart

app_name = 'item'

urlpatterns = [
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('', views.items, name='items'),
    path('<int:item_id>/price/', views.item_price, name='price'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('consolidate-cart/', consolidate_cart, name='consolidate_cart'),
]
