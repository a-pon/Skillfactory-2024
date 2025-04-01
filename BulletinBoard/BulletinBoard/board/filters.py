from django_filters import FilterSet

from .models import Respond


class RespondFilter(FilterSet):
    class Meta:
        model = Respond
        fields = {
            'advert__header': ['icontains'],
        }
