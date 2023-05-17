from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    Language_Choice = (
        ('Nepali', 'Nepali'),
        ('Hindi', 'Hindi'),
        ('English', 'English'),
    )

    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=Language_Choice, default='Hindi')
    song_img = models.FileField()
    year = models.IntegerField()
    singer = models.CharField(max_length=200)
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Document(models.Model):
    file = models.FileField(upload_to='file/')


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
