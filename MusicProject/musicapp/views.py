from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from http.client import HTTPResponse
from django.http import JsonResponse, request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Document
from .forms import DocumentForm
from django.contrib import messages
# from musicapp.produce_mfcc import process_input
from musicapp.predict import predict_genre
#from recommendation import recommend_songs
import numpy as np
# from .models import MusicFile
# from .forms import MusicFileForm

import librosa
import math

def process_input(audio_file, track_duration):
    
  SAMPLE_RATE = 22050
  NUM_MFCC = 13
  N_FTT=2048
  HOP_LENGTH=512
  TRACK_DURATION = track_duration # measured in seconds
  SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION
  NUM_SEGMENTS = 10

  samples_per_segment = int(SAMPLES_PER_TRACK / NUM_SEGMENTS)
  num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / HOP_LENGTH)

  signal, sample_rate = librosa.load(audio_file, sr=SAMPLE_RATE)
  
  for d in range(10):

    # calculate start and finish sample for current segment
    start = samples_per_segment * d
    finish = start + samples_per_segment

    # extract mfcc
    mfcc = librosa.feature.mfcc(y=signal[start:finish], sr=sample_rate, n_mfcc=NUM_MFCC, n_fft=N_FTT, hop_length=HOP_LENGTH)
    mfcc = mfcc.T

    return mfcc

# Create your views here.
def index(request):
    return render(request,'musicapp/index.html')
def all_songs(request):

    #Display recent songs
    if not request.user.is_anonymous :
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent = None
        recent_songs = None

    first_time = False
    #Last played song
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(id=7)

    else:
        first_time = True
        last_played_song = Song.objects.get(id=7)

    #Display all songs
    songs = Song.objects.all()

    #Display few songs on home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:5]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)
    
    # Display Hindi Songs
    songs_nepali = list(Song.objects.filter(language='Nepali').values('id'))
    sliced_ids = [each['id'] for each in songs_nepali][:5]
    indexpage_nepali_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Hindi Songs
    songs_hindi = list(Song.objects.filter(language='Hindi').values('id'))
    sliced_ids = [each['id'] for each in songs_hindi][:5]
    indexpage_hindi_songs = Song.objects.filter(id__in=sliced_ids)

    # Display English Songs
    songs_english = list(Song.objects.filter(language='English').values('id'))
    sliced_ids = [each['id'] for each in songs_english][:5]
    indexpage_english_songs = Song.objects.filter(id__in=sliced_ids)

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query)).distinct()
        context = {'all_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/all_songs.html', context)

    context = {
        'all_songs':indexpage_songs,
        'recent_songs': recent_songs,
        'nepali_songs': indexpage_nepali_songs,
        'hindi_songs':indexpage_hindi_songs,
        'english_songs':indexpage_english_songs,
        'last_played':last_played_song,
        'first_time': first_time,
        'query_search':False,
    }
    return render(request, 'musicapp/all_songs.html', context=context)

def nepali_songs(request):

    nepali_songs = Song.objects.filter(language='Nepali')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        hindi_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'nepali_songs': hindi_songs}
        return render(request, 'musicapp/nepali_songs.html', context)

    context = {'nepali_songs':nepali_songs,'last_played':last_played_song}
    return render(request, 'musicapp/nepali_songs.html',context=context)


def hindi_songs(request):

    hindi_songs = Song.objects.filter(language='Hindi')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        hindi_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'hindi_songs': hindi_songs}
        return render(request, 'musicapp/hindi_songs.html', context)

    context = {'hindi_songs':hindi_songs,'last_played':last_played_song}
    return render(request, 'musicapp/hindi_songs.html',context=context)


def english_songs(request):

    english_songs = Song.objects.filter(language='English')

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        english_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'english_songs': english_songs}
        return render(request, 'musicapp/english_songs.html', context)

    context = {'english_songs':english_songs,'last_played':last_played_song}
    return render(request, 'musicapp/english_songs.html',context=context)

@login_required(login_url='login')
def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('all_songs')

@login_required(login_url='login')
def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('recent')


# def all_songs(request):
#     songs = Song.objects.all()

#     first_time = False
#     #Last played song
#     if not request.user.is_anonymous:
#         last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
#         if last_played_list:
#             last_played_id = last_played_list[0]['song_id']
#             last_played_song = Song.objects.get(id=last_played_id)
#     else:
#         first_time = True
#         last_played_song = Song.objects.get(id=7)

    
#     # apply search filters
#     qs_singers = Song.objects.values_list('singer').all()
#     s_list = [s.split(',') for singer in qs_singers for s in singer]
#     all_singers = sorted(list(set([s.strip() for singer in s_list for s in singer])))
#     qs_languages = Song.objects.values_list('language').all()
#     all_languages = sorted(list(set([l.strip() for lang in qs_languages for l in lang])))
    
#     if len(request.GET) > 0:
#         search_query = request.GET.get('q')
#         search_singer = request.GET.get('singers') or ''
#         search_language = request.GET.get('languages') or ''
#         filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(Q(language__icontains=search_language)).filter(Q(singer__icontains=search_singer)).distinct()
#         context = {
#         'songs': filtered_songs,
#         'last_played':last_played_song,
#         'all_singers': all_singers,
#         'all_languages': all_languages,
#         'query_search': True,
#         }
#         return render(request, 'musicapp/all_songs.html', context)

