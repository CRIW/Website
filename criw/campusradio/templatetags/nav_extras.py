from django import template
from campusradio.models import Show, Page
register = template.Library()

@register.inclusion_tag('campusradio/nav.html')
def show_nav():
    shows = Show.objects.all()
    pages = Page.objects.all()
    return {'shows': shows, 'pages': pages}
