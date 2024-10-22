from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny # type: ignore
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination # for pagination # type: ignore

class QuestionPagination(PageNumberPagination):
    page_size = 5

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = QuestionPagination # for pagination
    # permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Assign owner to the created question
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # for Custom permission
    # permission_classes = [IsOwnerOrReadOnly]

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [AllowAny]
