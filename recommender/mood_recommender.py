import pandas as pd


# recommender/mood_recommender.py

import pandas as pd

# def assign_moods_to_movies(df):
#     """
#     Function to classify moods based on the genre, plot, or any other attribute.
#     Assumes the mood column is not already present.
#     """
#     # For now, just a simple placeholder classification
#     # You can implement the actual classification logic here
#     def mood_classifier(genre):
#         if 'Action' in genre:
#             return 'Exciting'
#         elif 'Comedy' in genre:
#             return 'Fun'
#         elif 'Romance' in genre:
#             return 'Romantic'
#         # Add more conditions based on genres or custom rules
#         return 'Any'
#
#     # Apply the mood_classifier to the Genre column or any other relevant column
#     df['Mood'] = df['Genre'].apply(mood_classifier)
#     return df

def assign_moods_to_movies(df):
    """
    Function to classify moods based on the genre column.
    Assumes the mood column is not already present.
    """
    mood_to_genre = {
        "happy": ["Comedy", "Animation", "Adventure"],
        "exciting": ["Action", "Adventure", "Science Fiction", "Superhero Action"],
        "romantic": ["Romance"],
        "historical": ["Biography"],
        "thrilling": ["Thriller", "Horror", "Science Fiction"],
        "emotional": ["Drama", "Romance", "Family"],
        "fantasy": ["Fantasy"],
        "scary": ["Horror"],
        "fun": ["Comedy", "Animation", "Adventure"]
    }

    # Reverse mapping from genre to moods for faster lookup
    genre_to_mood = {}
    for mood, genres in mood_to_genre.items():
        for genre in genres:
            genre_to_mood.setdefault(genre, []).append(mood)

    def mood_classifier(genre_list):
        """
        Classifies movies based on their genres.
        Assigns the most relevant mood(s) based on predefined mapping.
        """
        if not isinstance(genre_list, str):  # Handle missing or invalid genre data
            return "Any"

        genres = genre_list.split(", ")  # Assuming genres are stored as comma-separated values
        matched_moods = set()

        for genre in genres:
            if genre in genre_to_mood:
                matched_moods.update(genre_to_mood[genre])

        return ", ".join(matched_moods) if matched_moods else "Any"

    # Apply mood classification to each row
    df["Mood"] = df["Genre"].apply(mood_classifier)
    return df



# Function to recommend movies based on multiple filters
def recommend_movies_by_filters(mood, genre, imdb_min, release_year, director, actor, df):
    filtered_df = df.copy()

    # Apply filters based on mood
    if mood:
        filtered_df = filtered_df[filtered_df['Mood'].str.contains(mood, case=False, na=False)]

    # Apply filters based on genre
    if genre:
        filtered_df = filtered_df[filtered_df['Genre'].str.contains(genre, case=False, na=False)]

    # Apply filters based on IMDb rating
    if imdb_min:
        filtered_df = filtered_df[filtered_df['IMDb Rating'] >= float(imdb_min)]

    # Apply filters based on release year
    if release_year:
        filtered_df = filtered_df[filtered_df['Release Year'] == int(release_year)]

    # Apply filters based on director
    if director:
        filtered_df = filtered_df[filtered_df['Director'].str.contains(director, case=False, na=False)]

    # Apply filters based on actor
    if actor:
        filtered_df = filtered_df[filtered_df['Lead Star Cast'].str.contains(actor, case=False, na=False)]

    # Sort the filtered movies by IMDb rating (descending)
    return filtered_df.sort_values(by='IMDb Rating', ascending=False)
