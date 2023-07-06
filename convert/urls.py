from django.urls import path
from . import views


urlpatterns = [

    path('', views.record, name='home'),
    
    # path("<int:pk>",views.delete, name='delete'), 
]