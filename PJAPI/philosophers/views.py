from importlib import util
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from django.db.models import Q
from .models import Philosopher, UserInput
from .serializers import PhilosopherSerializer
from sentence_transformers import SentenceTransformer, SimilarityFunction

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


nltk.download('vader_lexicon')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') #lightweight and efficient, can use BERT instead but its heavier
model.similarity_fn_name = SimilarityFunction.COSINE

def analyze_user_input(user_text): # returns keywords, sentiment and embeddings
    #keywords = user_text.split() # simple tokenization
    keywords = model.tokenizer.tokenize(user_text) #upgraded tokenization

    embeddings = model.encode(user_text)

    # sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(user_text)['compound']

    if sentiment_score > 0:
        sentiment = 'Positive'
    elif sentiment_score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return keywords, sentiment, embeddings

def match_philosopher(user_text): # returns matched philosopher based on keywords or sentiment
    keywords, sentiment, user_embeddings = analyze_user_input(user_text)

    # search for philosophers that match the keywords or sentiment
    matched_philosopher = Philosopher.objects.filter(
        Q(core_ideas__icontains=keywords[0]) | Q(tone=sentiment)
    )
    # only returning the first match for now
    return matched_philosopher.first()

def match_philosopher_transformer(user_text): # returns matched philosopher based on transformer embeddings
    keywords, sentiment, user_embeddings = analyze_user_input(user_text)

    philosophers = Philosopher.objects.all()

    highest_similarity = 0
    matched_philosopher = None

    for philosopher in philosophers:
        philosopher_bio = philosopher.bio
        philosopher_embeddings = model.encode(philosopher_bio)# only using bio for now
        # calculate cosine similarity between user input and philosopher bio
        similarity_scores = model.similarity(user_embeddings, philosopher_embeddings)

        # Get the maximum similarity score
        max_similarity_score = similarity_scores.max().item()
        logging.info(f"Similarity score with {philosopher.name}: {max_similarity_score}")
        
        if max_similarity_score > highest_similarity:
            highest_similarity = max_similarity_score
            matched_philosopher = philosopher

    logging.info(f"Highest similarity score: {highest_similarity} with philosopher: {matched_philosopher.name}")
    
    return matched_philosopher

def user_input_view(request): # returns the result of the user input
    if request.method == 'POST':
        user_text = request.POST.get('user_text')
        matched_philosopher = match_philosopher_transformer(user_text)

        # save user input and match to database for further improvement
        user_input = UserInput(user_text=user_text, matched_philosopher=matched_philosopher)
        user_input.save()

        return render(request, 'result.html', {'philosopher': matched_philosopher})
    return render(request, 'input_form.html')