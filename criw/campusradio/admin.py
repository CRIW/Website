from django.contrib import admin
from .models import Show, Host, Episode, Page, Image
# Register your models here.

class ShowAdmin(admin.ModelAdmin):
	fields = ['name','description','image']

class HostAdmin(admin.ModelAdmin):
	fields = ['name', 'bio', 'image', 'shows']

class EpisodeAdmin(admin.ModelAdmin):
	list_display = ('show','name','published', 'added','slug')
	list_filter = ('show',)
	date_hierachy = 'added'
	fields = ['archive_link', 'name','added', 'description','image','mp3_link','waveform_link', 'show']

class PageAdmin(admin.ModelAdmin):
	fields = ['title', 'markdown_content']

class ImageAdmin(admin.ModelAdmin):
	fields = ['name', 'image', 'description']

admin.site.register(Show, ShowAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Image, ImageAdmin)
