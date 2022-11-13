import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from press.models import Category, Post, CoolUser
from django.db.models import Count

def home(request):
    now = datetime.datetime.now()
    msg = 'Welcome to Coolpres'
    categories = Category.objects.annotate(num_posts=Count('post')).values('label', 'num_posts')
    user = request.user
    li_cats = [f'<li> Category: {cat["label"]} Posts: {cat["num_posts"]}</li>' for cat in categories]
    cats_ul = f'<ul>{"".join(li_cats)}</ul>'

    posts = Post.objects.order_by('-creation_date')[:5]
    li_posts = [f'<li>{post}</li>' for post in posts]
    posts_ul = f'<ul>{"".join(li_posts)}</ul>'

    html = f"<html><head><title>{msg}</title><body><h1>{msg}</h1><h2>Number of posts per category:</h2><section>{cats_ul}</section><h2>Latest 5 posts created:</h2><section>{posts_ul}</section></body></html>"
    return HttpResponse(html)

def authors(request):
    authors = CoolUser.objects.all().values('user__first_name', 'user__last_name', 'user__username', 'github_profile','gh_repositories')
    li_authors = [f'<li><b>First name:</b>{author["user__first_name"]} <b>Last name:</b>{author["user__last_name"]} <b>Username:</b> {author["user__username"]} <b>Github profile:</b> {author["github_profile"]} <b>Repositories:</b> {author["gh_repositories"]}</li>' for author in authors]
    authors_ul = f'<ul>{"".join(li_authors)}</ul>'

    html = f"<html><head><body><h2>Authors:</h2><section>{authors_ul}</section></body></html>"
    return HttpResponse(html)

def render_a_post(post):
    return f'<div style="margin: 20px;padding-bottom: 10px;"><h2>{post.title}</h2><p style="color: gray;">{post.body}</p><p>{post.author.user.username}</p></div>'


def posts_list(request):
    objects = Post.objects.all()[:20]
    return render(request, 'posts_list.html', {'posts_list': objects})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts_detail.html', {'post_obj': post})