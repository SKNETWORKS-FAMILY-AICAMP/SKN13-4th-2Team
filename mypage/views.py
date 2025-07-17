from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import messages
from .models import Profile, Playlist, ListeningHistory
from .forms import ProfileForm, PlaylistForm

@login_required
def index(request):
    user_profile = request.user.profile
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    # Calculate track count for each playlist
    for playlist in playlists:
        playlist.track_count = playlist.tracks.count() # Explicitly get the count
    return render(request, 'mypage/index.html', {'user_profile': user_profile, 'playlists': playlists})

@login_required
def profile_edit(request):
    user_profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 업데이트되었습니다.") # Add success message
            return redirect('mypage:index')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'mypage/profile_edit.html', {'form': form})

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, "플레이리스트가 성공적으로 생성되었습니다.") # Add success message
            return redirect('mypage:index')
    else:
        form = PlaylistForm()
    return render(request, 'mypage/create_playlist.html', {'form': form})

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    return render(request, 'mypage/playlist_detail.html', {'playlist': playlist})

@login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, "플레이리스트가 성공적으로 업데이트되었습니다.") # Add success message
            return redirect('mypage:playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'mypage/edit_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
    if request.method == 'POST':
        playlist.delete()
        messages.success(request, "플레이리스트가 성공적으로 삭제되었습니다.") # Add success message
        return redirect('mypage:index')
    # No need to render a separate confirmation page anymore
    return redirect('mypage:playlist_detail', playlist_id=playlist_id) # Redirect back if GET request (shouldn't happen with modal)

@login_required
def listening_history(request):
    history = ListeningHistory.objects.filter(user=request.user).order_by('-listened_at')
    return render(request, 'mypage/listening_history.html', {'history': history})