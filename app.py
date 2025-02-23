from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import random
import pandas as pd
from recommender.mood_recommender import recommend_movies_by_filters, assign_moods_to_movies

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Load movie dataset
df = pd.read_csv("data/movies.csv")
df = assign_moods_to_movies(df)

# ---------- Unified Home Page ----------
@app.route('/')
def home():
    return render_template('home.html')

# ---------- Mood-Based Movie Recommender Routes ----------
@app.route('/mood-recommender')
def mood_recommender():
    genres = df['Genre'].unique()
    moods = df['Mood'].unique()
    actors = df['Lead Star Cast'].unique()
    return render_template('index.html', genres=genres, moods=moods, actors=actors)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_mood = request.form.get('mood', '')
    user_genre = request.form.get('genre', '')
    imdb_min = request.form.get('imdb_min', '')
    release_year = request.form.get('release_year', '')
    director = request.form.get('director', '')
    actor = request.form.get('actor', '')

    recommended_movies = recommend_movies_by_filters(
        user_mood, user_genre, imdb_min, release_year, director, actor, df
    )
    movies_list = recommended_movies[['Title', 'Mood', 'IMDb Rating']].to_dict(orient='records')
    return jsonify(movies_list)

# ---------- Movie Trivia Routes ----------
def generate_trivia_question(movies_df):
    """Generate a trivia question with multiple choice options."""
    movie = movies_df.sample(1).iloc[0]
    question_type = random.choice(['year', 'director', 'actor', 'genre'])

    if question_type == 'year':
        question = f"In which year was the movie '{movie['Title']}' released?"
        correct_answer = str(movie['Release Year'])
        options = list(set([correct_answer] + [str(y) for y in random.sample(movies_df['Release Year'].dropna().astype(int).tolist(), 3)]))
    elif question_type == 'director':
        question = f"Who directed the movie '{movie['Title']}'?"
        correct_answer = movie['Director']
        options = list(set([correct_answer] + random.sample(movies_df['Director'].dropna().tolist(), 3)))
    elif question_type == 'actor':
        question = f"Who was the lead actor in '{movie['Title']}'?"
        correct_answer = movie['Lead Star Cast']
        options = list(set([correct_answer] + random.sample(movies_df['Lead Star Cast'].dropna().tolist(), 3)))
    elif question_type == 'genre':
        question = f"What genre is the movie '{movie['Title']}'?"
        correct_answer = movie['Genre']
        options = list(set([correct_answer] + random.sample(movies_df['Genre'].dropna().tolist(), 3)))

    random.shuffle(options)
    return question, correct_answer, options

@app.route('/trivia', methods=['GET', 'POST'])
def trivia():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = session.get('correct_answer')

        if user_answer and correct_answer:
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            message = "✅ Correct!" if is_correct else f"❌ Incorrect! The correct answer was: {correct_answer}."
            return render_template('trivia.html', question=session['question'], options=session['options'], message=message)

    if 'question' not in session:
        question, correct_answer, options = generate_trivia_question(df)
        session['question'] = question
        session['correct_answer'] = correct_answer
        session['options'] = options

    return render_template('trivia.html', question=session['question'], options=session['options'], message=None)

@app.route('/next-trivia', methods=['POST'])
def next_trivia():
    """Generate a new trivia question when the user presses 'Next Question'."""
    question, correct_answer, options = generate_trivia_question(df)
    session['question'] = question
    session['correct_answer'] = correct_answer
    session['options'] = options
    return redirect(url_for('trivia'))

@app.route('/restart-trivia', methods=['POST'])
def restart_trivia():
    """Restart the trivia game."""
    session.clear()
    return redirect(url_for('trivia'))

if __name__ == '__main__':
    app.run(debug=True)
