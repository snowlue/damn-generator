from random import choice
import pymorphy2


def tag_value(slovo, number_v_slovare, tag_slova): # gender, number, animacy
    if tag_slova == "gender":
        return morph.parse(slovo)[number_v_slovare].tag.gender
    elif tag_slova == "number":
        return morph.parse(slovo)[number_v_slovare].tag.number
    elif tag_slova == "animacy":
        return morph.parse(slovo)[number_v_slovare].tag.animacy


def inflect(slovo, number_v_slovare, charact):
    return morph.parse(slovo)[number_v_slovare].inflect({charact})


#=====================================================
morph = pymorphy2.MorphAnalyzer(lang='ru')

sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы']
prilag_mass = ['голубой', 'анимешный', '']
prinadl_mass = ['конь', 'кошкодевка']
from_mass = ['Дагестан', 'США']
choose = choice(['gent', 'ablt', '']) # родит. - gent, творит. - ablt
choose_country = choice(['gent', ''])

words = [choice(sush_mass)]
prilag = choice(prilag_mass)

if words[0] == 'гей':
    gender = tag_value(words[0], 1, 'gender')
    number = tag_value(words[0], 1, 'number')
else:
    try:
        gender = tag_value(words[0], 0, 'gender')
        number = tag_value(words[0], 0, 'number')
        if number == 'plur':
            morph.parse(prilag)[0].inflect({number}) #inflect(prilag, 0, "number")
        else:
            morph.parse(prilag)[0].inflect({gender}) #inflect(prilag, 0, "gender")
    except Exception:
        gender = 'neut'
        number = 'sing'

if prilag:
    if number == 'plur':
        words = [morph.parse(prilag)[0].inflect({number}).word] + [words[0]]
    else:
        words = [morph.parse(prilag)[0].inflect({gender}).word] + [words[0]]

if choose:
    prinadl = choice(prinadl_mass)
    if tag_value(words[-1], 0, 'animacy') == 'anim' and choose == 'ablt':
        words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
        words += [morph.parse(prinadl)[0].inflect({choose}).word]
    elif tag_value(words[-1], 0, 'animacy') == 'inan' and choose == 'gent':
        words += [morph.parse(prinadl)[0].inflect({choose}).word]

if choose_country:
    country = morph.parse(choice(from_mass))[0].inflect({choose_country})
    if 'Abbr' in country.tag:
        country = country.word.upper()
    elif 'Geox' in country.tag:
        country = country.word.capitalize()
    else:
        country = country.word
    words += ['из ' + country]


print(' '.join(words))
