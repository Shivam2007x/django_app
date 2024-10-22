import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

#for resful testing 
from rest_framework.test import APITestCase # type: ignore
from django.urls import reverse
from rest_framework import status # type: ignore
from django.contrib.auth.models import User
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self): #`test_was_published_recently_with_future_question` method creates a Question instance with a pub_date in the future
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self): #`test_no_questions` method creates a response object by making a GET request to the index view    
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index')) #`test_no_questions` method creates a response object by making a GET request to the index view
        self.assertEqual(response.status_code, 200) # Check the response status code
        self.assertContains(response, "No polls are available.") # Check the response content
        self.assertQuerySetEqual(response.context['page_obj'], []) # Check the context


class QuestionAPITests(APITestCase):

    def setUp(self): #`setUp` method is run before each test case method
        self.user = User.objects.create_user(username='testuser', password='testpass') # Create a user
        self.client.login(username='testuser', password='testpass') # Log the user in

    def test_create_question(self): #`test_create_question` method creates a new question using the API
        url = reverse('question-list')  # Assuming default router names
        data = {'question_text': 'New Question', 'pub_date': '2024-10-18T12:00:00Z'} # Data to create a new question
        response = self.client.post(url, data, format='json') # Send a POST request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Check the response status code
        self.assertEqual(Question.objects.count(), 1) # Check the number of questions
        self.assertEqual(Question.objects.get().question_text, 'New Question') # Check the question text