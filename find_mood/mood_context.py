import pandas as pd
from transformers import pipeline

def main():
    # Load GPT-2 model for text generation
    print("Loading GPT-2 model...")
    generator = pipeline("text-generation", model="gpt2")

    # Function to analyze movie synopsis and determine mood using GPT-2
    def get_mood_from_synopsis(synopsis):
        prompt = f"Based on this movie synopsis, categorize its mood as happy, thrilling, romantic, scary, emotional, exciting, fun, or fantastical: {synopsis} \nMood:"
        response = generator(prompt, max_length=50, num_return_sequences=1)
        mood = response[0]["generated_text"].split("Mood:")[-1].strip().split("\n")[0]  # Extract mood
        return mood.lower()

    # Function to assign moods to all movies in the dataset
    def assign_moods_to_movies(df):
        print("Assigning moods to movies...")
        df["Mood"] = df["Synopsis"].apply(get_mood_from_synopsis)  # Apply GPT-2 mood classification
        return df

    # Function to recommend movies based on mood
    def recommend_movies_by_mood_gpt(mood, df):
        return df[df["Mood"].str.contains(mood, case=False, na=False)].sort_values(by="IMDb Rating", ascending=False)

    # Load movie dataset (Replace 'movies_metadata.csv' with your actual file)
    print("Loading movie dataset...")
    df = pd.read_csv("movies_metadata.csv")

    # Assign moods to movies using GPT-2
    df = assign_moods_to_movies(df)

    # Example usage: Recommend movies for a given mood
    user_mood = input("Enter a mood (e.g., thrilling, happy, romantic): ").strip().lower()
    recommended_movies = recommend_movies_by_mood_gpt(user_mood, df)

    # Display recommendations
    print("\nRecommended Movies:")
    print(recommended_movies[["Title", "Mood", "IMDb Rating"]])

    # Save updated dataset with moods
    df.to_csv("moods.csv", index=False)
    print("\nMoods assigned and saved to moods.csv")

if __name__ == "__main__":
    main()
