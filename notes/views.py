from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
from .models import Note
from .forms import NoteForm, NoteSearchForm

class NoteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 5
    permission_required = 'notes.can_view_note'
    
    def get_queryset(self):
        # 获取基础查询集 - 只获取当前用户的笔记
        queryset = Note.objects.filter(author=self.request.user).order_by('-created_at')
        
        # 搜索功能
        search_form = NoteSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data['search']:
            if self.request.user.has_perm('notes.can_search_note'):
                search_term = search_form.cleaned_data['search']
                queryset = queryset.filter(
                    Q(title__icontains=search_term) | 
                    Q(content__icontains=search_term)
                )
            else:
                messages.error(self.request, 'У вас нет прав для поиска заметок')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = NoteSearchForm(self.request.GET)
        
        # 为统计信息准备数据
        notes = context.get('notes', [])
        
        # 统计各种优先级和完成状态的笔记数量
        high_count = medium_count = low_count = completed_count = 0
        
        # 如果是分页后的查询集，需要重新查询统计信息
        if hasattr(self, 'object_list'):
            # 重新查询以避免切片问题
            base_queryset = Note.objects.filter(author=self.request.user)
            
            # 如果有搜索条件，应用搜索过滤
            search_form = NoteSearchForm(self.request.GET)
            if search_form.is_valid() and search_form.cleaned_data['search']:
                if self.request.user.has_perm('notes.can_search_note'):
                    search_term = search_form.cleaned_data['search']
                    base_queryset = base_queryset.filter(
                        Q(title__icontains=search_term) | 
                        Q(content__icontains=search_term)
                    )
            
            # 统计数量
            high_count = base_queryset.filter(priority='high').count()
            medium_count = base_queryset.filter(priority='medium').count()
            low_count = base_queryset.filter(priority='low').count()
            completed_count = base_queryset.filter(is_completed=True).count()
        
        context['high_count'] = high_count
        context['medium_count'] = medium_count
        context['low_count'] = low_count
        context['completed_count'] = completed_count
        
        return context

class NoteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'
    permission_required = 'notes.can_view_note'
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

class NoteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    permission_required = 'notes.can_add_note'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Заметка успешно создана!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новой заметки'
        return context
    
    def get_success_url(self):
        return reverse_lazy('note_list')

class NoteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    permission_required = 'notes.can_change_note'
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Заметка успешно обновлена!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование заметки: {self.object.title}'
        return context
    
    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})

class NoteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    permission_required = 'notes.can_delete_note'
    
    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Заметка успешно удалена!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('note_list')