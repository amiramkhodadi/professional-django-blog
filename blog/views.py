from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView

from blog.models import Post


# Create your views here.
# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 1)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         # If page_number is out of range get last page of results
#         posts = paginator.page(paginator.num_pages)
#
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request, 'blog/post_list.html', {'posts': posts})

class PostListView(ListView):
    # model = Post
    queryset = Post.published.all()

    template_name = 'blog/post_list.html'
    # khate bala ro mitonim ham benevisim v ham nanevisim chon khode class base in karo bramon mikone k by deafault in template mad nazr ast
    context_object_name = "posts"
    # because the default is object_list

    paginate_by = 1


def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                              publish__day=day, slug=post)
    # try :
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post not exist')

    return render(request, 'blog/post_detail.html', {'post': posts})
