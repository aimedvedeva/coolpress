import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from press.forms import CommentForm, PostForm, CategoryForm
from press.models import Category, Post, Comment, CoolUser
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
    authors = CoolUser.objects.all().values('user__first_name', 'user__last_name', 'user__username', 'github_profile', 'gh_repositories')
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
    data = request.POST or {'votes': 10}
    form = CommentForm(data)

    comments = post.comment_set.order_by('-creation_date')
    return render(request, 'posts_detail.html', {'post_obj': post, 'comment_form': form, 'comments': comments})

@login_required
def add_post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = request.POST or {'votes': 10}
    form = CommentForm(data)
    if request.method == 'POST':
        if form.is_valid():
            votes = form.cleaned_data.get('votes')
            body = form.cleaned_data['body']
            Comment.objects.create(votes=votes, body=body, post=post, author=request.user.cooluser)
            return HttpResponseRedirect(reverse('posts-detail', kwargs={'post_id': post_id}))

    return render(request, 'comment-add.html', {'form': form, 'post': post})

@login_required
def post_update(request, post_id=None):
    post = None
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.user != post.author.user:
            return HttpResponseBadRequest('Not allowed to change others posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            username = request.user.username
            instance.author = CoolUser.objects.get(user__username=username)
            instance.save()
            return HttpResponseRedirect(reverse('posts-detail', kwargs={'post_id': instance.id}))
    else:
        form = PostForm(instance=post)

    return render(request, 'posts_update.html', {'form': form})

@login_required
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data['body']
            image_link = form.cleaned_data.get('image_link')
            category = form.cleaned_data.get('category')
            status = form.cleaned_data.get('status')
            post = Post.objects.create(title=title, body=body, image_link=image_link, category=category, status=status,
                                   author=request.user.cooluser)
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'posts_create.html', {'form': form})

@login_required
def category_create(request):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            label = form.cleaned_data.get('label')
            slug = form.cleaned_data.get('slug')
            category = Category.objects.create(label=label, slug=slug, created_by=request.user.cooluser)
            category.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'categories_create.html', {'form': form})

