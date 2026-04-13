from django.urls import path
from . import views

urlpatterns = [
    path('', views.roundone, name='roundone'),
    path('next_question/', views.next_question, name='next_question'),
    path('answer/', views.answer_question, name='answer_question'),
    path('result/', views.result_view, name='result'),
    path('start/', views.start_view, name='start'),
    #path('statistics/', views.get_statistics, name='get_statistics'),
    path('leaderboard', views.leaderboard_view, name='leaderboard')
]