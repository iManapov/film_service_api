
def clear_sort_string(sort_string: str, es_text_field: str = None) -> str:
    """
    Функция для очистки query параметра sort

    :param sort_string: поле для фильтрации
    :param es_text_field:
    :return:
    """
    if sort_string:
        if es_text_field:
            if es_text_field in sort_string:
                sort_string = sort_string.replace(es_text_field, es_text_field + '.raw')
        if sort_string[0] == '-':
            sort_string = ':'.join([sort_string[1:], 'desc'])
    return sort_string
