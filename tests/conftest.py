import os
import sys
import django
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.test_settings')
django.setup()

from django.contrib.auth.models import User
from diary.models import Entry

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='secret123'
    )

@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='otheruser',
        email='other@example.com',
        password='secret456'
    )

@pytest.fixture
def entry(user):
    return Entry.objects.create(
        title='Тестовая запись',
        content='Содержимое записи',
        author=user
    )

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='secret123')
    return client