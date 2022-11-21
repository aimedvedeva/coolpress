from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.urls import reverse

from press.models import Category, Post, CoolUser, PostStatus, Comment, CommentStatus


class PostPagesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='oscar')
        cu = CoolUser.objects.create(user=user)
        category = Category.objects.create(label='Tech', slug='tech')
        titles = ['Awesome tech out new', 'Even greater news coming', 'Hello from the first Google IA']
        for title in titles:
            post = Post.objects.create(category=category, title=title, author=cu,
                                       status=PostStatus.PUBLISHED)

        titles = ['Secret news', 'Tesla is behind FTX']
        for title in titles:
            Post.objects.create(category=category, title=title, author=cu)
        cls.user = user
        cls.post = post
        cls.cu = cu

        votes = 10
        comment = Comment.objects.create(votes=votes, post=post, author=cu)
        cls.comment = comment

    def setUp(self):
        self.client = Client()

    def test_post_detail(self):
        response = self.client.get(reverse('posts-detail', kwargs={'post_id': self.post.id}))

        self.assertEqual(response.status_code, 200)
    def test_post_comment_existence(self):
        comments = self.post.comment_set.values()
        self.assertEqual(1, len(comments))

    def test_check_change_comment_status(self):
        self.comment.status = CommentStatus.NON_PUBLISHED
        self.comment.save()
        response = self.client.get(reverse('posts-detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(0, len(response.context['comments'].values()))


    def test_posts(self):
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['posts_list']), 3)
