from django.test import TestCase
from django.db.utils import IntegrityError
from pyday_social_network.models import PyDayUser, FollowingRelation
from pyday_social_network.views import *
from django.test import Client
from django.core.urlresolvers import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from pyday_social_network.services import *
from pyday_social_network.forms import RegisterUserForm
from datetime import datetime
from pyday.settings import GREETINGS


class PyDayUserTest(TestCase):

    def setUp(self):
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")

    def test_user_creation(self):
        self.assertEqual(self.user.first_name, "MynameisWhat")
        self.assertEqual(self.user.last_name, "MynameisWho")
        self.assertEqual(self.user.email, "bla@bla.bla")
        self.assertNotEqual(self.user.password, "secret")

    # TODO
    def test_user_creation_post(self):
        pass

    def test_user_creation_save(self):
        PyDayUser.objects._create_user("bla@bla2.bla", "secret",
                                       "MynameisWhat",
                                       "MynameisWho")
        self.assertEqual(len(PyDayUser.objects.all()), 2)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            PyDayUser.objects._create_user("", "secret",
                                           "MynameisWhat",
                                           "MynameisWho")

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                           "MynameisWhat",
                                           "MynameisWho")


class FollowingRelationTest(TestCase):

    def setUp(self):
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.user2 = PyDayUser.objects._create_user("bla@bla2.bla", "secret",
                                                    "MynameisWhat",
                                                    "MynameisWho")

    def test_follow(self):
        self.user.follow(self.user2.id)
        self.assertEqual(len(FollowingRelation.objects.all()), 1)
        rel = FollowingRelation.objects.get(pk=1)
        self.assertEqual(rel.followed, self.user2)
        self.assertEqual(rel.follower, self.user)

    def test_unfollow(self):
        self.user.follow(self.user2.id)
        self.user.unfollow(self.user2.id)
        self.assertEqual(len(FollowingRelation.objects.all()), 0)

    def test_unfollow_not_followed(self):
        self.assertFalse(self.user.unfollow(self.user2.id)[0])

    def test_follow_followed(self):
        self.user.follow(self.user2.id)
        self.assertFalse(self.user.follow(self.user2.id)[0])

    def test_following_followers(self):
        self.user.follow(self.user2.id)
        self.assertEqual(self.user.following, [self.user2])
        self.assertEqual(self.user2.followers, [self.user])

    def test_friends(self):
        self.user.follow(self.user2.id)
        self.user2.follow(self.user.id)
        self.assertEqual(self.user.friends, [self.user2])
        self.assertEqual(self.user2.friends, [self.user])


