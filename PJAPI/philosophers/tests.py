from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Philosopher
from .views import analyze_user_input, match_philosopher

# Create your tests here.

class PhilosopherModelTestCase(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.philosopher = Philosopher.objects.create(
            name='Plato',
            bio='Plato was an ancient Greek philosopher who was a student of Socrates and the teacher of Aristotle.',
            school_of_thought='Platonism',
            core_ideas=['Idealism', 'Theory of Forms'],
            tone='Neutral',
            works=['The Republic', 'Symposium'],
            era='Ancient',
            quotes=['"Courage is knowing what not to fear."'],
        )

    def test_philosopher_exists(self):
        philosopher = Philosopher.objects.get(name='Plato')
        self.assertIsNotNone(philosopher)

    def test_analyze_user_input_neutral(self):
        user_text = 'What is the meaning of life?'
        keywords, sentiment = analyze_user_input(user_text)
        self.assertEqual(keywords, ['What', 'is', 'the', 'meaning', 'of', 'life?'])
        self.assertEqual(sentiment, 'Neutral')

    def test_philosopher_matching(self):
        user_text = 'What is the meaning of life?'
        matched_philosopher = match_philosopher(user_text)
        self.assertEqual(matched_philosopher, Philosopher.objects.get(name='Plato'))

    def test_user_input_view(self):
        response = self.client.post(reverse('user_input'), {'user_text': 'What is the meaning of life?'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Plato')

    def test_analyze_user_input_negative(self):
        user_text = 'I hate everything.'
        keywords, sentiment = analyze_user_input(user_text)
        self.assertEqual(keywords, ['I', 'hate', 'everything.'])
        self.assertEqual(sentiment, 'Negative')

    def test_analyze_user_input_positive(self):
        user_text = 'I love everything.'
        keywords, sentiment = analyze_user_input(user_text)
        self.assertEqual(keywords, ['I', 'love', 'everything.'])
        self.assertEqual(sentiment, 'Positive')
