import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse

from diary.models import Entry
from users.models import Profile

pytestmark = pytest.mark.django_db

class TestEntryModel:
    def test_str_method(self, entry):
        assert str(entry) == entry.title

    def test_absolute_url(self, entry):
        assert entry.get_absolute_url() == reverse('diary:entry_detail', args=[entry.id])

    def test_ordering(self, user):
        entry1 = Entry.objects.create(title='Старая', content='...', author=user)
        import time
        time.sleep(0.01)  # чтобы created_at различались
        entry2 = Entry.objects.create(title='Новая', content='...', author=user)
        entries = Entry.objects.filter(author=user)
        assert entries.first() == entry2
        assert entries.last() == entry1

    def test_author_cascade_delete(self, user, entry):
        user.delete()
        assert Entry.objects.filter(pk=entry.pk).count() == 0

class TestProfileSignal:
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='sigtest', password='pass')
        assert Profile.objects.filter(user=user).exists()

    def test_profile_saved_on_user_save(self, user):
        profile = user.profile
        profile.save()  # просто проверяем, что сигнал не ломается
        assert Profile.objects.get(user=user) == profile

class TestEntryModel:
    def test_absolute_url(self, entry):
        expected_url = reverse('diary:entry_detail', args=[entry.id])
        assert entry.get_absolute_url() == expected_url

