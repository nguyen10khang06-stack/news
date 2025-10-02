from django import forms
from .models import News # Import Model News

class NewsForm(forms.ModelForm):
    """Form dùng để tạo hoặc chỉnh sửa một bài viết News."""
    class Meta:
        model = News
        # Chỉ cho phép chỉnh sửa các trường này. Bỏ qua created_at, views, slug...
        fields = ['title', 'content', 'category', 'image']