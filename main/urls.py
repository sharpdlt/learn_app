from django.urls import path
from .views import user_activate, index

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/register/activate/<str:sign>/',
         user_activate, name='register_activate'),
]
