from random import choice
import pymorphy2


def tag_value(slovo, number_v_slovare, tag): 
    """
    (слово, номер в словаре, тэг) = значение тэга
    gender, number, animacy
    """
    if tag == "gender":
        return morph.parse(slovo)[number_v_slovare].tag.gender
    elif tag == "number":
        return morph.parse(slovo)[number_v_slovare].tag.number
    elif tag == "animacy":
        return morph.parse(slovo)[number_v_slovare].tag.animacy


#=====================================================
morph = pymorphy2.MorphAnalyzer(lang='ru')

sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы']
prilag_mass = ['голубой', 'анимешный', '']
prinadl_mass = ['конь', 'кошкодевка']
from_mass = ['Дагестан', 'США', "пещера"]

words = [choice(sush_mass)]
prilag = choice(prilag_mass)
padezh = choice(['gent', 'ablt', '']) # родит. - gent, творит. - ablt
choose_from = choice(['gent', ''])

if words[0] == 'гей':
    gender = tag_value(words[0], 1, 'gender')
    number = tag_value(words[0], 1, 'number')
else:
    try:
        gender = tag_value(words[0], 0, 'gender')
        number = tag_value(words[0], 0, 'number')
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

if padezh:
    prinadl = choice(prinadl_mass)
    if tag_value(words[-1], 0, 'animacy') == 'anim' and padezh == 'ablt':
        words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
        words += [morph.parse(prinadl)[0].inflect({padezh}).word]
    elif tag_value(words[-1], 0, 'animacy') == 'inan' and padezh == 'gent':
        words += [morph.parse(prinadl)[0].inflect({padezh}).word]

if choose_from:
    from_ = morph.parse(choice(from_mass))[0].inflect({choose_from})
    if 'Abbr' in from_.tag:
        from_ = from_.word.upper()
    elif 'Geox' in from_.tag:
        from_ = from_.word.capitalize()
    else:
        from_ = from_.word
    words += ['из ' + from_]


print(' '.join(words))
