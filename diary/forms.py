from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from diary.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Заголовок"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Текст записи...",
                }
            ),
        }


