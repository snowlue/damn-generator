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


# gent — родит., ablt - творит., accs - винит., accs - предл.
padezh_prinadl = choice(['gent', 'ablt'])
padezh_from = choice(['gent', 'loct'])

words, prilag = [choice(sush_mass)], choice(prilag_mass)
prinadl, glagol, from_ = choice(prinadl_mass), choice(glagol_mass), choice(from_mass)
# words, prilag, prinadl, glagol, from_  = ['ниггер'], 'тупой', 'рабы', 'обосраться', 'наркопритон'
sush = words[0]

# СБОР ИНФОРМАЦИИ О СУЩЕСТВИТЕЛЬНОМ
if sush == 'гей':
    gender, number = 'masc', 'sing'
elif sush == 'Диляра Равильевна':
    gender, number = 'femn', 'sing'
else:
    sush = sush.split()[0] if len(sush.split()) > 1 else sush
    gender = get_tag(sush, 'род')
    number = get_tag(sush, 'число')
    try:
        if number == 'plur':
            inflector(prilag, {number})
        else:
            inflector(prilag, {gender})
    except Exception:
        gender, number = 'neut', 'sing'

# ДОБАВЛЕНИЕ ПРИЛАГАТЕЛЬНОГО
if prilag:  # если есть слово
    if number == 'plur':
        words = [inflector(prilag, {number, case}).word.capitalize()] + [sush]
    else:
        words = [inflector(prilag, {gender, case}).word.capitalize()] + [sush]
else:
    capital = words[0].split()
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
        if glagol:
            if number == 'plur':
                if glagol.endswith('ся'):
                    words += [inflector(glagol, {number}).word]
                else:
                    words += [inflector(glagol, {number, '3per'}).word]
            else:
                if glagol.endswith('ся'):
                    words += [inflector(glagol, {gender}).word]
                else:
                    words += [inflector(glagol, {'3per'}).word]

            if 'intr' in morph.parse(glagol)[0].tag:  # совершенный вид
                words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
                words += [inflector(prinadl, {'ablt'}).word]
            elif 'tran' in morph.parse(glagol)[0].tag:
                words += [inflector(prinadl, {'accs'}).word]
        else:  # нет глагола
            words += ['c' if not prinadl.startswith('с') or prinadl.startswith('со') else 'co']
            words += [inflector(prinadl, {'ablt'}).word]
    elif get_tag(sush, 'одуш') == 'inan' and padezh_prinadl == 'gent':
        words += [inflector(prinadl, {padezh_prinadl}).word]
        if from_:
            words += locate

print(' '.join(words))
