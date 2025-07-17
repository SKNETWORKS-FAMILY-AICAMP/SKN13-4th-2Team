from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'home/index.html')

def music_player_popup(request):
    return render(request, 'music_player_popup.html')