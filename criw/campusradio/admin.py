from django.contrib import admin
from .models import Show, Host, Episode, Page, Image, Index
# Register your models here.

class ShowAdmin(admin.ModelAdmin):
	fields = ['name','slot','description','image']

class HostAdmin(admin.ModelAdmin):
	fields = ['name', 'bio', 'image', 'shows']

class EpisodeAdmin(admin.ModelAdmin):
	list_display = ('show','name','published', 'added','slug')
	list_filter = ('show',)
	date_hierachy = 'added'
	fields = ['archive_link', 'show', 'name','added', 'description','image','mp3_link','waveform_link']

class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'markdown_content']

class ImageAdmin(admin.ModelAdmin):
	list_display = ('name','slug')
	fields = ['name', 'image', 'description']

admin.site.register(Show, ShowAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Index)
