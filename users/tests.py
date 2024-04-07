from django.test import TestCase, RequestFactory,client
from django.urls import reverse
from django.contrib.messages import get_messages
from users.models import Feedback
from users.views import feedback
from users.views import profile
from users.views import contact
from django.test import TestCase
from django.contrib.auth.models import User,Group
from django.urls import reverse
from users.models import Profile
from users.views import signup
from users.forms import UserRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Feedback
from .models import Contact

class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample contact
        Contact.objects.create(
            name='ahmad',
            email='ahmad@gmail.com',
            report='This is a test report.'
        )

    def test_name_max_length(self):
        contact = Contact.objects.get(id=1)
        max_length = contact._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_email_field(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.email, 'ahmad@gmail.com')

    def test_report_max_length(self):
        contact = Contact.objects.get(id=1)
        max_length = contact._meta.get_field('report').max_length
        self.assertEqual(max_length, 2048)

    def test_str_representation(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(str(contact), 'ahmad ')

    def test_name_field(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.name, 'ahmad')

    def test_email_field(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.email, 'ahmad@gmail.com')

    def test_report_field(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(contact.report, 'This is a test report.')

    def test_str_representation(self):
        contact = Contact.objects.get(id=1)
        self.assertEqual(str(contact), 'ahmad')

    def test_object_creation(self):
        contact_count = Contact.objects.count()
        self.assertEqual(contact_count, 1)

    def test_object_deletion(self):
        contact = Contact.objects.get(id=1)
        contact.delete()
        contact_count = Contact.objects.count()
        self.assertEqual(contact_count, 0)

class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample feedback
        Feedback.objects.create(
            name='Ahmad',
            stars=4,
            text='This is a test feedback.'
        )

    def test_name_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def test_stars_field(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEqual(feedback.stars, 4)

    def test_text_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('text').max_length
        self.assertEqual(max_length, 500)

    def test_str_representation(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEqual(str(feedback), 'Ahmad')
    def test_name_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def test_stars_field(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEqual(feedback.stars, 4)

    def test_text_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field('text').max_length
        self.assertEqual(max_length, 500)

    def test_str_representation(self):
        feedback = Feedback.objects.get(id=1)
        self.assertEqual(str(feedback), 'Ahmad')

    def test_feedback_creation(self):
        feedback_count = Feedback.objects.count()
        self.assertEqual(feedback_count, 1)

    def test_feedback_deletion(self):
        feedback = Feedback.objects.get(id=1)
        feedback.delete()
        feedback_count = Feedback.objects.count()
        self.assertEqual(feedback_count, 0)

    def test_feedback_text_not_empty(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(feedback.text)

    def test_feedback_name_not_empty(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(feedback.name)

    def test_feedback_stars_range(self):
        feedback = Feedback.objects.get(id=1)
        self.assertTrue(1 <= feedback.stars <= 5)

    def test_feedback_text_contains(self):
        feedback = Feedback.objects.get(id=1)
        self.assertIn('test feedback', feedback.text.lower())    


class UserTestCase(TestCase):
    
    def setUp(self):
        self.user_data = {
           'username': 'testuser',
             'email': 'test@example.com',
             'password1': 'testpassword',
            'password2': 'testpassword'
        }

    def test_signup_user(self):
        response = self.client.post(reverse('signup'), self.user_data)
        self.assertEqual(response.status_code, 302)  

    def test_login_user(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        login_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  

    def test_invalid_login_user(self):
         login_data = {'username': 'wronguser', 'password': 'wrongpassword'}
         response = self.client.post(reverse('login'), login_data)
         self.assertEqual(response.status_code, 200)  

    def test_create_user_form_valid(self):
         form = UserRegisterForm(data=self.user_data)
         self.assertTrue(form.is_valid())  

    def test_create_user_form_invalid(self):
        
         invalid_data = self.user_data.copy()
         invalid_data['password2'] = 'differentpassword'
         form = UserRegisterForm(data=invalid_data)
         self.assertFalse(form.is_valid()) 

        

    def test_login_view(self):
         # יבדוק כי הנתיב להתחברות מחזיר קוד תקין
         url = reverse('login')
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
         # יבדוק כי הנתיב להתנתקות מחזיר קוד תקין
         url = reverse('logout')
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_empty_email_password(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_empty_email(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

    def test_empty_password(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

class FeedbackTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_feedback_post(self):
        url = reverse('feedback')
        request = self.factory.post(url, {'username': 'testuser', 'stars': '5', 'text': 'Great feedback!'})
        request.user = self.user


    def test_feedback_get(self):
        url = reverse('feedback')
        request = self.factory.get(url)

        response = feedback(request)
        self.assertEqual(response.status_code, 200)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

class ContactTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_contact_post(self):
        url = reverse('contact')
        request = self.factory.post(url, {'name': 'Test User', 'email': 'test@example.com', 'report': 'Test report'})





class ModelTestCase(TestCase):
    def testProfileImageThumbnail(self):
        user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')
        large_image_path = 'path/to/large_image.jpg'
       

        
        

    def testContactCreation(self):

        contact = Contact.objects.create(name='Test User', email='test@example.com', report='Test report')
        self.assertIsInstance(contact, Contact, "Contact instance should be created successfully")

    def testFeedbackCreation(self):

        feedback = Feedback.objects.create(name='Test User', stars=5, text='Great feedback!')
        self.assertIsInstance(feedback, Feedback, "Feedback instance should be created successfully")

    def testProfileImageDefault(self):
        user = User.objects.create(username='testuser', email='test@example.com', password='testpassword')


    def testContactStrMethod(self):
        contact = Contact.objects.create(name='Test User', email='test@example.com', report='Test report')
        self.assertEqual(str(contact), 'Test User', "__str__ method of Contact model should return correct value")

    def testFeedbackStrMethod(self):
        feedback = Feedback.objects.create(name='Test User', stars=5, text='Great feedback!')
        self.assertEqual(str(feedback), 'Test User', "__str__ method of Feedback model should return correct value")






class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        invalid_form_data = {
            'username': '',  
            'email': 'invalid_email',  
            'password1': 'testpassword',
            'password2': 'differentpassword'  
        }
        form = UserRegisterForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

class LoginFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'tuser',
            'password': 'tpass'
        }
        form = LoginForm(data=form_data)
       

    def test_invalid_form(self):
        invalid_form_data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=invalid_form_data)
        self.assertFalse(form.is_valid())

class UserUpdateFormTest(TestCase):
    def test_valid_form(self):
        user = User.objects.create(username='tuser', email='test@gmail.com')
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())


