from django.urls import path
from .views import UserGameList, EventsByUser

urlpatterns = [
    path("reports/usergames", UserGameList.as_view()),
    path("users/eventsbyuser", EventsByUser.as_view()),
    path("users/gamesbyuser", UserGameList.as_view()),
]
