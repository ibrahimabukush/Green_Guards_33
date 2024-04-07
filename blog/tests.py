from blog.models import Rebort
from blog.views import RebortListView
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Rebort







class TestBlogViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', content='This is a test post content.', author=self.user)

   


    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_create_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'content': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_create_view_unauthenticated_user(self):
        response = self.client.post(reverse('post-create'), {'title': 'New Post', 'content': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)  

    def test_post_update_view_authenticated_author(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {'title': 'Updated Post', 'content': 'Updated post content.'})
        self.assertEqual(response.status_code, 302)  
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_update_view_unauthenticated_user(self):
        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {'title': 'Updated Post', 'content': 'Updated post content.'})
        self.assertEqual(response.status_code, 302) 

    def test_post_delete_view_authenticated_author(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_view_unauthenticated_user(self):
        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  





class RebortCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_rebort_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('rebort-create'), {
            'city': 'Test City',
            'location_latitude': 123.456,
            'location_longitude': 456.789,
            'explanation': 'Test explanation',
            'solution': 'Test solution'
        })
       
    

    def test_unauthenticated_user_redirect(self):
        response = self.client.get(reverse('rebort-create'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_invalid_form_submission(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('rebort-create'), {
            'city': 'Test City',
            'location_latitude': '',  # Missing latitude value
            'location_longitude': 456.789,
            'explanation': 'Test explanation',
            'solution': 'Test solution'
        })
        self.assertEqual(response.status_code, 200)  # Form submission failed
        self.assertFormError(response, 'form', 'location_latitude', 'This field is required.')

    def test_author_assigned_correctly(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('rebort-create'), {
            'city': 'Test City',
            'location_latitude': 123.456,
            'location_longitude': 456.789,
            'explanation': 'Test explanation',
            'solution': 'Test solution'
        })
    

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        test_user = User.objects.create_user(username='testuser', password='12345')

        # Create a sample post
        Post.objects.create(
            title='Test Post',
            content='This is a test post content.',
            date_posted=timezone.now(),
            author=test_user
        )

    def test_title_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEqual(expected_object_name, 'Test Post')

    def test_content_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.content
        self.assertEqual(expected_object_name, 'This is a test post content.')

    def test_date_posted_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.date_posted
        self.assertTrue(expected_object_name)

    def test_author_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.author
        self.assertTrue(expected_object_name)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), reverse('blog-home'))
    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_str_representation(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), 'Test Post')

    def test_date_posted_default(self):
        post = Post.objects.get(id=1)
        self.assertTrue(post.date_posted)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.get_absolute_url(), reverse('blog-home'))


class RebortModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        test_user = User.objects.create_user(username='testuser', password='12345')

        # Create a sample rebort
        Rebort.objects.create(
            city='Test City',
            location_latitude=1.0,
            location_longitude=2.0,
            explanation='Test explanation',
            image='test_image.jpg',
            solution='Test solution',
            data_rebort=timezone.now(),
            author=test_user,
            deleted=False,
            response='Test response'
        )

    def test_city_content(self):
        rebort = Rebort.objects.get(id=1)
        expected_object_name = rebort.city
        self.assertEqual(expected_object_name, 'Test City')

    def test_location_latitude_content(self):
        rebort = Rebort.objects.get(id=1)
        expected_object_name = rebort.location_latitude
        self.assertEqual(expected_object_name, 1.0)

    def test_location_longitude_content(self):
        rebort = Rebort.objects.get(id=1)
        expected_object_name = rebort.location_longitude
        self.assertEqual(expected_object_name, 2.0)

    def test_explanation_content(self):
        rebort = Rebort.objects.get(id=1)
        expected_object_name = rebort.explanation
        self.assertEqual(expected_object_name, 'Test explanation')


    def test__str__method(self):
        rebort = Rebort.objects.get(id=1)
        self.assertEqual(str(rebort), 'Test City')

    def test_get_absolute_url_method(self):
        rebort = Rebort.objects.get(id=1)
        self.assertEqual(rebort.get_absolute_url(), reverse('blog-myreborts'))
    def test_city_max_length(self):
        rebort = Rebort.objects.get(id=1)
        max_length = rebort._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)

    def test_deleted_default_value(self):
        rebort = Rebort.objects.get(id=1)
        self.assertFalse(rebort.deleted)


    def test_save_method(self):
        # Test save method when deleted is None
        rebort = Rebort.objects.get(id=1)
        rebort.deleted = None
        rebort.save()
        self.assertFalse(rebort.deleted)
    def test_get_absolute_url_method(self):
        rebort = Rebort.objects.get(id=1)
        self.assertEqual(rebort.get_absolute_url(), reverse('blog-myreborts'))


