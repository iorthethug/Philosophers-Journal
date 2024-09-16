from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from django.db.models import Q
from .models import Philosopher, UserInput
from .serializers import PhilosopherSerializer
from transformers import AutoTokenizer

nltk.download('vader_lexicon')
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2') #why this one

def analyze_user_input(user_text): #2 returns keywords and sentiment maybe the transformer here? NLKT
    #keywords = user_text.split() # simple tokenization UPGRADE LATER
    keywords = tokenizer.tokenize(user_text) #upgraded tokenization

    # sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(user_text)['compound']

    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return keywords, sentiment

def match_philosopher(user_text): #3 returns matched philosopher
    keywords, sentiment = analyze_user_input(user_text)

    # search for philosophers that match the keywords or sentiment
    matched_philosopher = Philosopher.objects.filter(
        Q(core_ideas__icontains=keywords[0]) | Q(tone=sentiment)
    )
    # only returning the first match for now
    return matched_philosopher.first()

def user_input_view(request): #1 returns the response
    if request.method == 'POST':
        user_text = request.POST.get('user_text')
        matched_philosopher = match_philosopher(user_text)

        # save user input and match to database for further improvement
        user_input = UserInput(user_text=user_text, matched_philosopher=matched_philosopher)
        user_input.save()

        return render(request, 'result.html', {'philosopher': matched_philosopher})
    return render(request, 'input_form.html')