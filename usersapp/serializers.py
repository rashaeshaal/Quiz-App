from rest_framework import serializers
from adminapp.models import Quiz, Question
from .models import Submission, UserAnswer
from adminapp.serializers import UserSerializer

class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['correct_answer']  

class UserQuizSerializer(serializers.ModelSerializer):
    questions = UserQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'category', 'is_active', 'questions']

class UserAnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.ReadOnlyField(source='question.id')
    correct_answer = serializers.ReadOnlyField(source='question.correct_answer')

    class Meta:
        model = UserAnswer
        fields = ['id', 'question_id', 'selected_option', 'correct_answer']

class SubmissionSerializer(serializers.ModelSerializer):
    quiz_title = serializers.ReadOnlyField(source='quiz.title')
    answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'quiz_id', 'quiz_title', 'score', 'submitted_at', 'answers']
