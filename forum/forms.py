from django import forms
from .models import Thread, Post, Category

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': '카테고리 이름',
            'description': '설명',
        }