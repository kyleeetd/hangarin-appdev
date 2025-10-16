from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Category, Priority, Task, SubTask, Note
from .forms import CategoryForm, PriorityForm, TaskForm, SubTaskForm, NoteForm

# Helper ListView that supports ?q=search & ?order=field
class BaseListView(ListView):
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        order = self.request.GET.get('order')
        if q:
            # naive search in title/description if present
            if hasattr(self.model, 'title'):
                qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
            elif hasattr(self.model, 'name'):
                qs = qs.filter(name__icontains=q)
        if order:
            qs = qs.order_by(order)
        return qs

# -------------------- TASK VIEWS --------------------
class TaskListView(BaseListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")

# -------------------- CATEGORY VIEWS --------------------
class CategoryListView(BaseListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/form.html"
    success_url = reverse_lazy("category-list")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/form.html"
    success_url = reverse_lazy("category-list")

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "categories/del.html"
    success_url = reverse_lazy("category-list")

# -------------------- PRIORITY VIEWS --------------------
class PriorityListView(BaseListView):
    model = Priority
    template_name = "priorities/list.html"
    context_object_name = "priorities"

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priorities/form.html"
    success_url = reverse_lazy("priority-list")

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = "priorities/form.html"
    success_url = reverse_lazy("priority-list")

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = "priorities/del.html"
    success_url = reverse_lazy("priority-list")

# -------------------- SUBTASK VIEWS --------------------
class SubTaskListView(BaseListView):
    model = SubTask
    template_name = "subtasks/list.html"
    context_object_name = "subtasks"

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtasks/form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = "subtasks/form.html"
    success_url = reverse_lazy("subtask-list")

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = "subtasks/del.html"
    success_url = reverse_lazy("subtask-list")

# -------------------- NOTE VIEWS --------------------
class NoteListView(BaseListView):
    model = Note
    template_name = "notes/list.html"
    context_object_name = "notes"

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/form.html"
    success_url = reverse_lazy("note-list")

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/form.html"
    success_url = reverse_lazy("note-list")

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "notes/del.html"
    success_url = reverse_lazy("note-list")

# -------------------- DASHBOARD --------------------
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task_count'] = Task.objects.count()
        ctx['done_count'] = Task.objects.filter(status='done').count()
        ctx['pending_count'] = Task.objects.filter(status='pending').count()
        ctx['categories'] = Category.objects.annotate(task_count=Count('task')).order_by('-task_count')[:5]
        ctx['priorities'] = Priority.objects.annotate(task_count=Count('task')).order_by('-task_count')[:5]
        return ctx
