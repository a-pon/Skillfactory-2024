from django import template

register = template.Library()

BADWORDS = ['Asteroid', 'asteroid', 'Bird', 'bird', 'Spot', 'spot']


@register.filter()
def censor(sentence):
    if isinstance(sentence, str):
        sentence = sentence.split()

        for i, word in enumerate(sentence):
            if any(badword in word for badword in BADWORDS):
                sentence[i] = f'{word[0]}' + ''.join(['*' if c.isalpha() else c for c in word[1:]])

        return ' '.join(sentence)
    else:
        raise TypeError('not a string')
