from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=10)
    contents = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["title", "contents", "main_image"]
        # fields = "__all__"
