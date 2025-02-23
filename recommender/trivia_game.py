# recommender/trivia_game.py

import random
import pandas as pd

import random

def generate_trivia_question(movies_df):
    """Generates a random trivia question and multiple choice options."""
    # Choose a random movie
    movie = movies_df.sample(1).iloc[0]

    # Randomly choose what type of trivia question to ask
    question_type = random.choice(['year', 'director', 'actor', 'genre'])

    if question_type == 'year':
        question = f"In which year was the movie '{movie['Title']}' released?"
        correct_answer = movie['Release Year']
        # Filter for movies with a similar release year for incorrect answers
        options = [correct_answer]
        while len(options) < 4:
            random_movie = movies_df.sample(1).iloc[0]
            if random_movie['Release Year'] != correct_answer and random_movie['Release Year'] not in options:
                options.append(random_movie['Release Year'])

    elif question_type == 'director':
        question = f"Who directed the movie '{movie['Title']}'?"
        correct_answer = movie['Director']
        # Filter for movies with different directors
        options = [correct_answer]
        while len(options) < 4:
            random_movie = movies_df.sample(1).iloc[0]
            if random_movie['Director'] != correct_answer and random_movie['Director'] not in options:
                options.append(random_movie['Director'])

    elif question_type == 'actor':
        question = f"Who was the lead actor in '{movie['Title']}'?"
        correct_answer = movie['Lead Star Cast']
        # Filter for movies with different lead actors
        options = [correct_answer]
        while len(options) < 4:
            random_movie = movies_df.sample(1).iloc[0]
            if random_movie['Lead Star Cast'] != correct_answer and random_movie['Lead Star Cast'] not in options:
                options.append(random_movie['Lead Star Cast'])

    elif question_type == 'genre':
        question = f"What genre is the movie '{movie['Title']}'?"
        correct_answer = movie['Genre']
        # Filter for movies with different genres
        options = [correct_answer]
        while len(options) < 4:
            random_movie = movies_df.sample(1).iloc[0]
            if random_movie['Genre'] != correct_answer and random_movie['Genre'] not in options:
                options.append(random_movie['Genre'])

    # Shuffle options so that the correct answer is not always first
    random.shuffle(options)

    return question, correct_answer, options
