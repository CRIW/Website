from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, FileResponse
from .models import Show, Episode, Host, Page, Image, Index
# Create your views here.

def index(request):
	shows = Show.objects.all()
	index = Index.objects.get()
	return render(request, 'campusradio/index.html', {'index': index,'shows': shows})

def show(request, show_slug):
	show = get_object_or_404(Show,slug=show_slug)
	episodes = Episode.objects.filter(show__slug = show_slug)
	hosts = Host.objects.filter(shows=show)
	return render(request, 'campusradio/show.html', {'show': show, 'episodes': episodes, 'hosts': hosts})

def episodes(request):
	episodes = Episodes.objects.all()
	return render(request, 'campusradio/episodes.html', {'episodes':episodes})

def episode(request, episode_slug):
	episode = get_object_or_404(Episode,slug=episode_slug)
	return render(request, 'campusradio/episode_full.html', {'episode': episode})

def page(request, page_slug):
	page = get_object_or_404(Page,slug=page_slug)
	return render(request, 'campusradio/page.html', {'page': page})

def image(request, image_slug):
	image = get_object_or_404(Image,slug=image_slug)
	content_type = 'image/jpeg';
	if(image.image.path.endswith('.jpeg') or image.image.path.endswith('.jpg')):
		content_type = 'image/jpeg'
	if(image.image.path.endswith('.png')):
		content_type = 'image/png'
	return FileResponse(open(image.image.path, 'rb'), content_type=content_type)
