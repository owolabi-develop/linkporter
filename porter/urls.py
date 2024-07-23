from django.urls import path,include

from . views import (index,
                     delete_articles,
                     process_schedule,
                     user_registration,
                     acct_activation,
                     surveyView)


urlpatterns = [
    path("",index,name="index"),

    path("delete/<int:article_id>/",delete_articles,name="delete"),
    path('schedule/',process_schedule, name="process_schedule"),
    path('signup/',user_registration,name='signup'),
    path('activate/<str:uidb64>/<str:token>/', acct_activation,name='activate'),
    path("survey/",surveyView,name='survey')  
]
