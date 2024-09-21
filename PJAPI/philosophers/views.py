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
from transformers import pipeline

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


nltk.download('vader_lexicon')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') #lightweight and efficient, can use BERT instead but its heavier
model.similarity_fn_name = SimilarityFunction.COSINE

# Initialize sentiment analysis pipeline from Hugging Face's transformers
sentiment_pipeline = pipeline('text-classification')

sia = SentimentIntensityAnalyzer()

def analyze_user_input(user_text): # returns keywords, sentiment and embeddings

    keywords = model.tokenizer.tokenize(user_text) #upgraded tokenization

    embeddings = model.encode(user_text)
    
    # VADER sentiment analysis
    sentiment_score_vader = sia.polarity_scores(user_text)['compound']
    sentiment_label_vader = 'Positive' if sentiment_score_vader > 0.33 else 'Negative' if sentiment_score_vader < -0.33 else 'Neutral'
    
    logging.info(f"Sentiment score with VADER: {sentiment_score_vader} and label: {sentiment_label_vader}")
    
    sentiment = sentiment_label_vader
    
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

        philosopher_tone_string = ' '.join(philosopher.tone) if isinstance(philosopher.tone, list) else philosopher.tone

        philosopher_embeddings_bio = model.encode(philosopher.bio)
        philosopher_embeddings_quotes = model.encode(philosopher.quotes)

        similarity_scores_bio = model.similarity(user_embeddings, philosopher_embeddings_bio)
        similarity_scores_quotes = model.similarity(user_embeddings, philosopher_embeddings_quotes)

        max_similarity_score_bio = similarity_scores_bio.max().item()
        max_similarity_score_quotes = similarity_scores_quotes.max().item()

        sentiment_match_score = 1 if philosopher_tone_string == sentiment else 0 # bonus score if sentiment matches

        # Similarity scores and sentiment match score
        composite_score = (0.9 * (max_similarity_score_bio + max_similarity_score_quotes)) + (0.2 * sentiment_match_score)

        logging.info(f"Scoring with {philosopher.name}: comp={composite_score}, bio={max_similarity_score_bio}, quotes={max_similarity_score_quotes}, sentiment={sentiment_match_score}")
        
        if composite_score > highest_similarity:
            highest_similarity = composite_score
            matched_philosopher = philosopher

    logging.info(f"Highest similarity score: {highest_similarity} with philosopher: {matched_philosopher.name}")
    
    return matched_philosopher

def user_input_view(request): # returns the result of the user input
    if request.method == 'POST':
        user_text = request.POST.get('user_text')
        matched_philosopher = match_philosopher_transformer(user_text)

        # save user input and match to database for further improvement
        user_input = UserInput(user_text=user_text, matched_philosopher=matched_philosopher)
        user_input.save() #not sure where its saved??

        return render(request, 'result.html', {'philosopher': matched_philosopher})
    return render(request, 'input_form.html')