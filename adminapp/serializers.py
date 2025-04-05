# adminapp/serializers.py
from rest_framework import serializers
from .models import User, Category, Quiz, Question, QuizSubmission

# adminapp/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'is_admin', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('is_admin'):
            validated_data.update({'is_superuser': True, 'is_staff': True})
        return User.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True}
        }

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    

    
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer']
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'category', 'is_active', 'questions']
class QuizSubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)
    class Meta:
        model = QuizSubmission
        fields = ['id', 'user', 'quiz', 'score', 'submitted_at']
        read_only_fields = ['id', 'user', 'quiz', 'submitted_at']
        extra_kwargs = {'score': {'required': True}}

    def create(self, validated_data):
        submission = QuizSubmission.objects.create(
            user=self.context['request'].user,
            quiz=validated_data['quiz'],
            score=validated_data['score']
        )
        return submission
    
    