from django.urls import path
from .views import AllSubmissionsView, CategoryView, LoginView, QuestionToggleView, QuizToggleView, QuizView, QuestionView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='category-detail'),
    path('quizzes/', QuizView.as_view(), name='quizzes'),
    path('quizzes/<int:pk>/', QuizView.as_view(), name='quiz-detail'),
    path('questions/', QuestionView.as_view(), name='questions'),
    path('questions/<int:pk>/', QuestionView.as_view(), name='question-detail'),
    path('quizzes/<int:pk>/toggle/', QuizToggleView.as_view(), name='quiz-toggle'),
    path('questions/<int:pk>/toggle/', QuestionToggleView.as_view(), name='question-toggle'),
    path('submissions/', AllSubmissionsView.as_view(), name='all-submissions'),
]