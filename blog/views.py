from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

def post_list(request):
    try:
        posts = Post.published.all()
    except Post.DoesNotExist:
        raise Http404("No posts published yet.")
    return render(request, 'post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year,
                              publish__month=month, publish__day=day)
    return render(request, 'post/detail.html', {'post': posts})