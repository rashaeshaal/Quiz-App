# usersapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('handlelogin/', views.LoginView.as_view(), name='handle-login'),
    path('quizzes/active/', views.ActiveQuizView.as_view(), name='active-quizzes'),
    path('submissions/', views.SubmissionView.as_view(), name='submissions'),
    path('past-submissions/', views.PastSubmissionsView.as_view(), name='past-submissions'),
]