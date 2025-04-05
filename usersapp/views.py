from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from adminapp.models import Quiz, Question
from adminapp.serializers import QuizSerializer
from .models import Submission, UserAnswer
from .serializers import SubmissionSerializer

class ActiveQuizView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        quizzes = Quiz.objects.filter(is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

class SubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        submissions = Submission.objects.filter(user=request.user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.is_admin:
            return Response({'error': 'Admins cannot submit quizzes'}, status=status.HTTP_403_FORBIDDEN)
        
        quiz = Quiz.objects.get(pk=request.data['quiz_id'])
        answers = request.data['answers']  # Format: [{'question_id': 1, 'selected_option': 2}, ...]
        
        # Calculate score
        score = 0
        submission = Submission.objects.create(user=request.user, quiz=quiz, score=0)
        
        for answer in answers:
            question = Question.objects.get(pk=answer['question_id'])
            is_correct = question.correct_option == answer['selected_option']
            if is_correct:
                score += 1
            UserAnswer.objects.create(
                submission=submission,
                question=question,
                selected_option=answer['selected_option']
            )
        
        submission.score = score
        submission.save()
        return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)