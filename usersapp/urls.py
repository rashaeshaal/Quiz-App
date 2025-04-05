from django.urls import path
from .views import ActiveQuizView, SubmissionView

urlpatterns = [
    path('quizzes/', ActiveQuizView.as_view(), name='active-quizzes'),
    path('submissions/', SubmissionView.as_view(), name='submissions'),
]