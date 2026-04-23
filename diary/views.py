from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm
from .models import Entry




@login_required
def my_entries_list(request):
    """
    Отображает список всех записей текущего пользователя.
    Доступно только авторизованным.
    """
    # Фильтруем записи по автору = текущий пользователь
    entries = Entry.objects.filter(author=request.user)

    context = {
        "entries": entries,
        "entry_count": entries.count(),
    }
    return render(request, "diary/entry_list.html", context)


@login_required
def entry_detail(request, pk):
    """Просмотр одной записи"""
    entry = get_object_or_404(Entry, pk=pk, author=request.user)
    return render(request, "diary/entry_detail.html", {"entry": entry})


@login_required
def entry_create(request):
    """Создание новой записи"""
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            messages.success(request, "Запись создана!")
            return redirect("diary:entry_detail", pk=entry.pk)
    else:
        form = EntryForm()
    return render(
        request, "diary/entry_form.html", {"form": form, "title": "Новая запись"}
    )


@login_required
def entry_edit(request, pk):
    """Редактирование записи"""
    entry = get_object_or_404(Entry, pk=pk, author=request.user)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена!")
            return redirect("diary:entry_detail", pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
    return render(
        request, "diary/entry_form.html", {"form": form, "title": "Редактирование"}
    )


@login_required
def entry_delete(request, pk):
    """Удаление записи с подтверждением"""
    entry = get_object_or_404(Entry, pk=pk, author=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Запись удалена!")
        return redirect("diary:entry_list")
    return render(request, "diary/entry_confirm_delete.html", {"entry": entry})
