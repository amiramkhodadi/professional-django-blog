from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


# @register.simple_tag(name='my_tag') ==>> dar soraty k bkhahim y name delkhah braye tag dashte bashim
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/latest_post.html')
def show_latest_posts(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {
        'latest_post': latest_post
    }


@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


import markdown
from django.utils.safestring import mark_safe


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
