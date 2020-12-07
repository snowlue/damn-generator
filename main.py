from random import choice
import pymorphy2


morph = pymorphy2.MorphAnalyzer(lang='ru')

sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы']
prilag_mass = ['голубой', 'анимешный', '']
prinadl_mass = ['конь', 'кошкодевка']
from_mass = ['Дагестан', 'США']
choose = choice(['gent', 'ablt', ''])
choose_country = choice(['gent', ''])

words = [choice(sush_mass)]
prilag = choice(prilag_mass)

if words[0] == 'гей':
    gender = morph.parse(words[0])[1].tag.gender
    number = morph.parse(words[0])[1].tag.number
else:
    try:
        gender = morph.parse(words[0])[0].tag.gender
        number = morph.parse(words[0])[0].tag.number
        if number == 'plur':
            morph.parse(prilag)[0].inflect({number})
        else:
            morph.parse(prilag)[0].inflect({gender})
    except Exception:
        gender = 'neut'
        number = 'sing'
if prilag:
    if number == 'plur':
        words = [morph.parse(prilag)[0].inflect({number}).word] + [words[0]]
    else:
        words = [morph.parse(prilag)[0].inflect({gender}).word] + [words[0]]

if choose:
    pr = choice(prinadl_mass)
    if morph.parse(words[-1])[0].tag.animacy == 'anim' and choose == 'ablt':
        words += ['c' if not pr.startswith('с') or pr.startswith('со') else 'co']
        words += [morph.parse(pr)[0].inflect({choose}).word]
    elif morph.parse(words[-1])[0].tag.animacy == 'inan' and choose == 'gent':
        words += [morph.parse(pr)[0].inflect({choose}).word]

if choose_country:
    c = morph.parse(choice(from_mass))[0].inflect({choose_country})
    if 'Abbr' in c.tag:
        c = c.word.upper()
    elif 'Geox' in c.tag:
        c = c.word.capitalize()
    else:
        c = c.word
    words += ['из ' + c]


print(' '.join(words))
