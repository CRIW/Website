from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
import os
import markdown
from urllib.request import urlopen
import json
from dateutil import parser


# Create your models here.

def get_show_image_path(instance, filename):
	return os.path.join('uploads', 'shows', str(instance.slug), filename)

def get_host_image_path(instance, filename):
	return os.path.join('uploads', 'host', str(instance.slug), filename)

def get_episode_image_path(instance, filename):
	return os.path.join('uploads', 'episode', str(instance.slug), filename)

def get_image_path(instance, filename):
	return os.path.join('uploads', 'images', str(instance.slug), filename)

def get_index_path(instance, filename):
	return os.path.join('uploads', 'index', filename)

#A radioshow
class Show(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	description = models.TextField(blank=True)
	slot = models.CharField(max_length=400, blank=True)
	image = models.ImageField(upload_to=get_show_image_path, blank=True, null=True)
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Show, self).save(*args, **kwargs)
		if(self.image.width > 1024): #resize image if excessively large
			try:
				from PIL import Image
				im = Image.open(self.image.path)
				size = (1024, self.image.height * (1024 / self.image.width))
				im.thumbnail(size, Image.ANTIALIAS)
				im.save(self.image.path)
			except:
				"Nothing"
	def get_absolute_url(self):
		return reverse('show', kwargs={'show_slug':self.slug})

#Someone who hosts a radioshow
class Host(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	bio = models.TextField(blank=True)
	image = models.ImageField(upload_to=get_host_image_path, blank=True, null=True)
	shows = models.ManyToManyField(Show)
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Host, self).save(*args, **kwargs)
		if(self.image.width > 512): #resize image if excessively large
			try:
				from PIL import Image
				im = Image.open(self.image.path)
				size = (512, self.image.height * (512 / self.image.width))
				im.thumbnail(size, Image.ANTIALIAS)
				im.save(self.image.path)
			except:
				"Nothing"
#An episode of a show
class Episode(models.Model):
	name = models.CharField(max_length=200, blank=True)
	published = models.DateTimeField(auto_now_add=True)
	added = models.DateTimeField(blank=True, null=True)
	slug = models.SlugField()
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to=get_host_image_path, blank=True, null=True)
	archive_link = models.URLField()
	mp3_link = models.CharField(max_length=200,blank=True)
	waveform_link = models.CharField(max_length=200,blank=True)
	show = models.ForeignKey(
        'Show',
        on_delete=models.CASCADE,
    )
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		metadata = None
		if (not self.added) or (not self.mp3_link) or (not self.description) or (not self.name) or (not self.waveform_link):
			metadata = get_archive_metadata(self.archive_link)
		if not self.mp3_link:
			self.mp3_link = metadata['mp3_link']
		if not self.description:
			self.description = metadata['metadata']['description']
		if not self.name:
			self.name = metadata['metadata']['title']
		if not self.added:
			self.added = parser.parse(metadata['metadata']['addeddate'])
		if not self.waveform_link:
			self.waveform_link = metadata['waveform_link']
		if not self.id:
			other_episodes = Episode.objects.all()
			i = 2
			self.slug = slugify(self.name)
			while other_episodes.filter(slug=self.slug).count() > 0:
				self.slug = slugify(self.name + "-" + str(i))
				i = i + 1
		super(Episode, self).save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('episode', kwargs={'episode_slug':self.slug})
	class Meta:
		ordering = ('-added',);

#Fetches the mp3 download url from the internet archive link
def get_archive_mp3_url(archive_url):
	descriptor = archive_url[archive_url.rindex('/')+1:]
	metadata_url = 'https://archive.org/metadata/' + descriptor
	content = urlopen(metadata_url).read().decode('utf-8')
	metadata = json.loads(content + "")
	for f in metadata['files']:
		if("MP3" in f['format']):
			return 'https://archive.org/download/' + descriptor + '/' + f['name']
	return None

#Fetches the description from the internet archive link
def get_archive_description(archive_url):
	descriptor = archive_url[archive_url.rindex('/')+1:]
	metadata_url = 'https://archive.org/metadata/' + descriptor
	content = urlopen(metadata_url).read().decode('utf-8')
	metadata = json.loads(content + "")
	try:
		return metadata['metadata']['description']
	except:
		return None

#Fetches metadata from the internet archive link
def get_archive_metadata(archive_url):
	descriptor = archive_url[archive_url.rindex('/')+1:]
	metadata_url = 'https://archive.org/metadata/' + descriptor
	content = urlopen(metadata_url).read().decode('utf-8')
	metadata = json.loads(content + "")
	try:
		for f in metadata['files']:
			if("MP3" in f['format']):
				metadata['mp3_link'] = 'https://archive.org/download/' + descriptor + '/' + f['name']
			if("PNG" in f['format']):
				metadata['waveform_link'] = 'https://archive.org/download/' + descriptor + '/' + f['name']
		return metadata
	except:
		return None

#Class for independent pages
class Page(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	sort = models.SmallIntegerField(default=0)
	markdown_content = models.TextField()
	html_content = models.TextField()
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		self.html_content = markdown.markdown(self.markdown_content)
		super(Page, self).save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('page', kwargs={'page_slug':self.slug})
	class Meta:
		ordering = ('sort',);


#Image class for embedding images into pages
class Image(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	description = models.TextField(blank=True)
	published = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Image, self).save(*args, **kwargs)
		if(self.image.width > 2048): #resize image if excessively large
			try:
				from PIL import Image as img
				im = img.open(self.image.path)
				size = (2048, self.image.height * (2048 / self.image.width))
				im.thumbnail(size, img.ANTIALIAS)
				im.save(self.image.path)
			except:
				"Nothing"

class Index(models.Model):
	markdown_content = models.TextField()
	html_content = models.TextField(blank=True)
	image = models.ImageField(upload_to=get_index_path, blank=True, null=True)
	def save(self, *args, **kwargs):
		self.html_content = markdown.markdown(self.markdown_content)
		super(Index, self).save(*args, **kwargs)
		if(self.image and self.image.width > 1024): #resize image if excessively large
			try:
				from PIL import Image as img
				im = img.open(self.image.path)
				size = (1024, self.image.height * (1024 / self.image.width))
				im.thumbnail(size, img.ANTIALIAS)
				im.save(self.image.path)
			except:
				"Nothing"

#Class for independent pages
class Article(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	markdown_content = models.TextField()
	html_content = models.TextField()
	published = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		self.html_content = markdown.markdown(self.markdown_content)
		super(Article, self).save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('article', kwargs={'article_slug':self.slug})
	class Meta:
		ordering = ('-published',);
