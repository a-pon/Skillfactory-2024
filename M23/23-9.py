python manage.py shell

from news.models import Author, Category, Post, PostCategory, Comment
from django.contrib.auth.models import User

user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

category1 = Category.objects.create(name='sport')
category2 = Category.objects.create(name='nature')
category3 = Category.objects.create(name='it')
category4 = Category.objects.create(name='space')

news1h = 'HEROIC Obliterate Astralis To Secure A Spot At IEM Dallas 2025'
news1c = '''HEROIC have secured the final spot at IEM Dallas 2025 after delivering a crushing 2-0 defeat to Astralis in the lower bracket final of Europe’s closed qualifier.
HEROIC came out swinging on Mirage, quickly establishing a 9-3 lead at halftime. The second half was even more brutal for Astralis, as they failed to secure a single T-side round. HEROIC shut them out entirely, closing the map with a comfortable 13-3 victory. Yasin Yasin "xfl0ud" Koç was the standout performer on this map, delivering a phenomenal 2.63 rating performance to completely destroy Astralis on their CT-side.
Nuke turned out to be an even worse match-to-forget for Astralis, as HEROIC stormed through the first half, racing to an 11-0 lead, fueled by an incredible showing from Simon "yxngstxr" Boije, who matched xfl0ud’s 2..63 rating on this map. Astralis finally managed to get on the board with a CT-side round, but the damage was already done. Despite a brief moment of success in the second half, where they secured two rounds, Astralis had no chance of mounting a comeback. HEROIC sealed the deal with a 13-2 win, booking their ticket to IEM Dallas.
With Astralis recently returning from PGL Cluj-Napoca, HEROIC had the advantage of extra preparation time. However, it’s also important to address Astralis’ visibly poor performance, as they struggled throughout, squandering four crucial two-man advantages across the series. Zooming out on the results, cadiaN and his team suffered a crushing 5-26 defeat in total against their former organization.
HEROIC now join the list of European teams qualifying for the $300,000 LAN event, but they had somewhat of a rocky start in the beginning of the qualifier. They began the tournament with a 2-1 victory over Zero Tenacity, which was followed by a drop to the lower brackets thanks to a loss to 3DMAX. However, they made an impressive comeback defeating BIG, Metizport, and finally, Astralis to reach Dallas.'''

post1h = 'How AI is revealing the language of the birds'
post1c = '''Crows make a huge number of different sounds; Artificial Intelligence could help us understand what they mean.
Researchers have been eavesdropping on an unusual family of crows in Spain, collecting data on hundreds of thousands of different sounds the birds made. Small microphones recorded a variety of soft calls, far quieter than the familiar 'caws' people usually hear. The team then used AI to analyse the sounds and group them together. The researchers hope is to one day be able to understand the meaning of the birds' vocalisations and perhaps even try to speak their language.'''

post2h = 'Asteroid 2024 YR4 now unlikely to hit Earth — but scientists are ready for future threats'
post2c = '''Objects that could strike the planet will be spotted more regularly as new asteroid-hunting telescopes come online.
The latest calculations indicate that the asteroid known as 2024 YR4 is much less likely to hit Earth than earlier measurements had suggested. Late on 19 February, telescope observations of the object allowed researchers to revise down the estimated chance of impact in 2032 from 3.1% — the greatest such threat ever recorded — to a still-worrying 1.5%.
This value is likely to fall even further, to less than 1%, says Richard Moissl, head of the European Space Agency’s Planetary Defence Office, based in Frascati, Italy. As data floods in, uncertainty regarding 2024 YR4’s ‘impact corridor’ — the path it will take in the vicinity of Earth — is shrinking. If, as the uncertainty in an asteroid’s path gets smaller, Earth’s orbit remains within it, the likelihood of impact grows — which is why, earlier this week, space agencies reported that the risk had climbed. But now Earth is on the fringes of this region and edging out.
YR4 has given researchers their first chance to test an international protocol for responding to such hazards, put in place after the Chelyabinsk meteor hit Earth in 2013 without any warning. And with new asteroid-hunting telescopes coming online all the time, astronomers are likely to see many more close calls, says Moissl. “It’s not if, it’s when.”'''

news1 = Post.objects.create(author=author1, type=news, header=news1h, content=news1c)
post1 = Post.objects.create(author=author2, header=post1h, content=post1c)
post2 = Post.objects.create(author=author2, header=post2h, content=post2c)

news1.categories.add(1,3)
post1.categories.add(2,3)
post2.categories.add(4)

comment1 = Comment.objects.create(post=news1, user=user2, content='Lorem ipsum dolor sit amet')
comment2 = Comment.objects.create(post=post1, user=user1, content='Consectetur adipiscing elit')
comment3 = Comment.objects.create(post=post1, user=user2, content='Sed do eiusmod tempor incididunt')
comment4 = Comment.objects.create(post=post2, user=user1, content='Ut enim ad minim veniam')

news1.like()
post1.like()
post1.dislike()
post2.dislike()
comment1.like()
comment2.dislike()
comment3.dislike()
comment4.dislike()

author1.update_rating()
author2.update_rating()

print(Author.objects.all().order_by('-rating').values('user__username', 'rating')[0])

print(Post.objects.all().order_by('-rating').values('time', 'author__user__username', 'rating', 'header')[0])
print(Post.objects.all().order_by('-rating')[0].preview())

best_post = Post.objects.all().order_by('-rating')[0]
print(Comment.objects.filter(post=best_post).values('time', 'user__username', 'rating', 'content'))
