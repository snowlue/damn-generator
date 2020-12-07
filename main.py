from random import choice
import pymorphy2


def tag_val(slovo, number_v_slovare, tag): 
    """
    (слово, номер в словаре, тэг) = значение тэга
    gender, number, animacy
    """
    if tag == "gen":
        return morph.parse(slovo)[number_v_slovare].tag.gender
    elif tag == "num":
        return morph.parse(slovo)[number_v_slovare].tag.number
    elif tag == "ani":
        return morph.parse(slovo)[number_v_slovare].tag.animacy
    elif tag == "cas":
        return morph.parse(slovo)[number_v_slovare].tag.case


morph = pymorphy2.MorphAnalyzer(lang='ru')

#=====================================================
sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы', 'ублюдки', 'Фёдор', 'Диляра Равильевна']
prilag_mass = ['голубой', 'анимешный', 'тупой', 'карликовый', 'опущенный','']
prinadl_mass = ['шаболда', 'лошадь', 'кошкодевка', 'бомжи']
from_mass = ['Дагестан', 'США', 'пещера', 'помойка']
glagol_mass = ['толкает', 'уничтожает', 'долбится','насилует','ест', 'бьёт', '']

words = [choice(sush_mass)]
sush = words[0]
prilag = choice(prilag_mass)
padezh_prinadl = choice(['gent', 'ablt', '']) # родит. - gent, творит. - ablt, винит. - accs, предл. - loct
choose_from = choice(['gent', 'loct', ''])
glagol = choice(glagol_mass)
case = ''

if sush == 'гей': #сбор информации о существительном
    gender = tag_val(sush, 1, 'gen') #morph.parse(words[0])[1].tag.gender
    number = tag_val(sush, 1, 'num') #morph.parse(words[0])[1].tag.number
    case = 'nomn'
else:
    try:
        gender = tag_val(sush, 0, 'gen') #morph.parse(words[0])[0].tag.gender
        number = tag_val(sush, 0, 'num') #morph.parse(words[0])[0].tag.number
        if number == 'plur':
            morph.parse(prilag)[0].inflect({number})
        else:
            morph.parse(prilag)[0].inflect({gender})
    except Exception:
        gender = 'neut'
        number = 'sing'
        case = 'nomn'

if prilag: #если есть слово
    if case == '':
        case = tag_val(sush, 0, 'cas')
    if number == 'plur':
        words = [morph.parse(prilag)[0].inflect({number, case}).word] + [sush]
    else:
        words = [morph.parse(prilag)[0].inflect({gender, case}).word] + [sush]

if choose_from: #если есть падеж, значит есть и слово
    from_ = morph.parse(choice(from_mass))[0].inflect({choose_from})
    if 'Abbr' in from_.tag:
        from_ = from_.word.upper()
    elif 'Geox' in from_.tag:
        from_ = from_.word.capitalize()
    else:
        from_ = from_.word
    if choose_from == "gent":
        locate = ['из ' + from_]
    elif choose_from == "loct":
        locate = ['в ' + from_]

if padezh_prinadl: #если есть падеж, значит есть и слово
    prinadl = choice(prinadl_mass)
    if tag_val(sush, 0, 'ani') == 'anim' and padezh_prinadl == 'ablt':
        if choose_from:
            words += locate
        if glagol: #глагол?
            if 'intr' in morph.parse(glagol)[0].tag: #совершенный вид
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
        else: #нет глагола
            words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
            words += [morph.parse(prinadl)[0].inflect({'ablt'}).word]
    elif tag_val(sush, 0, 'ani') == 'inan' and padezh_prinadl == 'gent':
        words += [morph.parse(prinadl)[0].inflect({padezh_prinadl}).word]
        if choose_from:
            words += locate

words[0] = words[0].capitalize()
print(' '.join(words))
