def difference_between_lists(list1: list, list2: list) -> list:
    """
    :param list1: Primeira lista
    :param list2: Segunda lista
    :type list1: list
    :type list2: list
    :return: Vai retornar uma lista, com os itens que não se repetiram nas listas
    :rtype: list
    """
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))