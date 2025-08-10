from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post


# Create your views here.
def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/post_list.html', {'posts': posts, 'tag': tag})


# class PostListView(ListView):
#     # model = Post
#     queryset = Post.published.all()
#
#     template_name = 'blog/post_list.html'
#     # khate bala ro mitonim ham benevisim v ham nanevisim chon khode class base in karo bramon mikone k by deafault in template mad nazr ast
#     context_object_name = "posts"
#     # because the default is object_list
#
#     paginate_by = 1


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year=year, publish__month=month,
                             publish__day=day, slug=post)
    # try :
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('Post not exist')

    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'similar_post': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # khate zir adrress ro b sorat kamel b hamrah damane tarif mikone
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/share.html', {'form': form, 'post': post, 'sent': sent})


@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/comment.html', {'form': form, 'post': post, 'comment': comment})
