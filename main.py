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
sush_mass = ['жопа', 'ниггер', 'очко', 'Ъ', 'гей', 'выборы', 'ублюдки', 'Фёдор',
             'Диляра Равильевна', 'Максим', 'мразь', 'пидор', 'мошонка',
             'анимешник', 'импотент', 'говно', 'мать Максима', 'спермотоксикозник']
prilag_mass = ['голубой', 'анимешный', 'тупой', 'карликовый',
               'опущенный', 'голодный', 'новогодний', 'ссанинский', 'каловый', 'засранный']
prinadl_mass = ['шаболда', 'лошадь', 'кошкодевка', 'бомжи',
                'говно', 'рабы', 'украинцы', 'чеченцы', '']
from_mass = ['Дагестан', 'США', 'пещера', 'помойка',
             'наркопритон', 'рабство', 'подвал', 'хата Феди', 'ноготь', '']
glagol_mass = ['толкать', 'уничтожать', 'долбиться',
               'насиловать', 'жрать', 'бить', 'унижать',
               'заебаться', 'обосраться', 'карать', '']


def generate_one():
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
        if prilag == 'ссанинский':
            prilag_parser = morph.parse(prilag)[1]
        else:
            prilag_parser = morph.parse(prilag)[0]
        if number == 'plur':
            words = [inflector(prilag_parser, {number, 'nomn'}).word.capitalize()] + [words[0]]
        else:
            words = [inflector(prilag_parser, {gender, 'nomn'}).word.capitalize()] + [words[0]]
    else:
        capital = words[0].split()
        words = [capital[0].capitalize()] + capital[1:]

    # ВЫЧИСЛЕНИЕ ПРИНАДЛЕЖНОСТИ
    if from_:
        from_ = [from_.split()[0], *from_.split()[1:]] if len(from_.split()) > 1 else [from_]
        ffrom_ = inflector(from_[0], {padezh_from})
        if 'Abbr' in ffrom_.tag:
            ffrom_ = ffrom_.word.upper()
        elif 'Geox' in ffrom_.tag:
            ffrom_ = ffrom_.word.capitalize()
        else:
            ffrom_ = ffrom_.word

        if padezh_from == "gent":
            if ffrom_ == 'ногтя':
                locate = ['из-под ' + ffrom_] + from_[1:]
            else:
                locate = ['из ' + ffrom_] + from_[1:]
        elif padezh_from == "loct":
            locate = ['в ' + ffrom_] + from_[1:]

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

        return ' '.join(words)


if __name__ == '__main__':
    print(generate_one())
