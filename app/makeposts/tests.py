import os
from django.core.files import File
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from makeposts.forms import CommentForm
from .models import Post, Comments, Following


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='tester', password='1234asdasd!')
        cwd = os.path.dirname(__file__)
        file_path = os.path.join(cwd, '../media/test_files/myImage.jpg')
        Post.objects.create(author=user, title="TitleForTests", image=File(open(file_path, 'rb')))

    def test_author_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_post_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, "TitleForTests")


class PostViewTest(TestCase):
    def test_if_not_logged_in(self):
        response = self.client.get(reverse('post-create'))
        self.assertRedirects(response, '/login/?next=/post/new/')

    def test_if_logged_in(self):
        user = User.objects.create(username='testuser1')
        user.set_password('1X<ISRUkw+tuK')
        user.save()
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        user = User.objects.create(username='tester')
        user.set_password('1234asdasd!')
        user.save()
        client = Client()
        self.client.login(username='tester', password='1234asdasd!')
        cwd = os.path.dirname(__file__)
        file_path = os.path.join(cwd, '../media/test_files/myImage.jpg')
        response = self.client.post(reverse('post-create'),
                                    data={'title': "Test", 'content': "Content", 'image': File(open(file_path, 'rb'))})
        self.assertEqual(Post.objects.last().title, "Test")


class CommentsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='tester2', password='1234asdasd!')
        cwd = os.path.dirname(__file__)
        file_path = os.path.join(cwd, '../media/test_files/myImage.jpg')
        post = Post.objects.create(author=user, title="TitleForTests", image=File(open(file_path, 'rb')))
        Comments.objects.create(post_id=post.id, commenter=user.id, comment="Test Comments", username=user)

    def test_post_id(self):
        post = Post.objects.last()
        comment = Comments.objects.last()
        self.assertEqual(comment.post_id, post.id)

    def test_author_id(self):
        comment = Comments.objects.last()
        self.assertEqual(comment.commenter, User.objects.filter(username='tester2').last().id)

    def test_author_username(self):
        comment = Comments.objects.last()
        self.assertEqual(comment.username, User.objects.filter(username='tester2').last().username)


class CommentsFormTest(TestCase):
    def test_comment_form_valid(self):
        form = CommentForm(data={'comment': "Hello"})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        #Empty form
        form = CommentForm()
        self.assertFalse(form.is_valid())


class CommentsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='tester2')
        user.set_password('1234asdasd!')
        user.save()
        cwd = os.path.dirname(__file__)
        file_path = os.path.join(cwd, '../media/test_files/myImage.jpg')
        post = Post.objects.create(author=user, title="TitleForTests", image=File(open(file_path, 'rb')))
        Comments.objects.create(post_id=post.id, commenter=user.id, comment="Test Comments", username=user)

    def test_commenting(self):
        self.client.login(username='tester2', password='1234asdasd!')
        user = User.objects.filter(username='tester2').last()
        post = Post.objects.last()
        self.client.post(f"/post/{post.id}/comment/", data={'comment': "Test comment"})
        comment = Comments.objects.last()
        self.assertEqual(comment.post_id, post.id)
        self.assertEqual(comment.commenter, user.id)


class FollowModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        follower = User.objects.create(username='tester2', password='1234asdasd!')
        followed = User.objects.create(username='tester3', password='1234asdasd!')
        Following.objects.create(user_id=followed.id, follower=follower.id)

    def test_follower_id(self):
        following = Following.objects.last()
        follower = User.objects.filter(username='tester2').first()
        self.assertEqual(following.follower, follower.id)

    def test_followed_id(self):
        following = Following.objects.last()
        followed = User.objects.filter(username='tester3').first()
        self.assertEqual(following.user_id, followed.id)

    def test_followed_label(self):
        following = Following.objects.last()
        field_label = following._meta.get_field('user_id').verbose_name
        self.assertEquals(field_label, 'user id')

    def test_follower_id(self):
        following = Following.objects.last()
        field_label = following._meta.get_field('follower').verbose_name
        self.assertEqual(field_label, 'follower')


class FollowTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='Test1')
        user1.set_password('asdasd123')
        user1.save()
        user2 = User.objects.create(username='Test2')
        user2.set_password('asdasd123')
        user2.save()
        cwd = os.path.dirname(__file__)
        file_path = os.path.join(cwd, '../media/test_files/myImage.jpg')
        post = Post.objects.create(author=user1, title="TitleForTests", image=File(open(file_path, 'rb')))
        post.save()

    def test_follow_view(self):
        self.client.login(username='Test2', password='asdasd123')
        post = Post.objects.last()
        self.assertEqual(post.id, 1)
        user = User.objects.filter(username='Test2').last()
        response = self.client.get(reverse('follow', kwargs={'username': post.author}))
        self.assertRedirects(response, reverse('profile-view', kwargs={'username':post.author}))
        following = Following.objects.last()
        self.assertEqual(following.user_id, post.id)
        self.assertEqual(following.follower, user.id)
