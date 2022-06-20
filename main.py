from random import choice
from typing import Literal

import pymorphy2
from pymorphy2.analyzer import Parse


def get_tag(word: str, tag: Literal['род', 'число', 'одуш', 'падеж'], num_in_list: int = 0) -> None | str:
    """Выдаёт значение выбранного тега tag для слова word из базы pymorphy2.

    Параметры
    =========
    word: str
        слово, для которого осуществляется поиск тег
    tag: Literal['род', 'число', 'одуш', 'падеж']
        тег, характеризующий слово
    num_in_list: int = 0
        номер по порядку в списке результатов парсера pymorphy2
    """

    if tag == 'род':
        return morph.parse(word)[num_in_list].tag.gender
    if tag == 'число':
        return morph.parse(word)[num_in_list].tag.number
    if tag == 'одуш':
        return morph.parse(word)[num_in_list].tag.animacy
    if tag == 'падеж':
        return morph.parse(word)[num_in_list].tag.case
    return None


def inflector(word: str | Parse, tags: set[str], num_in_list: int = 0) -> Parse:
    """Возвращает объект Parse, в котором содержится слово word, склонённое по тегам tags.

    Параметры
    =========
    word: str | Parse
        слово или объект выдачи morph.parse()
    tag: set[str]
        множество тегов, по которым нужно просклонять слово
    num_in_list: int = 0
        номер по порядку в списке результатов парсера pymorphy2
    """
    if isinstance(word, Parse):
        return word.inflect(tags)
    return morph.parse(word)[num_in_list].inflect(tags)


morph = pymorphy2.MorphAnalyzer(lang='ru')

# =====================================================
nouns = ['жопа', 'ниггер', 'очко', 'Ъ', 'выборы', 'ублюдки', 'Фёдор',
         'Максим', 'мразь', 'пидор', 'мошонка',
         'анимешник', 'импотент', 'говно', 'мать Максима', 'спермотоксикозник',
         'транссексуал', 'уёбок', 'Барак Обама']
adjectives = ['голубой', 'анимешный', 'тупой', 'карликовый',
              'опущенный', 'голодный', 'новогодний', 'каловый', 'засранный']
affiliation = ['шаболда', 'лошадь', 'кошкодевка', 'бомжи',
               'говно', 'рабы', 'украинцы', 'чеченцы', '']
homes = ['Дагестан', 'США', 'пещера', 'помойка',
         'наркопритон', 'рабство', 'подвал', 'хата Феди', 'ноготь', 'Гейропа',
         'хрущёвка', '']
verbs = ['толкать', 'уничтожать', 'долбиться',
         'насиловать', 'жрать', 'бить', 'унижать',
         'заебаться', 'обосраться на', 'карать', 'дрочить на',
         'пытать', 'ссать на', 'блевать на']


def generate_one():
    # gent — родит., ablt - творит., accs - винит., accs - предл.
    case_affil, case_home = choice(['gent', 'ablt']), choice(['gent', 'loct'])

    words, adj = [choice(nouns)], choice(adjectives)
    affil, verb, home = choice(affiliation), choice(verbs), choice(homes)
    noun = words[0]

    # СБОР ИНФОРМАЦИИ О СУЩЕСТВИТЕЛЬНОМ
    noun = noun.split()[0] if len(noun.split()) > 1 else noun
    gender = get_tag(noun, 'род')
    number = get_tag(noun, 'число')
    try:
        if number == 'plur':
            inflector(adj, {number})
        else:
            inflector(adj, {gender})
    except Exception:
        gender, number = 'neut', 'sing'

    # ДОБАВЛЕНИЕ ПРИЛАГАТЕЛЬНОГО
    if adj:  # если есть слово
        adj_parser = morph.parse(adj)[0]
        if number == 'plur':
            words = [inflector(adj_parser, {number, 'nomn'}).word.capitalize()] + [words[0]]
        else:
            words = [inflector(adj_parser, {gender, 'nomn'}).word.capitalize()] + [words[0]]
    else:
        capital = words[0].split()
        words = [capital[0].capitalize()] + capital[1:]

    # ВЫЧИСЛЕНИЕ ПРИНАДЛЕЖНОСТИ
    if home:
        home = [home.split()[0], *home.split()[1:]] if len(home.split()) > 1 else [home]
        home_inf = inflector(home[0], {case_home})
        if 'Abbr' in home_inf.tag:
            home_inf = home_inf.word.upper()
        elif 'Geox' in home_inf.tag:
            home_inf = home_inf.word.capitalize()
        else:
            home_inf = home_inf.word

        if case_home == "gent":
            if home_inf == 'ногтя':
                locate = ['из-под ' + home_inf] + home[1:]
            else:
                locate = ['из ' + home_inf] + home[1:]
        elif case_home == "loct":
            locate = ['в ' + home_inf] + home[1:]

    # ДОБАВЛЕНИЕ ГЛАГОЛА И ПРИНАДЛЕЖНОСТИ
    if affil:  # если есть падеж, значит есть и слово
        if get_tag(noun, 'одуш') == 'anim' and case_affil == 'ablt':
            if home:
                words += locate
            if verb:
                verb, prepos = (verb.split()[0], verb.split()[1]) if len(verb.split()) == 2 else (verb, '')
                if number == 'plur':
                    if verb.endswith('ся'):
                        words += [inflector(verb, {number}).word]
                    else:
                        words += [inflector(verb, {number, '3per'}).word]
                else:
                    if verb.endswith('ся'):
                        words += [inflector(verb, {gender}).word]
                    else:
                        words += [inflector(verb, {'3per'}).word]

                if 'intr' in morph.parse(verb)[0].tag:  # совершенный вид
                    if prepos:
                        words += [prepos]
                        if affil != 'анимешники':
                            words += [inflector(affil, {'accs'}).word]
                        else:
                            words += [inflector(affil, {'gent'}).word]
                    else:
                        words += ['c' if not affil.startswith('с') or affil.startswith('со') else 'co']
                        words += [inflector(affil, {'ablt'}).word]
                elif 'tran' in morph.parse(verb)[0].tag:
                    if prepos:
                        words += [prepos]
                    if affil != 'анимешники':
                        words += [inflector(affil, {'accs'}).word]
                    else:
                        words += [inflector(affil, {'gent'}).word]
            else:  # нет глагола
                words += ['c' if not affil.startswith('с') or affil.startswith('со') else 'co']
                words += [inflector(affil, {'ablt'}).word]
        # elif get_tag(sush, 'одуш') == 'anim' and case_affil == 'gent' and glagol:
        elif get_tag(noun, 'одуш') == 'inan' and case_affil == 'gent':
            words += [inflector(affil, {case_affil}).word]
            if home:
                words += locate
    return ' '.join(words)


if __name__ == '__main__':
    print(generate_one())
