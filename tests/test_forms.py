import pytest
from diary.forms import EntryForm
from users.forms import CustomUserCreationForm
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

class TestEntryForm:
    def test_valid_form(self):
        form = EntryForm(data={
            'title': 'Работает',
            'content': 'Какой-то текст'
        })
        assert form.is_valid()

    def test_invalid_form_missing_title(self):
        form = EntryForm(data={'content': 'Только текст'})
        assert not form.is_valid()
        assert 'title' in form.errors

    def test_invalid_form_empty_content(self):
        form = EntryForm(data={'title': 'Заголовок', 'content': ''})
        assert not form.is_valid()

    def test_form_widgets(self):
        form = EntryForm()
        assert 'class="form-control"' in str(form['title'])
        assert 'placeholder="Заголовок"' in str(form['title'])
        assert 'rows="10"' in str(form['content'])


class TestCustomUserCreationForm:
    def test_valid_registration(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'Str0ngP@ss',
            'password2': 'Str0ngP@ss',
        })
        assert form.is_valid()
        user = form.save()
        assert user.email == 'new@example.com'
        assert user.check_password('Str0ngP@ss')

    def test_duplicate_email_invalid(self):
        User.objects.create_user(username='existing', email='duplicate@example.com', password='pass')
        form = CustomUserCreationForm(data={
            'username': 'another',
            'email': 'duplicate@example.com',
            'password1': 'pass123',
            'password2': 'pass123',
        })
        assert not form.is_valid()
        assert 'email' in form.errors
        assert 'уже зарегистрирован' in str(form.errors['email'])

    def test_passwords_mismatch(self):
        form = CustomUserCreationForm(data={
            'username': 'mismatch',
            'email': 'm@m.com',
            'password1': 'pass123',
            'password2': 'wrong',
        })
        assert not form.is_valid()