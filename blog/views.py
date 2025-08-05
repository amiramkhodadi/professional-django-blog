from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Post


# Create your views here.
def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                              publish__day=day, slug=post)
    # try :
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post not exist')

    return render(request, 'blog/post_detail.html', {'post': posts})
