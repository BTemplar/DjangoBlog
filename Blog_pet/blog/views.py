from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404

def post_list(request):
    try:
        posts = Post.published.all()
    except Post.DoesNotExist:
        raise Http404("No posts published yet.")
    return render(request, 'post/list.html', {'posts': posts})

def post_detail(request, id):
    posts = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'post/detail.html', {'post': posts})