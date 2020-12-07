from random import choice
import pymorphy2


morph = pymorphy2.MorphAnalyzer(lang='ru')

ass = ['жопа', 'ниггер', 'принцесса', 'очко',
       'пидор', 'Ъ', 'гей', 'босс', 'кожевник',
       'залупа', 'мусор', 'Максим', 'Боб', 'выборы']
pril = ['голубой', 'разорванный', 'треснувший', 'красный',
        'продажный', 'поехавший', 'обдолбанный', 'анальный',
        'чёрный', 'тюремный', 'анимешный', 'путинский', '']
prinadl = ['собака', 'конь', 'слон', 'кошкодевка', 'гном']
from_ = ['Дагестан', 'Чечня', 'Украина', 'США', 'Венесуэла', 'ФСБ']
choose = choice(['gent', 'ablt', ''])
choose_country = choice(['gent', ''])


words = [choice(ass)]
p = choice(pril)

if words[0] == 'гей':
    gender = morph.parse(words[0])[1].tag.gender
    number = morph.parse(words[0])[1].tag.number
else:
    try:
        gender = morph.parse(words[0])[0].tag.gender
        number = morph.parse(words[0])[0].tag.number
        if number == 'plur':
            morph.parse(p)[0].inflect({number})
        else:
            morph.parse(p)[0].inflect({gender})
    except Exception:
        gender = 'neut'
        number = 'sing'
if p:
    if number == 'plur':
        words = [morph.parse(p)[0].inflect({number}).word] + [words[0]]
    else:
        words = [morph.parse(p)[0].inflect({gender}).word] + [words[0]]

if choose:
    pr = choice(prinadl)
    if morph.parse(words[-1])[0].tag.animacy == 'anim' and choose == 'ablt':
        words += ['c' if not pr.startswith('с') or pr.startswith('со') else 'co']
        words += [morph.parse(pr)[0].inflect({choose}).word]
    elif morph.parse(words[-1])[0].tag.animacy == 'inan' and choose == 'gent':
        words += [morph.parse(pr)[0].inflect({choose}).word]

if choose_country:
    c = morph.parse(choice(from_))[0].inflect({choose_country})
    if 'Abbr' in c.tag:
        c = c.word.upper()
    elif 'Geox' in c.tag:
        c = c.word.capitalize()
    else:
        c = c.word
    words += ['из ' + c]


print(' '.join(words))
