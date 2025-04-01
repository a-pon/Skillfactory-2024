from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Advert(models.Model):
    tank,heal,dd,trade,guild,quest,smith,leather,potion,spell=(
        'TA','HE','DD','TR','GM','QG','SM','LW','PB','SM')
    CATEGORIES = [
        (tank, 'Танки'),
        (heal, 'Хилы'),
        (dd, 'ДД'),
        (trade, 'Торговцы'),
        (guild, 'Гилдмастеры'),
        (quest, 'Квестгиверы'),
        (smith, 'Кузнецы'),
        (leather, 'Кожевники'),
        (potion, 'Зельевары'),
        (spell, 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    header = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.id)])


class Respond(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
