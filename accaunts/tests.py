from django.test import TestCase
# Import necessary modules for testing
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


# Create a test case for the Profile model
class ProfileModelTest(TestCase):

    # Define setup method to create test data
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword'
        )

    # Test Profile creation
    def test_profile_creation(self):
        # Create a profile for the test user
        profile = Profile.objects.create(
            user=self.user, date_of_birth='2000-01-01'
        )

        # Check if the profile was created successfully
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.date_of_birth, '2000-01-01')

    # Test Profile string representation
    def test_profile_str(self):
        # Create a profile for the test user
        profile = Profile.objects.create(
            user=self.user, date_of_birth='2000-01-01'
        )

        # Check if the string representation is correct
        self.assertEqual(str(profile), 'testuser profili')