# Song...
class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.post(reverse('pyday_social_network:register_login'),
                                        {'first_name': 'ha', 'last_name': 'ha',
                                         'email': 'haha@ha.ha',
                                         'password': '1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(PyDayUser.objects.all()), 1)
            self.assertTrue(PyDayUser.objects.get(email='haha@ha.ha'))
            self.assertContains(response, "You have registered")

    def test_post_not_successful(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.post(reverse('pyday_social_network:register_login'),
                                        {'first_name': 'ha', 'last_name': 'ha',
                                         'email': '', 'password': '1'})


class UploadPictureViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.user2 = PyDayUser.objects._create_user("bla2@bla.bla", "secret",
                                                    "MynameisWhat",
                                                    "MynameisWho")
        self.client.login(email='bla@bla.bla', password='secret')

    def test_post(self):
        picture = open('./media/pictures/profile.jpg', 'rb')
        response = self.client.post(reverse('pyday_social_network:upload_picture'),
                                    {'picture': picture})
        self.assertNotEqual(PyDayUser.objects.get(
            email="bla@bla.bla").picture, PyDayUser.objects.get(email="bla2@bla.bla").picture)

    def tearDown(self):
        PyDayUser.objects.get(email='bla@bla.bla').delete()


class ViewsTestNotLogged(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")

    def test_login_redirect(self):
        response = self.client.get(
            reverse('pyday_social_network:login'), follow=True)
        self.assertEqual(response.redirect_chain,
                         [('/social/main', 302), ('/social/main/', 301),
                          ('/social/register/?next=/social/main/', 302)])

    def test_login_redirect_anonymous(self):
        self.client.login(email='bla@bla.bla', password='secret')
        with self.assertTemplateUsed('main.html'):
            response = self.client.get(
                reverse('pyday_social_network:login'), follow=True)
            self.assertEqual(response.redirect_chain,
                             [('/social/main', 302), ('/social/main/', 301)])

    def test_login_success(self):
        with self.assertTemplateUsed('main.html'):
            response = self.client.post(reverse('pyday_social_network:login'),
                                        {'email': "bla@bla.bla",
                                            'password': 'secret'},
                                        follow=True)
            self.assertEqual(response.redirect_chain, [('/social/main', 302),
                                                       ('/social/main/', 301)])

    def test_login_invalid_form(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.post(reverse('pyday_social_network:login'),
                                        {'password': 'secret'},
                                        follow=True)
            self.assertContains(response, "Invalid form")

    def test_login_wrong_email(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.post(reverse('pyday_social_network:login'),
                                        {'email': "bla@bla.bla2",
                                         'password': 'secret'},
                                        follow=True)
            self.assertContains(response, "Invalid email/password")


class ViewsTestLogged(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                                   "MynameisWhat",
                                                   "MynameisWho")
        self.client.login(email='bla@bla.bla', password='secret')

    def test_main(self):
        with self.assertTemplateUsed('main.html'):
            response = self.client.get(reverse('pyday_social_network:main'))
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.get(reverse('pyday_social_network:logout'))
            self.assertEqual(response.status_code, 200)

    def test_display_all_users(self):
        self.display('pyday_social_network:all_users')

    def display(self, name_url):
        with self.assertTemplateUsed('all_users.html'):
            response = self.client.get(reverse(name_url))
            self.assertEqual(response.status_code, 200)

    def test_display_following(self):
        self.display('pyday_social_network:following')

    def test_display_followers(self):
        self.display('pyday_social_network:followers')

    def test_display_friends(self):
        self.display('pyday_social_network:friends')

    def test_follow(self):
        user2 = PyDayUser.objects._create_user("bla2@bla.bla", "secret",
                                               "MynameisWhat",
                                               "MynameisWho")
        response = self.client.get(
            '/social/follow/{}'.format(user2.id), follow=True)
        self.assertTrue(PyDayUser.objects.get(email=user2.email)
                        in PyDayUser.objects.get(email=self.user.email).following)
        self.assertTrue(PyDayUser.objects.get(email=self.user.email)
                        in PyDayUser.objects.get(email=user2.email).followers)

        self.assertEqual(response.redirect_chain,
                         [('/social/profile', 302), ('/social/profile/', 301)])

    def test_follow_already_following(self):
        user2 = PyDayUser.objects._create_user("bla2@bla.bla", "secret",
                                               "MynameisWhat",
                                               "MynameisWho")
        self.user.follow(user2.id)
        with self.assertTemplateUsed('error.html'):
            response = self.client.get('/social/follow/{}'.format(user2.id))
            self.assertContains(
                response, "You have already followed this user")

    def test_unfollow(self):
        user2 = PyDayUser.objects._create_user("bla2@bla.bla", "secret",
                                               "MynameisWhat",
                                               "MynameisWho")
        self.user.follow(user2.id)
        response = self.client.get(
            '/social/unfollow/{}'.format(user2.id), follow=True)
        self.assertTrue(PyDayUser.objects.get(email=user2.email)
                        not in PyDayUser.objects.get(email=self.user.email).following)
        self.assertTrue(PyDayUser.objects.get(email=self.user.email)
                        not in PyDayUser.objects.get(email=user2.email).followers)

        self.assertEqual(response.redirect_chain,
                         [('/social/profile', 302), ('/social/profile/', 301)])

    def test_unfollow_already_not_following(self):
        user2 = PyDayUser.objects._create_user("bla2@bla.bla", "secret",
                                               "MynameisWhat",
                                               "MynameisWho")
        with self.assertTemplateUsed('error.html'):
            response = self.client.get('/social/unfollow/{}'.format(user2.id))
            self.assertContains(response, "You do not follow this user")

    def test_display_profile(self):
        with self.assertTemplateUsed('profile.html'):
            response = self.client.get(
                "/social/profile/{}".format(self.user.id))
            self.assertEqual(response.status_code, 200)

    def test_display_non_existing(self):
        with self.assertTemplateUsed('error.html'):
            response = self.client.get("/social/profile/100")
            self.assertContains(response, 'User does not exist.')


class ServicesTest(TestCase):

    def test_regitster_user_post(self):
        rf = RequestFactory()
        post_request = rf.post('', {'email': "bla2@bla.bla",
                                    'password': "secret",
                                    'first_name': "MynameisWhat",
                                    'last_name': "MynameisWho"})
        self.assertTrue(register_user_post(post_request, RegisterUserForm))
        self.assertEqual(len(PyDayUser.objects.all()), 1)
        user = PyDayUser.objects.get(id=1)
        self.assertEqual(user.email, "bla2@bla.bla")
        self.assertNotEqual(user.password, "secret")
        self.assertEqual(user.first_name, "MynameisWhat")
        self.assertEqual(user.last_name, "MynameisWho")

    def test_current_events(self):
        date_time = datetime.now()
        user = PyDayUser.objects._create_user("bla@bla.bla", "secret",
                                              "MynameisWhat",
                                              "MynameisWho")
        event = Event(owner=user, from_time=date_time.hour,
                      to_time=date_time.hour + 1,
                      importance="important", caption="",
                      date=date_time, title="title")
        event.save()
        self.assertEqual(get_current_events(date_time.hour, date_time, user),
                         [event])

    def test_get_greeting(self):
        self.assertEqual(get_greeting(9), GREETINGS[0][2])
        self.assertEqual(get_greeting(12), GREETINGS[1][2])
        self.assertEqual(get_greeting(16), GREETINGS[2][2])
        self.assertEqual(get_greeting(21), GREETINGS[3][2])

'''class FormTests(TestCase):

    def test_form_upload_picture(self):
        picture = open('./media/pictures/profile.jpg', 'rb')
        file_dict = {'file': SimpleUploadedFile(picture.name, picture.read())}
        form = UploadPictureForm(file_dict)
        self.assertTrue(form.is_valid())
'''
