from django import forms
from .models import Category, Priority, Task, SubTask, Note

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['level']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'due_date', 'status']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['task', 'title', 'completed']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'content']
