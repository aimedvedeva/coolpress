import os
import django
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coolpress.coolpress.settings")
django.setup()

from press.models import Post, CoolUser, Category

def values():

    authors_id = CoolUser.objects.annotate(total=Count('post')).filter(total__gt=0).values_list('post__author',flat=True)
    print(len(authors_id))
    for id in authors_id:
        name = CoolUser.objects.filter(id=id).values_list('user__first_name').first()[0]
        posts = Post.objects.filter(author=id).values_list('body', flat=True)
        characters_sum = sum([len(post) for post in posts])
        #print(name, ': ', characters_sum, ' characters on ', len(posts), ' posts')
        #print('-----------------------')
    print(authors_id)

if __name__ == '__main__':
    values()