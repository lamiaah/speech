from  django.urls import path
from convert.Api import views
urlpatterns = [
    # path('collect/',views.collect),
    path('bytes/', views.apirecord),
    path("add/",views.add
         ),
    
   
]
