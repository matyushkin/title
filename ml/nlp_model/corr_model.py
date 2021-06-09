import json
import random
from itertools import combinations
from collections import OrderedDict

from sklearn.preprocessing import minmax_scale
import pandas as pd
import spacy

import os

nlp = spacy.load("ml/nlp_model/model-best")

# в файле tags.json хранятся данные о маркерах
with open(f'ml/nlp_model/tags.json') as f:
    tags = json.load(f)

# определим, какие сущности мы зарезервировали
tag_names = list(tags.keys())

df = pd.read_csv(f'ml/nlp_model/df_ner_corr.csv',
                 index_col=0)

# преобразуем строки к множествам
df.NER = df.NER.apply(eval)

# нормировка диапазона между 0 и 1.
df.VALUE = minmax_scale(df.VALUE)

df = df.sort_values(by='VALUE',
                    ascending=False)

# приведем значения к десятибалльной шкале
# с точностью 0.1
df.VALUE = df.VALUE.apply(lambda x: 10*round(x, 2))


def str_to_ents(s):
    """Выделяет из строки имена сущностей, их долю от
    всей длины строки, индексы начала и конца """
    seq = nlp(s).ents
    labels, indices = [], []
    for ent in seq:
        if ent.label_ in tag_names:
            labels.append(ent.label_)
            indices.append([ent.start_char, ent.end_char])
    try:
        fraction = len(''.join(str(ent) for ent in seq))/len(s)
    except ZeroDivisionError:
        fraction = 0.0
    return labels, fraction, indices


def find_value(ner_set, df=df):
    """Находит числовое значение,
    соответствующее набору именованных сущностей"""
    if len(ner_set) <= 3:
        cond = (df.NER == ner_set, 'VALUE')
        try:
            value = df.loc[cond].values[0]
        except IndexError:
            value = 0.0
    else:
        cs = combinations(ner_set, 3)
        best_value = 0.0
        best_triad = set()
        for c in cs:
            v = find_value(set(c))
            if v > best_value:
                best_triad = c
                best_value = v
        value = best_value
    return value


def find_set_with_greater_value(subset, df=df, exclude={}):
    """Возвращает полный список сущностей,
    добавление которых к subset повышает оценку value"""

    value = find_value(subset)
    cond = df.apply(lambda x: (subset.issubset(x.NER) and (x.VALUE > value)),
                    axis=1)
    ners = df[cond].NER.to_list()
    values = df[cond].VALUE.to_list()
    suggestions = []
    for triad in ners:
        # выкидываем имеющиеся 1 или 2 тега
        # и добавляем те, что их дополняют
        s = triad - subset
        for item in s:
            if item not in suggestions and item not in exclude:
                suggestions.append(item)
    return OrderedDict(zip(suggestions, values))


def highlight_best_pair(subset, df=df):
    """Находит пару с лучшими возможностями для
    расширения"""

    L = [set(pair) for pair in combinations(subset, 2)]
    value_max = 0
    pair_max = {}

    for pair in L:
        ordered_dict = find_set_with_greater_value(pair)
        for i in subset - pair:
            ordered_dict.pop(i, None)
        best_ner = next(iter(ordered_dict))
        total_max = ordered_dict[best_ner]
        if total_max > value_max:
            pair_max = pair

    # остальные сущности запомним, чтобы не предлагать
    others = subset - pair_max
    return {'best_pair': pair_max,
            'others': others}


def suggest(subset, df=df):
    """Определяет предложение пользователю
    для текущего набора именованных сущностей subset"""
    if len(subset) < 3:
        od = find_set_with_greater_value(subset)
    else:
        h = highlight_best_pair(subset)
        pair = h['best_pair']
        others = h['others']
        od = find_set_with_greater_value(pair, exclude=others)
    return od


def tooltip_card(ent, definition, examples):
    examples = ', '.join(examples)
    s = f'<b>{ent}</b>: {definition}</br>'
    s += f'<i>Примеры</i>: {examples}'
    return s


