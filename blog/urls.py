from django.urls import path

from blog import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # path('', views.post_list, name='post_list'),
    path('', views.post_list, name='post_list'),
    path('share/<int:post_id>', views.post_share, name='share_post'),
    path(
        'comment/<int:post_id>/', views.comment_post, name='comment_post'
    ),
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.search_post, name='search_post'),
]
