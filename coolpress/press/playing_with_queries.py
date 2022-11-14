import os
import django
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolpress.coolpress.settings")
django.setup()

from press.models import Post, CoolUser, Category

def values():
    authors_id = CoolUser.objects.annotate(total=Count('post')).filter(total__gt=0).values_list('post__author', flat=True)
    for id in authors_id:
        name = CoolUser.objects.filter(id=id).values_list('user__first_name').first()[0]
        posts = Post.objects.filter(author=id).values_list('body', flat=True)
        characters_sum = sum([len(post) for post in posts])
        titles = Post.objects.filter(author=id).values_list('title', flat=True)
        titles_sum = sum([len(title) for title in titles])
        print(name, ': ', characters_sum+titles_sum, ' characters on ', len(posts), ' posts')

if __name__ == '__main__':
    values()