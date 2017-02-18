from django import template
register = template.Library()

@register.inclusion_tag('campusradio/episode.html')
def episode(episode):
    return {'episode': episode}
