
from django.urls import path
from .views import home,generate_bill

app_name='phonepay'
urlpatterns = [
    path('<int:item_id>/',home, name='home'),
    # path('success/' , success , name='success'),
    path('generate_bill/', generate_bill, name='generate_bill')
]