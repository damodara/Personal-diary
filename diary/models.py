from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # новые записи сверху

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("diary:entry_detail", args=[str(self.id)])