def suggest_to_html(s):
    """Возвращает строку с HTML-представлением
    идей для улучшения"""
    text = f'{s["comment"]} {s["suggestion_start"]}'
    accusatives = s["accusatives"]
    suggestions = s["suggestions"]
    definitions_out = s["definitions_out"]
    examples_out = s["examples_out"]
    text_adds = []
    for acc, ent, d, ex in zip(accusatives,
                               suggestions,
                               definitions_out,
                               examples_out):
        t = f'{acc} '
        t += f'<button class="{ent} btn btn-success" type="button" '
        t += f'data-bs-toggle="tooltip" data-bs-html="true" '
        t += f'title="{tooltip_card(ent, d, ex)} ">'
        t += f'{ent}'
        t += '</button>'
        text_adds.append(t)
    if len(suggestions) >= 2:
        text += ', '.join(text_adds[:-1]) + f' или {text_adds[-1]}'
    else:
        text += ', '.join(text_adds)
    return f"{text}."


def title_to_html(s):
    """Возвращает строку с HTML-представлением заголовка"""
    text = s["text"]
    indices = s["indices"][::-1]
    ents = s["ents"][::-1]
    definitions_in = s["definitions_in"][::-1]
    examples_in = s["examples_in"]
    for pair, ent, d, ex in zip(indices,
                                ents,
                                definitions_in,
                                examples_in):
        start, end = pair
        text = text[:end] + '</button>' + text[end:]
        t = f'<button class="{ent} btn btn-info" type="button" '
        t += f'data-bs-toggle="tooltip" data-bs-html="true" '
        t += f'title="{tooltip_card(ent, d, ex)} ">'
        text = text[:start] + t + text[start:]
    return f"{text}."


def rating_to_html(rating):
    rating = str(round(rating, 1))
    rating_html = f'<button class="btn btn-danger" id="rating">{rating}</button> балла из 10 по шкале говорящего заголовка.'
    return rating_html


def human_suggest(ents, df=df):
    """Возвращает строки, которые мы показываем пользователю"""
    subset = set(ents)
    value = find_value(subset)
    # 4 первых элемента (или меньше, если их есть)
    suggestions = list(suggest(subset).keys())[:4]
    suggestion_start = "Попробуйте указать: "
    if len(subset) == 0:
        comment = "Мы не смогли распознать сущностей, характерных для IT-статей."
        value == 0.0
    elif 0.0 < value <= 5.0:
        comment = "Заголовок получил низкую оценку."
        if len(subset) >= 3:
            comment += f" Хотя мы распознали несколько индикаторов, " \
                "все они относятся к малочитаемым публикациям."
    elif 5.0 < value <= 9.0:
        comment = "Хороший заголовок для IT-статьи."
        suggestion_start = "Чтобы его улучшить, укажите или сделайте более явными: "
    elif 9.0 < value < 10.0:
        comment = "Отличный заголовок для IT-публикации!"
    elif value == 10.0:
        comment = "Поздравляем! Заголовок набрал максимально возможный балл — 10 из 10"
        suggestions = []
        suggestion_start = ""

    definitions_in, examples_in = [], []
    accusatives, definitions_out, examples_out = [], [], []
    for ent in ents:
        definitions_in.append(tags[ent]["definition"])
        examples_in.append(tags[ent]["examples"])

    for ent in suggestions:
        accusatives.append(random.choice(tags[ent]["accusative"]))
        definitions_out.append(tags[ent]["definition"])
        examples_out.append(tags[ent]["examples"])

    return {'rating': value,
            'ents': ents,
            'definitions_in': definitions_in,
            'examples_in': examples_in,
            'comment': comment,
            'suggestion_start': suggestion_start,
            'suggestions': suggestions,
            'accusatives': accusatives,
            'definitions_out': definitions_out,
            'examples_out': examples_out}


def text_to_suggestion(text):
    '''Возвращает всё, что необходимо для рендеринга подсказки'''
    ents, _, indices = str_to_ents(text)
    s = human_suggest(ents, df=df)
    s['indices'] = indices
    s['text'] = text
    return {'rating': s['rating'],
    'title_html': title_to_html(s),
    'suggest_html': suggest_to_html(s),
    'rating_html': rating_to_html(s['rating'])}
