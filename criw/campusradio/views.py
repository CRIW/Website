from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, FileResponse
from .models import Show, Episode, Host, Page, Image, Index, Article
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

def news(request, archive=False):
	items = []
	episodes = Episode.objects.all()
	articles = Article.objects.all()
	if archive == False:
		i = 3 #Number of articles to show
	else:
		i = -1#Show all articles and episodes

	episode_num = 0
	article_num = 0

	while i != 0:
		if(episode_num >= len(episodes)) and (article_num >= len(articles)):
			break
		if(episode_num >= len(episodes)):
			items += [{'type': 'article', 'article': articles[article_num]}]
			article_num = article_num + 1
			i = i - 1
			continue;
		if(article_num >= len(articles)):
			items += [{'type': 'episode', 'episode': episodes[episode_num]}]
			episode_num = episode_num + 1
			i = i - 1
			continue
		if(articles[article_num].published > episodes[episode_num].added):
			items += [{'type': 'article', 'article': articles[article_num]}]
			last_date = articles[article_num].published
			article_num = article_num + 1
			i = i - 1
			continue
		else:
			items += [{'type': 'episode', 'episode': episodes[episode_num]}]
			last_date = episodes[episode_num].added
			episode_num = episode_num + 1
			i = i - 1
			continue
	print(items)
	return render(request, 'campusradio/news.html', {'archive': archive, 'items': items})

def article(request, article_slug):
	article = get_object_or_404(Article,slug=article_slug)
	return render(request, 'campusradio/article.html', {'article': article})

def team(request):
	hosts = Host.objects.all()
	index = Index.objects.get()
	return render(request, 'campusradio/team.html', {'hosts': hosts, 'index': index})

def host(request, team_slug):
	host = get_object_or_404(Host, slug=team_slug)
	return render(request, 'campusradio/host.html', {'host': host})
