from random import choice
from typing import Set
import pymorphy2
from pymorphy2.analyzer import Parse


def get_tag(word: str, tag: str, num_in_list: int = 0):
    """
    (слово, тег, номер в списке рез-ов) -> значение тега
    """
    if tag == 'род':
        return morph.parse(word)[num_in_list].tag.gender
    elif tag == 'число':
        return morph.parse(word)[num_in_list].tag.number
    elif tag == 'одуш':
        return morph.parse(word)[num_in_list].tag.animacy
    elif tag == 'падеж':
        return morph.parse(word)[num_in_list].tag.case


def inflector(word: str or Parse, tags: Set[str], num_in_list: int = 0):
    """
    (слово | объект Parse, теги, номер в списке рез-ов) -> объект Parse
    """
    if isinstance(word, Parse):
        return word.inflect(tags)
    else:
        a = morph.parse(word)
        return morph.parse(word)[num_in_list].inflect(tags)


morph = pymorphy2.MorphAnalyzer(lang='ru')

# =====================================================
sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы', 'ублюдки', 'Фёдор', 'Диляра Равильевна']
prilag_mass = ['голубой', 'анимешный', 'тупой', 'карликовый', 'опущенный', 'голодный']
prinadl_mass = ['шаболда', 'лошадь', 'кошкодевка', 'бомжи', '']
from_mass = ['Дагестан', 'США', 'пещера', 'помойка', '']
glagol_mass = ['толкает', 'уничтожает', 'долбится', 'насилует', 'ест', 'бьёт', '']

padezh_prinadl = choice(['gent', 'ablt'])  # gent — родит., ablt - творит., accs - винит., accs - предл.
padezh_from = choice(['gent', 'loct'])

words = [choice(sush_mass)]
prilag = choice(prilag_mass)
prinadl = choice(prinadl_mass)
glagol = choice(glagol_mass)
from_ = inflector(choice(from_mass), {padezh_from})
sush = words[0]

case = ''

# СБОР ИНФОРМАЦИИ О СУЩЕСТВИТЕЛЬНОМ
if sush == 'гей':
    gender = get_tag(sush, 'род', 1)
    number = get_tag(sush, 'число', 1)
    case = 'nomn'
else:
    try:
        gender = get_tag(sush, 'род')
        number = get_tag(sush, 'число')
        if number == 'plur':
            inflector(prilag, {number})
        else:
            inflector(prilag, {gender})
    except Exception:
        gender = 'neut'
        number = 'sing'
        case = 'nomn'

# ДОБАВЛЕНИЕ ПРИЛАГАТЕЛЬНОГО
if prilag:  # если есть слово
    if not case:
        case = get_tag(sush, 'падеж')
    if number == 'plur':
        words = [inflector(prilag, {number, case}).word.capitalize()] + [sush]
    else:
        words = [inflector(prilag, {gender, case}).word.capitalize()] + [sush]
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
    if get_tag(sush, 'одуш') == 'anim' and padezh_prinadl == 'ablt':
        if from_:
            words += locate
        if glagol:  # глагол?
            if 'intr' in morph.parse(glagol)[0].tag:  # совершенный вид
                if number == 'plur':
                    words += [inflector(glagol, {number}).word]
                else:
                    words += [glagol]
                words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
                words += [inflector(prinadl, {'ablt'}).word]
            elif 'tran' in morph.parse(glagol)[0].tag:
                if number == 'plur':
                    words += [inflector(glagol, {number}).word]
                else:
                    words += [glagol]
                words += [inflector(prinadl, {'accs'}).word]
        else:  # нет глагола
            words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
            words += [inflector(prinadl, {'ablt'}).word]
    elif get_tag(sush, 'одуш') == 'inan' and padezh_prinadl == 'gent':
        words += [inflector(prinadl, {padezh_prinadl}).word]
        if from_:
            words += locate

print(' '.join(words))
