from rest_framework import serializers
from .models import Submission, UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)
    class Meta:
        model = Submission
        fields = '__all__'