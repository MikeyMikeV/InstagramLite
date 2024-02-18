from django import template
from ..models import Profile

register = template.Library()

@register.filter(name='has_liked')
def has_liked(profile, obj):
    # post = Post.objects.get(pk = pid)
    return obj.likes.contains(profile)

def find_profile(profile_id):
    return Profile.objects.get(profile_id)