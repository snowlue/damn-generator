from random import choice
import pymorphy2


def get_tag(slovo, num_in_dict, tag):
    """
    (слово, номер в словаре, тег) = значение тега
    gender, number, animacy
    """
    if tag == "род":
        return morph.parse(slovo)[num_in_dict].tag.gender
    elif tag == "число":
        return morph.parse(slovo)[num_in_dict].tag.number
    elif tag == "одуш":
        return morph.parse(slovo)[num_in_dict].tag.animacy
    elif tag == "падеж":
        return morph.parse(slovo)[num_in_dict].tag.case


morph = pymorphy2.MorphAnalyzer(lang='ru')

# =====================================================
sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы', 'ублюдки', 'Фёдор', 'Диляра Равильевна']
prilag_mass = ['голубой', 'анимешный', 'тупой', 'карликовый', 'опущенный', '']
prinadl_mass = ['шаболда', 'лошадь', 'кошкодевка', 'бомжи', '']
from_mass = ['Дагестан', 'США', 'пещера', 'помойка', '']
glagol_mass = ['толкает', 'уничтожает', 'долбится', 'насилует', 'ест', 'бьёт', '']

padezh_prinadl = choice(['gent', 'ablt']) # родит. - gent, творит. - ablt, винит. - accs, предл. - loct
padezh_from = choice(['gent', 'loct'])

words = [choice(sush_mass)]
prilag = choice(prilag_mass)
prinadl = choice(prinadl_mass)
glagol = choice(glagol_mass)
from_ = morph.parse(choice(from_mass))[0].inflect({padezh_from})
sush = words[0]

case = ''

# СБОР ИНФОРМАЦИИ О СУЩЕСТВИТЕЛЬНОМ
if sush == 'гей':
    gender = get_tag(sush, 1, 'род')
    number = get_tag(sush, 1, 'число')
    case = 'nomn'
else:
    try:
        gender = get_tag(sush, 0, 'род')
        number = get_tag(sush, 0, 'число')
        if number == 'plur':
            morph.parse(prilag)[0].inflect({number})
        else:
            morph.parse(prilag)[0].inflect({gender})
    except Exception:
        gender = 'neut'
        number = 'sing'
        case = 'nomn'

# ДОБАВЛЕНИЕ ПРИЛАГАТЕЛЬНОГО
if prilag:  # если есть слово
    if case == '':
        case = get_tag(sush, 0, 'падеж')
    if number == 'plur':
        words = [morph.parse(prilag)[0].inflect({number, case}).word.capitalize()] + [sush]
    else:
        words = [morph.parse(prilag)[0].inflect({gender, case}).word.capitalize()] + [sush]
else:
    capital = sush.split()
    words = [capital[0].capitalize()] + capital[1:]

# ВЫЧИСЛЕНИЕ ПРИНАДЛЕЖНОСТИ
if from_:
    if 'Abbr' in from_.tag:
        from_ = from_.word.upper()
    elif 'Geox' in from_.tag:
        from_ = from_.word.capitalize()
    else:
        from_ = from_.word
    if padezh_from == "gent":
        locate = ['из ' + from_]
    elif padezh_from == "loct":
        locate = ['в ' + from_]

# ДОБАВЛЕНИЕ ГЛАГОЛА И ПРИНАДЛЕЖНОСТИ
if prinadl:  # если есть падеж, значит есть и слово
    if get_tag(sush, 0, 'одуш') == 'anim' and padezh_prinadl == 'ablt':
        if from_:
            words += locate
        if glagol:  # глагол?
            if 'intr' in morph.parse(glagol)[0].tag:  # совершенный вид
                if number == 'plur':
                    words += [morph.parse(glagol)[0].inflect({number}).word]
                else:
                    words += [glagol]
                words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
                words += [morph.parse(prinadl)[0].inflect({'ablt'}).word]
            elif 'tran' in morph.parse(glagol)[0].tag:
                if number == 'plur':
                    words += [morph.parse(glagol)[0].inflect({number}).word]
                else:
                    words += [glagol]
                words += [morph.parse(prinadl)[0].inflect({'accs'}).word]
        else:  # нет глагола
            words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
            words += [morph.parse(prinadl)[0].inflect({'ablt'}).word]
    elif get_tag(sush, 0, 'одуш') == 'inan' and padezh_prinadl == 'gent':
        words += [morph.parse(prinadl)[0].inflect({padezh_prinadl}).word]
        if from_:
            words += locate

print(' '.join(words))
