from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from blog.models import Post
# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request  , 'blog/post_list.html',{'posts' : posts})


def post_detail(request , id):
    posts = get_object_or_404(Post , id = id , status = Post.Status.PUBLISHED)
    # try :
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post not exist')

    return render(request , 'blog/post_detail.html' , {'post' : posts })
