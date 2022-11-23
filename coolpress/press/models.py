from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from press.user_info_manager import get_gravatar_image, get_github_repositories, get_github_stars

class CoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gravatar_link = models.URLField(null=True, blank=True, editable=False)
    gravatar_updated_at = models.DateTimeField(editable=False)
    github_profile = models.CharField(max_length=150, null=True, blank=True)
    gh_repositories = models.IntegerField(null=True, blank=True)
    gh_stars = models.IntegerField(null=True, blank=True)
    last_github_check = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(CoolUser, self).save(*args, **kwargs)

        email = self.user.email
        if email:
            image_link = self.gravatar_link
            image_link_new = get_gravatar_image(email)
            if (image_link != image_link_new):
                self.gravatar_updated_at = timezone.now()
            self.gravatar_link = image_link_new
            super(CoolUser, self).save()

        # if self.gh_repositories is None and self.github_profile:
        #     repositories = get_github_repositories(self.github_profile)
        #
        #     if repositories is not None:
        #         self.gh_repositories = repositories
        #         self.save()
        #
        # if self.gh_stars is None and self.github_profile:
        #     stars = get_github_stars(self.github_profile)
        #
        #     if stars is not None:
        #         self.gh_stars = stars
        #         self.save()
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    label = models.CharField(max_length=200)
    slug = models.SlugField()
    created_by = models.ForeignKey(CoolUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.label} ({self.id})'


class PostStatus:
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'


class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField(null=True)
    image_link = models.URLField(null=True)

    status = models.CharField(max_length=32,
                              choices=[(PostStatus.DRAFT, 'Draft'),
                                       (PostStatus.PUBLISHED, 'Published Post')],
                              default=PostStatus.DRAFT)

    author = models.ForeignKey(CoolUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category.label}: {self.title}'



class CommentStatus:
    PUBLISHED = 'PUBLISHED'
    NON_PUBLISHED = 'NON_PUBLISHED'


class Comment(models.Model):
    body = models.TextField()
    status = models.CharField(max_length=32,
                              choices=[(CommentStatus.PUBLISHED, 'Published'),
                                       (CommentStatus.NON_PUBLISHED, 'Non Published')],
                              default=CommentStatus.PUBLISHED)
    votes = models.IntegerField()

    author = models.ForeignKey(CoolUser, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.body[:10]} - from: {self.author.user.username}'