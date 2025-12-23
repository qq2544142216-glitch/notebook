from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Note(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="Приоритет"
    )
    is_completed = models.BooleanField(default=False, verbose_name="Выполнено")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ['-created_at']
        permissions = [
            ("can_view_note", "Может просматривать заметки"),
            ("can_add_note", "Может добавлять заметки"),
            ("can_change_note", "Может изменять заметки"),
            ("can_delete_note", "Может удалять заметки"),
            ("can_search_note", "Может искать заметки"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'pk': self.pk})