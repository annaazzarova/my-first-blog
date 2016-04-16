import urllib

from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
import feedparser, time, datetime


def db_update(request):
    d = feedparser.parse('http://tnt-dance.ru/load/rss/')
    for field in d.entries:
        post = Post()
        post.title = field.title
        post.url = field.link
        post.author = request.user
        post.text = field.summary
        created_date = field.published_parsed
        post.published_date = timezone.now()
        post.created_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', created_date)
        post.save()
    d = feedparser.parse('http://гранитанца.рф/feed/')
    for field in d['entries']:
        post = Post()
        post.title = field.title
        post.url = field.link
        post.text = field.summary
        post.author = request.user
        created_date = field.published_parsed
        post.published_date = timezone.now()
        post.created_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', created_date)
        post.save()
    d = feedparser.parse('http://blog.ted.com/feed/')
    for field in d['entries']:
        post = Post()
        post.title = field.title
        post.url = field.link
        post.text = field.summary
        post.author = request.user
        created_date = field.published_parsed
        post.published_date = timezone.now()
        post.created_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', created_date)
        post.save()
    return HttpResponse("ok")


def post_list(request):
    posts = Post.objects.order_by('created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})