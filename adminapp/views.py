# adminapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Category, Quiz, Question, QuizSubmission
from .serializers import UserSerializer, CategorySerializer, QuizSerializer, QuestionSerializer
from usersapp.serializers import SubmissionSerializer
from usersapp.models import Submission

#admin registeration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data={**request.data, 'is_admin': True, 'is_superuser': True, 'is_staff': True})
        if serializer.is_valid():
            user = serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#admin login    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        if not user or not user.check_password(request.data.get('password')):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_admin:
            return Response({'error': 'Admin access only'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data})

# Category Views
class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # No created_by needed
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Quiz Views
class QuizListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QuizDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    
    def put(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Question Views
class QuestionListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizToggleView(APIView):
    permission_classes = [IsAdminUser]
    
    def patch(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        quiz.is_active = not quiz.is_active
        quiz.save()
        return Response(QuizSerializer(quiz).data)

#  Submission Views
class SubmissionListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

class SubmissionDetailView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            submission = Submission.objects.get(pk=pk)
            serializer = SubmissionSerializer(submission)
            return Response(serializer.data)
        except Submission.DoesNotExist:
            return Response({"detail": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)