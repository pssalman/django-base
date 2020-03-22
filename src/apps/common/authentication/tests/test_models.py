from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        username = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        username = 'test'
        user = get_user_model().objects.create_user(email, username, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_with_full_name(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        username = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name='first',
            last_name='last'
        )
        self.assertEqual(user.get_full_name, 'first last')

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        username = 'test'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, username, 'test123')

    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error"""
        email = 'test@londonappdev.com'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, None, 'test123')

    def test_new_user_invalid_username_and_email(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, None, 'test123')

    def test_new_user_no_password(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', username='')

    def test_new_user_invalid_data(self):
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user()

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_new_superuser_with_no_is_superuser(self):
        """Test creating a new superuser with is_superuser=False"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='super@user.com', username='super', password='foo', is_superuser=False)

    def test_create_new_superuser_is_not_staff(self):
        """Test creating a new superuser with is_staff=False"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email='super@user.com', username='super', password='foo', is_staff=False)

    def test_send_email_to_user(self):
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        username = 'test'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )
        email_user = user.email_user('subject', 'body.', 'from@example.com')
        self.assertEqual(email_user, 1)

    def test_send_email(self):
        mail.send_mail(
            'Example subject here',
            'Here is the message body.',
            'from@example.com',
            ['to@example.com']
        )
        # Now you can test delivery and email contents
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual( mail.outbox[0].subject, 'Example subject here')
        self.assertEqual(mail.outbox[0].body, 'Here is the message body.')
        self.assertEqual(mail.outbox[0].from_email, 'from@example.com')
        self.assertEqual(mail.outbox[0].to, ['to@example.com'])
