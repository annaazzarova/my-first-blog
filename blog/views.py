import urllib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
import feedparser, time, datetime
import requests


def db_update(request):
    n = 0;
    posts = Post.objects.all()
    urls = ['http://tnt-dance.ru/load/rss/', 'http://гранитанца.рф/feed/', 'http://blog.ted.com/feed/']
    for url in urls:
        d = feedparser.parse(url)
        for field in d.entries:
            post_exist = False
            post = Post()
            post.title = field.title
            post.url = field.link
            post.author = request.user
            post.text = field.summary
            created_date = field.published_parsed
            post.published_date = timezone.now()
            post.created_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', created_date)
            for p in posts:
                if p.title == post.title:
                    post_exist = True
            if not post_exist:
                n += 1
                post.save()
    print(requests.get('http://tnt-dance.ru/load/rss/').text)
    return render(request, 'blog/db_upload.html', {'n': n})


def post_list(request):
    posts_list = Post.objects.order_by('-created_date')
    paginator = Paginator(posts_list, 20)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

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