#     context = {
#         'songs': songs,
#         'last_played':last_played_song,
#         'first_time':first_time,
#         'all_singers': all_singers,
#         'all_languages': all_languages,
#         'query_search' : False,
#         }
#     return render(request, 'musicapp/all_songs.html', context=context)


def recent(request):
    
    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)

    #Display recent songs
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if recent and not request.user.is_anonymous :
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs = None

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {'recent_songs': filtered_songs,'last_played':last_played_song,'query_search':True}
        return render(request, 'musicapp/recent.html', context)

    context = {'recent_songs':recent_songs,'last_played':last_played_song,'query_search':False}
    return render(request, 'musicapp/recent.html', context=context)


@login_required(login_url='login')
def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()

    # Add data to recent database
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()

    #Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=7)


    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)

    context = {'songs': songs, 'playlists': playlists, 'is_favourite': is_favourite,'last_played':last_played_song}
    return render(request, 'musicapp/detail.html', context=context)

def classify(request):
    return render(request,'musicapp/classify.html')

def mymusic(request):
    return render(request, 'musicapp/mymusic.html')

def result(request):
    return render(request, 'musicapp/result.html')

def about(request):
    return render(request, 'musicapp/about.html')

def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')
    
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs}
    return render(request, 'musicapp/favourite.html', context=context)

# def model_form_upload(request):
#     documents = Document.objects.all()
#     if request.method == 'POST':
#         if len(request.FILES) == 0:
#             messages.error(request,'Upload a file')
#             return redirect("home")

#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploadfile = request.FILES['document']
#             print(uploadfile.name)
#             print(uploadfile.size)
#             if not uploadfile.name.endswith('.wav'):
#                 messages.error(request,'Only .wav file type is allowed')
#                 return redirect("home")
#             track_duration =  30   
#             new_input_mfcc= process_input(uploadfile,track_duration)  
#             X_to_predict = new_input_mfcc[np.newaxis, ..., np.newaxis]
#             print(X_to_predict.shape) 
#             genre = predict(X_to_predict)
#             print(genre)

#             context = {'genre':genre}
#             return render(request,'musicapp/result.html',context)

#     else:
#         form = DocumentForm()

#     #return render(request,'musicapp/result.html',{'documents':documents,'form':form})
#     return render(request,'musicapp/result.html',{'documents':documents,'form':form, 'genre':genre})

def model_form_upload(request):
    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request,'Upload a file')
            return redirect("home")

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploadfile = request.FILES['document']
            print(uploadfile.name)
            print(uploadfile.size)
            
            # if not uploadfile.name.endswith('.wav'):
            #     messages.error(request,'Only .wav file type is allowed')
            #     return redirect("home")
            track_duration =  30   
            new_input_mfcc= process_input(uploadfile,track_duration)
            print(type(new_input_mfcc))
            

            X_to_predict = new_input_mfcc[np.newaxis, ..., np.newaxis]
            print(X_to_predict)
            print(X_to_predict.shape) 
            genre = predict_genre(X_to_predict)
            
            print(genre)

            context = {'genre': genre}
            return render(request, 'musicapp/result.html', context)

    else:
        print("Error")
        form = DocumentForm()
        context = {'documents': documents, 'form': form}
    return redirect("classify")

def PlaylistClassify(request,id):
    print(id)
    songs = Song.objects.filter(id=id)
    print(songs)
    to_track=''
    for song in songs:#
        to_track = song.song_file
    
    print(to_track)
    # if not uploadfile.name.endswith('.wav'):
    #     messages.error(request,'Only .wav file type is allowed')
    #     return redirect("home")
    track_duration =  30   
    new_input_mfcc= process_input(to_track,track_duration)
    print(type(new_input_mfcc))
    

    X_to_predict = new_input_mfcc[np.newaxis, ..., np.newaxis]
    print(X_to_predict)
    print(X_to_predict.shape) 
    genre = predict_genre(X_to_predict)
    
    print(genre)

    context = {'genre': genre}
    return render(request, 'musicapp/result.html', context)



    # def classify_genre(request):
    #     if request.method == 'POST':
    #         form = MusicFileForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             # Save the file to the database
    #             music_file = form.save()
    #             # Perform genre classification on the file
    #             genre = classify_genre(music_file.file.path)
    #             # Update the MusicFile object with the genre
    #             music_file.genre = genre
    #             music_file.save()
    #             # Return the classification result
    #             return render(request, 'classify.html', {'music_file': music_file})
    #     else:
    #         form = MusicFileForm()
    #     return render(request, 'index.html', {'form': form})

@login_required(login_url='login')
def recommend(request):
    # Get the user's recent songs
    recent_songs = User.objects.filter(recent__user=request.user)

    # Pass the recent songs to the recommendation algorithm
    recommended_songs = recommend_songs(recent_songs)

    context = {'recommended_songs': recommended_songs}
    return render(request, 'musicapp/recommend.html', context=context)