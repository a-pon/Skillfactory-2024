from django import forms
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    time = DateFilter(
        field_name='time',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'author__user__username': ['icontains'],
        }
