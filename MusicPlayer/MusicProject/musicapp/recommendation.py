# recommendation.py

from musicapp.models import Song, UserPreference

def recommend_songs(user):
    # Retrieve user's preferred genres
    user_preferences = UserPreference.objects.filter(user=user)
    preferred_genres = [preference.genre for preference in user_preferences]

    # Find songs that match the preferred genres
    recommended_songs = Song.objects.filter(genre__in=preferred_genres)

    return recommended_songs
