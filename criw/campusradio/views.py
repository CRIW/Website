from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Show
# Create your views here.

def index(request):
	shows = Show.objects.all()
	return render(request, 'campusradio/index.html', {'shows': shows})

def show(request, show_slug):
	show = get_object_or_404(Show,slug=show_slug)
	return render(request, 'campusradio/show.html', {'show': show})

def episodes(request):
	episodes = Episodes.objects.all()
	return render(request, 'campusradio/episodes.html', {'episodes':episodes})

def episode(request, episode_slug):
	show = get_object_or_404(Episode,slug=episode_slug)
	return render(request, 'campusradio/episode.html', {'episode': episode})
