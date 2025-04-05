from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from adminapp.models import Quiz, Question, User
from adminapp.serializers import QuizSerializer, UserSerializer
from .models import Submission, UserAnswer
from .serializers import SubmissionSerializer, UserQuizSerializer

#user register
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data={**request.data, 'is_admin': False})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#user login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        if not user or not user.check_password(request.data.get('password')) or user.is_admin:
            return Response({'error': 'Invalid user credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data})

#view active quizzes
class ActiveQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserQuizSerializer(Quiz.objects.filter(is_active=True), many=True).data)

#submit quiz
class SubmissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_admin:
            return Response({'error': 'Admins cannot submit quizzes'}, status=status.HTTP_403_FORBIDDEN)

        try:
            quiz = Quiz.objects.get(pk=request.data['quiz_id'])
            submission = Submission.objects.create(user=request.user, quiz=quiz, score=0)
            
            score = sum(
                1 for answer in request.data['answers']
                if (question := Question.objects.get(pk=answer['question_id'])).correct_answer == answer['selected_option']
            )
            
            UserAnswer.objects.bulk_create([
                UserAnswer(submission=submission, question=Question.objects.get(pk=answer['question_id']), selected_option=answer['selected_option'])
                for answer in request.data['answers']
            ])
            
            submission.score = score
            submission.save()
            return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

        except (Quiz.DoesNotExist, Question.DoesNotExist):
            return Response({'error': 'Quiz or Question not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'error': 'Invalid request format'}, status=status.HTTP_400_BAD_REQUEST)

#view past submissions
class PastSubmissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_admin:
            return Response({'error': 'Admins cannot view user submissions'}, status=status.HTTP_403_FORBIDDEN)

        submissions = Submission.objects.filter(user=request.user).select_related('quiz')
        return Response({
            'user': {'email': request.user.email, 'name': request.user.name},
            'submissions': [submission.pop('user') or submission for submission in SubmissionSerializer(submissions, many=True).data]
        })
