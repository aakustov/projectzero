from django.urls import path
from . import views

urlpatterns = [
    path('', views.roundone, name='roundone'),
    path('next_question/', views.next_question, name='next_question'),
    path('answer/', views.answer_question, name='answer_question'),
    path('result/', views.result_view, name='result'),
    path('start1/', views.start_view, name='start1'),
    #path('statistics/', views.get_statistics, name='get_statistics'),
    path('leaderboard1', views.leaderboard_view, name='leaderboard1')
]