from django.contrib.auth.models import User
from django.urls import reverse

from users.forms import CustomUserCreationForm




class TestRegisterView:
    def test_get_register_page(self, client, db):  # добавили db
        response = client.get(reverse("users:register"))
        assert response.status_code == 200

    def test_post_valid_registration(self, client, db):  # добавили db
        response = client.post(
            reverse("users:register"),
            data={
                "username": "reguser",
                "email": "reg@example.com",
                "password1": "Str0ngP@ss1",
                "password2": "Str0ngP@ss1",
            },
        )
        assert response.status_code == 302
        assert response.url == reverse("login")
        assert User.objects.filter(username="reguser").exists()

    def test_post_invalid_registration(self, client, db):  # добавили db
        response = client.post(
            reverse("users:register"),
            data={
                "username": "reguser",
                "email": "invalid",
                "password1": "pass",
                "password2": "wrong",
            },
        )
        assert response.status_code == 200
        assert response.context["form"].errors


class TestMyEntriesList:
    def test_entries_list_shows_only_users_entries(
        self, authenticated_client, user, another_user, entry
    ):
        # entry уже создан для user (через фикстуру entry)
        # создаём запись другого пользователя
        from diary.models import Entry

        other_entry = Entry.objects.create(
            title="Чужая", content="...", author=another_user
        )
        response = authenticated_client.get(reverse("diary:entry_list"))
        assert response.status_code == 200
        entries = response.context["entries"]
        assert len(entries) == 1
        assert entries[0] == entry
        assert response.context["entry_count"] == 1

    def test_entries_list_empty(self, authenticated_client, user):
        # удаляем все записи пользователя
        from diary.models import Entry

        Entry.objects.filter(author=user).delete()
        response = authenticated_client.get(reverse("diary:entry_list"))
        assert response.status_code == 200
        assert response.context["entry_count"] == 0
        assert list(response.context["entries"]) == []


class TestEntryDetail:
    def test_detail_own_entry(self, authenticated_client, entry):
        response = authenticated_client.get(
            reverse("diary:entry_detail", args=[entry.pk])
        )
        assert response.status_code == 200
        assert response.context["entry"] == entry

    def test_detail_another_user_404(self, authenticated_client, another_user):
        from diary.models import Entry

        other_entry = Entry.objects.create(
            title="Чужая", content="...", author=another_user
        )
        response = authenticated_client.get(
            reverse("diary:entry_detail", args=[other_entry.pk])
        )
        assert response.status_code == 404


class TestEntryCreate:
    def test_create_get_form(self, authenticated_client):
        response = authenticated_client.get(reverse("diary:entry_create"))
        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["title"] == "Новая запись"

    def test_create_post_valid(self, authenticated_client, user):
        data = {"title": "Новая запись", "content": "Текст записи"}
        response = authenticated_client.post(reverse("diary:entry_create"), data)
        assert response.status_code == 302  # редирект на детали
        from diary.models import Entry

        entry = Entry.objects.get(title="Новая запись")
        assert entry.author == user
        assert entry.content == "Текст записи"
        assert response.url == reverse("diary:entry_detail", args=[entry.pk])

    def test_create_post_invalid(self, authenticated_client):
        data = {"title": "", "content": ""}
        response = authenticated_client.post(reverse("diary:entry_create"), data)
        assert response.status_code == 200
        assert response.context["form"].errors
        assert "title" in response.context["form"].errors


class TestEntryEdit:
    def test_edit_get_form(self, authenticated_client, entry):
        response = authenticated_client.get(
            reverse("diary:entry_edit", args=[entry.pk])
        )
        assert response.status_code == 200
        assert response.context["form"].instance == entry
        assert response.context["title"] == "Редактирование"

    def test_edit_post_valid(self, authenticated_client, entry):
        data = {"title": "Изменённый заголовок", "content": "Изменённый текст"}
        response = authenticated_client.post(
            reverse("diary:entry_edit", args=[entry.pk]), data
        )
        assert response.status_code == 302
        entry.refresh_from_db()
        assert entry.title == "Изменённый заголовок"
        assert entry.content == "Изменённый текст"
        assert response.url == reverse("diary:entry_detail", args=[entry.pk])

    def test_edit_post_invalid(self, authenticated_client, entry):
        data = {"title": "", "content": ""}
        response = authenticated_client.post(
            reverse("diary:entry_edit", args=[entry.pk]), data
        )
        assert response.status_code == 200
        assert response.context["form"].errors

    def test_edit_another_user_404(self, authenticated_client, another_user):
        from diary.models import Entry

        other_entry = Entry.objects.create(
            title="Чужая", content="...", author=another_user
        )
        response = authenticated_client.get(
            reverse("diary:entry_edit", args=[other_entry.pk])
        )
        assert response.status_code == 404


class TestEntryDelete:
    def test_delete_get_confirmation(self, authenticated_client, entry):
        response = authenticated_client.get(
            reverse("diary:entry_delete", args=[entry.pk])
        )
        assert response.status_code == 200
        assert response.context["entry"] == entry

    def test_delete_post(self, authenticated_client, entry):
        response = authenticated_client.post(
            reverse("diary:entry_delete", args=[entry.pk])
        )
        assert response.status_code == 302
        assert response.url == reverse("diary:entry_list")
        from diary.models import Entry

        assert not Entry.objects.filter(pk=entry.pk).exists()

    def test_delete_another_user_404(self, authenticated_client, another_user):
        from diary.models import Entry

        other_entry = Entry.objects.create(
            title="Чужая", content="...", author=another_user
        )
        response = authenticated_client.get(
            reverse("diary:entry_delete", args=[other_entry.pk])
        )
        assert response.status_code == 404
