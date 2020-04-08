import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from makeposts.models import Post
from users.models import Following


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='tester2')
        user.set_password('1234asdasd!')
        user.save()
        user2 = User.objects.create(username='Test2')
        user2.set_password('asdasd123')
        user2.save()

    def test_profile_redirect(self):
        self.client.login(username='tester2', password='1234asdasd!')
        username = User.objects.all().last()
        response = self.client.get(f"/profile/{username}/")
        self.assertEqual(str(response), '<HttpResponse status_code=200, "text/html; charset=utf-8">')



class FollowModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        follower = User.objects.create(username='tester2', password='1234asdasd!')
        followed = User.objects.create(username='tester3', password='1234asdasd!')
        Following.objects.create(user_id=followed, follower=follower)

    def test_follower_id(self):
        following = Following.objects.last()
        follower = User.objects.filter(username='tester2').first()
        self.assertEqual(following.follower, follower.id)

    def test_followed_id(self):
        following = Following.objects.last()
        followed = User.objects.filter(username='tester3').first()
        self.assertEqual(following.user_id, followed)

    def test_followed_label(self):
        following = Following.objects.last()
        field_label = following._meta.get_field('user_id').verbose_name
        self.assertEquals(field_label, 'user id')

    def test_follower_id(self):
        following = Following.objects.last()
        field_label = following._meta.get_field('follower').verbose_name
        self.assertEqual(field_label, 'follower')


class FollowViewTest(TestCase):
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
        self.assertRedirects(response, reverse('profile-view', kwargs={'username': post.author}))
        following = Following.objects.last()
        self.assertEqual(following.user_id, post.author)
        self.assertEqual(following.follower, user)

class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        searcher = User.objects.create(username='tester')
        searcher.set_password('1234asdasd!')
        searcher.save()
        User.objects.create(username='tester1', password='1234asdasd!')

    def test_search_view(self):
        self.client.login(username='tester', password='1234asdasd!')
        url = '{url}?{filter}={value}'.format(
            url=reverse('insta-search'),
            filter='q', value='tester1')
        response = self.client.get(url)
        self.assertRedirects(response, '/profile/tester1', status_code=302,
                             target_status_code=301)

    def test_search_fail(self):
        self.client.login(username='tester', password='1234asdasd!')
        url = '{url}?{filter}={value}'.format(
            url=reverse('insta-search'),
            filter='q', value='teste')
        response = self.client.get(url)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200)

    def test_query_search_filter(self):
        self.client.login(username='tester', password='1234asdasd!')
        self.assertQuerysetEqual(User.objects.filter(username__icontains='tester1'), ["<User: tester1>"])
