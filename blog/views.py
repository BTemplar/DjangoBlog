from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
    """Generic class-based view listing a queryset."""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'

def post_list(request):
    try:
        posts_list = Post.published.all()
        paginator = Paginator(posts_list, 3)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    except Post.DoesNotExist:
        raise Http404("No posts published yet.")
    return render(request, 'post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                              publish__month=month, publish__day=day)
    return render(request, 'post/detail.html', {'post': posts})

def post_share(request, post_id):
    """Share a post via email."""
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {'post': post, 'form': form, 'sent': sent})
